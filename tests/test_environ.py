import pytest

from jt.environ import Environ

def test_construct_empty():
    "An empty environment is not None"
    assert Environ(dict()) != None

def test_construct_nonempty():
    "An environment with a populated dict is not None"
    assert Environ({"one": 1, "two": 2,}) != None

def test_construct_empty_with_parent():
    "An environment with an empty dict but a reasonable parent is not None"
    assert Environ(dict(), parent=Environ({"one": 1, "two": 2,})) != None

def test_empty():
    "Empty environment, no parents, shouldn't be able to lookup anything"
    e = Environ(dict())
    with pytest.raises(LookupError) as k:
        e.lookup(("who","cares"))
    assert "who" in str(k.value)

def test_empty_path():
    "An empty path should return our top level dict"
    e = Environ({"a": 1, "b": 2})
    assert e.lookup(list()) == {"a": 1, "b": 2}

@pytest.fixture
def l1p0():
    return Environ({"bastard": "William",
                 "confessor": "Edward",
                 "terrible": "Ivan"})

def test_one_level_no_parents(l1p0):
    "one level environment, no parents, should find an existing key"
    assert l1p0.lookup(("bastard",)) == "William"

def test_one_level_no_parents(l1p0):
    "one level environment, no parents, should not find an non-existing key"
    with pytest.raises(LookupError) as k:
        l1p0.lookup(("magnificent",))
    assert "magnificent" in str(k.value)

@pytest.fixture
def l2p0():
    kings = {"bastard": "William",
                 "confessor": "Edward",
                 "terrible": "Ivan"}
    fruits = {"apple": "Mmm, delicious",
              "orange": "Pithy indeed",
              "banana": "Not a phone"}
    return Environ({"fruits": fruits, "kings": kings})

def test_two_level_no_parents_exist(l2p0):
    "two level environment, no parents, should find an existing key"
    assert l2p0.lookup(("kings","bastard")) == "William"
    assert l2p0.lookup(("fruits","banana")) == "Not a phone"

def test_two_level_no_parents_noexist(l2p0):
    "two level environment, no parents, should not find an non-existing key"
    with pytest.raises(LookupError) as k:
        l2p0.lookup(("kings","magnificent"))
    assert "kings.magnificent" in str(k.value)
    with pytest.raises(LookupError) as k:
        l2p0.lookup(("fruits","magnificent"))
    assert "fruits.magnificent" in str(k.value)

@pytest.fixture
def l1p1():
    first = {"shadow": "Son of Odin",
             "low-key": "Oh, you know who"}
    second = {"shadow": "You must never go there",
              "mufasa": "Simba's dad"}
    return Environ(first, parent=Environ(second))

def test_one_level_one_parent_non_exist(l1p1):
    "One level environment, a parent, non-existent key"
    with pytest.raises(LookupError) as k:
        l1p1.lookup(( "wednesday", ))
    assert "wednesday" in str(k.value)

def test_one_level_one_parent_exist_1st_level(l1p1):
    "One level environment, a parent, existent key in root"
    assert l1p1.lookup(("low-key",)) == "Oh, you know who"

def test_one_level_one_parent_exist_2nd_level(l1p1):
    "One level environment, a parent, existent key in parent"
    assert l1p1.lookup(("mufasa",)) == "Simba's dad"

def test_one_level_one_parent_shadows(l1p1):
    "One level environment, a parent, key in root shadows one in parent"
    assert l1p1.lookup(("shadow",)) == "Son of Odin"

def test_one_level_one_parent_absolute(l1p1):
    "One level environment, a parent, absolute resolution must KeyError"
    with pytest.raises(LookupError):
        l1p1.lookup(("mufasa",),absolute=True)

