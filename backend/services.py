import os
import random
from models import ProductRequest, ProductResponse

# Mock data for fallback when no API key is present
MOCK_DESCRIPTIONS = [
    "Experience the ultimate in quality with the {name}. Designed for {audience}, this product features {features}. It's the perfect addition to your daily routine, offering reliability and style.",
    "Unlock new possibilities with {name}. Tailored strictly for {audience}, it brings {features} to the table. Elevate your experience today.",
    "Discover the precision of the {name}. A game-changer for {audience}, highlighting {features} for maximum efficiency."
]

MOCK_KEYWORDS = ["premium", "quality", "durable", "innovative", "must-have", "top-rated"]

from dotenv import load_dotenv

load_dotenv()

def generate_product_content(request: ProductRequest) -> ProductResponse:
    # Use the key provided by the user (or from env)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
         # Fallback error if not found
         return ProductResponse(
            product_name=request.product_name,
            description="[ERROR] API Key not found. Please set GEMINI_API_KEY in .env file.",
            keywords=["error"]
        )

    return _generate_gemini(request, api_key)

def _generate_gemini(request: ProductRequest, api_key: str) -> ProductResponse:
    """
    Integration with Google Gemini API.
    """
    try:
        import google.generativeai as genai
        import json
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        You are a professional copywriter.
        Generate a {request.tone} product description for:
        Product: {request.product_name}
        Audience: {request.target_audience}
        Features: {', '.join(request.features)}
        
        Also provide 5 SEO keywords.
        
        Output strictly valid JSON with keys: "description" (string) and "keywords" (list of strings).
        Do not include markdown code blocks (```json). Just the raw JSON.
        """
        
        response = model.generate_content(prompt)
        
        # Clean up potential markdown formatting if Gemini adds it
        content_str = response.text.strip()
        if content_str.startswith("```json"):
            content_str = content_str[7:]
        if content_str.endswith("```"):
            content_str = content_str[:-3]
            
        content = json.loads(content_str)
        
        return ProductResponse(
            product_name=request.product_name,
            description=content.get("description", "Description generation failed."),
            keywords=content.get("keywords", [])
        )
        
    except ImportError:
         return ProductResponse(
            product_name=request.product_name,
            description="[ERROR] google-generativeai library not installed.",
            keywords=["error"]
        )
    except Exception as e:
         return ProductResponse(
            product_name=request.product_name,
            description=f"[ERROR] Gemini Generation failed: {str(e)}",
            keywords=["error"]
        )
