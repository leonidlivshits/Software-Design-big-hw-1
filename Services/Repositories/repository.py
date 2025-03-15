from typing import Generic, TypeVar, List, Optional
from Domain.interfaces.entity import IEntity

T = TypeVar('T', bound=IEntity)

class IRepository(Generic[T]):
    def add(self, entity: T) -> None:
        raise NotImplementedError
    
    def get(self, entity_id: int) -> Optional[T]:
        raise NotImplementedError
    
    def get_all(self) -> List[T]:
        raise NotImplementedError