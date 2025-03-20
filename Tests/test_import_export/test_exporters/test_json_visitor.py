from datetime import datetime
import json
from pathlib import Path
from Services.import_export.exporters.json_visitor import JsonExportVisitor
from Domain.Entities.Operation import Operation
from Domain.enums.transaction_type import TransactionType


def test_json_export_operation(tmp_path, sample_operation):
    exporter = JsonExportVisitor(tmp_path)
    
    exporter._serialize = lambda obj: {
        "id": obj.id,
        "type": obj.type.value,
        "amount": obj.amount,
        "date": obj.date.isoformat()
    }
    
    exporter.visit_operation(sample_operation)
    
    with open(next(tmp_path.glob("operations_*.json"))) as f:
        data = json.load(f)[0]
        assert data["type"] == "income"
        assert data["amount"] == 500.0

def test_json_export_edge_cases(tmp_path):

    exporter = JsonExportVisitor(tmp_path)
    
    exporter._serialize = lambda obj: {
        "id": obj.id,
        "type": obj.type.value,
        "amount": obj.amount,
        "date": obj.date.isoformat()
    }

    operation = Operation(
        id=1,
        type=TransactionType.EXPENSE,
        amount=0.01,
        date=datetime.min,
        bank_account_id=None
    )
    
    exporter.visit_operation(operation)
    
    with open(next(tmp_path.glob("operations_*.json"))) as f:
        data = json.load(f)[0]
        assert data["amount"] == 0.01