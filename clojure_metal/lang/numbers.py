from fn import PolymorphicFn, wrap_fn, extend
from base_types import Object, id_gen, true, false
from rpython.rlib.rbigint import rbigint
import rt as RT

#### Int ####

class WInt(Object):
    _type = id_gen.next_id()
    def type(self):
        return WInt._type

    def __init__(self, int_value):
        self._int_value = int_value

def wrap_int(i):
    assert isinstance(i, int)
    return WInt(i)

RT._equiv.extend(WInt._type, wrap_fn(lambda a, b: RT._equiv_int.invoke2(b, a)))
@extend(WInt._type, RT._equiv_int)
def _eq_int_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WInt)
    if a._int_value == b._int_value:
        return true
    return false
@extend(WInt._type, RT._equiv_bigint)
def _eq_int_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WInt)
    return true if a._bigint_value.eq(rbigint.fromint(b._int_value)) else false

RT._add.extend(WInt._type, wrap_fn(lambda  a, b: RT._add_int.invoke2(b, a)))
@extend(WInt._type, RT._add_int)
def _add_int_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WInt)
    return wrap_int(a._int_value + b._int_value)
@extend(WInt._type, RT._add_bigint)
def _add_int_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WInt)
    return wrap_bigint(a._bigint_value.add(rbigint.fromint(b._int_value)))

int_zero = wrap_int(0)

#### BigInt ####

class WBigInt(Object):
    _type = id_gen.next_id()
    def type(self):
        return WBigInt._type

    def __init__(self, bigint_value):
        self._bigint_value = bigint_value

def wrap_bigint(l):
    assert isinstance(l, rbigint)
    return WBigInt(l)

RT._equiv.extend(WBigInt._type, wrap_fn(lambda a, b: RT._equiv_bigint.invoke2(b, a)))
@extend(WBigInt._type, RT._equiv_bigint)
def _eq_bigint_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WBigInt)
    return true if a._bigint_value.eq(b._bigint_value) else false
@extend(WBigInt._type, RT._equiv_int)
def _eq_bigint_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WBigInt)
    return true if b._bigint_value.eq(rbigint.fromint(a._int_value)) else false

RT._add.extend(WBigInt._type, wrap_fn(lambda  a, b: RT._add_bigint.invoke2(b, a)))
@extend(WBigInt._type, RT._add_bigint)
def _add_bigint_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WBigInt)
    return wrap_bigint(a._bigint_value.add(b._bigint_value))
@extend(WBigInt._type, RT._add_int)
def _add_bigint_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WBigInt)
    return wrap_bigint(b._bigint_value.add(rbigint.fromint(a._int_value)))
