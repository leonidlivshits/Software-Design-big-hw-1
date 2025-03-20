from Domain.Entities import BankAccount
from Services.Repositories.IRepository import IRepository
from Services.Repositories.in_memory_repository import InMemoryRepository

def test_add_and_get():
    repo = InMemoryRepository[BankAccount]()
    account = BankAccount(id=1, name="Test", balance=100)
    repo.add(account)
    assert repo.get(1) == account

def test_remove():
    repo = InMemoryRepository[BankAccount]()
    account = BankAccount(id=1, name="Test", balance=100)
    repo.add(account)
    repo.remove(1)
    assert repo.get(1) is None