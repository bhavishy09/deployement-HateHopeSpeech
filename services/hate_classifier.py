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




_SERVICE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.abspath(os.path.join(_SERVICE_DIR, "..", "models", "hope_hate_model.pkl"))


EMOTION_LABELS = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

HOPE_LABELS = {"joy", "love", "surprise"}



model = None
tokenizer = None

def load_model():
    """
    Lazy loads the model and tokenizer if they haven't been loaded yet.
    """
    global model, tokenizer
    if model is not None and tokenizer is not None:
        return

    print("⏳ Loading model and tokenizer...")
    try:
        if not os.path.isfile(MODEL_PATH):
            raise OSError(f"Model file not found at '{MODEL_PATH}'")
            
        with open(MODEL_PATH, 'rb') as f:
            loaded_data = pickle.load(f)
        
        if isinstance(loaded_data, dict) and 'model' in loaded_data:
            model = loaded_data['model']
            print("✅ Model loaded from .pkl file dictionary.")
        else:
            model = loaded_data 
            print("✅ Model loaded from .pkl file (standalone).")

        if model and "transformers" in str(type(model)):
            tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            print("✅ Hugging Face tokenizer loaded for DistilBert model.")

    except Exception as e:
        print(f"❌ Error loading model or tokenizer: {e}")
        model = None
        tokenizer = None

def predict_hope_hate(text):
    """
    Analyzes text to classify its emotion and determine if it's Hope or Hate speech.
    """
    # Ensure model is loaded before prediction
    load_model()

    if not model or not tokenizer:
        print("❌ Model or tokenizer is not loaded. Cannot perform prediction.")
        return {"text": text, "hope_hate": "Unknown", "emotion": "unknown", "score": 0.0}

    try:
      
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

    
        with torch.no_grad():
            outputs = model(**inputs)
        
        
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)[0]
        
   
        prediction_index = torch.argmax(probabilities).item()
        score = probabilities[prediction_index].item()
        
       
        predicted_emotion = EMOTION_LABELS[prediction_index]


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
