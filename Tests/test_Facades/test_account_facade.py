def test_create_account(account_facade):
    account = account_facade.create_account(1, "Test", 1000.0)
    assert account.id == 1
    assert account.name == "Test"

def test_delete_account(account_facade, sample_account):
    account_facade.create_account(sample_account.id, sample_account.name, sample_account.balance)
    account_facade.delete_account(sample_account.id)
    assert account_facade.get_account(sample_account.id) is None