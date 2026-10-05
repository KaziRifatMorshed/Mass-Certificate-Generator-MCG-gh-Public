"""Singleton metaclass shared across models."""
from abc import ABCMeta


class SingletonMeta(ABCMeta):
    """Singleton metaclass that extends ABCMeta so it is compatible with ABC subclasses."""

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
