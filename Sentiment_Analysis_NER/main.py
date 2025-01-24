# Step 1: Initialize Stanza for NER
# Step 2: Perform NER on the transcribed text
# Replacing entities with their NER tags
# Step 3: Perform Sentiment Analysis using Hugging Face Transformers
import os
from groq import Groq
import stanza
from transformers import pipeline
import dotenv

dotenv.load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Groq client
client = Groq(api_key=GROQ_API_KEY) # Create .env file with GROQ_API_KEY
filename = 'mcd2.mp3'

# Transcribing audio using whisper
with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),
        model="whisper-large-v3-turbo",
        response_format="verbose_json",
    )

transcribed_text = transcription.text
print("Transcribed Text:", transcribed_text)


stanza.download("en")
nlp = stanza.Pipeline(lang="en", processors="tokenize,ner")

doc = nlp(transcribed_text)
print("\nNamed Entities:")
for entity in doc.ents:
    print(f"Entity: {entity.text}, Type: {entity.type}")

modified_text = transcribed_text
for entity in doc.ents:
    modified_text = modified_text.replace(entity.text, entity.type)

print("\nModified Text with NER:", modified_text)

sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased")

# Analyzing sentiment of the modified text
sentiment_result = sentiment_pipeline(modified_text)
print("\nSentiment Analysis Result:", sentiment_result)