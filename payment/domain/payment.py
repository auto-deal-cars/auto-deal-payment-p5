"""Payment domain model"""
from typing import Optional
from pydantic import BaseModel, Field

class Payment(BaseModel):
    """Payment domain model"""
    idempotency_key: str = Field(..., description="Idempotency key")
    payment_id: int = Field(..., description="Payment id")
    status: str = Field(..., description="Payment status")
    order_id: int = Field(..., description="Order id")
    vehicle_id: int = Field(..., description="Vehicle id")
    created_at: Optional[str] = Field(default=None, description="Payment created at")
    updated_at: Optional[str] = Field(default=None, description="Payment updated at")
