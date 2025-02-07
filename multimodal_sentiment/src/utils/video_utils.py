import cv2
import numpy as np
from typing import Tuple, List
import tempfile
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_path: str) -> str:
    """Extract audio from video file"""
    video = VideoFileClip(video_path)
    temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    video.audio.write_audiofile(temp_audio.name, verbose=False, logger=None)
    return temp_audio.name

def get_video_info(video_path: str) -> dict:
    """Get video metadata"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps
    cap.release()
    
    return {
        "fps": fps,
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "duration": duration
    }

def sample_frames(video_path: str, sample_rate: int = 1) -> List[np.ndarray]:
    """Sample frames from video at given rate"""
    frames = []
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % sample_rate == 0:
            frames.append(frame)
            
        frame_count += 1
        
    cap.release()
    return frames

def resize_frame(frame: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
    """Resize frame while maintaining aspect ratio"""
    h, w = frame.shape[:2]
    target_w, target_h = target_size
    
    # Calculate scaling factor
    scale = min(target_w/w, target_h/h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    resized = cv2.resize(frame, (new_w, new_h))
    
    # Create canvas of target size
    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    
    # Center the resized image
    y_offset = (target_h - new_h) // 2
    x_offset = (target_w - new_w) // 2
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    
    return canvas
