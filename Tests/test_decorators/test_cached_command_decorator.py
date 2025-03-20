import pytest
from unittest.mock import MagicMock
from Commands.decorators.cached_command_decorator import CachedCommandDecorator
from Domain.interfaces.command import ICommand

class MockCommand(ICommand):
    def __init__(self, result):
        self.result = result
        
    def execute(self):
        return self.result

def test_cached_command_returns_cached_result():
    real_command = MockCommand("test_result")
    cached_command = CachedCommandDecorator(real_command)
    
    result1 = cached_command.execute()
    result2 = cached_command.execute()
    
    assert result1 == result2
    assert result1 == "test_result"

def test_cache_key_uniqueness():
    cmd1 = MockCommand("result1")
    cmd2 = MockCommand("result2")
    
    decorator1 = CachedCommandDecorator(cmd1)
    decorator2 = CachedCommandDecorator(cmd2)
    
    assert decorator1._get_cache_key() != decorator2._get_cache_key()

def test_cache_expiration(monkeypatch):
    mock_time = MagicMock()
    monkeypatch.setattr("time.time", mock_time)
    
    cmd = MockCommand("result")
    cached = CachedCommandDecorator(cmd, ttl=10)
    
    mock_time.return_value = 0
    cached.execute()
    
    mock_time.return_value = 11
    result = cached.execute()
    
    assert result == "result"
    assert len(cached._cache) == 1