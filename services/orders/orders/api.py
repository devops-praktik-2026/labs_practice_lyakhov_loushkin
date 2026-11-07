from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from orders import models, schemas
from orders.db import get_db

router = APIRouter()


@router.post("/orders", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(
        account_id=order.account_id,
        item=order.item,
        quantity=order.quantity,
        created_at=datetime.now(timezone.utc)  # Явно задаём время
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order