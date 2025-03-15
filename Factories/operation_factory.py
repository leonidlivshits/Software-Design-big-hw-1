from datetime import datetime
from typing import Optional
from Domain.Entities.Operation import Operation
from Domain.enums.transaction_type import TransactionType
from Domain.exceptions import DomainException

class OperationFactory:
    @staticmethod
    def create(
        id: int,
        type: str,
        account_id: int,
        amount: float,
        date: datetime,
        category_id: Optional[int] = None,
        description: Optional[str] = None
    ) -> Operation:
        try:
            return Operation(
                id=id,
                type=TransactionType(type.lower()),
                bank_account_id=account_id,
                amount=amount,
                date=date,
                category_id=category_id,
                description=description
            )
        except DomainException as e:
            raise ValueError(str(e)) from e