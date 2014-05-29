import rt as RT
from base_types import Object, nil, id_gen, true, false
from aseq import ASeq
from fn import extend_rt
from numbers import wrap_int
from rpython.rlib.rarithmetic import r_uint32
from murmur3 import mix_col_hash
import util as UT

class APersistentVector(Object):
    def __init__(self):
        self._hash = None

    def rt_seq(self):
        if self._cnt > 0:
            return IndexedSeq(self, 0)
        return nil

    def rt_hash(self):
        if self._hash is None:
            n = r_uint32(0)
            hash = r_uint32(1)
            for x in range(self._cnt):
                hash = r_uint32(31) * hash + UT.hash(UT.nth(wrap_int(x)))._int_value
                n += 1
                x = RT.next.invoke1(x)

            self._hash = wrap_int(int(mix_col_hash(hash, n)))

        return self._hash

    def rt_equiv(self, other):
        if UT.is_satisfies(RT.IPersistentVector, other):
            if UT.equiv(RT.count.invoke1(self), UT.count(other)) is false:
                return false
            for x in range(self._cnt):
                i = wrap_int(x)
                if RT.equiv(RT.nth.invoke1(self, i), UT.nth(self, i)) is false:
                    return false
            return true
        else:
            if RT.is_satisfies.invoke1(RT.Sequential, other) is false:
                return false
            ms = RT.seq.invoke1(other)

            for x in range(self._cnt):

                if ms is nil or UT.equiv(UT.nth(x, wrap_int(x)), UT.first(ms)) is false:
                    return false


                ms = UT.next(ms)

            if ms is not nil:
                return false

        return true



@extend_rt
class IndexedSeq(ASeq):
    _type = id_gen.next_id()
    def type(self):
        return self._type

    def __init__(self, v, idx, meta=nil):
        ASeq.__init__(meta)
        self._v = v
        self._idx = idx

    def rt_first(self):
        return RT.nth.invoke1(self._v, wrap_int(self._idx))

    def rt_next(self):
        ## todo cast int
        if self._idx + 1 < RT.count.invoke1()._int_value:
            return IndexedSeq(self._v, self._idx + 1)
        return nil

    def rt_index(self):
        return wrap_int(self._idx)

    def rt_count(self):
        return wrap_int(RT.count.invoke1(self._v)._int_value - 1)

    def rt_with_meta(self, meta):
        return IndexedSeq(self._v, self._idx, meta)

    def rt_meta(self, meta):
        return self._meta
