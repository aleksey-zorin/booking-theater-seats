"""Тесты зрителей."""

from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, "Иванов Иван", "+7-900", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иванов Иван"
    assert user.phone == "+7-900"
    assert user.email == "ivan@example.com"


def test_user_from_data_and_to_data():
    original = User(2, "Петрова Анна", "+7-901", "a@example.com")
    restored = User.from_data(original.to_data())
    assert restored.id == original.id
    assert restored.name == original.name
    assert restored.email == original.email


def test_add_user_assigns_id():
    users: list[User] = []
    user = add_user(users, "Сидоров", "+7-902")
    assert user.id == 1
    assert users == [user]


def test_find_user():
    users = [User(1, "Иванов", "+7-900"), User(2, "Петрова", "+7-901")]
    assert len(find_user(users, "иван")) == 1
    assert len(find_user(users, "+7-901")) == 1
    assert find_user(users, "xyz") == []


def test_find_user_by_id():
    users = [User(1, "Иванов", "+7-900")]
    assert find_user_by_id(users, 1).name == "Иванов"
    assert find_user_by_id(users, 99) is None
