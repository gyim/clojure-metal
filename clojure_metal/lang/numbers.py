from fn import PolymorphicFn, wrap_fn, extend
from base_types import Object, id_gen, true, false
import rt as RT


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

RT._add.extend(WInt._type, wrap_fn(lambda  a, b: RT._add_int.invoke2(b, a)))
@extend(WInt._type, RT._add_int)
def _add_int(b, a):
    assert isinstance(a, WInt)
    assert isinstance(b, WInt)
    return wrap_int(a._int_value + b._int_value)


int_zero = wrap_int(0)