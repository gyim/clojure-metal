from base_types import Object, id_gen


class AbstractMethodException(BaseException):
    def __init__(self, method):
        self.method = method


class IFn(Object):
    def invoke0(self):
        raise AbstractMethodException(str(0))
    def invoke1(self, a):
        raise AbstractMethodException(str(1))
    def invoke2(self, a, b):
        raise AbstractMethodException(str(2))
    def invoke3(self, a, b, c):
        raise AbstractMethodException(str(3))

class AFn(IFn):
    def type(self):
        return AFn._type
    _type = id_gen.next_id()



class PolymorphicFn(IFn):
    _type = id_gen.next_id()
    def __init__(self):
        self.table = {}

    def type(self):
        return PolymorphicFn._type

    def extend(self, tp, fn):
        self.table[tp] = fn

    def invoke1(self, a):
        f = self.table[a.type()]
        return f.invoke1(a)

    def invoke2(self, a, b):
        f = self.table[a.type()]
        return f.invoke2(a, b)

    def invoke3(self, a, b, c):
        f = self.table[a.type()]
        return f.invoke3(a, b, c)



def wrap_fn(fn):
    argc = fn.func_code.co_argcount

    if argc == 0:
        class WFn0(AFn):
            def invoke0(self):
                return fn()
        return WFn0()

    if argc == 1:
        class WFn1(AFn):
            def invoke1(self, a):
                return fn(a)
        return WFn1()

    if argc == 2:
        class WFn2(AFn):
            def invoke2(self, a, b):
                return fn(a, b)
        return WFn2()

    assert False

def wrap_varargs(fn):
    class WVarArgs(AFn):
        def invoke0(self):
            return fn()
        def inovke1(self, a):
            return fn(a)
        def invoke2(self, a, b):
            return fn(a, b)
        def invoke3(self, a, b, c):
            return fn(a, b, c)

    return WVarArgs()

class extend(object):
    def __init__(self, tid, pfn):
        self._pfn = pfn
        self._tid = tid
    def __call__(self, fn):
        self._pfn.extend(self._tid, wrap_fn(fn))
        return self._pfn

