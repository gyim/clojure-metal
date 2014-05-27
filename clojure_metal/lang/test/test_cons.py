import clojure_metal.lang.rt as RT
from clojure_metal.lang.base_types import nil, Object, id_gen
from clojure_metal.lang.cons import Cons


class Thing(Object):
    _type = id_gen.next_id()
    def type(self):
        return Thing._type

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