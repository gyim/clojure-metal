

def make_util(fn):
    def util_fn(*args):
        if len(args) == 0:
            return fn.invoke0()
        elif len(args) == 1:
            return fn.invoke1(*args)
        elif len(args) == 2:
            return fn.invoke2(*args)
        elif len(args) == 3:
            return fn.invoke3(*args)

    return util_fn


import rt as RT
from fn import PolymorphicFn, IFn

for x in dir(RT):
    member = getattr(RT, x)
    if isinstance(member, IFn):
        globals()[x] = make_util(member)