# -*- coding: utf-8 -*-
"""
This script loads a pre-trained model for hope/hate speech classification.
It works by first classifying text into one of six emotions, and then mapping
that emotion to either 'Hope' or 'Hate'.
"""
import os
import pickle
import torch
from transformers import AutoTokenizer

# --- Configuration ---

# Setup file paths
_SERVICE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.abspath(os.path.join(_SERVICE_DIR, "..", "models", "hope_hate_model.pkl"))

# Define the emotion labels based on the training dataset (dair-ai/emotion)
EMOTION_LABELS = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

# Define which emotions are categorized as "Hope"
HOPE_LABELS = {"joy", "love", "surprise"}

# --- Model and Tokenizer Loading ---

model = None
tokenizer = None

try:
    # Check if model file exists
    if not os.path.isfile(MODEL_PATH):
        raise OSError(f"Model file not found at '{MODEL_PATH}'")
        
    with open(MODEL_PATH, 'rb') as f:
        loaded_data = pickle.load(f)
    
    # Load model from the pickle file
    if isinstance(loaded_data, dict) and 'model' in loaded_data:
        model = loaded_data['model']
        print("✅ Model loaded from .pkl file dictionary.")
    else:
        model = loaded_data # Assumed to be a standalone model
        print("✅ Model loaded from .pkl file (standalone).")

    # If it's a transformers model, load its tokenizer
    if model and "transformers" in str(type(model)):
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        print("✅ Hugging Face tokenizer loaded for DistilBert model.")

except Exception as e:
    print(f"❌ Error loading model or tokenizer: {e}")
    model = None
    tokenizer = None

# --- Prediction Function ---

def predict_hope_hate(text):
    """
    Analyzes text to classify its emotion and determine if it's Hope or Hate speech.
    """
    if not model or not tokenizer:
        print("❌ Model or tokenizer is not loaded. Cannot perform prediction.")
        return {"text": text, "hope_hate": "Unknown", "emotion": "unknown", "score": 0.0}

    try:
        # 1. Tokenize the input text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

        # 2. Get model prediction in inference mode
        with torch.no_grad():
            outputs = model(**inputs)
        
        # 3. Process the output logits to get probabilities
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)[0]
        
        # 4. Get the predicted class index and its confidence score
        prediction_index = torch.argmax(probabilities).item()
        score = probabilities[prediction_index].item()
        
        # 5. Map the index to its corresponding emotion label
        predicted_emotion = EMOTION_LABELS[prediction_index]

        # 6. Classify the emotion as "Hope" or "Hate"
        hope_hate = "Hope" if predicted_emotion in HOPE_LABELS else "Hate"

    except IndexError:
        print(f"❌ Error: Prediction index {prediction_index} is out of bounds for EMOTION_LABELS.")
        hope_hate, predicted_emotion, score = "Unknown", "unknown", 0.0
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        hope_hate, predicted_emotion, score = "Unknown", "unknown", 0.0

    return {
        "text": text,
        "hope_hate": hope_hate,
        "emotion": predicted_emotion,
        "score": round(float(score), 3)
    }
