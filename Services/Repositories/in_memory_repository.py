from typing import Dict, TypeVar, List, Optional
from Services.Repositories.IRepository import IRepository
from Domain.interfaces.entity import IEntity

T = TypeVar('T', bound=IEntity)

class InMemoryRepository(IRepository[T]):
    def __init__(self):
        self._storage: Dict[int, T] = {}

    def add(self, entity: T) -> None:
        self._storage[entity.id] = entity

    def get(self, entity_id: int) -> Optional[T]:
        return self._storage.get(entity_id)

    def get_all(self) -> List[T]:
        return list(self._storage.values())

    def remove(self, entity_id: int) -> None:
        if entity_id in self._storage:
            del self._storage[entity_id]