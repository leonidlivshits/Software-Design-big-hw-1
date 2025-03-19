import json
from pathlib import Path
from datetime import datetime
from typing import Any
from Domain.interfaces.export_visitor import IExportVisitor
from Domain.Entities import BankAccount, Category, Operation

class JsonExportVisitor(IExportVisitor):
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def _serialize(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj.__dict__

    def visit_bank_account(self, account: BankAccount) -> str:
        filename = self.output_dir / f"account_{account.id}.json"
        with open(filename, 'w') as f:
            json.dump(account, f, default=self._serialize, indent=2)
        return str(filename)

    def visit_category(self, category: Category) -> str:
        filename = self.output_dir / f"category_{category.id}.json"
        with open(filename, 'w') as f:
            json.dump(category, f, default=self._serialize, indent=2)
        return str(filename)

    def visit_operation(self, operation: Operation) -> str:
        filename = self.output_dir / f"operation_{operation.id}.json"
        with open(filename, 'w') as f:
            json.dump(operation, f, default=self._serialize, indent=2)
        return str(filename)