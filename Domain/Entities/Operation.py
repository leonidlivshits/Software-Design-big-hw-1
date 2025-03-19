from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from Domain.enums.transaction_type import TransactionType
from Domain.exceptions import DomainException

@dataclass
class Operation:
    id: int
    type: TransactionType
    bank_account_id: int
    amount: float
    date: datetime
    description: Optional[str] = None
    category_id: Optional[int] = None

    def __post_init__(self):
        if self.amount <= 0:
            raise DomainException("Amount must be positive")
        
class OperationFactory:
    @staticmethod
    def create(
        id: int,
        type: str,
        account_id: int,
        amount: float,
        date: datetime,
        category_id: int = None,
        description: str = None
    ) -> Operation:
        if type.lower() not in ("income", "expense"):
            raise ValueError("Invalid operation type")
        
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if date > datetime.now():
            raise ValueError("Operation date cannot be in the future")

        return Operation(
            id=id,
            type=TransactionType(type.lower()),
            bank_account_id=account_id,
            amount=amount,
            date=date,
            category_id=category_id,
            description=description
        )