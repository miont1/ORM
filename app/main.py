from .database import SessionLocal, init_db
from .crud import (
    add_book_to_order,
    create_author,
    create_book,
    create_order,
    create_user,
    get_all_orders,
    get_all_users,
    get_all_users_by_name,
    get_user_by_email,
    get_users_by_pattern,
)


def main():
    # Ініціалізуємо базу даних
    init_db()

    # Створюємо сесію
    db = SessionLocal()

    # Додаємо користувачів
    create_user(db, name="John Doe", email="john4@example.com")
    create_user(db, name="Jane Doe", email="jane4@example.com")

    # Виводимо всіх користувачів
    users = get_all_users(db)
    print("All users")
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")

    email = get_user_by_email(db, "jane2@example.com")
    print("User by email")
    print(email.email)

    users_by_name = get_all_users_by_name(db, "John")
    print("Users by name")
    for user in users_by_name:
        print(user.email)

    users_by_pattern = get_users_by_pattern(db, "j_n_%")
    print("Users by pattern")
    for user in users_by_pattern:
        print(user.email)

    create_author(db, name="Author2")
    create_author(db, name="Author3")
    create_book(db, title="Book2", author_ids=[2, 3])
    create_order(db, user_id=1)
    add_book_to_order(db, order_id=2, book_id=2, quantity=999)

    orders = get_all_orders(db)
    print(orders)


if __name__ == "__main__":
    main()
