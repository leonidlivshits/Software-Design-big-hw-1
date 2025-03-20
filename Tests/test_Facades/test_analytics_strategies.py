from datetime import datetime
from Domain.Entities.Operation import Operation
from Domain.enums.transaction_type import TransactionType
from Services.Facades.analytics_strategies import CategoryGroupingStrategy


def test_category_grouping():
    strategy = CategoryGroupingStrategy()
    operations = [
        Operation(id = 1, category_id=1, bank_account_id=1, date = datetime.now(),  amount=200, type=TransactionType.EXPENSE),
        Operation(id = 2, category_id=1, bank_account_id=1, date = datetime.now(), amount=300, type=TransactionType.EXPENSE)
    ]
    
    result = strategy.analyze(operations)
    assert result[1] == 500.0