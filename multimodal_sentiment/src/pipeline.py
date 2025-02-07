from typing import Dict, Optional
import os
import logging
import dask
from dask.distributed import Client, LocalCluster
from concurrent.futures import ThreadPoolExecutor

from .text_analysis.text_processor import TextSentimentAnalyzer
from .audio_analysis.audio_processor import AudioSentimentAnalyzer
from .video_analysis.video_processor import VideoSentimentAnalyzer
from .fusion.sentiment_fusion import SentimentFusionPipeline
from .utils.video_utils import extract_audio_from_video, get_video_info
from .utils.parallel_processor import DaskParallelProcessor
from .config.config import ConfigManager

class MultimodalSentimentPipeline:
    """Complete multimodal sentiment analysis pipeline with parallel processing"""
    
    def __init__(self, config_path: Optional[str] = None, n_workers: int = None):
        # Initialize configuration
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.get_config()
        self.n_workers = n_workers
        
        # Initialize analyzers
        self.text_analyzer = TextSentimentAnalyzer(
            model_name=self.config.text.model_name
        )
        self.audio_analyzer = AudioSentimentAnalyzer()
        self.video_analyzer = VideoSentimentAnalyzer(n_workers=n_workers)
        
        # Initialize fusion pipeline
        self.fusion_pipeline = SentimentFusionPipeline(
            fusion_method=self.config.fusion.method
        )
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _analyze_text_from_audio(self, audio_path: str) -> Dict:
        """Analyze sentiment from transcribed audio"""
        try:
            self.logger.info("Starting text analysis...")
            text_result = self.text_analyzer.analyze_sentiment(audio_path)
            self.logger.info("Text analysis completed")
            return text_result
        except Exception as e:
            self.logger.error(f"Error in text analysis: {str(e)}")
            return None
            
    def _analyze_audio(self, audio_path: str) -> Dict:
        """Analyze sentiment from audio features"""
        try:
            self.logger.info("Starting audio analysis...")
            audio_result = self.audio_analyzer.analyze_sentiment(audio_path)
            self.logger.info("Audio analysis completed")
            return audio_result
        except Exception as e:
            self.logger.error(f"Error in audio analysis: {str(e)}")
            return None
            
    def _analyze_video(self, video_path: str) -> Dict:
        """Analyze sentiment from video frames"""
        try:
            self.logger.info("Starting video analysis...")
            video_result = self.video_analyzer.analyze_video(
                video_path,
                sample_rate=self.config.video.frame_sample_rate
            )
            self.logger.info("Video analysis completed")
            return video_result
        except Exception as e:
            self.logger.error(f"Error in video analysis: {str(e)}")
            return None
            
    def analyze(self, video_path: str) -> Dict:
        """
        Analyze sentiment from video using all modalities in parallel
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary containing analysis results and fusion
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        # Get video info
        video_info = get_video_info(video_path)
        self.logger.info(f"Processing video: {video_info}")
        
        # Extract audio
        audio_path = extract_audio_from_video(video_path)
        
        try:
            # Create Dask cluster for parallel processing
            with DaskParallelProcessor(n_workers=self.n_workers) as processor:
                # Create delayed objects for each analysis
                text_delayed = dask.delayed(self._analyze_text_from_audio)(audio_path)
                audio_delayed = dask.delayed(self._analyze_audio)(audio_path)
                video_delayed = dask.delayed(self._analyze_video)(video_path)
                
                # Compute all analyses in parallel
                text_result, audio_result, video_result = dask.compute(
                    text_delayed, audio_delayed, video_delayed
                )
                
                # Perform fusion
                fusion_result = self.fusion_pipeline.fuse_sentiments(
                    text_result=text_result,
                    audio_result=audio_result,
                    video_result=video_result
                )
                
                return {
                    "video_info": video_info,
                    "analysis_results": {
                        "text": text_result,
                        "audio": audio_result,
                        "video": video_result
                    },
                    "fusion_result": fusion_result
                }
                
        finally:
            # Cleanup
            try:
                os.unlink(audio_path)
            except:
                pass
                
    def update_config(self, **kwargs):
        """Update pipeline configuration"""
        self.config_manager.update_config(**kwargs)
        self.config = self.config_manager.get_config()
