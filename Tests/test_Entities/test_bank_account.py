import pytest
from Domain.Entities.BankAccount import BankAccount
from Domain.exceptions import DomainException


def test_negative_balance():
    with pytest.raises(DomainException):
        BankAccount(id=1, name="Test", balance=-100)