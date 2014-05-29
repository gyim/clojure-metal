import rt as RT
from fn import extend_rt
from base_types import Object, id_gen, nil, false, true
from numbers import wrap_int
from murmur3 import hash_int
from rpython.rlib.rarithmetic import r_uint32

class StringIntern(object):
    def __init__(self):
        self._strs = {}
    def intern(self, s):
        if s not in self._strs:
            self._strs[s] = String(s)

        return self._strs[s]

interned_strings = StringIntern()

@extend_rt
class String(Object):
    _type = id_gen.next_id()
    def type(self):
        return String._type

    def __init__(self, str_value):
        self._str_value = str_value

    def get_str_value(self):
        return self._str_value

    def rt_name(self):
        return self._str_value

    def rt_namespace(self):
        return nil

    def rt_hash(self):
        return wrap_int(int(hash_int(r_uint32(hash(self._str_value)))))

    def rt_equiv(self, other):
        if not isinstance(other, String):
            return false
        return true if self._str_value is other._str_value else false

def intern(s):
    assert isinstance(s, str)
    return interned_strings.intern(s)

def wrap_string(s):
    assert isinstance(s, str)
    return String(s)