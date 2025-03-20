import json
from pathlib import Path
from datetime import datetime

from Domain.Entities.Category import Category
from Domain.interfaces.export_visitor import IExportVisitor

class JsonExportVisitor(IExportVisitor):
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def visit_bank_account(self, account) -> str:
        filename = self.output_dir / f"accounts_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        self._write_json(filename, [account])
        return str(filename)

    def visit_category(self, category) -> str:
        filename = self.output_dir / f"categories_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        self._write_json(filename, [category])
        return str(filename)

    def visit_operation(self, operation) -> str:
        filename = self.output_dir / f"operations_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        self._write_json(filename, [operation])
        return str(filename)

    def _write_json(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(
                [self._serialize(item) for item in data],
                f,
                default=self._serialize,
                indent=2
            )

    def _serialize(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj.__dict__
