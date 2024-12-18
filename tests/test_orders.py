import pytest
import sqlalchemy
from app.models import User, Author, Order, Book
from app.crud import (
    get_all_orders,
    add_book_to_order,
)


def test_create_order(db_session):
    # Створення тестових користувачів
    user = User(name="john", email="john@example.com")
    db_session.add(user)

    author1 = Author(name="Author1")
    db_session.add(author1)

    author2 = Author(name="Author2")
    db_session.add(author2)

    book1 = Book(title="Book1", authors=[author1, author2])
    db_session.add(book1)

    book2 = Book(title="Book2", authors=[author2])
    db_session.add(book2)

    order1 = Order(user_id=1)
    db_session.add(order1)

    order2 = Order(user_id=1)
    db_session.add(order2)

    db_session.commit()

    add_book_to_order(db_session, order_id=1, book_id=1, quantity=2)
    add_book_to_order(db_session, order_id=1, book_id=2, quantity=5)

    add_book_to_order(db_session, order_id=2, book_id=2, quantity=5)
    add_book_to_order(db_session, order_id=2, book_id=2, quantity=5)
    add_book_to_order(db_session, order_id=2, book_id=1, quantity=3)

    # Виконання тесту
    orders = get_all_orders(db_session)
    print(orders)
    assert len(orders) == 2

    quantity_books_order2 = 0
    for book in order2.books:
        quantity_books_order2 += order2.get_book_quantity(book_id=book.id)
    assert quantity_books_order2 == 13

    # Перевірка додавання книги до неіснуючого замовлення
    with pytest.raises(ValueError, match="Замовлення з ID 3 не знайдено."):
        add_book_to_order(db_session, order_id=3, book_id=2, quantity=5)
