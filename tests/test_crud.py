from app.models import User
from app.crud import get_users_by_pattern


def test_get_users_by_pattern(db_session):
    # Створення тестових користувачів
    user1 = User(name="john", email="john@example.com")
    user2 = User(name="jane", email="jane@example.com")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    # Виконання тесту
    users = get_users_by_pattern(db_session, "j_n_")

    assert len(users) == 1
    assert users[0].name == "jane"  
