from clojure_metal.lang.symbol import intern
import clojure_metal.lang.util as UT
from clojure_metal.lang.base_types import true, false, nil

def test_symbol():
    a = intern("foo")
    b = intern("bar")
    c = intern("foo", "bar")
    d = intern("foo")

    assert UT.equiv(a, b) is false
    assert UT.equiv(a, c) is false
    assert UT.equiv(a, d) is true

    assert UT.equiv(UT.hash(a), UT.hash(b)) is false
    assert UT.equiv(UT.hash(a), UT.hash(c)) is false
    assert UT.equiv(UT.hash(a), UT.hash(d)) is true

