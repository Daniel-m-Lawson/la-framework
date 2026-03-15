"""LaList: A type-safe, generic collection supporting efficient O(1) key-based lookups."""

from typing import (
    Callable,
    Optional,
    TypeVar,
    Generic,
    List,
    Dict,
    Any,
    overload,
    Union,
)
from .la_keyed_class import LaKeyedClass

T = TypeVar("T", bound=LaKeyedClass)


class LaList(Generic[T]):
    """A type-safe list of LaKeyedClass objects with optional sorting and slicing."""

    def __init__(self):
        self._items: List[T] = []
        self._key_map: Dict[tuple, T] = {}

    def append(self, item: T) -> None:
        """Add an item to the list, enforcing unique keys."""
        if item.key in self._key_map:
            raise ValueError(f"Duplicate key: {item.key}")
        self._items.append(item)
        self._key_map[item.key] = item

    def get(self, key) -> T:
        """Retrieve an item by its key."""
        if key not in self._key_map:
            raise KeyError(f"Key not found: {key}")
        return self._key_map[key]

    def sort(
        self, key: Optional[Callable[[T], Any]] = None, reverse: bool = False
    ) -> None:
        """
        Sort the internal items list in-place.
        If key is None, sort by the items themselves.
        """
        if key is None:
            # Sort by items themselves (requires LaKeyedClass to implement __lt__)
            self._items.sort(reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)

    def __iter__(self):
        """Iterate over the internal items."""
        return iter(self._items)

    def __len__(self):
        """Return the number of items in the list."""
        return len(self._items)

    def __repr__(self):
        """Debug representation."""
        return f"{self.__class__.__name__}({self._items})"

    @overload
    def __getitem__(self, index_or_slice: int) -> T: ...

    @overload
    def __getitem__(self, index_or_slice: slice) -> "LaList[T]": ...

    def __getitem__(self, index_or_slice: Union[int, slice]) -> Union[T, "LaList[T]"]:
        if isinstance(index_or_slice, slice):
            new_list = self.__class__()  ## Use the same class as self
            new_list._items = self._items[index_or_slice]
            new_list._key_map = {item.key: item for item in new_list._items}
            return new_list
        return self._items[index_or_slice]
