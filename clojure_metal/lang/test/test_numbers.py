from clojure_metal.lang.numbers import wrap_int, wrap_bigint, WInt, WBigInt
import clojure_metal.lang.rt as RT
from clojure_metal.lang.base_types import true, false, nil
from rpython.rlib.rbigint import rbigint
from itertools import product

def wrap_num(n, type):
    if type == WInt:
        return wrap_int(n)
    elif type == WBigInt:
        return wrap_bigint(rbigint.fromint(n))

def get_num(val):
    if type(val) == WInt:
        return val._int_value
    elif type(val) == WBigInt:
        return val._bigint_value.toint()

num_types = [WInt, WBigInt]
op_casts = {
    (WInt,WInt): WInt,
    (WInt,WBigInt): WBigInt,
    (WBigInt,WBigInt): WBigInt,
}
def get_op_cast(t1, t2):
    if (t1,t2) in op_casts:
        return op_casts[(t1,t2)]
    else:
        return op_casts[(t2,t1)]

def test_create_int():
    a = wrap_int(0)
    b = wrap_int(1)
    c = wrap_int(1)

    assert RT._equiv.invoke2(a, b) is false
    assert RT._equiv.invoke2(b, c) is true

def test_equivs():
    for t1, t2 in product(num_types, num_types):
        v1 = wrap_num(1, t1)
        v2 = wrap_num(1, t2)
        v3 = wrap_num(2, t2)
        assert RT._equiv.invoke2(v1, v2) is true
        assert RT._equiv.invoke2(v1, v3) is false

def test_add():
    for t1, t2 in product(num_types, num_types):
        v1 = wrap_num(1, t1)
        v2 = wrap_num(2, t2)
        v3 = RT._add.invoke2(v1, v2)
        assert type(v3) == get_op_cast(t1, t2)
        assert get_num(v3) == 3
