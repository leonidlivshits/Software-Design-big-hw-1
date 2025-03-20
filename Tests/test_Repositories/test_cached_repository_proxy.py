from Domain.Entities.BankAccount import BankAccount
from Services.Repositories.cached_repository_proxy import CachedRepositoryProxy
from Services.Repositories.in_memory_repository import InMemoryRepository


def test_cached_repository_proxy():
    repo = CachedRepositoryProxy(InMemoryRepository())
    entity = BankAccount(id=1, name="Test", balance=100)
    
    repo.add(entity)
    assert repo.get(1) == entity
    repo.remove(1)
    assert repo.get(1) is None