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