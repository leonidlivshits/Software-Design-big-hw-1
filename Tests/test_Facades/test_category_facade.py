from Domain.Entities.Category import Category
from Domain.enums.transaction_type import TransactionType


def test_create_category(category_facade, sample_category):
    category = category_facade.create_category(sample_category)
    assert category.id == 1

def test_find_by_type(category_facade, sample_category):
    category_facade.create_category(sample_category)
    result = category_facade.find_by_type("expense")
    assert len(result) == 1