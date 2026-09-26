"""Зрители театра."""


class User:
    """Зритель."""

    def __init__(self, user_id: int, name: str,
                 phone: str, email: str = "") -> None:
        self.id = user_id
        self.name = name
        self.phone = phone
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать зрителя из словаря."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            phone=data["phone"],
            email=data.get("email", ""),
        )

    def to_data(self) -> dict:
        """Преобразовать в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
        }

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.phone})"


def add_user(users: list[User], name: str, phone: str,
             email: str = "") -> User:
    """Добавить зрителя, вернуть созданный объект."""
    new_id = max((u.id for u in users), default=0) + 1
    user = User(new_id, name, phone, email)
    users.append(user)
    return user


def find_user(users: list[User], query: str) -> list[User]:
    """Найти зрителей по подстроке имени или телефона."""
    q = query.lower()
    return [u for u in users
            if q in u.name.lower() or q in u.phone.lower()]


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти зрителя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def show_users(users: list[User]) -> None:
    """Вывести список зрителей."""
    if not users:
        print("Зрителей нет.")
        return
    for user in users:
        print(user)
