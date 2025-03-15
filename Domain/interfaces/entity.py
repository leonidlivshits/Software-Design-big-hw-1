from abc import ABC, abstractmethod

class IEntity(ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        pass