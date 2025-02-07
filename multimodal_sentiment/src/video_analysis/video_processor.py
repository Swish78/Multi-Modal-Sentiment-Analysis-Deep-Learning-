import cv2
import numpy as np
from deepface import DeepFace
from typing import Dict, List, Optional, Tuple
import logging
from ..utils.parallel_processor import DaskParallelProcessor, BatchProcessor
from concurrent.futures import ThreadPoolExecutor

class FaceDetector:
    """Advanced face detection and tracking"""
    
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.previous_faces = []
        
    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces.tolist()
        
    def track_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Track faces across frames"""
        current_faces = self.detect_faces(frame)
        
        if not self.previous_faces:
            self.previous_faces = current_faces
            return current_faces
            
        # Simple tracking by finding closest previous face
        tracked_faces = []
        for curr_face in current_faces:
            closest_dist = float('inf')
            closest_prev = None
            
            for prev_face in self.previous_faces:
                dist = np.sqrt((curr_face[0] - prev_face[0])**2 + 
                             (curr_face[1] - prev_face[1])**2)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_prev = prev_face
                    
            tracked_faces.append(curr_face)
            
        self.previous_faces = tracked_faces
        return tracked_faces

class EmotionAnalyzer:
    """Analyze emotions from facial expressions"""
    
    def __init__(self):
        self.emotion_weights = {
            'happy': 1.0,
            'surprise': 0.5,
            'neutral': 0.0,
            'sad': -0.5,
            'angry': -1.0,
            'fear': -0.8,
            'disgust': -0.7
        }
        
    def analyze_face(self, face_img: np.ndarray) -> Dict[str, float]:
        """Analyze emotions in a face image"""
        try:
            result = DeepFace.analyze(
                face_img, 
                actions=['emotion'],
                enforce_detection=False
            )
            emotions = result[0]['emotion']
            return emotions
        except Exception as e:
            logging.warning(f"Failed to analyze face: {str(e)}")
            return {}
            
    def compute_sentiment_score(self, emotions: Dict[str, float]) -> float:
        """Convert emotions to sentiment score"""
        if not emotions:
            return 0.0
            
        weighted_sum = sum(self.emotion_weights[emotion] * score 
                         for emotion, score in emotions.items())
        return np.tanh(weighted_sum / 100)  # Normalize to [-1, 1]

class VideoSentimentAnalyzer:
    """Complete video sentiment analysis pipeline with parallel processing"""
    
    def __init__(self, n_workers: int = None):
        self.face_detector = FaceDetector()
        self.emotion_analyzer = EmotionAnalyzer()
        self.n_workers = n_workers
        self.logger = logging.getLogger(__name__)
        
    def _process_frame(self, frame: np.ndarray) -> Dict[str, float]:
        """Process a single frame"""
        faces = self.face_detector.track_faces(frame)
        
        frame_emotions = []
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            emotions = self.emotion_analyzer.analyze_face(face_img)
            if emotions:
                frame_emotions.append(emotions)
                
        if not frame_emotions:
            return {"score": 0.0, "emotions": {}}
            
        # Average emotions across all faces
        avg_emotions = {}
        for emotion in self.emotion_analyzer.emotion_weights.keys():
            avg_emotions[emotion] = np.mean([e.get(emotion, 0.0) for e in frame_emotions])
            
        sentiment_score = self.emotion_analyzer.compute_sentiment_score(avg_emotions)
        
        return {
            "score": sentiment_score,
            "emotions": avg_emotions
        }
        
    def analyze_video(self, video_path: str, sample_rate: int = 1) -> Dict[str, float]:
        """Analyze sentiment from video file using parallel processing"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        frame_count = 0
        
        # Extract frames
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % sample_rate == 0:
                frames.append(frame)
                
            frame_count += 1
            
        cap.release()
        
        if not frames:
            return {
                "compound_score": 0.0,
                "frame_scores": [],
                "average_emotions": {}
            }
            
        # Process frames in parallel using Dask
        try:
            with DaskParallelProcessor(n_workers=self.n_workers) as processor:
                frame_results = processor.process_frames(
                    frames,
                    self._process_frame,
                    batch_size=10
                )
        except Exception as e:
            self.logger.error(f"Error in parallel processing: {str(e)}")
            # Fallback to sequential processing
            self.logger.info("Falling back to sequential processing")
            frame_results = [self._process_frame(frame) for frame in frames]
        
        # Compute overall statistics
        scores = [r["score"] for r in frame_results]
        emotions = [r["emotions"] for r in frame_results if r["emotions"]]
        
        avg_emotions = {}
        if emotions:
            for emotion in self.emotion_analyzer.emotion_weights.keys():
                avg_emotions[emotion] = np.mean([e.get(emotion, 0.0) for e in emotions])
        
        return {
            "compound_score": float(np.mean(scores)),
            "frame_scores": scores,
            "average_emotions": avg_emotions,
            "processed_frames": len(frame_results)
        }
