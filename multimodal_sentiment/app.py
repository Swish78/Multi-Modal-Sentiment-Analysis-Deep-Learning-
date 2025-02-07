import gradio as gr
from sentiment_analyzer import MultiModalSentimentAnalyzer
import tempfile
import os

analyzer = MultiModalSentimentAnalyzer()

def analyze_video(video_path):
    if video_path is None:
        return "Please upload a video file."
    
    # Save the uploaded video to a temporary file
    temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    temp_video.close()
    os.rename(video_path, temp_video.name)
    
    # Analyze the video
    results = analyzer.analyze(temp_video.name)
    
    # Clean up
    os.unlink(temp_video.name)
    
    # Format results
    output = f"""
    ### Results:
    - Final Sentiment Score: {results['final_score']:.2f}
    
    ### Individual Modality Scores:
    - Text Score: {results['text_score']:.2f}
    - Audio Score: {results['audio_score']:.2f}
    - Video Score: {results['video_score']:.2f}
    
    ### Transcribed Text:
    {results['transcribed_text']}
    """
    
    return output

# Create Gradio interface
iface = gr.Interface(
    fn=analyze_video,
    inputs=gr.Video(label="Upload Video"),
    outputs=gr.Markdown(),
    title="Multimodal Sentiment Analysis",
    description="Upload a video to analyze sentiment from text (speech), audio, and facial expressions.",
    examples=[],
)

if __name__ == "__main__":
    iface.launch()
