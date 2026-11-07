import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from orders.main import app
from orders.db import Base, get_db

# Создаём тестовую базу в памяти (SQLite)
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Создаёт таблицы перед каждым тестом и удаляет после."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    """Подменяет get_db на тестовую сессию."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Принудительно подменяем зависимость в приложении
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def order_payload():
    return {
        "account_id": 1,
        "item": "Тестовая пицца",
        "quantity": 2
    }