import csv
from pathlib import Path
from datetime import datetime

import pytest

from Domain.Entities.Operation import Operation
from Domain.enums.transaction_type import TransactionType
from Services.import_export.exporters.csv_visitor import CsvExportVisitor

def test_csv_export_account(tmp_path, sample_account):
    from Services.import_export.exporters.csv_visitor import CsvExportVisitor
    exporter = CsvExportVisitor(tmp_path)
    
    exporter.visit_bank_account = lambda account: exporter._write_csv(
        Path(tmp_path) / "accounts_test.csv",
        [account],
        ["id", "name", "balance"],
        lambda x: [x.id, x.name, x.balance]
    )
    
    exporter.visit_bank_account(sample_account)
    
    with open(Path(tmp_path) / "accounts_test.csv") as f:
        reader = csv.DictReader(f)
        row = next(reader)
        assert row["id"] == "1"
        assert row["name"] == "Test Account"

