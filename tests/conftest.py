import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL_ORM")
if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL_ORM environment variable is not set")


engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def setup_database():
    # Створення таблиць в тестовій базі даних
    Base.metadata.create_all(bind=engine)
    yield
    # Очистка після тестів
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(setup_database):
    # Підключення до сесії для тестів
    db = SessionLocal()
    yield db
    db.close()
