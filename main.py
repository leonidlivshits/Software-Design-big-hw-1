# from datetime import datetime
# from Infrastructure.di.container import Container

# def main():
#     container = Container()
    
#     # Создание аккаунта
#     account_facade = container.get_account_facade()
#     account = account_facade.create_account(1, "Main Account", 1000)
#     print(f"Created account: {account.name} (Balance: {account.balance})")
    
#     # Пример работы с аналитикой
#     analytics = container.get_analytics_facade()
#     report = analytics.perform_analysis("balance")
#     print(f"Analytics report: {report}")
    
#     # Пример экспорта
#     exporter = container.get_exporter("csv")
#     export_path = exporter.visit_bank_account(account)
#     print(f"Exported to: {export_path}")

# if __name__ == "__main__":
#     main()



from Infrastructure.di.container import Container
from UserInterface.ConsoleInterface import ConsoleInterface

def main():
    container = Container()
    ui = ConsoleInterface(container)
    ui.run()

if __name__ == "__main__":
    main()