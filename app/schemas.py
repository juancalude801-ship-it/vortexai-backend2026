from pydantic import BaseModel, EmailStr
from typing import Optional, List

class BuyerCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    city: str
    state: str
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    strategy: Optional[str] = None

class BuyerOut(BuyerCreate):
    id: int
    class Config:
        from_attributes = True

class SellerIntake(BaseModel):
    full_name: str
    phone: str
    email: Optional[EmailStr] = None
    property_address: str
    city: str
    state: str
    reason: Optional[str] = None
    asking_price: Optional[int] = None
    timeline: Optional[str] = None
    notes: Optional[str] = None

class DealOut(BaseModel):
    id: int
    address: str
    city: str
    state: str
    zipcode: Optional[str] = None
    list_price: Optional[int] = None
    beds: Optional[int] = None
    baths: Optional[float] = None
    sqft: Optional[int] = None
    year_built: Optional[int] = None
    property_type: Optional[str] = None

    arv: Optional[int] = None
    repairs: Optional[int] = None
    mao: Optional[int] = None

    score: int
    status: str

    class Config:
        from_attributes = True

class UnderwriteRequest(BaseModel):
    arv: Optional[int] = None
    repairs: Optional[int] = None
    assignment_fee: Optional[int] = 10000
    investor_rule: Optional[float] = 0.70  # 70% rule
