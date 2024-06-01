from typing import List, Optional


class UserModel:
    users = []
    id_counter = 1

    @classmethod
    def get_users(cls) -> List[dict]:
        return cls.users

    @classmethod
    def create_user(cls, name: str, email: str) -> dict:
        user = {"id": cls.id_counter, "name": name, "email": email}
        cls.users.append(user)
        cls.id_counter += 1
        return user

    @classmethod
    def delete_user(cls, user_id: int) -> bool:
        for user in cls.users:
            if user["id"] == user_id:
                cls.users.remove(user)
                return True
        return False
