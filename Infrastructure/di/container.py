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

# DI-контейнер
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


        self.importers = {
            'csv': CsvImporter(
                self.account_facade,
                self.operation_facade
            ),
            'json': JsonImporter(
                self.account_facade,
                self.operation_facade
            )
        }

        self.exporters = {'csv': CsvExportVisitor(), 'json': JsonExportVisitor()}



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
    
    
