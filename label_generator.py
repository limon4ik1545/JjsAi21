"""
Label Generator Tool for JjsAi21
Helps create labeled training data from gameplay videos.
"""

import cv2
import json
import os
from pathlib import Path
from datetime import datetime


class LabelGenerator:
    """
    Interactive tool for labeling gameplay videos.
    Press keys to mark different actions:
    - 0: Idle
    - 1: Walk Forward
    - 2: Walk Backward
    - 3: Jump
    - 4: Crouch
    - 5: Light Attack
    - 6: Heavy Attack
    - 7: Skill Q
    - 8: Skill R (Special)
    - 9: Skill E
    - s: Save current label
    - q: Quit
    """
    
    def __init__(self, video_path, output_dir='data/labels'):
        self.video_path = video_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.labels = []
        self.current_action = None
        self.frame_number = 0
        
        # Action mapping
        self.action_map = {
            ord('0'): 'idle',
            ord('1'): 'walk_forward',
            ord('2'): 'walk_backward',
            ord('3'): 'jump',
            ord('4'): 'crouch',
            ord('5'): 'light_attack',
            ord('6'): 'heavy_attack',
            ord('7'): 'skill_q',
            ord('8'): 'skill_r',
            ord('9'): 'skill_e',
        }
        
        self.action_names = {v: k for k, v in self.action_map.items()}
        
    def run(self):
        """Run the labeling interface."""
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            print(f"Error: Could not open video {self.video_path}")
            return
        
        print("=" * 60)
        print("JjsAi21 - Video Labeling Tool")
        print("=" * 60)
        print("\nControls:")
        print("  0-9: Select action type")
        print("  s: Save current frame with selected action")
        print("  n: Next frame")
        print("  b: Previous frame")
        print("  q: Quit and save all labels")
        print("\nAction mapping:")
        for key, action in self.action_map.items():
            print(f"  {chr(key)}: {action}")
        print("=" * 60)
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        print(f"\nVideo: {self.video_path}")
        print(f"Total frames: {total_frames}, FPS: {fps}")
        print("=" * 60)
        
        while True:
            cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
            ret, frame = cap.read()
            
            if not ret:
                print("End of video reached")
                break
            
            # Display frame info
            info_text = f"Frame: {self.frame_number}/{total_frames} | "
            if self.current_action:
                info_text += f"Selected: {self.current_action}"
            else:
                info_text += "No action selected"
            
            cv2.putText(frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Show recent labels
            if self.labels:
                recent = self.labels[-5:]
                for i, label in enumerate(recent):
                    label_text = f"F{label['frame']}: {label['action']}"
                    cv2.putText(frame, label_text, (10, 60 + i*25),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            cv2.imshow('Labeling Tool', frame)
            
            key = cv2.waitKey(0) & 0xFF
            
            if key == ord('q'):
                break
            elif key in self.action_map:
                self.current_action = self.action_map[key]
                print(f"Selected action: {self.current_action}")
            elif key == ord('s'):
                if self.current_action:
                    self.labels.append({
                        'frame': self.frame_number,
                        'action': self.current_action,
                        'timestamp': self.frame_number / fps,
                        'video_path': str(self.video_path)
                    })
                    print(f"Labeled frame {self.frame_number} as '{self.current_action}'")
                else:
                    print("Please select an action first (0-9)")
            elif key == ord('n'):
                self.frame_number = min(self.frame_number + 1, total_frames - 1)
            elif key == ord('b'):
                self.frame_number = max(self.frame_number - 1, 0)
            elif key == ord('d'):
                # Delete last label
                if self.labels:
                    removed = self.labels.pop()
                    print(f"Removed label: {removed}")
        
        cap.release()
        cv2.destroyAllWindows()
        
        self.save_labels()
    
    def save_labels(self):
        """Save all labels to JSON file."""
        if not self.labels:
            print("No labels to save")
            return
        
        # Group labels by video
        video_name = Path(self.video_path).stem
        output_file = self.output_dir / f"{video_name}.json"
        
        # Convert action names to IDs
        action_to_id = {
            'idle': 0,
            'walk_forward': 1,
            'walk_backward': 2,
            'jump': 3,
            'crouch': 4,
            'light_attack': 5,
            'heavy_attack': 6,
            'skill_q': 7,
            'skill_r': 8,
            'skill_e': 9
        }
        
        labeled_data = {
            'video_path': str(self.video_path),
            'total_frames': len(self.labels),
            'labels': []
        }
        
        for label in self.labels:
            labeled_data['labels'].append({
                'frame': label['frame'],
                'action': action_to_id.get(label['action'], 0),
                'action_name': label['action'],
                'timestamp': label['timestamp']
            })
        
        with open(output_file, 'w') as f:
            json.dump(labeled_data, f, indent=2)
        
        print(f"\nSaved {len(self.labels)} labels to {output_file}")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python label_generator.py <video_path>")
        print("\nExample:")
        print("  python label_generator.py data/videos/gameplay.mp4")
        return
    
    video_path = sys.argv[1]
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        return
    
    generator = LabelGenerator(video_path)
    generator.run()


if __name__ == '__main__':
    main()
