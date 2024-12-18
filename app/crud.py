from sqlalchemy.orm import Session
from .models import Author, Book, Order, User, OrderItem


def create_user(db: Session, name: str, email: str) -> User:
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


def create_order(db: Session, user_id: int) -> Order:

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User with id {user_id} does not exist.")

    new_order = Order(user_id=user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def create_book(db: Session, title: str, author_ids: list) -> Book:
    book = Book(title=title)

    authors = db.query(Author).filter(Author.id.in_(author_ids)).all()
    book.authors = authors

    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def create_author(db: Session, name: str) -> Author:
    author = Author(name=name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def add_book_to_order(db: Session, order_id: int, book_id: int, quantity: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    book = db.query(Book).filter(Book.id == book_id).first()

    if not order:
        raise ValueError(f"Замовлення з ID {order_id} не знайдено.")
    if not book:
        raise ValueError(f"Книгу з ID {book_id} не знайдено.")
    if quantity <= 0:
        raise ValueError("Кількість має бути більше нуля.")

    order_item = OrderItem(order_id=order_id, book_id=book_id, quantity=quantity)
    db.add(order_item)
    db.commit()


def get_all_orders(db: Session):
    return db.query(Order).all()
