
import rt as RT
from fn import extend_rt
from base_types import Object, id_gen, nil, false, true
from numbers import wrap_int
import util as UT
from murmur3 import hash_int
from string import wrap_string, intern as intern_string
from rpython.rlib.rarithmetic import r_uint32
from murmur3 import hash_combine

@extend_rt
class Symbol(Object):
    _type = id_gen.next_id()
    def type(self):
        return Symbol._type

    def __init__(self, ns, name):
        self._name = name
        self._ns = ns

    def rt_name(self):
        return self._name

    def rt_namespace(self):
        return self._ns

    def rt_hash(self):
        h = hash_combine(r_uint32(UT.hash(self._name)._int_value), r_uint32(UT.hash(self._ns)._int_value))
        return wrap_int(int(h))

    def rt_equiv(self, other):
        if not isinstance(other, Symbol):
            return false
        return true if self._name is other._name and \
                    self._ns is other._ns else false

def intern(ns, name=None):
    if name is None:
        name = ns
        ns = None

    assert ns is None or isinstance(ns, str)
    assert isinstance(name, str)

    ns_i = nil if ns is None else intern_string(ns)
    name_i = intern_string(name)

    return Symbol(ns_i, name_i)