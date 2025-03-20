import csv
from datetime import datetime
from typing import List

from Domain.Entities.BankAccount import BankAccount
from Domain.Entities.Category import Category
from Domain.Entities.Operation import Operation
from Domain.enums import TransactionType



class CsvImporter:
    def __init__(self, account_facade, operation_facade):
        self.account_facade = account_facade
        self.operation_facade = operation_facade

    def import_data(self, file_path: str, entity_type: str) -> int:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                if entity_type == "accounts":
                    return self._import_accounts(rows)
                elif entity_type == "operations":
                    return self._import_operations(rows)
                elif entity_type == "categories":
                    return self._import_categories(rows)
                else:
                    raise ValueError("Неизвестный тип сущности")
        except Exception as e:
            raise ValueError(f"Ошибка импорта CSV: {str(e)}")

    def _import_accounts(self, rows: List[dict]) -> int:
        count = 0
        for row in rows:
            try:
                self._validate_row(row, ['id', 'name', 'balance'])
                self.account_facade.create_account(
                    account_id=int(row['id']),
                    name=row['name'],
                    balance=float(row['balance']))
                count += 1
            except Exception as e:
                print(f"Ошибка в строке {row}: {str(e)}")
        return count

    def _import_operations(self, rows: List[dict]) -> int:
        count = 0
        for row in rows:
            try:
                self._validate_row(row, ['id', 'type', 'amount', 'date', 'bank_account_id'])
                operation = Operation(
                    id=int(row['id']),
                    type=self._parse_transaction_type(row['type']),
                    amount=float(row['amount']),
                    date=datetime.strptime(row['date'], "%Y-%m-%d"),
                    bank_account_id=int(row['bank_account_id']),
                    category_id=int(row['category_id']) if row.get('category_id') else None
                )
                self.operation_facade.create_operation(operation)
                count += 1
            except Exception as e:
                print(f"Ошибка в строке {row}: {str(e)}")
        return count

    def _validate_row(self, row: dict, required_fields: list):
        missing = [field for field in required_fields if field not in row]
        if missing:
            raise ValueError(f"Отсутствуют обязательные поля: {', '.join(missing)}")

    def _parse_transaction_type(self, type_str: str) -> TransactionType:
        try:
            return TransactionType(type_str.lower())
        except ValueError:
            raise ValueError(f"Недопустимый тип операции: {type_str}")
