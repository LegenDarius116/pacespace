from abc import ABC, abstractmethod


class User(ABC):
    """A class that mimics an abstract class for Users"""
    @abstractmethod
    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name

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
