import pytest
from la_framework import LaList, LaKeyedClass


class Item(LaKeyedClass):
    """Simple concrete LaKeyedClass for testing."""

    def __init__(self, id: int, value: str):
        self.id = id
        self.value = value

    @property
    def key(self):
        return self.id


def test_append_and_len():
    lst = LaList() 
    lst.append(Item(1, "a"))
    lst.append(Item(2, "b"))
    assert len(lst) == 2


def test_get_by_key():
    lst = LaList()
    lst.append(Item(1, "a"))
    assert lst.get(1).value == "a"


def test_get_missing_key_raises():
    lst = LaList()
    with pytest.raises(KeyError):
        lst.get(99)


def test_duplicate_key_raises():
    lst = LaList()
    lst.append(Item(1, "a"))
    with pytest.raises(ValueError):
        lst.append(Item(1, "duplicate"))


def test_iter():
    lst = LaList()
    lst.append(Item(1, "a"))
    lst.append(Item(2, "b"))
    assert [item.id for item in lst] == [1, 2]


def test_index_access():
    lst = LaList()
    lst.append(Item(1, "a"))
    lst.append(Item(2, "b"))
    assert lst[0].value == "a"
    assert lst[1].value == "b"


def test_slice():
    lst = LaList()
    for i in range(5):
        lst.append(Item(i, str(i)))
    sliced = lst[1:3]
    assert len(sliced) == 2
    assert sliced[0].id == 1
    assert sliced[1].id == 2


def test_sort_default():
    lst = LaList()
    lst.append(Item(3, "c"))
    lst.append(Item(1, "a"))
    lst.append(Item(2, "b"))
    lst.sort()
    assert [item.id for item in lst] == [1, 2, 3]


def test_sort_by_key_fn():
    lst = LaList()
    lst.append(Item(1, "banana"))
    lst.append(Item(2, "apple"))
    lst.append(Item(3, "cherry"))
    lst.sort(key=lambda item: item.value)
    assert [item.value for item in lst] == ["apple", "banana", "cherry"]
