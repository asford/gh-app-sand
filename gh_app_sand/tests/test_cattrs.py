import pytest
import attr
import cattr

from ..cattrs import ignore_unknown_attribs

def test_ignore_unknown_attribs():
    standard = cattr.global_converter
    tolerant = cattr.Converter()

    @ignore_unknown_attribs(converter=tolerant)
    @attr.s(auto_attribs=True)
    class Foo:
        bar: int

    nofoo = dict()
    foo = {"bar": 1}
    fooplus = {"bar": 1, "bat": 2}

    with pytest.raises(TypeError):
        standard.structure(nofoo, Foo)
    assert Foo(1) == standard.structure(foo, Foo)
    with pytest.raises(TypeError):
        standard.structure(fooplus, Foo)

    with pytest.raises(TypeError):
        tolerant.structure(nofoo, Foo)
    assert Foo(1) == tolerant.structure(foo, Foo)
    assert Foo(1) == tolerant.structure(fooplus, Foo)
