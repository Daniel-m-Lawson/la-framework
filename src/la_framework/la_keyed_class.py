"""
This module provides base classes for keyed data structures.
"""

from abc import ABC, abstractmethod
from typing import Any


class LaKeyedClass(ABC):
    """A class that has a key property."""

    @property
    @abstractmethod
    def key(self) -> Any:
        pass

    def __lt__(self, other):
        # Sort by key by default
        if not isinstance(other, LaKeyedClass):
            return NotImplemented
        return self.key < other.key
