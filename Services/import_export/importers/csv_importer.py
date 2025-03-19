import csv
from datetime import datetime
from typing import List
from Domain.Entities import BankAccount, Operation, Category
from Domain.enums import TransactionType

class CsvImporter:
    def import_accounts(self, file_path: str) -> List[BankAccount]:
        accounts = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                accounts.append(BankAccount(
                    id=int(row['id']),
                    name=row['name'],
                    balance=float(row['balance'])
                ))
        return accounts

    def import_operations(self, file_path: str) -> List[Operation]:
        operations = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                operations.append(Operation(
                    id=int(row['id']),
                    type=TransactionType(row['type']),
                    bank_account_id=int(row['account_id']),
                    amount=float(row['amount']),
                    date=datetime.strptime(row['date'], "%Y-%m-%d"),
                    category_id=int(row['category_id']) if row['category_id'] else None
                ))
        return operations