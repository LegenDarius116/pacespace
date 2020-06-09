from .user import User


class Teacher(User):
    """Class representing a Teacher Account"""
    def __init__(self, id: int, name: str):
        super().__init__(id=id, name=name)
