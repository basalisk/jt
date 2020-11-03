# Honestly I think there are two separate ideas here that should be split out
# into little utility libraries. That of a 'shadowing' class where several
# containers can be stacked in order and searches for elements are answered
# by the first that has the key. The second idea is that of a 'dict' like thing
# that takes lists as keys, making a hierarchial lookup. These feel like they
# should be in some part of the standard library but I don't know it well
# enough yet.

#Duh, I could use chainmap, but the tuple->multilevel dict thing...

from typing import Any, Optional, Tuple

class Environ:
    root: dict
    parent: Any # not really but recursive types are whack

    def __init__(self, root: dict, *, parent: Optional[Any]=None) -> None:
        self.root = root
        self.parent = parent

    def lookup(self, path: Tuple[str]) -> Any:
        try:
            found = self.root
            for here in path:
                found = found[here]
            return found

        except(KeyError,IndexError):
            if self.parent == None:
                raise KeyError('.'.join(path)) from None
            return self.parent.lookup(path)

