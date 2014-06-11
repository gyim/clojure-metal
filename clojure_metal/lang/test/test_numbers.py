from clojure_metal.lang.numbers import wrap_int, wrap_bigint, WInt, WBigInt
import clojure_metal.lang.rt as RT
from clojure_metal.lang.base_types import true, false, nil
from rpython.rlib.rbigint import rbigint
from rpython.rlib.rarithmetic import maxint
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

def test_sign():
    for t in num_types:
        v0 = wrap_num(0, t)
        v1 = wrap_num(1, t)
        vm1 = wrap_num(-1, t)

        assert RT._iszero.invoke1(v0) is true
        assert RT._iszero.invoke1(v1) is false
        assert RT._iszero.invoke1(vm1) is false

        assert RT._ispos.invoke1(v0) is false
        assert RT._ispos.invoke1(v1) is true
        assert RT._ispos.invoke1(vm1) is false

        assert RT._isneg.invoke1(v0) is false
        assert RT._isneg.invoke1(v1) is false
        assert RT._isneg.invoke1(vm1) is true

def test_add():
    for t1, t2 in product(num_types, num_types):
        v1 = wrap_num(1, t1)
        v2 = wrap_num(2, t2)

        v3 = RT._add.invoke2(v1, v2)
        v3p = RT._addP.invoke2(v1, v2)
        assert type(v3) == get_op_cast(t1, t2)
        assert type(v3p) == get_op_cast(t1, t2)
        assert get_num(v3) == 3
        assert get_num(v3p) == 3

def test_multiply():
    for t1, t2 in product(num_types, num_types):
        v2 = wrap_num(2, t1)
        v3 = wrap_num(3, t2)

        v6 = RT._multiply.invoke2(v2, v3)
        v6p = RT._multiplyP.invoke2(v2, v3)
        assert type(v6) == get_op_cast(t1, t2)
        assert type(v6p) == get_op_cast(t1, t2)
        assert get_num(v6) == 6
        assert get_num(v6p) == 6

def test_quotient():
    for t1, t2 in product(num_types, num_types):
        v6 = wrap_num(6, t1)
        v3 = wrap_num(3, t2)

        v2 = RT._quotient.invoke2(v6, v3)
        assert type(v2) == get_op_cast(t1, t2)
        assert get_num(v2) == 2

def test_remainder():
    for t1, t2 in product(num_types, num_types):
        v5 = wrap_num(5, t1)
        v3 = wrap_num(3, t2)

        v2 = RT._remainder.invoke2(v5, v3)
        assert type(v2) == get_op_cast(t1, t2)
        assert get_num(v2) == 2

def test_lt():
    for t1, t2 in product(num_types, num_types):
        v1 = wrap_num(1, t1)
        v2 = wrap_num(2, t2)

        c1 = RT._lt.invoke2(v1, v2)
        c2 = RT._lt.invoke2(v1, v1)
        assert c1 is true
        assert c2 is false


def test_negate():
    for t in num_types:
        v0 = wrap_num(0, t)
        v1 = wrap_num(1, t)
        v0neg = RT._negate.invoke1(v0)
        v1neg = RT._negate.invoke1(v1)

        assert type(v0neg) == type(v0)
        assert type(v1neg) == type(v1)
        assert get_num(v0neg) == 0
        assert get_num(v1neg) == -1

def test_binop_overflow():
    v1 = wrap_int(maxint - 1)
    v2 = wrap_int(2)

    def assert_overflows(f):
        try:
            f.invoke2(v1, v2)
            assert False, "Should overflow"
        except OverflowError:
            pass

    def assert_converts_to_bigint(f, v):
        expected = wrap_bigint(rbigint.fromlong(v))
        result = f.invoke2(v1, v2)
        assert type(result) == WBigInt
        assert result._bigint_value.eq(expected._bigint_value)

    assert_overflows(RT._add)
    assert_overflows(RT._multiply)
    assert_converts_to_bigint(RT._addP, maxint+1)
    assert_converts_to_bigint(RT._multiplyP, (maxint-1)*2)

def test_unary_overflow():
    pos = wrap_int(maxint)
    neg = wrap_int(-maxint-1)

    def assert_overflows(f, x):
        try:
            f.invoke1(x)
            assert False, "Should overflow"
        except OverflowError:
            pass

    def assert_converts_to_bigint(f, x, n):
        expected = wrap_bigint(rbigint.fromlong(n))
        result = f.invoke1(x)
        assert type(result) == WBigInt
        assert result._bigint_value.eq(expected._bigint_value)

    assert_overflows(RT._negate, neg)
    assert_overflows(RT._inc, pos)
    assert_overflows(RT._dec, neg)
    assert_converts_to_bigint(RT._negateP, neg, maxint+1)
    assert_converts_to_bigint(RT._incP, pos, maxint+1)
    assert_converts_to_bigint(RT._decP, neg, -maxint-2)
