import pytest

def test_json_import_accounts(test_account_json, account_facade):
    from Services.import_export.importers.json_importer import JsonImporter
    importer = JsonImporter(account_facade, None)
    
    count = importer.import_data(str(test_account_json), "accounts")
    assert count == 1
    account = account_facade.get_account(1)
    assert account.name == "Test Account"
    assert account.balance == 1000.0

def test_json_import_operations(test_operation_json, operation_facade, account_facade):
    from Services.import_export.importers.json_importer import JsonImporter
    
    account_facade.create_account(1, "Test", 1000)
    importer = JsonImporter(None, operation_facade)
    
    count = importer.import_data(str(test_operation_json), "operations")
    assert count == 1
    assert account_facade.get_account(1).balance == 1500.0

def test_json_import_errors(broken_accounts_json, account_facade):
    from Services.import_export.importers.json_importer import JsonImporter
    importer = JsonImporter(account_facade, None)
    
    importer.import_data(str(broken_accounts_json), "accounts")
    assert len(account_facade.get_all_accounts()) == 0