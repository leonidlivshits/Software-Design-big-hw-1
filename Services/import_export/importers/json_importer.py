import json
from datetime import datetime
from typing import List
from Domain.Entities import BankAccount, Operation, Category
from Domain.enums import TransactionType

class JsonImporter:
    def import_accounts(self, file_path: str) -> List[BankAccount]:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return [BankAccount(**item) for item in data]

    def import_operations(self, file_path: str) -> List[Operation]:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return [
                Operation(
                    id=item['id'],
                    type=TransactionType(item['type']),
                    bank_account_id=item['account_id'],
                    amount=item['amount'],
                    date=datetime.fromisoformat(item['date']),
                    category_id=item.get('category_id')
                ) for item in data
            ]