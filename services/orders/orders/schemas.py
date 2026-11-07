from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class OrderCreate(BaseModel):
    account_id: int
    item: str
    quantity: int = Field(..., ge=1)


class OrderResponse(BaseModel):
    id: int
    account_id: int
    item: str
    quantity: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)