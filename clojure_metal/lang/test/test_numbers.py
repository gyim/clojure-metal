from clojure_metal.lang.numbers import wrap_int
import clojure_metal.lang.rt as RT
from clojure_metal.lang.base_types import true, false, nil


def test_create_int():
    a = wrap_int(0)
    b = wrap_int(1)
    c = wrap_int(1)

    assert RT._eq.invoke2(a, b) is false
    assert RT._eq.invoke2(b, c) is true