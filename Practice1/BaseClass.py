from abc import ABC, abstractmethod

class Entity(ABC):
    @abstractmethod
    def display_info(self):
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, data):
        pass

    @abstractmethod
    def to_json(self):
        pass