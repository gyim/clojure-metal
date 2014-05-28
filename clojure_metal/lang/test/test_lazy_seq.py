import clojure_metal.lang.rt as RT
from clojure_metal.lang.fn import wrap_fn
from clojure_metal.lang.base_types import nil, true, false

def range_to(max, i = 0):
    if i < max:
        return RT.lazy_seq.invoke1(wrap_fn(lambda: range_to(max, i + 1)))
    else:
        return nil



def test_lazy_seq_equality():
    a = range_to(10)
    b = range_to(10)

    assert RT.equiv.invoke2(a, b) is true