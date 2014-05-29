from clojure_metal.lang.string import wrap_string, intern
import clojure_metal.lang.util as UT
from clojure_metal.lang.base_types import true, false, nil

def test_string():
    a = wrap_string("foo")
    b = wrap_string("bar")
    c = intern("foo")

    assert UT.equiv(a, b) is false
    assert UT.equiv(a, c) is true

    assert UT.equiv(UT.hash(a), UT.hash(b)) is false
    assert UT.equiv(UT.hash(a), UT.hash(c)) is true
