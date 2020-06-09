from .user import User


class Student(User):
    """Class representing a Student Account"""
    def __init__(self, user_id: int, user_name: str):
        super().__init__(user_id=user_id, user_name=user_name)
