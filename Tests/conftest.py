import json
from pytest import fixture
from datetime import datetime

from Infrastructure.di.container import Container
from Services.Repositories.in_memory_repository import InMemoryRepository
from Services.Repositories.cached_repository_proxy import CachedRepositoryProxy
from Services.Facades.account_facade import AccountFacade
from Services.Facades.operation_facade import OperationFacade
from Services.Facades.category_facade import CategoryFacade
from Domain.Entities import BankAccount, Operation, Category
from Domain.enums import TransactionType
from UserInterface.ConsoleInterface import ConsoleInterface

@fixture
def account_repo():
    return CachedRepositoryProxy(InMemoryRepository[BankAccount]())

@fixture
def operation_repo():
    return CachedRepositoryProxy(InMemoryRepository[Operation]())

@fixture
def category_repo():
    return CachedRepositoryProxy(InMemoryRepository[Category]())

@fixture
def account_facade(account_repo):
    return AccountFacade(account_repo)

@fixture
def operation_facade(operation_repo, account_facade):
    return OperationFacade(operation_repo, account_facade)

@fixture
def category_facade(category_repo):
    return CategoryFacade(category_repo)

@fixture
def sample_account():
    return BankAccount(id=1, name="Test Account", balance=1000.0)

@fixture
def sample_operation(sample_account):
    return Operation(
        id=1,
        type=TransactionType.INCOME,
        bank_account_id=sample_account.id,
        amount=500.0,
        date=datetime.now(),
        category_id=1
    )

@fixture
def sample_category():
    return Category(id=1, type=TransactionType.EXPENSE, name="Food")

@fixture
def broken_accounts_csv(tmp_path):
    file = tmp_path / "broken.csv"
    file.write_text("id,name\n1,Test")
    return file



@fixture
def test_account_csv(tmp_path):
    csv_content = "id,name,balance\n1,Test,1000"
    test_file = tmp_path / "test.csv"
    test_file.write_text(csv_content)
    return test_file

@fixture
def test_operation_csv(tmp_path):
    csv_content = """id,type,amount,date,bank_account_id
1,income,500.0,2023-01-01,1"""
    file_path = tmp_path / "test_ops.csv"
    file_path.write_text(csv_content)
    return file_path


@fixture
def test_account_json(tmp_path, sample_account):
    data = [{
        "id": sample_account.id,
        "name": sample_account.name,
        "balance": sample_account.balance
    }]
    file = tmp_path / "accounts.json"
    file.write_text(json.dumps(data))
    return file

@fixture
def test_operation_json(tmp_path, sample_operation):
    data = [{
        "id": sample_operation.id,
        "type": sample_operation.type.value,
        "amount": sample_operation.amount,
        "date": sample_operation.date.isoformat(),
        "bank_account_id": sample_operation.bank_account_id,
        "category_id": sample_operation.category_id
    }]
    file = tmp_path / "operations.json"
    file.write_text(json.dumps(data))
    return file

@fixture
def broken_accounts_json(tmp_path):
    data = [{"id": 1, "name": "Invalid Account"}]
    file = tmp_path / "broken_accounts.json"
    file.write_text(json.dumps(data))
    return file


@fixture
def container():
    return Container()

@fixture
def console(container):
    return ConsoleInterface(container)