from dataclasses import dataclass
from Domain.enums.transaction_type import TransactionType

@dataclass
class Category:
    id: int
    type: TransactionType
    name: str