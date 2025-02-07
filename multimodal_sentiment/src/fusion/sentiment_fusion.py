import numpy as np
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
import json

@dataclass
class ModalityResult:
    """Container for modality-specific results"""
    score: float
    confidence: float
    metadata: Dict

class WeightedAverageFusion:
    """Simple weighted average fusion strategy"""
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or {
            'text': 0.4,
            'audio': 0.3,
            'video': 0.3
        }
        
    def fuse(self, modality_results: Dict[str, ModalityResult]) -> Dict[str, Union[float, Dict]]:
        """Fuse multiple modality results using weighted average"""
        weighted_sum = 0.0
        total_weight = 0.0
        
        for modality, weight in self.weights.items():
            if modality in modality_results:
                result = modality_results[modality]
                weighted_sum += weight * result.score * result.confidence
                total_weight += weight * result.confidence
                
        if total_weight == 0:
            return {
                "compound_score": 0.0,
                "confidence": 0.0,
                "modality_contributions": {}
            }
            
        final_score = weighted_sum / total_weight
        
        # Calculate individual contributions
        contributions = {}
        for modality, result in modality_results.items():
            weight = self.weights.get(modality, 0.0)
            contribution = (weight * result.score * result.confidence) / total_weight
            contributions[modality] = {
                "contribution": float(contribution),
                "confidence": float(result.confidence)
            }
            
        return {
            "compound_score": float(final_score),
            "confidence": float(total_weight / sum(self.weights.values())),
            "modality_contributions": contributions
        }

class AdaptiveWeightFusion:
    """Adaptive fusion that adjusts weights based on confidence"""
    
    def __init__(self, base_weights: Optional[Dict[str, float]] = None):
        self.base_weights = base_weights or {
            'text': 0.4,
            'audio': 0.3,
            'video': 0.3
        }
        
    def _compute_adaptive_weights(self, modality_results: Dict[str, ModalityResult]) -> Dict[str, float]:
        """Compute adaptive weights based on confidence scores"""
        confidence_sum = sum(result.confidence for result in modality_results.values())
        
        if confidence_sum == 0:
            return self.base_weights
            
        adaptive_weights = {}
        for modality, result in modality_results.items():
            base_weight = self.base_weights.get(modality, 0.0)
            confidence_weight = result.confidence / confidence_sum
            adaptive_weights[modality] = (base_weight + confidence_weight) / 2
            
        # Normalize weights
        weight_sum = sum(adaptive_weights.values())
        return {k: v/weight_sum for k, v in adaptive_weights.items()}
        
    def fuse(self, modality_results: Dict[str, ModalityResult]) -> Dict[str, Union[float, Dict]]:
        """Fuse results with adaptive weighting"""
        adaptive_weights = self._compute_adaptive_weights(modality_results)
        
        weighted_sum = 0.0
        for modality, result in modality_results.items():
            weight = adaptive_weights.get(modality, 0.0)
            weighted_sum += weight * result.score
            
        # Calculate confidence based on agreement between modalities
        scores = [result.score for result in modality_results.values()]
        score_std = np.std(scores) if scores else 1.0
        agreement_confidence = np.exp(-score_std)  # High agreement = low std = high confidence
        
        contributions = {}
        for modality, result in modality_results.items():
            weight = adaptive_weights.get(modality, 0.0)
            contribution = weight * result.score
            contributions[modality] = {
                "contribution": float(contribution),
                "weight": float(weight),
                "confidence": float(result.confidence)
            }
            
        return {
            "compound_score": float(weighted_sum),
            "confidence": float(agreement_confidence),
            "modality_contributions": contributions,
            "adaptive_weights": adaptive_weights
        }

class SentimentFusionPipeline:
    """Complete sentiment fusion pipeline"""
    
    def __init__(self, fusion_method: str = "adaptive"):
        self.fusion_method = fusion_method
        self.fusers = {
            "weighted": WeightedAverageFusion(),
            "adaptive": AdaptiveWeightFusion()
        }
        
    def fuse_sentiments(self, 
                       text_result: Optional[Dict] = None,
                       audio_result: Optional[Dict] = None,
                       video_result: Optional[Dict] = None) -> Dict[str, Union[float, Dict]]:
        """Fuse multiple modality results into final sentiment"""
        
        modality_results = {}
        
        # Process text results
        if text_result:
            modality_results['text'] = ModalityResult(
                score=text_result.get('compound_score', 0.0),
                confidence=text_result.get('confidence', 0.5),
                metadata=text_result
            )
            
        # Process audio results
        if audio_result:
            modality_results['audio'] = ModalityResult(
                score=audio_result.get('compound_score', 0.0),
                confidence=0.5,  # Could be calculated from feature reliability
                metadata=audio_result
            )
            
        # Process video results
        if video_result:
            modality_results['video'] = ModalityResult(
                score=video_result.get('compound_score', 0.0),
                confidence=video_result.get('confidence', 0.5),
                metadata=video_result
            )
            
        # Perform fusion
        fuser = self.fusers.get(self.fusion_method, self.fusers["adaptive"])
        fusion_result = fuser.fuse(modality_results)
        
        return {
            "fusion_method": self.fusion_method,
            "result": fusion_result,
            "modality_results": {
                k: v.metadata for k, v in modality_results.items()
            }
        }
