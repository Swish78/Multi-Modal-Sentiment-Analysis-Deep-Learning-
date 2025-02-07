from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import os

@dataclass
class TextConfig:
    model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"
    max_length: int = 512
    batch_size: int = 32

@dataclass
class AudioConfig:
    sample_rate: int = 22050
    n_mfcc: int = 13
    hop_length: int = 512
    n_fft: int = 2048

@dataclass
class VideoConfig:
    frame_sample_rate: int = 5
    target_size: tuple = (224, 224)
    batch_size: int = 16

@dataclass
class FusionConfig:
    method: str = "adaptive"
    modality_weights: Dict[str, float] = None
    
    def __post_init__(self):
        if self.modality_weights is None:
            self.modality_weights = {
                "text": 0.4,
                "audio": 0.3,
                "video": 0.3
            }

@dataclass
class ModelConfig:
    text: TextConfig = TextConfig()
    audio: AudioConfig = AudioConfig()
    video: VideoConfig = VideoConfig()
    fusion: FusionConfig = FusionConfig()

class ConfigManager:
    """Manage configuration settings"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config = ModelConfig()
        
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
            
    def load_config(self, config_path: str) -> None:
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
            
        # Update configurations
        self.config.text = TextConfig(**config_dict.get('text', {}))
        self.config.audio = AudioConfig(**config_dict.get('audio', {}))
        self.config.video = VideoConfig(**config_dict.get('video', {}))
        self.config.fusion = FusionConfig(**config_dict.get('fusion', {}))
        
    def save_config(self, config_path: Optional[str] = None) -> None:
        """Save configuration to JSON file"""
        save_path = config_path or self.config_path
        if not save_path:
            raise ValueError("No config path specified")
            
        config_dict = {
            'text': {
                'model_name': self.config.text.model_name,
                'max_length': self.config.text.max_length,
                'batch_size': self.config.text.batch_size
            },
            'audio': {
                'sample_rate': self.config.audio.sample_rate,
                'n_mfcc': self.config.audio.n_mfcc,
                'hop_length': self.config.audio.hop_length,
                'n_fft': self.config.audio.n_fft
            },
            'video': {
                'frame_sample_rate': self.config.video.frame_sample_rate,
                'target_size': self.config.video.target_size,
                'batch_size': self.config.video.batch_size
            },
            'fusion': {
                'method': self.config.fusion.method,
                'modality_weights': self.config.fusion.modality_weights
            }
        }
        
        with open(save_path, 'w') as f:
            json.dump(config_dict, f, indent=4)
            
    def get_config(self) -> ModelConfig:
        """Get current configuration"""
        return self.config
        
    def update_config(self, **kwargs) -> None:
        """Update configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
