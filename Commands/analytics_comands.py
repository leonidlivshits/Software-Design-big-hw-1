from abc import ABC, abstractmethod
from datetime import datetime
from Domain.interfaces.command import ICommand
from Services.Facades.analytics_facade import AnalyticsFacade

class AnalyticsCommand(ICommand, ABC):
    def __init__(self, facade: AnalyticsFacade):
        self.facade = facade

class BalanceReportCommand(AnalyticsCommand):
    def __init__(self, facade: AnalyticsFacade, start_date=None, end_date=None):
        super().__init__(facade)
        self.start_date = start_date
        self.end_date = end_date

    def execute(self):
        return self.facade.perform_analysis(
            "balance", 
            self.start_date, 
            self.end_date
        )

class CategoryReportCommand(AnalyticsCommand):
    def execute(self):
        return self.facade.perform_analysis("categories")
    

class GenerateCategoryReportCommand(ICommand):
    def __init__(self, facade: AnalyticsFacade):
        self.facade = facade

    def execute(self):
        return self.facade.get_category_report()
