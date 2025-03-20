import pytest
from Services.import_export.importers.csv_importer import CsvImporter


def test_import_accounts(test_account_csv, account_facade):
    
    importer = CsvImporter(account_facade, None)
    count = importer.import_data(str(test_account_csv), "accounts")
    assert count == 1
    assert account_facade.get_account(1).name == "Test"

def test_import_operations(test_operation_csv, sample_account, operation_facade, account_facade):

    account_facade.create_account(sample_account.id, sample_account.name, sample_account.balance)
    importer = CsvImporter(account_facade, operation_facade)
    count = importer.import_data(str(test_operation_csv), "operations")
    
    assert count == 1
    assert account_facade.get_account(1).balance == 1500.0

def test_csv_import_errors(broken_accounts_csv, account_facade):
    from Services.import_export.importers.csv_importer import CsvImporter
    importer = CsvImporter(account_facade, None)
    
    importer.import_data(str(broken_accounts_csv), "accounts")
    assert len(account_facade.get_all_accounts()) == 0