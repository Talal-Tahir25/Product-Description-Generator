import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # User provided key previously
    api_key = "AIzaSyCDYE4DhvBWF1bCWTZrDFl8hgFwmkdPeow"

with open("models.txt", "w") as f:
    try:
        f.write(f"Checking models...\n")
        genai.configure(api_key=api_key)
        
        f.write("Listing available models:\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"- {m.name}\n")
    except Exception as e:
        f.write(f"Error listing models: {e}\n")
