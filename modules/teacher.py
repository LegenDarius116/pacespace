from .user import User


class Teacher(User):
    """Class representing a Teacher Account"""
    def __init__(self, user_id: int, user_name: str):
        super().__init__(user_id=user_id, user_name=user_name)
