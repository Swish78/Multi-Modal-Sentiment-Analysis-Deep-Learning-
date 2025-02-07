# Multimodal Sentiment Analysis System

This project implements a multimodal sentiment analysis system that analyzes sentiment from video inputs using three modalities:
1. Text (transcribed speech)
2. Audio (tone and acoustic features)
3. Video (facial expressions)

## Features
- Speech-to-text transcription using OpenAI's Whisper
- Text sentiment analysis using DistilBERT
- Audio feature analysis using Librosa
- Facial expression analysis using DeepFace
- Weighted fusion of all modalities
- Simple web interface using Gradio

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the web interface:
```bash
python app.py
```

## How it Works

The system processes videos through three parallel pipelines:

1. **Text Pipeline**:
   - Transcribes speech to text using Whisper
   - Analyzes sentiment using DistilBERT

2. **Audio Pipeline**:
   - Extracts MFCC features using Librosa
   - Computes audio-based sentiment score

3. **Video Pipeline**:
   - Extracts frames from video
   - Analyzes facial expressions using DeepFace
   - Computes frame-by-frame sentiment scores

The final sentiment score is computed as a weighted average:
- Text: 40%
- Audio: 30%
- Video: 30%

## Usage

1. Open the web interface (default: http://localhost:7860)
2. Upload a video file
3. Wait for the analysis to complete
4. View the results including:
   - Overall sentiment score
   - Individual modality scores
   - Transcribed text

## Notes
- The system works best with clear speech and visible faces
- Processing time depends on video length
- Ensure good lighting and audio quality for best results
