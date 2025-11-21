import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY environment variable!")

genai.configure(api_key=api_key)

SYSTEM_PROMPT= """
You are a Content Creator Assistant you are supposed to help motivate and assist the content creators (specifically youtubers).
"""

MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

def chatbot(prompt :str) -> str :
    response = model.generate_content(SYSTEM_PROMPT+prompt)
    print(response.text)
    return response.text
