import clojure_metal.lang.rt as RT
from clojure_metal.lang.base_types import nil, Object, id_gen, true
from clojure_metal.lang.cons import Cons
from clojure_metal.lang.persistent_vector import create, EMPTY as EMPTY_VEC
from clojure_metal.lang.numbers import wrap_int


class Thing(Object):
    _type = id_gen.next_id()
    def type(self):
        return Thing._type

thing = Thing()
thing2 = Thing()
thing3 = Thing()


def test_create():
    assert create(thing, thing2, thing3)


def test_large_vector():
    r = EMPTY_VEC
    for x in range(1024 * 2):
        r = RT.conj.invoke2(r, wrap_int(x))
        c = RT.count.invoke1(r)
        assert c._int_value == x + 1

    assert r

    for x in range(1024 * 2):
        v = RT.nth.invoke2(r, wrap_int(x))
        assert RT._eq.invoke2(v, wrap_int(x)) is true

