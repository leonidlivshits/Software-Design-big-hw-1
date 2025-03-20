import csv
from pathlib import Path
from datetime import datetime
from Domain.interfaces.export_visitor import IExportVisitor
from Domain.Entities.Category import Category
from Domain.Entities.BankAccount import BankAccount
from Domain.Entities.Operation import Operation    

class CsvExportVisitor(IExportVisitor):
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def visit_bank_account(self, account) -> str:
        filename = self.output_dir / f"accounts_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        self._write_csv(filename, [account], ["id", "name", "balance"])
        return str(filename)

    def visit_category(self, category) -> str:
        filename = self.output_dir / f"categories_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        self._write_csv(filename, [category], ["id", "type", "name"])
        return str(filename)

    def visit_operation(self, operation) -> str:
        filename = self.output_dir / f"operations_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        self._write_csv(filename, [operation], 
                      ["id", "type", "amount", "date","bank_account_id", "category_id"],
                      lambda op: [
                          op.id,
                          op.type.value,
                          op.amount,
                          op.date.strftime("%Y-%m-%d"),
                          op.bank_account_id,
                          op.category_id
                      ])
        return str(filename)

    def _write_csv(self, filename, data, headers, transformer=lambda x: x):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for item in data:
                writer.writerow(transformer(item))