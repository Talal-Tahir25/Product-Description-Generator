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

def generate_product_content(request: ProductRequest) -> ProductResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return _generate_mock(request)
    
    return _generate_llm(request, api_key)

def _generate_mock(request: ProductRequest) -> ProductResponse:
    """Fallback generator when no API key is provided."""
    features_str = ", ".join(request.features)
    template = random.choice(MOCK_DESCRIPTIONS)
    
    description = template.format(
        name=request.product_name,
        audience=request.target_audience,
        features=features_str
    )
    
    # Generate some pseudo-dynamic keywords
    keywords = list(set([request.product_name.split()[0].lower(), request.target_audience.split()[0].lower()] + 
               random.sample(MOCK_KEYWORDS, 4)))
    
    return ProductResponse(
        product_name=request.product_name,
        description=description,
        keywords=keywords
    )

def _generate_llm(request: ProductRequest, api_key: str) -> ProductResponse:
    """
    Real integration with OpenAI (or compatible LLM).
    Note: Requires 'openai' package installed.
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        Generate a {request.tone} product description for:
        Product: {request.product_name}
        Audience: {request.target_audience}
        Features: {', '.join(request.features)}
        
        Also provide 5 SEO keywords.
        Format output as JSON with keys: description, keywords (list).
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional copywriter."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        import json
        content = json.loads(response.choices[0].message.content)
        
        return ProductResponse(
            product_name=request.product_name,
            description=content.get("description", "Description generation failed."),
            keywords=content.get("keywords", [])
        )
        
    except ImportError:
        return ProductResponse(
            product_name=request.product_name,
            description="[ERROR] OpenAI library not installed. Please install it or unset the API key to use mock mode. (pip install openai)",
            keywords=["error"]
        )
    except Exception as e:
         return ProductResponse(
            product_name=request.product_name,
            description=f"[ERROR] LLM Generation failed: {str(e)}",
            keywords=["error"]
        )
