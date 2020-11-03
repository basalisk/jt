# Honestly I think there are two separate ideas here that should be split out
# into little utility libraries. That of a 'shadowing' class where several
# containers can be stacked in order and searches for elements are answered
# by the first that has the key. The second idea is that of a 'dict' like thing
# that takes lists as keys, making a hierarchial lookup. These feel like they
# should be in some part of the standard library but I don't know it well
# enough yet.

#Duh, I could use chainmap, but the tuple->multilevel dict thing...

from typing import Any, Optional, Tuple

def indexify(word):
    if isinstance(word,int):
        return '[{}]'.format(word)
    elif isinstance(word,str):
        return '.{}'.format(word)
    else: 
        return '###{}###'.format(word)

def pullpath(path):
    if not isinstance(path,tuple): 
        return 'something funky about {path}'.format(path)
    return ''.join(map(indexify,path))


class Environ:
    root: dict
    parent: Any # not really but recursive types are whack

    def __init__(self, root: dict, *, parent: Optional[Any]=None) -> None:
        self.root = root
        self.parent = parent

    def lookup(self, path: Tuple[str], *, absolute:bool=False) -> Any:
        try:
            found = self.root
            for here in path:
                if isinstance(here,(int,slice)) and not isinstance(found,list):
                    raise LookupError
                if isinstance(here,str) and not isinstance(found,dict):
                    raise LookupError
                found = found[here]
            return found

        except(LookupError):
            if self.parent == None or absolute:
                raise LookupError(pullpath(path)) from None
            try:
                return self.parent.lookup(path)
            except(LookupError):
                raise LookupError(pullpath(path)) from None

