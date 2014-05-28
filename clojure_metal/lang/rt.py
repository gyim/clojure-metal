from fn import PolymorphicFn, wrap_fn, wrap_varargs, defprotocol, Protocol
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
defprotocol("ICollection", "_conj")
defprotocol("IIntEquiv", "_equiv_int")
defprotocol("ISeqable", '_seq')
defprotocol("Sequential")

defprotocol("Number", "_number_add")

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
def count(a):
    if is_satisfies.invoke2(ICounted, a):
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

#####

@wrap_fn
def are_identical(a, b):
    return true if a is b else false

@wrap_fn
def is_nil(a):
    return true if a is nil else false

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



### Array