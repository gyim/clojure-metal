import rt as RT
import util as UT
from base_types import true, false, nil, Object
from fn import extend
from numbers import wrap_int
from rpython.rlib.rarithmetic import r_uint32
from murmur3 import mix_col_hash

class ASeq(Object):
    def __init__(self):
        self._hash = None

    def rt_equiv(self, obj):
        if not UT.is_satisfies(RT.Sequential, obj):
            return false
        ms = UT.seq(obj)
        s = UT.seq(self)
        while s is not nil:
            if ms is nil or UT.equiv(UT.first(s), UT.first(ms)) is false:
                return false
            ms = UT.next(ms)
            s = UT.next(s)
        return true if ms is nil else false

    def rt_hash(self):
        if self._hash is None:
            n = r_uint32(0)
            hash = r_uint32(1)
            x = RT.seq.invoke1(self)
            while x is not nil:
                hash = r_uint32(31) * hash + UT.hash(UT.first(x))._int_value
                n += 1
                x = RT.next.invoke1(x)


            self._hash = wrap_int(int(mix_col_hash(hash, n)))

        return self._hash

    def rt_seq(self):
        return self





