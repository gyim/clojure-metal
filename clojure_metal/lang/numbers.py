from fn import PolymorphicFn, wrap_fn, extend
from base_types import Object, id_gen, true, false
from rpython.rlib.rbigint import rbigint
from rpython.rlib.rarithmetic import ovfcheck
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

int_zero = wrap_int(0)

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

@extend(WInt._type, RT._iszero)
def _iszero_int(n):
    assert isinstance(n, WInt)
    return true if n._int_value == 0 else false

@extend(WInt._type, RT._ispos)
def _ispos_int(n):
    assert isinstance(n, WInt)
    return true if n._int_value > 0 else false

@extend(WInt._type, RT._isneg)
def _isneg_int(n):
    assert isinstance(n, WInt)
    return true if n._int_value < 0 else false

RT._add.extend(WInt._type, wrap_fn(lambda  a, b: RT._add_int.invoke2(b, a)))
@extend(WInt._type, RT._add_int)
def _add_int_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WInt)
    return wrap_int(ovfcheck(a._int_value + b._int_value))
@extend(WInt._type, RT._add_bigint)
def _add_int_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WInt)
    return wrap_bigint(a._bigint_value.add(rbigint.fromint(b._int_value)))

RT._addP.extend(WInt._type, wrap_fn(lambda  a, b: RT._addP_int.invoke2(b, a)))
@extend(WInt._type, RT._addP_int)
def _add_int_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WInt)
    try:
        return wrap_int(ovfcheck(a._int_value + b._int_value))
    except OverflowError:
        return wrap_bigint(rbigint.fromint(a._int_value).add(rbigint.fromint(b._int_value)))

RT._multiply.extend(WInt._type, wrap_fn(lambda  a, b: RT._multiply_int.invoke2(b, a)))
@extend(WInt._type, RT._multiply_int)
def _multiply_int_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WInt)
    return wrap_int(ovfcheck(a._int_value * b._int_value))
@extend(WInt._type, RT._multiply_bigint)
def _multiply_int_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WInt)
    return wrap_bigint(a._bigint_value.mul(rbigint.fromint(b._int_value)))

RT._multiplyP.extend(WInt._type, wrap_fn(lambda  a, b: RT._multiplyP_int.invoke2(b, a)))
@extend(WInt._type, RT._multiplyP_int)
def _multiply_int_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WInt)
    try:
        return wrap_int(ovfcheck(a._int_value * b._int_value))
    except OverflowError:
        return wrap_bigint(rbigint.fromint(a._int_value).mul(rbigint.fromint(b._int_value)))

RT._quotient.extend(WInt._type, wrap_fn(lambda  a, b: RT._quotient_int.invoke2(b, a)))
@extend(WInt._type, RT._quotient_int)
def _quotient_int_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WInt)
    return wrap_int(a._int_value / b._int_value)
@extend(WInt._type, RT._quotient_bigint)
def _quotient_int_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WInt)
    return wrap_bigint(a._bigint_value.div(rbigint.fromint(b._int_value)))

RT._remainder.extend(WInt._type, wrap_fn(lambda  a, b: RT._remainder_int.invoke2(b, a)))
@extend(WInt._type, RT._remainder_int)
def _remainder_int_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WInt)
    return wrap_int(a._int_value % b._int_value)
@extend(WInt._type, RT._remainder_bigint)
def _remainder_int_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WInt)
    return wrap_bigint(a._bigint_value.mod(rbigint.fromint(b._int_value)))

RT._lt.extend(WInt._type, wrap_fn(lambda  a, b: RT._lt_int.invoke2(b, a)))
@extend(WInt._type, RT._lt_int)
def _lt_int_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WInt)
    return true if a._int_value < b._int_value else false
@extend(WInt._type, RT._lt_bigint)
def _lt_int_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WInt)
    return true if a._bigint_value.lt(rbigint.fromint(b._int_value)) else false

@extend(WInt._type, RT._negate)
def _negate_int(n):
    assert isinstance(n, WInt)
    return wrap_int(ovfcheck(-n._int_value))

@extend(WInt._type, RT._negateP)
def _negateP_int(n):
    assert isinstance(n, WInt)
    try:
        return wrap_int(ovfcheck(-n._int_value))
    except OverflowError:
        return wrap_bigint(rbigint.fromint(n._int_value).neg())

@extend(WInt._type, RT._inc)
def _inc_int(n):
    assert isinstance(n, WInt)
    return wrap_int(ovfcheck(n._int_value + 1))

@extend(WInt._type, RT._incP)
def _incP_int(n):
    assert isinstance(n, WInt)
    try:
        return wrap_int(ovfcheck(n._int_value + 1))
    except OverflowError:
        return wrap_bigint(rbigint.fromint(n._int_value).add(bigint_one._bigint_value))

@extend(WInt._type, RT._dec)
def _dec_int(n):
    assert isinstance(n, WInt)
    return wrap_int(ovfcheck(n._int_value - 1))

@extend(WInt._type, RT._decP)
def _decP_int(n):
    assert isinstance(n, WInt)
    try:
        return wrap_int(ovfcheck(n._int_value - 1))
    except OverflowError:
        return wrap_bigint(rbigint.fromint(n._int_value).sub(bigint_one._bigint_value))

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

bigint_zero = wrap_bigint(rbigint.fromint(0))
bigint_one = wrap_bigint(rbigint.fromint(1))

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

@extend(WBigInt._type, RT._iszero)
def _iszero_bigint(n):
    assert isinstance(n, WBigInt)
    return true if n._bigint_value.sign == 0 else false

@extend(WBigInt._type, RT._ispos)
def _ispos_bigint(n):
    assert isinstance(n, WBigInt)
    return true if n._bigint_value.sign > 0 else false

@extend(WBigInt._type, RT._isneg)
def _isneg_bigint(n):
    assert isinstance(n, WBigInt)
    return true if n._bigint_value.sign < 0 else false

RT._add.extend(WBigInt._type, wrap_fn(lambda  a, b: RT._add_bigint.invoke2(b, a)))
RT._addP.extend(WBigInt._type, wrap_fn(lambda  a, b: RT._add_bigint.invoke2(b, a)))
@extend(WBigInt._type, RT._add_bigint)
def _add_bigint_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WBigInt)
    return wrap_bigint(a._bigint_value.add(b._bigint_value))
def _add_bigint_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WBigInt)
    return wrap_bigint(b._bigint_value.add(rbigint.fromint(a._int_value)))
RT._add_int.extend(WBigInt._type, wrap_fn(_add_bigint_int))
RT._addP_int.extend(WBigInt._type, wrap_fn(_add_bigint_int))

RT._multiply.extend(WBigInt._type, wrap_fn(lambda  a, b: RT._multiply_bigint.invoke2(b, a)))
RT._multiplyP.extend(WBigInt._type, wrap_fn(lambda  a, b: RT._multiply_bigint.invoke2(b, a)))
@extend(WBigInt._type, RT._multiply_bigint)
def _multiply_bigint_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WBigInt)
    return wrap_bigint(a._bigint_value.mul(b._bigint_value))
def _multiply_bigint_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WBigInt)
    return wrap_bigint(b._bigint_value.mul(rbigint.fromint(a._int_value)))
RT._multiply_int.extend(WBigInt._type, wrap_fn(_multiply_bigint_int))
RT._multiplyP_int.extend(WBigInt._type, wrap_fn(_multiply_bigint_int))

RT._quotient.extend(WBigInt._type, wrap_fn(lambda  a, b: RT._quotient_bigint.invoke2(b, a)))
@extend(WBigInt._type, RT._quotient_bigint)
def _quotient_bigint_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WBigInt)
    return wrap_bigint(a._bigint_value.div(b._bigint_value))
@extend(WBigInt._type, RT._quotient_int)
def _quotient_bigint_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WBigInt)
    return wrap_bigint(rbigint.fromint(a._int_value).div(b._bigint_value))

RT._remainder.extend(WBigInt._type, wrap_fn(lambda  a, b: RT._remainder_bigint.invoke2(b, a)))
@extend(WBigInt._type, RT._remainder_bigint)
def _remainder_bigint_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WBigInt)
    return wrap_bigint(a._bigint_value.mod(b._bigint_value))
@extend(WBigInt._type, RT._remainder_int)
def _remainder_bigint_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WBigInt)
    return wrap_bigint(rbigint.fromint(a._int_value).mod(b._bigint_value))

RT._lt.extend(WBigInt._type, wrap_fn(lambda  a, b: RT._lt_bigint.invoke2(b, a)))
@extend(WBigInt._type, RT._lt_bigint)
def _lt_bigint_bigint(b, a):
    assert isinstance(a, WBigInt)
    assert isinstance(b, WBigInt)
    return true if a._bigint_value.lt(b._bigint_value) else false
@extend(WBigInt._type, RT._lt_int)
def _lt_bigint_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WBigInt)
    return true if rbigint.fromint(a._int_value).lt(b._bigint_value) else false

def _negate_bigint(n):
    assert isinstance(n, WBigInt)
    if n._bigint_value.sign == 0:
        return n
    else:
        return wrap_bigint(n._bigint_value.neg())
RT._negate.extend(WBigInt._type, wrap_fn(_negate_bigint))
RT._negateP.extend(WBigInt._type, wrap_fn(_negate_bigint))

def _inc_bigint(n):
    assert isinstance(n, WBigInt)
    if n._bigint_value.sign == 0:
        return n
    else:
        return wrap_bigint(n._bigint_value.add(bigint_one._bigint_value))
RT._inc.extend(WBigInt._type, wrap_fn(_inc_bigint))
RT._incP.extend(WBigInt._type, wrap_fn(_inc_bigint))

def _dec_bigint(n):
    assert isinstance(n, WBigInt)
    if n._bigint_value.sign == 0:
        return n
    else:
        return wrap_bigint(n._bigint_value.sub(bigint_one._bigint_value))
RT._dec.extend(WBigInt._type, wrap_fn(_dec_bigint))
RT._decP.extend(WBigInt._type, wrap_fn(_dec_bigint))
