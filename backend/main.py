from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ProductRequest, ProductResponse, AudienceRequest, AudienceResponse
from services import generate_product_content, generate_audience_suggestions
import uvicorn

app = FastAPI(title="Product Description Generator API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Product Generator API is running"}

@app.post("/generate", response_model=ProductResponse)
def generate_description(request: ProductRequest):
    try:
        response = generate_product_content(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/suggest_audiences", response_model=AudienceResponse)
def suggest_audiences(request: AudienceRequest):
    try:
        return generate_audience_suggestions(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
