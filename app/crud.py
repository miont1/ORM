from sqlalchemy.orm import Session
from .models import User


def create_user(db: Session, name: str, email: str):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session):
    return db.query(User).all()


def get_all_users_by_name(db: Session, name: str):
    return db.query(User).filter(User.name.ilike(f"%{name}%")).all()


def get_users_by_pattern(db: Session, pattern: str):
    return db.query(User).filter(User.name.ilike(pattern)).all()
