from abc import ABC, abstractmethod


class User(ABC):
    """A class that mimics an abstract class for Users"""
    @abstractmethod
    def __init__(self, user_id: int, user_name: str):
        self._id = user_id
        self._name = user_name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @id.setter
    def id(self, user_id):
        self._id = user_id

    @name.setter
    def name(self, user_name: str):
        self._name = user_name