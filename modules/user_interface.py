class UserInterface:
    """A class that mimics an interface for Users"""
    def __init__(self):
        raise NotImplementedError

    def get_id(self):
        raise NotImplementedError

    def set_id(self, user_id: str):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def set_name(self, user_name: str):
        raise NotImplementedError
