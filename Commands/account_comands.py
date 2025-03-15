from Domain.interfaces.command import ICommand
from Services.Facades.account_facade import AccountFacade

class CreateAccountCommand(ICommand):
    def __init__(self, facade: AccountFacade, account_id: int, name: str, balance: float):
        self._facade = facade
        self._account_id = account_id
        self._name = name
        self._balance = balance

    def execute(self):
        return self._facade.create_account(
            self._account_id, 
            self._name, 
            self._balance
        )