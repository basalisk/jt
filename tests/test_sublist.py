import pytest

from jt.environ import Environ
from jt.sublist import Literal, Simple, Subs

def test_base():
    '''Ensure the base class doesn't like being made'''
    with pytest.raises(NotImplementedError):
        Subs().output(None)

@pytest.fixture
def sampleobj():
    shadowed = Environ({"third": "Cheetahs","sixth": "Newts"})
    return Environ({ "first": "Lions",
                    "second": "Tigers",
                    "third": "Bears",
                    "fourth": "Oh My!",
                    "fifth": ["a","few","of","my",
                             {"favourite": "things",
                              "fierce": "creatures"}]},
                   parent=shadowed)


@pytest.mark.parametrize("word",["",
                                  "alpaca",
                                  "ksjslkjsdlkjdslfkjdslkjdslfskj"])
def test_empty_literal(sampleobj,word):
    "Literals produce the string they were created with"
    assert Literal(word).output(sampleobj) == word

def test_normal_empty():
    x = Simple(())
    assert x.output("Newt!") == "Newt!"
    assert x.output(3) == str(3)
    assert x.output(None) == str(None)
    assert x.output(True) == str(True)

#@pytest.mark.skip(reason="Not ready")
@pytest.mark.parametrize("target, result",
                        [(("first",),"Lions"),
                         (("fifth",0),"a"),
                         (("fifth",4,"fierce"),"creatures")])
def test_normal_simple(sampleobj,target,result):
    assert Simple(target).output(sampleobj) == result

@pytest.mark.parametrize("target",
                         [("fist",),
                          ("fifth","badpath",),
                          (3,"badpath",),
                          (None,"badpath",),
                          "break",
                          ("fifth",4,"nokey",)])
def test_normal_nokey_nodefault(target,sampleobj):
    with pytest.raises(LookupError):
        Simple(target).output(sampleobj)

@pytest.mark.parametrize("target, default, result",
                         [(("first",),"shouldn't see","Lions"),
                          (("fifth",0),"badness","a"),
                          (("fifth",4,"fierce"),"terrible","creatures"),
                          (("fist",),"default","default"),
                          (("fifth","badpath"),"nothing","nothing"),
                          (("fifth",4,"nokey"),"empty","empty")])
def test_normal_default(sampleobj,target,default,result):
    assert Simple(target,default=default).output(sampleobj) == result
