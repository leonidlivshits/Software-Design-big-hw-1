from typing import Dict, Type, Any
from Commands.analytics_comands import BalanceReportCommand
from Commands.decorators.cached_command_decorator import CachedCommandDecorator
from Domain.Entities import BankAccount, Category, Operation
from Domain.interfaces.command import ICommand
from Domain.interfaces.export_visitor import IExportVisitor
from Services.Facades.category_facade import CategoryFacade
from Services.Repositories.cached_repository_proxy import CachedRepositoryProxy
from Services.Repositories.IRepository import IRepository
from Services.Facades.analytics_facade import AnalyticsFacade
from Services.Facades.operation_facade import OperationFacade
from Services.Facades.account_facade import AccountFacade
from Services.Repositories.in_memory_repository import InMemoryRepository
from Services.import_export.exporters.csv_visitor import CsvExportVisitor
from Services.import_export.exporters.json_visitor import JsonExportVisitor

from Services.import_export.importers.csv_importer import CsvImporter
from Services.import_export.importers.json_importer import JsonImporter

# class Container:
#     def __init__(self):
#         self._dependencies: Dict[Type, Any] = {}
#         self._init_dependencies()

#         self.export_visitors = {
#             'csv': CsvExportVisitor(),
#             'json': JsonExportVisitor()
#         }

#     def _init_dependencies(self):
#         account_repo = CachedRepositoryProxy[BankAccount]()
#         operation_repo = CachedRepositoryProxy[Operation]()
        
#         self._dependencies[AccountFacade] = AccountFacade(account_repo)
#         self._dependencies[AnalyticsFacade] = AnalyticsFacade(operation_repo)

#     def resolve(self, dependency_type: Type) -> Any:
#         return self._dependencies.get(dependency_type)
    
#     def get_exporter(self, format: str) -> IExportVisitor:
#         return self.export_visitors[format]
#     # def get_exporter(self, format: str) -> IExportVisitor:
#     #     return self.exporters[format.lower()]

#     def get_balance_command(self) -> ICommand:
#         return CachedCommandDecorator(
#             BalanceReportCommand(self.analytics_facade)
#         )

# container = Container()
# account_facade = container.resolve(AccountFacade)
# analytics_facade = container.resolve(AnalyticsFacade)

# class Container:
#     def __init__(self):
#         # Инициализация реальных репозиториев
#         self._real_account_repo = InMemoryRepository[BankAccount]()
#         self._real_operation_repo = InMemoryRepository[Operation]()
        
#         # Инициализация прокси с кэшем
#         self.account_repo = CachedRepositoryProxy[BankAccount](self._real_account_repo)
#         self.operation_repo = CachedRepositoryProxy[Operation](self._real_operation_repo)
        
#         # Инициализация фасадов
#         self.account_facade = AccountFacade(self.account_repo)
#         self.analytics_facade = AnalyticsFacade(self.operation_repo)
        
#         # Инициализация экспортеров
#         self.exporters = {
#             'csv': CsvExportVisitor(),
#             'json': JsonExportVisitor()
#         }

#     def get_account_facade(self) -> AccountFacade:
#         return self.account_facade

#     def get_analytics_facade(self) -> AnalyticsFacade:
#         return self.analytics_facade

#     def get_exporter(self, format: str) -> IExportVisitor:
#         return self.exporters[format.lower()]




class Container:
    def __init__(self):
        # Репозитории
        self.account_repo = CachedRepositoryProxy(InMemoryRepository[BankAccount]())
        self.operation_repo = CachedRepositoryProxy(InMemoryRepository[Operation]())
        self.category_repo = CachedRepositoryProxy(InMemoryRepository[Category]())
        
        # Фасады
        self.account_facade = AccountFacade(self.account_repo)
        self.operation_facade = OperationFacade(
            self.operation_repo,
            self.account_facade
        )
        self.analytics_facade = AnalyticsFacade(
            self.operation_repo,
            self.account_repo,
            self.category_repo
        )
        self.category_facade = CategoryFacade(self.category_repo)
    # def __init__(self):
    #     # Repositories
    #     self.account_repo = CachedRepositoryProxy(InMemoryRepository[BankAccount]())
    #     self.operation_repo = CachedRepositoryProxy(InMemoryRepository[Operation]())
    #     self.category_repo = CachedRepositoryProxy(InMemoryRepository[Category]())

    #     # Facades
    #     self.account_facade = AccountFacade(self.account_repo)
    #     self.operation_facade = OperationFacade(self.operation_repo)
    #     self.analytics_facade = AnalyticsFacade(self.operation_repo)
    #     self.category_facade = CategoryFacade(self.category_repo)

    #     # Importers/Exporters
    #     self.importers = {'csv': CsvImporter(), 'json': JsonImporter()}
    #     self.exporters = {'csv': CsvExportVisitor(), 'json': JsonExportVisitor()}

    def get_exporter(self, format: str) -> IExportVisitor:
        return self.exporters[format.lower()]

    def get_importer(self, format: str):
        return self.importers[format.lower()]

    def get_category_facade(self) -> CategoryFacade:
        return self.category_facade
    
    def get_account_facade(self) -> AccountFacade:
        return self.account_facade
    
    def get_operation_facade(self) -> OperationFacade:
        return self.operation_facade
    
    def get_analytics_facade(self) -> AnalyticsFacade:
        return self.analytics_facade
    
    
