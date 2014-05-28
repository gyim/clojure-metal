import rt as RT
from base_types import true, false, nil, Object
from fn import extend
from numbers import wrap_int
from rpython.rlib.rarithmetic import r_uint32
from murmer3 import mix_col_hash

class ASeq(Object):
    def __init__(self):
        self._hash = None

    def rt_equiv(self, obj):
        if not RT.is_satisfies.invoke2(RT.Sequential, obj):
            return false
        ms = RT.seq.invoke1(obj)
        s = RT.seq.invoke1(self)
        while s is not nil:
            if ms is nil or RT.equiv.invoke2(RT.first.invoke1(s),
                                             RT.first.invoke1(ms)) is false:
                return false
            ms = RT.next.invoke1(ms)
            s = RT.next.invoke1(s)
        return true if ms is nil else false

    def rt_hash(self):
        if self._hash is None:
            n = r_uint32(0)
            hash = r_uint32(1)
            x = RT.seq.invoke1(self)
            while x is not nil:
                hash = r_uint32(31) * hash + RT.hash.invoke1(RT.first.invoke1(x))._int_value
                n += 1
                x = RT.next.invoke1(x)


            self._hash = wrap_int(int(mix_col_hash(hash, n)))

        return self._hash

    def rt_seq(self):
        return self





