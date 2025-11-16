from abc import ABC, abstractmethod

from models.roll_data import random_create_description


class Roller(ABC):
    @staticmethod
    @abstractmethod
    def generate(self):
        pass

    @staticmethod
    @abstractmethod
    def get_roll_description(self) -> random_create_description:
        pass
