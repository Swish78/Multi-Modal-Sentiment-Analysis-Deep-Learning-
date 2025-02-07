import torch
from transformers import pipeline
import whisper
from deepface import DeepFace
import librosa
import numpy as np
import cv2
from moviepy.editor import VideoFileClip
import os
import tempfile

class MultiModalSentimentAnalyzer:
    def __init__(self):
        # Initialize models
        self.text_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.whisper_model = whisper.load_model("base")
        
        # Weights for fusion
        self.weights = {
            'text': 0.4,
            'audio': 0.3,
            'video': 0.3
        }
    
    def extract_audio(self, video_path):
        """Extract audio from video file"""
        video = VideoFileClip(video_path)
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        video.audio.write_audiofile(temp_audio.name, verbose=False, logger=None)
        return temp_audio.name

    def analyze_text(self, audio_path):
        """Transcribe audio and analyze text sentiment"""
        # Transcribe audio to text
        result = self.whisper_model.transcribe(audio_path)
        text = result["text"]
        
        # Analyze sentiment
        sentiment = self.text_analyzer(text)[0]
        score = sentiment['score']
        if sentiment['label'] == 'NEGATIVE':
            score = -score
        
        return {
            'score': score,
            'text': text
        }

    def analyze_audio(self, audio_path):
        """Analyze audio sentiment based on features"""
        # Load audio
        y, sr = librosa.load(audio_path)
        
        # Extract features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfccs_mean = np.mean(mfccs, axis=1)
        
        # Simple rule-based scoring using MFCC values
        # This is a very basic approach - in real applications you'd want a trained model
        energy = np.mean(mfccs_mean)
        normalized_score = np.tanh(energy)  # Map to [-1, 1]
        
        return {
            'score': normalized_score,
            'energy': energy
        }

    def analyze_video(self, video_path):
        """Analyze facial expressions from video"""
        cap = cv2.VideoCapture(video_path)
        frame_scores = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            try:
                # Analyze every 30th frame to save time
                if len(frame_scores) % 30 == 0:
                    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                    
                    # Convert emotions to sentiment score
                    emotions = result[0]['emotion']
                    positive = emotions['happy'] + emotions['surprise']
                    negative = emotions['sad'] + emotions['angry'] + emotions['fear'] + emotions['disgust']
                    neutral = emotions['neutral']
                    
                    score = (positive - negative) / 100  # Normalize to [-1, 1]
                    frame_scores.append(score)
            except:
                continue
                
        cap.release()
        
        if not frame_scores:
            return {'score': 0.0}
        
        return {
            'score': np.mean(frame_scores)
        }

    def analyze(self, video_path):
        """Perform multimodal sentiment analysis"""
        # Extract audio
        audio_path = self.extract_audio(video_path)
        
        # Analyze each modality
        text_results = self.analyze_text(audio_path)
        audio_results = self.analyze_audio(audio_path)
        video_results = self.analyze_video(video_path)
        
        # Clean up temporary audio file
        os.unlink(audio_path)
        
        # Weighted fusion of scores
        final_score = (
            self.weights['text'] * text_results['score'] +
            self.weights['audio'] * audio_results['score'] +
            self.weights['video'] * video_results['score']
        )
        
        return {
            'final_score': final_score,
            'text_score': text_results['score'],
            'audio_score': audio_results['score'],
            'video_score': video_results['score'],
            'transcribed_text': text_results['text']
        }
