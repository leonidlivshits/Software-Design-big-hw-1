from typing import List, Optional
from Domain.Entities import Category
from Services.Repositories.IRepository import IRepository

class CategoryFacade:
    def __init__(self, repository: IRepository[Category]):
        self._repo = repository

    def create_category(self, category: Category) -> Category:
        if not category.name:
            raise ValueError("Category name cannot be empty")
        self._repo.add(category)
        return category

    def get_all_categories(self) -> List[Category]:
        return self._repo.get_all()
    
    def get_category(self, category_id: int) -> Optional[Category]:
        return self._repo.get(category_id)

    def find_by_type(self, category_type: str) -> List[Category]:
        return [c for c in self._repo.get_all() if c.type.value == category_type]