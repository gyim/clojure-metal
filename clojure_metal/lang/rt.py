from fn import PolymorphicFn, wrap_fn, wrap_varargs

_conj = PolymorphicFn()
_nth = PolymorphicFn()
_next = PolymorphicFn()
_first = PolymorphicFn()
_count = PolymorphicFn()
_with_meta = PolymorphicFn()

@wrap_fn
def cons(a, b):
    from cons import Cons
    return Cons(a, b)


@wrap_fn
def first(a):
    return _first.invoke1(a)

@wrap_fn
def next(a):
    return _next.invoke1(a)

@wrap_fn
def with_meta(a, b):
    return _with_meta.invoke2(a, b)

@wrap_fn
def conj(a, b):
    return _conj.invoke2(a, b)

@wrap_fn
def nth(a, b):
    return _nth.invoke2(a, b)

@wrap_fn
def count(a):
    return _count.invoke1(a)

_eq = PolymorphicFn()
