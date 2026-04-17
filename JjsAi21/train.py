"""
JjsAi21 - Video Analysis AI for Jujutsu Shenanigans
Main training module for analyzing gameplay videos, tracking player movements,
and detecting skill usage (including the special R-skill).
"""

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import os
import json
import time
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SkillDetectionModel(nn.Module):
    """
    Neural network for detecting skills and player movements in gameplay videos.
    Uses CNN for spatial feature extraction and LSTM for temporal analysis.
    """
    
    def __init__(self, num_classes=10, input_channels=3, hidden_size=256, num_layers=2):
        super(SkillDetectionModel, self).__init__()
        
        # CNN backbone for feature extraction
        self.conv_layers = nn.Sequential(
            nn.Conv2d(input_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((4, 4))
        )
        
        # Calculate flattened size
        self.flattened_size = 256 * 4 * 4
        
        # LSTM for temporal sequence analysis
        self.lstm = nn.LSTM(
            input_size=self.flattened_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.3
        )
        
        # Fully connected layers for classification
        self.fc_layers = nn.Sequential(
            nn.Linear(hidden_size, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
        
    def forward(self, x):
        # x shape: (batch, seq_len, channels, height, width)
        batch_size, seq_len, c, h, w = x.size()
        
        # Extract CNN features for each frame in sequence
        cnn_features = []
        for t in range(seq_len):
            frame = x[:, t, :, :, :]
            features = self.conv_layers(frame)
            features = features.view(batch_size, -1)
            cnn_features.append(features)
        
        # Stack features along sequence dimension
        cnn_features = torch.stack(cnn_features, dim=1)
        
        # Pass through LSTM
        lstm_out, _ = self.lstm(cnn_features)
        
        # Use the last hidden state for classification
        out = self.fc_layers(lstm_out[:, -1, :])
        
        return out


class GameplayDataset(Dataset):
    """
    Custom dataset for loading gameplay video frames and labels.
    """
    
    def __init__(self, video_paths, label_paths, seq_length=16, transform=None):
        """
        Args:
            video_paths: List of paths to video files
            label_paths: List of paths to corresponding label files
            seq_length: Number of frames per sequence
            transform: Optional transform to apply to frames
        """
        self.video_paths = video_paths
        self.label_paths = label_paths
        self.seq_length = seq_length
        self.transform = transform
        
    def __len__(self):
        return len(self.video_paths)
    
    def __getitem__(self, idx):
        video_path = self.video_paths[idx]
        label_path = self.label_paths[idx]
        
        # Load video and extract frames
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        while len(frames) < self.seq_length:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (128, 128))
            frame = frame.astype(np.float32) / 255.0
            
            if self.transform:
                frame = self.transform(frame)
            
            frames.append(frame)
        
        cap.release()
        
        # Pad if necessary
        while len(frames) < self.seq_length:
            frames.append(np.zeros_like(frames[0]))
        
        # Load labels
        with open(label_path, 'r') as f:
            labels = json.load(f)
        
        # Convert to tensor
        frames_tensor = torch.tensor(np.array(frames), dtype=torch.float32)
        frames_tensor = frames_tensor.permute(0, 3, 1, 2)  # (seq, H, W, C) -> (seq, C, H, W)
        
        label_tensor = torch.tensor(labels['action'], dtype=torch.long)
        
        return frames_tensor, label_tensor


def load_r_skill_description(config_path='r_skill_description.txt'):
    """
    Load and parse the R-skill description from config file.
    """
    r_skill_info = {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse the configuration
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            if line.startswith('#') or not line.strip():
                continue
                
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if value == '|':
                    current_section = key
                    r_skill_info[current_section] = []
                elif current_section:
                    r_skill_info[current_section].append(value)
                else:
                    r_skill_info[key] = value
                    
        logger.info(f"Successfully loaded R-skill description from {config_path}")
        return r_skill_info
        
    except FileNotFoundError:
        logger.warning(f"R-skill description file not found at {config_path}")
        return {}


def train_model(config):
    """
    Main training function for the AI model.
    """
    logger.info("Starting training process...")
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")
    
    # Load R-skill configuration
    r_skill_config = load_r_skill_description(config.get('r_skill_config', 'r_skill_description.txt'))
    logger.info(f"R-skill configuration loaded: {list(r_skill_config.keys())}")
    
    # Initialize model
    model = SkillDetectionModel(
        num_classes=config.get('num_classes', 10),
        hidden_size=config.get('hidden_size', 256),
        num_layers=config.get('num_layers', 2)
    ).to(device)
    
    # Loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.get('learning_rate', 0.001))
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5, factor=0.5)
    
    # Create data directories if they don't exist
    os.makedirs('videos', exist_ok=True)
    os.makedirs('labels', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Check for training data
    video_dir = Path('videos')
    label_dir = Path('labels')
    
    video_paths = list(video_dir.glob('*.mp4')) + list(video_dir.glob('*.avi'))
    label_paths = [label_dir / f.with_suffix('.json').name for f in video_paths]
    
    if not video_paths:
        logger.warning("No training videos found in data/videos directory.")
        logger.info("Please add gameplay videos and corresponding label files to start training.")
        logger.info("Creating sample structure for demonstration...")
        
        # Create dummy data for demonstration
        sample_video_path = video_dir / 'sample_gameplay.mp4'
        sample_label_path = label_dir / 'sample_gameplay.json'
        
        # Note: In real scenario, you would have actual videos and labels
        logger.info(f"Expected video format: MP4 or AVI files in {video_dir}")
        logger.info(f"Expected label format: JSON files with action labels in {label_dir}")
        
        return model
    
    # Create dataset and dataloader
    dataset = GameplayDataset(
        video_paths=[str(p) for p in video_paths],
        label_paths=[str(p) for p in label_paths],
        seq_length=config.get('seq_length', 16)
    )
    
    dataloader = DataLoader(
        dataset,
        batch_size=config.get('batch_size', 4),
        shuffle=True,
        num_workers=0
    )
    
    # Training loop
    num_epochs = config.get('num_epochs', 50)
    best_loss = float('inf')
    
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (frames, labels) in enumerate(dataloader):
            frames = frames.to(device)
            labels = labels.to(device)
            
            # Forward pass
            outputs = model(frames)
            loss = criterion(outputs, labels)
            
            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        avg_loss = total_loss / len(dataloader)
        accuracy = 100 * correct / total
        
        scheduler.step(avg_loss)
        
        logger.info(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%")
        
        # Save best model
        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': avg_loss,
            }, 'models/best_model.pth')
            logger.info(f"Saved best model with loss: {best_loss:.4f}")
        
        # Save checkpoint every 10 epochs
        if (epoch + 1) % 10 == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': avg_loss,
            }, f'models/checkpoint_epoch_{epoch+1}.pth')
    
    logger.info("Training completed!")
    return model


def analyze_video(video_path, model_path='models/best_model.pth'):
    """
    Analyze a single video using the trained model.
    """
    logger.info(f"Analyzing video: {video_path}")
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load model
    checkpoint = torch.load(model_path, map_location=device)
    model = SkillDetectionModel()
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    
    # Load video
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (128, 128))
        frame = frame.astype(np.float32) / 255.0
        frames.append(frame)
    
    cap.release()
    
    if len(frames) == 0:
        logger.error("No frames extracted from video")
        return
    
    # Process in sequences
    seq_length = 16
    results = []
    
    for i in range(0, len(frames), seq_length):
        seq_frames = frames[i:i+seq_length]
        
        # Pad if necessary
        while len(seq_frames) < seq_length:
            seq_frames.append(np.zeros_like(seq_frames[0]))
        
        # Prepare input
        input_tensor = torch.tensor(np.array(seq_frames), dtype=torch.float32)
        input_tensor = input_tensor.permute(0, 3, 1, 2).unsqueeze(0).to(device)
        
        # Predict
        with torch.no_grad():
            output = model(input_tensor)
            _, predicted = torch.max(output, 1)
            confidence = torch.softmax(output, dim=1)[0][predicted].item()
        
        results.append({
            'frame_range': (i, min(i+seq_length, len(frames))),
            'predicted_action': predicted.item(),
            'confidence': confidence
        })
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_path = f'logs/analysis_results_{timestamp}.json'
    
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Analysis complete. Results saved to {results_path}")
    return results


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='JjsAi21 - Gameplay Video Analysis AI')
    parser.add_argument('--mode', choices=['train', 'analyze'], default='train',
                       help='Mode: train or analyze')
    parser.add_argument('--video', type=str, help='Path to video file for analysis')
    parser.add_argument('--model', type=str, default='models/best_model.pth',
                       help='Path to trained model')
    parser.add_argument('--config', type=str, default='config/training_config.json',
                       help='Path to training configuration')
    
    args = parser.parse_args()
    
    # Load configuration
    config = {
        'num_classes': 10,
        'hidden_size': 256,
        'num_layers': 2,
        'seq_length': 16,
        'batch_size': 4,
        'learning_rate': 0.001,
        'num_epochs': 50,
        'r_skill_config': 'config/r_skill_description.txt'
    }
    
    # Override with config file if exists
    if os.path.exists(args.config):
        with open(args.config, 'r') as f:
            file_config = json.load(f)
            config.update(file_config)
    
    if args.mode == 'train':
        train_model(config)
    elif args.mode == 'analyze':
        if not args.video:
            logger.error("Video path required for analysis mode")
        else:
            analyze_video(args.video, args.model)
