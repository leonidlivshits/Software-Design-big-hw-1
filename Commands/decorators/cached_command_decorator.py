import functools
from typing import Any
from Domain.interfaces.command import ICommand

class CachedCommandDecorator(ICommand):
    def __init__(self, decorated: ICommand, ttl: int = 300):
        self._decorated = decorated
        self._cache: dict = {}
        self._ttl = ttl  # Время жизни кэша

    def execute(self) -> Any:
        cache_key = self._get_cache_key()
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        result = self._decorated.execute()
        self._cache[cache_key] = result
        return result

    def _get_cache_key(self) -> str:
        return f"{self._decorated.__class__.__name__}_{id(self._decorated)}"