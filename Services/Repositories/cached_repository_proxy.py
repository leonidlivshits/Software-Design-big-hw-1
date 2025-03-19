# from typing import Dict, TypeVar, Optional
# from Services.Repositories.IRepository import IRepository
# from Domain.interfaces.entity import IEntity

# T = TypeVar('T', bound=IEntity)

# class CachedRepositoryProxy(IRepository[T]):
#     def __init__(self, real_repository: IRepository[T]):
#         self._cache: Dict[int, T] = {}
#         self._real_repo = real_repository

#     def add(self, entity: T) -> None:
#         self._real_repo.add(entity)
#         self._cache[entity.id] = entity

#     def get(self, entity_id: int) -> Optional[T]:
#         if entity_id in self._cache:
#             return self._cache[entity_id]
#         entity = self._real_repo.get(entity_id)
#         if entity:
#             self._cache[entity_id] = entity
#         return entity

from typing import Dict, TypeVar, Optional, List
from Services.Repositories.IRepository import IRepository

T = TypeVar('T')

class CachedRepositoryProxy(IRepository[T]):
    def __init__(self, real_repository: IRepository[T]):
        self._cache: Dict[int, T] = {}
        self._real_repo = real_repository

    def add(self, entity: T) -> None:
        self._real_repo.add(entity)
        self._cache[entity.id] = entity

    def get(self, entity_id: int) -> Optional[T]:
        return self._cache.get(entity_id) or self._real_repo.get(entity_id)

    def get_all(self) -> List[T]:
        return self._real_repo.get_all()

    def remove(self, entity_id: int) -> None:
        self._real_repo.remove(entity_id)
        if entity_id in self._cache:
            del self._cache[entity_id]