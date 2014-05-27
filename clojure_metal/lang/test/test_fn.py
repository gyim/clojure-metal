from clojure_metal.lang.fn import IFn, AbstractMethodException, PolymorphicFn
from clojure_metal.lang.base_types import Object, id_gen

class Thing(Object):
    _type = id_gen.next_id()
    def type(self):
        return Thing._type

thing = Thing()
thing2 = Thing()
thing3 = Thing()

class SimpleFn(IFn):
    def invoke0(self):
        return thing
    def invoke1(self, a):
        return a


def test_calling():
    assert SimpleFn().invoke0() is thing
    try:
        SimpleFn().invoke2(thing, thing) is thing
        assert False
    except AbstractMethodException, ex:
        assert ex.method == "2"


def test_polymorphic_fn():
    pfn = PolymorphicFn()
    pfn.extend(thing.type(), SimpleFn())

    assert pfn.invoke1(thing) is thing
