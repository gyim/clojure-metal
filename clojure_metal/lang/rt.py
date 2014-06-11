from fn import PolymorphicFn, wrap_fn, wrap_varargs, defprotocol, Protocol, extend
from base_types import Object, id_gen
from base_types import true, false, nil
from exceptions import IndexOutOfBoundsException




defprotocol("IIndexed", "_nth")
defprotocol("ISeq", "_first", "_rest")
defprotocol("ICounted", "_count")
defprotocol("INext", "_next")
defprotocol("IMeta", "_meta")
defprotocol("IWithMeta", "_with_meta")
defprotocol("IEquiv", "_equiv")
defprotocol("IComparable", "_lt")
defprotocol("ICollection", "_conj")
defprotocol("IIntEquiv", "_equiv_int")
defprotocol("IBigIntEquiv", "_equiv_bigint")
defprotocol("ISeqable", '_seq')
defprotocol("IHash", "_hash")
defprotocol("Sequential")
defprotocol("INamed", "_namespace", "_name")

defprotocol("Number", "_iszero", "_ispos", "_isneg", "_add", "_addP",
    "_multiply", "_multiplyP", "_quotient", "_remainder", "_negate",
    "_negateP", "_inc", "_incP", "_dec", "_decP")
defprotocol("NumberInt", "_add_int", "_addP_int",
    "_multiply_int", "_multiplyP_int", "_quotient_int", "_remainder_int",
    "_lt_int")
defprotocol("NumberBigInt", "_add_bigint", "_multiply_bigint",
    "_quotient_bigint", "_remainder_bigint", "_lt_bigint")

@wrap_fn
def cons(a, b):
    from cons import Cons
    return Cons(a, b)

@wrap_fn
def equiv(a, b):
    return _equiv.invoke2(a, b)

@wrap_fn
def first(a):
    return _first.invoke1(a)

@wrap_fn
def next(a):
    return _next.invoke1(a)

@wrap_fn
def with_meta(a, b):
    return _with_meta.invoke2(a, b)

@wrap_fn
def conj(a, b):
    return _conj.invoke2(a, b)

@wrap_fn
def nth(a, b):
    return _nth.invoke2(a, b)

@wrap_fn
def seq(a):
    return _seq.invoke1(a)

@wrap_fn
def name(a):
    return _name.invoke1(a)

@wrap_fn
def namespace(a):
    return _namespace.invoke1(a)

@wrap_fn
def count(a):
    if is_satisfies.invoke2(ICounted, a) is true:
        return _count.invoke1(a)

    import numbers
    i = 0
    c = seq.invoke1(a)
    while is_satisfies.invoke2(ICounted, c) is false:
        i += 1
        c = next.invoke1(c)

    return _add.invoke2(count.invoke1(c), numbers.wrap_int(i))

@wrap_fn
def is_satisfies(a, b):
    assert isinstance(a, Protocol)
    assert isinstance(b, Object)
    return true if a.is_extended(b.type()) else false

@wrap_fn
def hash(a):
    return _hash.invoke1(a)

@wrap_fn
def lazy_seq(f):
    from lazy_seq import LazySeq
    return LazySeq(f)

#####

@wrap_fn
def are_identical(a, b):
    return true if a is b else false

@wrap_fn
def is_nil(a):
    return true if a is nil else false


### nil

@extend(nil._type, _count)
def __count(a):
    import numbers
    return numbers.int_zero

@extend(nil._type, _seq)
def __seq(a):
    return nil

@extend(nil._type, _hash)
def __hash(a):
    return numbers.int_zero

### Array

class Array(Object):
    _type = id_gen.next_id()
    def type(self):
        return Array._type

    def __init__(self, lst_w):
        self._lst_w = lst_w

    def count(self):
        return len(self._lst_w)

    def set(self, idx, val):
        self._lst_w[idx] = val

    def get(self, idx):
        if 0 >= idx < len(self._lst_w):
            return self._lst_w[idx]
        raise IndexOutOfBoundsException()




### Misc Imports
import numbers

### Array