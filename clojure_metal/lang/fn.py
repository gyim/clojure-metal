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


class Protocol(Object):
    def __init__(self, name, pfns):
        self._name = name
        self._pfns = pfns
        self.extended_by = {}

    def add_fn(self, pfn):
        self._pfns.append(pfn)
        return pfn

    def extend(self, tp):
        self.extended_by[tp] = tp

    def is_extended(self, tp):
        return tp in self.extended_by


class PolymorphicFn(IFn):
    _type = id_gen.next_id()
    def __init__(self, name, protocol):
        self._name = name
        self._table = {}
        self._protocol = protocol

    def type(self):
        return PolymorphicFn._type

    def extend(self, tp, fn):
        self._table[tp] = fn
        self._protocol.extend(tp)

    def invoke1(self, a):
        f = self._table[a.type()]
        return f.invoke1(a)

    def invoke2(self, a, b):
        f = self._table[a.type()]
        return f.invoke2(a, b)

    def invoke3(self, a, b, c):
        f = self._table[a.type()]
        return f.invoke3(a, b, c)

import inspect
def defprotocol(protoname, *pfns):
    gbls = inspect.currentframe().f_back.f_globals
    protocol = Protocol(protoname, [])
    gbls[protoname] = protocol
    for x in pfns:
        gbls[x] = protocol.add_fn(PolymorphicFn(x, protocol))


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

anames = "abcdefghijklmnopqrst"

def extend_rt(klass):
    import rt as RT
    rt_dir = dir(RT)
    for method in dir(klass):
        if method.startswith("rt_") and method[2:] in rt_dir:
            pfn = getattr(RT, method[2:])
            if isinstance(pfn, PolymorphicFn):
                argc = getattr(klass, method).im_func.func_code.co_argcount
                args = ",".join(anames[:argc - 1])
                exec "func = lambda self, {args}: self.{attr}({args})".format(
                            args=args,
                            attr=method)
                extend(klass._type, pfn)(func)
    return klass


class mark_as(object):
    def __init__(self, protocol):
        self.protocol = protocol
    def __call__(self, klass):
        self.protocol.extend(klass._type)
        return klass


