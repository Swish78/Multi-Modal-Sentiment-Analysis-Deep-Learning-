import librosa
import numpy as np
from typing import Dict, List, Tuple, Optional
import scipy.stats as stats

class AudioFeatureExtractor:
    """Advanced audio feature extraction and analysis"""
    
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
        self.feature_extractors = {
            "mfcc": self._extract_mfcc,
            "spectral": self._extract_spectral_features,
            "rhythm": self._extract_rhythm_features,
            "energy": self._extract_energy_features
        }
        
    def _extract_mfcc(self, y: np.ndarray) -> Dict[str, float]:
        """Extract MFCC features"""
        mfccs = librosa.feature.mfcc(y=y, sr=self.sample_rate, n_mfcc=13)
        mfcc_means = np.mean(mfccs, axis=1)
        mfcc_vars = np.var(mfccs, axis=1)
        
        return {
            f"mfcc_{i+1}_mean": float(mean) for i, mean in enumerate(mfcc_means)
        } | {
            f"mfcc_{i+1}_var": float(var) for i, var in enumerate(mfcc_vars)
        }
        
    def _extract_spectral_features(self, y: np.ndarray) -> Dict[str, float]:
        """Extract spectral features"""
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=self.sample_rate)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=self.sample_rate)[0]
        
        return {
            "spectral_centroid_mean": float(np.mean(spectral_centroids)),
            "spectral_rolloff_mean": float(np.mean(spectral_rolloff)),
            "spectral_bandwidth": float(np.std(spectral_centroids))
        }
        
    def _extract_rhythm_features(self, y: np.ndarray) -> Dict[str, float]:
        """Extract rhythm-related features"""
        tempo, _ = librosa.beat.beat_track(y=y, sr=self.sample_rate)
        zero_crossings = librosa.zero_crossings(y)
        
        return {
            "tempo": float(tempo),
            "zero_crossing_rate": float(np.mean(zero_crossings))
        }
        
    def _extract_energy_features(self, y: np.ndarray) -> Dict[str, float]:
        """Extract energy-based features"""
        rms = librosa.feature.rms(y=y)[0]
        return {
            "energy_mean": float(np.mean(rms)),
            "energy_std": float(np.std(rms)),
            "energy_skew": float(stats.skew(rms))
        }

class AudioSentimentAnalyzer:
    """Audio-based sentiment analysis using extracted features"""
    
    def __init__(self):
        self.feature_extractor = AudioFeatureExtractor()
        
    def _normalize_score(self, value: float, min_val: float = -1, max_val: float = 1) -> float:
        """Normalize values to range [-1, 1]"""
        return 2 * ((value - min_val) / (max_val - min_val)) - 1
        
    def analyze_sentiment(self, audio_path: str) -> Dict[str, float]:
        """Analyze sentiment from audio file"""
        # Load audio
        y, sr = librosa.load(audio_path)
        
        # Extract all features
        features = {}
        for feature_name, extractor in self.feature_extractor.feature_extractors.items():
            features.update(extractor(y))
            
        # Calculate sentiment scores based on features
        energy_score = self._normalize_score(features["energy_mean"])
        rhythm_score = self._normalize_score(features["tempo"], 50, 200)
        spectral_score = self._normalize_score(features["spectral_centroid_mean"])
        
        # Combine scores with weights
        compound_score = (
            0.4 * energy_score +
            0.3 * rhythm_score +
            0.3 * spectral_score
        )
        
        return {
            "compound_score": float(compound_score),
            "energy_score": float(energy_score),
            "rhythm_score": float(rhythm_score),
            "spectral_score": float(spectral_score),
            "features": features
        }
