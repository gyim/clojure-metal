from base_types import Object, id_gen, nil
from fn import extend, extend_rt
from exceptions import IndexOutOfBoundsException
import rt as RT
from fn import wrap_varargs
from numbers import wrap_int
from rpython.rlib.rarithmetic import r_uint


class Node(Object):
    def __init__(self, edit, array = None):
        self._edit = edit
        if array is None:
            self._array = [None] * 32
        else:
            self._array = array

NOEDIT = None
EMPTY_NODE = Node(NOEDIT, [None] * 32)



@extend_rt
class PersistentVector(Object):
    _type = id_gen.next_id()
    def type(self):
        return PersistentVector._type


    def __init__(self, meta, cnt, shift, root, tail):
        self._meta = meta
        self._cnt = cnt
        self._shift = shift
        self._root = root
        self._tail = tail

    def tailoff(self):
        if (self._cnt < 32):
            return 0
        return ((self._cnt - 1) >> 5) << 5

    def array_for(self, i):
        if i >= 0 and i < self._cnt:
            if i >= self.tailoff():
                return self._tail
            node = self._root
            level = self._shift
            while level > 0:
                node = node._array[(i >> level) & 0x1f]
                level -= 5
            return node._array
        raise IndexOutOfBoundsException()

    def nth(self, i, not_found=None):
        if not_found is not None:
            if 0 <= i < self._cnt:
                return self.nth(i, None)
            return not_found
        else:
            node = self.array_for(i)
            return node[i & 0x01f]

    def assoc_n(self, i, val):
        if 0 <= i < self._cnt:
            if i >= self.tailoff():
                new_tail = self._tail[:]
                new_tail[i & 0x1f] = val
                return PersistentVector(self._meta, self._cnt, self._shift, self._root, new_tail)
            new_root = self.do_assoc(self._shift, self._root, i, val)
            return PersistentVector(self._meta, self._cnt, self._shift, new_root, self._tail)

        if i == self._cnt:
            return self.cons(val)

        raise IndexOutOfBoundsException()

    def do_assoc(self, level, node, i, val):
        ret = Node(node._edit, node._array[:])
        if level == 0:
            ret._array[i & 0x01f] = val
        else:
            subidx = (i >> level) & 0x1f;
            ret._array[subidx] = self.do_assoc(level - 5, node._array[subidx], i, val)
        return ret

    def count(self):
        return self._cnt

    def with_meta(self, meta):
        return PersistentVector(meta, self._cnt, self._shift, self._root, self._tail)

    def meta(self):
        return self._meta

    def cons(self, val):
        i = self._cnt
        if self._cnt - self.tailoff() < 32:
            new_tail = self._tail[:]
            new_tail.append(val)
            return PersistentVector(self._meta, self._cnt + 1, self._shift, self._root, new_tail)

        tail_node = Node(self._root._edit, self._tail)
        new_shift = self._shift
        if (self._cnt >> 5) > (1 << self._shift):
            new_root = Node(self._root._edit)
            new_root._array[0] = self._root
            new_root._array[1] = self.new_path(self._root._edit, self._shift, tail_node)
            new_shift += 5

        else:
            new_root = self.push_tail(self._shift, self._root, tail_node)

        return PersistentVector(self._meta, self._cnt + 1, new_shift, new_root, [val])

    def push_tail(self, level, parent, tail_node):
        sub_idx = ((self._cnt - 1) >> level) & 0x01f
        ret = Node(parent._edit, parent._array[:])
        if level == 5:
            node_to_insert = tail_node
        else:
            child = parent._array[sub_idx]
            if child is not None:
                node_to_insert = self.push_tail(level - 5, child, tail_node)
            else:
                node_to_insert = self.new_path(self._root._edit, level - 5, tail_node)

        ret._array[sub_idx] = node_to_insert
        return ret

    def new_path(self, edit, level, node):
        if level == 0:
            return node
        ret = Node(edit)
        ret._array[0] = self.new_path(edit, level - 5, node)
        return ret

    def rt_conj(self, b):
        return self.cons(b)

EMPTY = PersistentVector(nil, r_uint(0), r_uint(5), EMPTY_NODE, [])

def create(*args):
    ret = EMPTY
    for val in args:
        ret = ret.cons(val)
    return ret

@extend(PersistentVector._type, RT._nth)
def nth(a, b):
    assert isinstance(a, PersistentVector)
    return a.nth(b._int_value)

@extend(PersistentVector._type, RT._count)
def count(a):
    assert isinstance(a, PersistentVector)
    return wrap_int(int(a._cnt))



