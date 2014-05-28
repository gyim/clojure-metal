import clojure_metal.lang.rt as RT
from clojure_metal.lang.base_types import nil, Object, id_gen
from clojure_metal.lang.cons import Cons, create
from clojure_metal.lang.base_types import true, false, nil
from clojure_metal.lang.fn import extend_rt

@extend_rt
class Thing(Object):
    _type = id_gen.next_id()
    def type(self):
        return Thing._type

    def rt_equiv(self, other):
        return true if self is other else false

thing = Thing()
thing2 = Thing()
thing3 = Thing()

def test_cons_creation():
    c = RT.cons.invoke2(nil, nil)
    assert c
    assert c.type() is Cons._type

def test_first_next():
    v = nil
    v = RT.cons.invoke2(thing, v)
    assert RT.first.invoke1(v) is thing
    assert RT.next.invoke1(v) is nil

def test_with_meta():
    v = RT.cons.invoke2(nil, nil)
    assert RT.with_meta.invoke2(v, thing2)

def test_cons_equiv():
    a = create(thing, thing2, thing3)
    b = create(thing, thing, thing)
    c = create(thing, thing2, thing3)

    assert RT.equiv.invoke2(a, b) is false
    assert RT.equiv.invoke2(a, c) is true