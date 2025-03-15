from typing import Dict, Type, Any
from Domain.Entities import BankAccount, Category, Operation
from Services.Repositories import IRepository, CachedRepositoryProxy
from Services.Facades import AccountFacade, AnalyticsFacade

class Container:
    def __init__(self):
        self._dependencies: Dict[Type, Any] = {}
        self._init_dependencies()

    def _init_dependencies(self):
        account_repo = CachedRepositoryProxy[BankAccount]()
        operation_repo = CachedRepositoryProxy[Operation]()
        
        self._dependencies[AccountFacade] = AccountFacade(account_repo)
        self._dependencies[AnalyticsFacade] = AnalyticsFacade(operation_repo)

    def resolve(self, dependency_type: Type) -> Any:
        return self._dependencies.get(dependency_type)

container = Container()
account_facade = container.resolve(AccountFacade)
analytics_facade = container.resolve(AnalyticsFacade)