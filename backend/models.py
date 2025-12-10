from pydantic import BaseModel
from typing import List, Optional

class ProductRequest(BaseModel):
    product_name: str
    features: List[str]
    target_audience: str
    tone: Optional[str] = "professional"

class ProductResponse(BaseModel):
    product_name: str
    description: str
    keywords: List[str]
