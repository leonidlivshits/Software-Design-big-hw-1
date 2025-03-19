# user_interface/console_interface.py
from datetime import datetime
from Domain.Entities.Category import Category
from Domain.Entities.Operation import Operation
from Infrastructure.di.container import Container
from Domain.enums import TransactionType

class ConsoleInterface:
    def __init__(self, container: Container):
        self.container = container
        self.current_account_id = None
        self.menu_stack = []
        
    def run(self):
        self._show_main_menu()

    def _show_main_menu(self):
        while True:
            print("\n=== Главное меню ===")
            print("1. Управление счетами")
            print("2. Управление операциями") 
            print("3. Аналитика и отчеты")
            print("4. Импорт/экспорт данных")
            print("5. Управление категориями")  # Новый пункт
            print("0. Выход")
            
            choice = input("Выберите пункт: ")
            
            if choice == "1":
                self._show_account_menu()
            elif choice == "2":
                self._show_operation_menu()
            elif choice == "3":
                self._show_analytics_menu()
            elif choice == "4":
                self._show_import_export_menu()
            if choice == "5":
                self._show_category_menu()
            elif choice == "0":
                exit()
            else:
                print("Неверный ввод!")

    def _show_account_menu(self):
        while True:
            print("\n--- Управление счетами ---")
            print("1. Создать счет")
            print("2. Просмотреть все счета")
            print("3. Выбрать текущий счет")
            print("4. Удалить счет")
            print("9. Назад")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self._create_account()
            elif choice == "2":
                self._list_accounts()
            elif choice == "3":
                self._select_account()
            elif choice == "4":
                self._delete_account()
            elif choice == "9":
                return
            else:
                print("Неверный ввод!")
    
    def _show_category_menu(self):
        while True:
            print("\n--- Управление категориями ---")
            print("1. Создать категорию")
            print("2. Просмотреть все категории")
            print("9. Назад")
            choice = input("Выберите действие: ")
            if choice == "1":
                self._create_category()
            elif choice == "2":
                self._list_categories()
            elif choice == "9":
                return

    def _create_account(self):
        try:
            account_id = int(input("Введите ID счета: "))
            name = input("Введите название счета: ")
            balance = float(input("Введите начальный баланс: "))
            
            facade = self.container.get_account_facade()
            account = facade.create_account(account_id, name, balance)
            print(f"Счет {account.name} создан!")
            
        except Exception as e:
            print(f"Ошибка: {str(e)}")

    def _list_accounts(self):
        facade = self.container.get_account_facade()
        accounts = facade.get_all_accounts()
        
        if not accounts:
            print("Нет созданных счетов")
            return
            
        for acc in accounts:
            print(f"{acc.id}: {acc.name} ({acc.balance:.2f} руб.)")

    def _select_account(self):
        self._list_accounts()
        try:
            account_id = int(input("Введите ID счета: "))
            facade = self.container.get_account_facade()
            account = facade.get_account(account_id)
            
            if account:
                self.current_account_id = account_id
                print(f"Выбран счет: {account.name}")
            else:
                print("Счет не найден!")
                
        except ValueError:
            print("Неверный формат ID!")

    def _create_operation(self):
        if not self.current_account_id:
            print("Сначала выберите счет!")
            return

        try:
            operation_id = int(input("Введите ID операции: "))
            amount = float(input("Сумма: "))
            type_choice = input("Тип (1 - доход, 2 - расход): ")
            category_id = int(input("ID категории: "))
            date_str = input("Дата (ГГГГ-ММ-ДД): ")

            if not self.container.category_facade.get_category(category_id):
                print("Ошибка: Категория не найдена!")
                return

            if type_choice not in ("1", "2"):
                raise ValueError("Неверный тип операции")
            
            
            
            date = datetime.strptime(date_str, "%Y-%m-%d")
            
            op_type = TransactionType.INCOME if type_choice == "1" else TransactionType.EXPENSE

            operation = Operation(
                id=operation_id,
                type=op_type,
                bank_account_id=self.current_account_id,
                amount=amount,
                date=date,
                category_id=category_id
            )

            self.container.operation_facade.create_operation(operation)
            print("Операция успешно создана!")

        except ValueError as ve:
            print(f"Ошибка ввода: {str(ve)}")
        except Exception as e:
            print(f"Ошибка: {str(e)}")

    def _delete_operation(self):
        try:
            operation_id = int(input("Введите ID операции для удаления: "))
            self.container.operation_facade.delete_operation(operation_id)
            print("Операция удалена!")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    def _show_operation_menu(self):
        # Реализация меню операций
        pass
        
    def _show_analytics_menu(self):
        while True:
            print("\n--- Аналитика ---")
            print("1. Баланс за период")
            print("2. Расходы по категориям")
            print("9. Назад")
            
            choice = input("Выберите отчет: ")
            
            if choice == "1":
                self._show_balance_report()
            elif choice == "2":
                self._show_category_report()
            elif choice == "9":
                return
            else:
                print("Неверный ввод!")

    def _show_balance_report(self):
        # try:
        #     start = input("Начальная дата (ГГГГ-ММ-ДД): ")
        #     end = input("Конечная дата (ГГГГ-ММ-ДД): ")
            
        #     start_date = datetime.strptime(start, "%Y-%m-%d") if start else None
        #     end_date = datetime.strptime(end, "%Y-%m-%d") if end else None
            
        #     report = self.container.analytics_facade.get_balance_report(
        #         start_date, 
        #         end_date
        #     )
            
        #     print(f"\nДоходы: {report['income']:.2f}")
        #     print(f"Расходы: {report['expense']:.2f}")
        #     print(f"Баланс: {report['difference']:.2f}")

        try:
            start = input("Начальная дата (ГГГГ-ММ-ДД): ")
            end = input("Конечная дата (ГГГГ-ММ-ДД): ")
            
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            
            report = self.container.analytics_facade.get_balance_report(
                start_date, 
                end_date
            )
            
            print(f"\nОтчет за период {start} - {end}:")
            print(f"Доходы: {report['income']:.2f} руб.")
            print(f"Расходы: {report['expense']:.2f} руб.")
            print(f"Итоговый баланс: {report['balance']:.2f} руб.")
            
        except Exception as e:
            print(f"Ошибка: {str(e)}")
        
    def _show_import_export_menu(self):
        # Реализация меню импорта/экспорта
        pass

    def _show_operation_menu(self):
        while True:
            print("\n--- Управление операциями ---")
            print("1. Создать операцию")
            print("2. Просмотреть все операции")
            print("3. Удалить операцию")
            print("9. Назад")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self._create_operation()
            elif choice == "2":
                self._list_operations()
            elif choice == "3":
                self._delete_operation()
            elif choice == "9":
                return
            else:
                print("Неверный ввод!")

    def _list_operations(self):
        if not self.current_account_id:
            print("Сначала выберите счет!")
            return
            
        try:
            facade = self.container.get_operation_facade()
            operations = facade.get_operations_by_account(self.current_account_id)
            
            if not operations:
                print("Нет операций по выбранному счету")
                return
                
            for op in operations:
                print(f"{op.id}: {op.type.name} {op.amount:.2f} руб. ({op.date.strftime('%Y-%m-%d')})")

        except Exception as e:
            print(f"Ошибка: {str(e)}")

    def _delete_operation(self):
        try:
            operation_id = int(input("Введите ID операции для удаления: "))
            facade = self.container.get_operation_facade()
            facade.delete_operation(operation_id)
            print("Операция удалена!")
            
        except Exception as e:
            print(f"Ошибка: {str(e)}")

    def _show_import_export_menu(self):
        while True:
            print("\n--- Импорт/Экспорт ---")
            print("1. Экспорт данных")
            print("2. Импорт данных")
            print("9. Назад")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self._export_data()
            elif choice == "2":
                self._import_data()
            elif choice == "9":
                return
            else:
                print("Неверный ввод!")

    def _export_data(self):
        try:
            format_choice = input("Формат (csv/json): ").lower()
            entity_choice = input("Тип данных (accounts/operations): ").lower()
            
            exporter = self.container.get_exporter(format_choice)
            
            if entity_choice == "accounts":
                accounts = self.container.get_account_facade().get_all_accounts()
                for acc in accounts:
                    exporter.visit_bank_account(acc)
                print(f"Экспортировано {len(accounts)} счетов")
                
            elif entity_choice == "operations":
                operations = self.container.get_operation_facade().get_all_operations()
                for op in operations:
                    exporter.visit_operation(op)
                print(f"Экспортировано {len(operations)} операций")
                
            else:
                print("Неверный тип данных!")
                
        except Exception as e:
            print(f"Ошибка экспорта: {str(e)}")

    def _import_data(self):
        try:
            format_choice = input("Формат (csv/json): ").lower()
            file_path = input("Путь к файлу: ")
            
            importer = self.container.get_importer(format_choice)
            result = importer.import_data(file_path)
            
            print(f"Импортировано {len(result)} записей")
            
        except Exception as e:
            print(f"Ошибка импорта: {str(e)}")

    def _show_category_report(self):
        try:
            report = self.container.analytics_facade.get_category_report()
            
            print("\n--- Расходы по категориям ---")
            for category_id, amount in report.items():
                print(f"Категория {category_id}: {amount:.2f} руб.")
                
        except Exception as e:
            print(f"Ошибка: {str(e)}")

    def _show_category_menu(self):
        while True:
            print("\n--- Управление категориями ---")
            print("1. Создать категорию")
            print("2. Список категорий")
            print("9. Назад")
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self._create_category()
            elif choice == "2":
                self._list_categories()
            elif choice == "9":
                return
            else:
                print("Неверный ввод!")

    def _create_category(self):
        try:
            category_id = int(input("Введите ID категории: "))
            name = input("Введите название категории: ")
            type_choice = input("Тип (1 - доход, 2 - расход): ")
            
            if type_choice not in ("1", "2"):
                raise ValueError("Неверный тип категории")
                
            category_type = TransactionType.INCOME if type_choice == "1" else TransactionType.EXPENSE
            category = Category(id=category_id, type=category_type, name=name)
            
            self.container.category_facade.create_category(category)
            print("Категория успешно создана!")
            
        except Exception as e:
            print(f"Ошибка: {str(e)}")

    def _list_categories(self):
        try:
            categories = self.container.category_facade.get_all_categories()
            if not categories:
                print("Нет созданных категорий")
                return
                
            for cat in categories:
                print(f"{cat.id}: {cat.name} ({cat.type.value})")
                
        except Exception as e:
            print(f"Ошибка: {str(e)}")

    
