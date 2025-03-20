def test_create_operation(operation_facade, sample_operation, account_facade):
    account_facade.create_account(1, "Test", 1000)
    operation_facade.create_operation(sample_operation)
    assert len(operation_facade.get_operations_by_account(1)) == 1
    assert account_facade.get_account(1).balance == 1500.0

def test_delete_operation_reverts_balance(operation_facade, sample_operation, account_facade):
    account = account_facade.create_account(1, "Test", 1000)
    operation_facade.create_operation(sample_operation)
    operation_facade.delete_operation(1)
    assert account.balance == 1000.0



