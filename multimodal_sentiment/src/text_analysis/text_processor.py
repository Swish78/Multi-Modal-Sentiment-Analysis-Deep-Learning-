from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Dict, List, Union

class TextSentimentAnalyzer:
    """Advanced text sentiment analyzer using transformer models"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.pipeline = pipeline("sentiment-analysis", model=model_name)
        
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text data"""
        # Remove extra whitespace
        text = " ".join(text.split())
        # Convert to lowercase
        text = text.lower()
        return text
        
    def get_emotion_scores(self, text: str) -> Dict[str, float]:
        """Get detailed emotion scores"""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=1)
        return {
            "positive": float(scores[0][1]),
            "negative": float(scores[0][0])
        }
        
    def analyze_sentiment(self, text: str) -> Dict[str, Union[float, str]]:
        """Comprehensive sentiment analysis"""
        # Preprocess text
        cleaned_text = self.preprocess_text(text)
        
        # Get basic sentiment
        sentiment = self.pipeline(cleaned_text)[0]
        
        # Get detailed scores
        emotion_scores = self.get_emotion_scores(cleaned_text)
        
        # Calculate compound score (-1 to 1)
        compound_score = emotion_scores["positive"] - emotion_scores["negative"]
        
        return {
            "compound_score": compound_score,
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"],
            "emotion_scores": emotion_scores,
            "processed_text": cleaned_text
        }
        
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Union[float, str]]]:
        """Batch process multiple texts"""
        return [self.analyze_sentiment(text) for text in texts]
