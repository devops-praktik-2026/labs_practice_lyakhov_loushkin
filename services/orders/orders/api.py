from fastapi import APIRouter, Depends, HTTPException, status
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
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Заказ {order_id} не найден")
    return order

@router.get("/orders", response_model=list[schemas.OrderResponse])
def get_orders_by_account(account_id: int, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.account_id == account_id).limit(limit).all()
    return orders