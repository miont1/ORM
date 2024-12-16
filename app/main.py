from .database import SessionLocal, init_db
from .crud import (
    create_user,
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
    create_user(db, name="John Doe2", email="john2@example.com")
    create_user(db, name="Jane Doe2", email="jane2@example.com")

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


if __name__ == "__main__":
    main()
