from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = password
        self.role = role

    def __json__(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
        }

    @abstractmethod
    def menu(self, store):
        pass