from sqlalchemy import Column, Integer, String, DateTime
from orders.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, index=True)
    item = Column(String)
    quantity = Column(Integer)
    created_at = Column(DateTime(timezone=True))