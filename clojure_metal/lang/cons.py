from base_types import Object, id_gen, nil
from fn import extend, extend_rt, mark_as
import rt as RT
from aseq import ASeq

@extend_rt
@mark_as(RT.Sequential)
class Cons(ASeq):
    def __init__(self, first, more, meta=nil):
        ASeq.__init__(self)
        self._first = first
        self._more = more
        self._meta = meta

    _type = id_gen.next_id()
    def type(self):
        return Cons._type


@extend(Cons._type, RT._first)
def first(self):
    assert isinstance(self, Cons)
    return self._first

@extend(Cons._type, RT._next)
def next(self):
    assert isinstance(self, Cons)
    return self._more

@extend(Cons._type, RT._with_meta)
def with_meta(self, meta):
    assert isinstance(self, Cons)
    return Cons(self._first, self._more, meta)


def create(*args):
    acc = nil
    for x in args:
        acc = Cons(x, acc)
    return acc