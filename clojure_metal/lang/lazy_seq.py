from aseq import ASeq
from base_types import id_gen, nil
import rt as RT
from fn import mark_as, extend_rt

@extend_rt
@mark_as(RT.Sequential)
class LazySeq(ASeq):
    _type = id_gen.next_id()
    def type(self):
        return LazySeq._type

    def __init__(self, f, meta=nil):
        ASeq.__init__(self)
        self._fn = f
        self._meta = meta

    def rt_with_meta(self, meta):
        return LazySeq(self._fn, self._meta)

    def rt_meta(self):
        return self._meta

    ## TODO: syncronize?
    def sval(self):
        if self._fn is not None:
            self._sv = self._fn.invoke0()
            self._fn = None
        if self._sv is not None:
            return self._sv
        return self._s

    ## TODO: syncronize?
    def rt_seq(self):
        self.sval()
        if self._sv is not None:
            ls = self._sv
            self._sv = None
            while isinstance(ls, LazySeq):
                ls = ls.sval()
            self._s = RT.seq.invoke1(ls)
        return self._s

    def rt_first(self):
        self.seq()
        if self._s is None:
            return nil
        return RT.first.invoke1(self._s)

    def rt_next(self):
        self.seq()
        if self._s is None:
            return nil
        return RT.next.invoke1(self._s)
