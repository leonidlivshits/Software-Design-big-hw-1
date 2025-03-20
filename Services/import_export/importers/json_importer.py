from datetime import datetime
import json
from typing import Dict, List, Union
from pathlib import Path
from Domain.Entities.BankAccount import BankAccount
from Domain.Entities.Operation import Operation
from Domain.Entities.Category import Category
from Domain.enums.transaction_type import TransactionType


class JsonImporter:
    def __init__(self, account_facade, operation_facade):
        self.account_facade = account_facade
        self.operation_facade = operation_facade

    def import_data(self, file_path: str, entity_type: str) -> int:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            if entity_type == "accounts":
                return self._import_accounts(data)
            elif entity_type == "operations":
                return self._import_operations(data)
            elif entity_type == "categories":
                return self._import_categories(data)
            else:
                raise ValueError("Неизвестный тип сущности")

    def _import_accounts(self, data: Union[Dict, List[Dict]]) -> int:
        count = 0
        items = data if isinstance(data, list) else [data]
        
        for item in items:
            try:
                if not all(key in item for key in ['id', 'name', 'balance']):
                    raise ValueError("Некорректная структура данных аккаунта")
                
                self.account_facade.create_account(
                    account_id=int(item['id']),
                    name=str(item['name']),
                    balance=float(item['balance']))
                count += 1
                
            except Exception as e:
                print(f"Ошибка импорта аккаунта: {str(e)}")
        return count
    
    def _import_operations(self, data: List[dict]) -> int:
        count = 0
        items = data if isinstance(data, list) else [data]
        
        for item in items:
            try:
                if not all(key in item for key in ['id', 'type', 'bank_account_id', 'amount', 'date', 'category_id']):
                    raise ValueError("Некорректная структура данных операции")
                
                operation = Operation(
                    id=item['id'],
                    type=TransactionType(item['type']),
                    bank_account_id=item['bank_account_id'],
                    amount=item['amount'],
                    date=datetime.fromisoformat(item['date']),
                    category_id=item.get('category_id')

                )
                self.operation_facade.create_operation(operation)
                count += 1
                
            except Exception as e:
                print(f"Ошибка импорта аккаунта: {str(e)}")
        return count
