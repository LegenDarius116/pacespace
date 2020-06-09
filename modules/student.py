from .user import User


class Student(User):
    """Class representing a Student Account"""
    def __init__(self, id: int, name: str):
        super().__init__(id=id, name=name)
