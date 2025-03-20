# ВШЭ-Банк (признан банкротом)

Лившиц Леонид БПИ 235

---

## Функционал
- **Основной:**
  - Создание/удаление счетов, категорий, операций.
  - Просмотр списка счетов и операций.
  - Выбор текущего счета для работы.

- **Дополнительный:**
  - Аналитика: баланс за период, расходы по категориям.
  - Импорт/экспорт данных в CSV и JSON.

---

## Паттерны
1. **Фасад** — `AccountFacade`, `OperationFacade`, `CategoryFacade`.  
   *Скрыли сложность работы с репозиториями.*
2. **Посетитель** — `CsvExportVisitor`, `JsonExportVisitor`.  
   *Экспорт данных в файлы без изменения классов сущностей.*
3. **Фабрика** — `OperationFactory`, `AccountFactory`.  
   *Создаем объекты с валидацией (например, запрет отрицательных сумм).*
4. **Прокси** — `CachedRepositoryProxy`.  
   *Кэшируем данные в памяти для быстрого доступа.*

---

## Принципы SOLID и GRASP
- **Single Responsibility**: Каждый класс отвечает за одну задачу (ну, почти).
- **High Cohesion**: Связанные части кода в одном месте.
- **Low Coupling**: Фасады и DI-контейнер уменьшают зависимости между модулями.

---


1. **Запуск:**
   ```
   git clone https://github.com/leonidlivshits/Software-Design-big-hw-1.git
   cd Software-Design-big-hw-1
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python main.py # Запуск программы
   pytest -s --cov --cov-report html --cov-fail-under 65 # Покрытие тестами, есть в мэйкфайле
   ```

