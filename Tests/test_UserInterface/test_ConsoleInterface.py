from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from Domain.Entities.BankAccount import BankAccount
from Domain.Entities.Category import Category
from Domain.Entities.Operation import Operation
from Domain.enums.transaction_type import TransactionType


def test_main_menu_exit(console, monkeypatch):
    with patch('builtins.input', side_effect=['0']):
        with pytest.raises(SystemExit):
            console.run()

def test_account_creation(console, monkeypatch):
    mock_input = MagicMock(side_effect=['1', 'Test Account', '1000'])
    monkeypatch.setattr('builtins.input', mock_input)
    
    console._create_account()
    accounts = console.container.get_account_facade().get_all_accounts()
    
    assert len(accounts) == 1
    assert accounts[0].name == "Test Account"

def test_operation_creation(console, sample_account, monkeypatch):
    mock_account_facade = MagicMock()
    mock_operation_facade = MagicMock()
    mock_category_facade = MagicMock()
    
    console.container.account_facade = mock_account_facade
    console.container.operation_facade = mock_operation_facade
    console.container.category_facade = mock_category_facade
    
    mock_account = sample_account
    mock_account_facade.get_account.return_value = mock_account
    mock_category_facade.get_category.return_value = Category(id=1, type=TransactionType.EXPENSE, name="Food")
    console.current_account_id = 1
    
    input_values = ['1', '500', '1', '1', '2023-01-01']
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))
    
    console._create_operation()
    
    mock_operation_facade.create_operation.assert_called_once()
    operation = mock_operation_facade.create_operation.call_args[0][0]
    assert operation.amount == 500
    assert operation.bank_account_id == 1
    assert operation.type == TransactionType.EXPENSE

def test_export_operations(console, monkeypatch):
    mock_exporter = MagicMock()
    mock_operation_facade = MagicMock()
    
    console.container.operation_facade = mock_operation_facade
    console.container.exporters['json'] = mock_exporter
    console.current_account_id = 1
    
    test_operation = Operation(
        id=1,
        type=TransactionType.INCOME,
        amount=500,
        bank_account_id=1,
        date=datetime.now()
    )
    mock_operation_facade.get_operations_by_account.return_value = [test_operation]
    
    input_values = ['json', 'operations']
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))
    
    console._export_data()

    mock_exporter.visit_operation.assert_called_once_with(test_operation)
    mock_operation_facade.get_operations_by_account.assert_called_with(1)

def test_invalid_date_input(console, monkeypatch):
    mock_input = MagicMock(side_effect=['invalid-date', '2023-01-01'])
    monkeypatch.setattr('builtins.input', mock_input)
    
    result = console._input_date("Введите дату: ")
    assert result == datetime(2023, 1, 1)

def test_category_creation(console, monkeypatch):
    mock_input = MagicMock(side_effect=['1', 'Food', '2'])
    monkeypatch.setattr('builtins.input', mock_input)
    
    console._create_category()
    categories = console.container.category_facade.get_all_categories()
    
    assert len(categories) == 1
    assert categories[0].type == TransactionType.EXPENSE





def test_delete_account_success(console, monkeypatch, capsys):
    test_account = BankAccount(id=1, name="Test", balance=1000)
    console.container.account_facade.create_account(test_account.id, test_account.name, test_account.balance)
    
    inputs = ["1"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    
    console._delete_account()
    
    captured = capsys.readouterr()
    assert "Аккаунт удалён!" in captured.out
    assert len(console.container.account_facade.get_all_accounts()) == 0

def test_list_accounts_with_data(console, capsys):
    console.container.account_facade.create_account(1, "Account1", 1000)
    console.container.account_facade.create_account(2, "Account2", 2000)
    
    console._list_accounts()
    
    captured = capsys.readouterr()
    assert "Account1 (1000.00 руб.)" in captured.out
    assert "Account2 (2000.00 руб.)" in captured.out

def test_select_account_invalid_id(console, monkeypatch, capsys):
    inputs = ["999"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    
    console._select_account()
    
    captured = capsys.readouterr()
    assert "Счет не найден!" in captured.out

def test_delete_operation_success(console, monkeypatch, capsys):
    console.container.account_facade.create_account(1, "Test Account", 1000)
    console.current_account_id = 1

    op = Operation(
        id=1,
        type=TransactionType.INCOME,
        bank_account_id=1,
        amount=500,
        date=datetime.now()
    )
    console.container.operation_facade.create_operation(op)

    inputs = ["1"]
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    
    console._delete_operation()

    captured = capsys.readouterr()
    assert "Операция удалена!" in captured.out
    assert len(console.container.operation_facade.get_operations_by_account(1)) == 0