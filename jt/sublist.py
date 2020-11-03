from typing import Any, Tuple, Optional

from jt.environ import Environ

#I probably ought to use ABCs for this, but meh

class Subs:
    """Base class for creating substitutions"""
    def __init__(self) -> None:
        pass
    def output(self,obj) -> str:
        raise NotImplementedError("Generic substitution makes no sense")

class Literal(Subs):
    """Simply outputs literal text"""
    text: str
    def __init__(self, text: str) -> None:
        self.text = text

    def output(self,obj: Environ) -> str:
        #really should be type Json but that has issues
        """Output the string we started with"""
        return self.text

class Simple(Subs):
    def __init__(self, path: Tuple[str]=(), *, absolute: bool = False, default:
                 Optional[str] = None) -> None:
        self.path = path
        self.absolute = absolute
        self.default = default

    def output(self, obj: Environ) -> str:
        """ Outputs the value of the path in the current object """
        if self.path == ():
            return str(obj)
        try:
            possible = obj.lookup(self.path,absolute=self.absolute)
        except(LookupError):
            possible = self.default
        if possible == None:
            raise LookupError
        return str(possible)

# Add conditional and loop substitutors
