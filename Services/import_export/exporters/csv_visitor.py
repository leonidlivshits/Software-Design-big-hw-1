import csv
from pathlib import Path
from datetime import datetime
from Domain.interfaces.export_visitor import IExportVisitor
from Domain.Entities import BankAccount, Category, Operation

class CsvExportVisitor(IExportVisitor):
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def visit_bank_account(self, account: BankAccount) -> str:
        filename = self.output_dir / f"account_{account.id}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Balance"])
            writer.writerow([account.id, account.name, account.balance])
        return str(filename)

    def visit_category(self, category: Category) -> str:
        filename = self.output_dir / f"category_{category.id}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Type", "Name"])
            writer.writerow([category.id, category.type.value, category.name])
        return str(filename)

    def visit_operation(self, operation: Operation) -> str:
        filename = self.output_dir / f"operation_{operation.id}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Type", "Amount", "Date", "Category"])
            writer.writerow([
                operation.id,
                operation.type.value,
                operation.amount,
                operation.date.isoformat(),
                operation.category_id
            ])
        return str(filename)
    
# class CsvExportVisitor:
#     def __init__(self, output_dir: str = "exports"):
#         self.output_dir = Path(output_dir)
#         self.output_dir.mkdir(exist_ok=True)

#     def visit_bank_account(self, account) -> str:
#         filename = self.output_dir / f"accounts_{datetime.now().strftime('%Y%m%d')}.csv"
#         with open(filename, 'a', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow([
#                 account.id,
#                 account.name,
#                 account.balance
#             ])
#         return str(filename)