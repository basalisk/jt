# Honestly I think there are two separate ideas here that should be split out
# into little utility libraries. That of a 'shadowing' class where several
# containers can be stacked in order and searches for elements are answered
# by the first that has the key. The second idea is that of a 'dict' like thing
# that takes lists as keys, making a hierarchial lookup. These feel like they
# should be in some part of the standard library but I don't know it well
# enough yet.

from typing import Union, Any, Optional, List

class Environ:
    root: dict
    parent: Any # not really but recursive types are whack

    def __init__(self, root: dict, *, parent: Optional[Any]=None) -> None:
        self.root = root
        self.parent = parent

    def lookup(self, path: List[str]) -> Any:
        try:
            search = list(reversed(path.copy()))
            found = self.root
            while len(search) >= 1:
                found = found[search.pop()]
            return found

        except(KeyError):
            if self.parent == None:
                raise KeyError('.'.join(path)) from None
            return self.parent.lookup(path)

