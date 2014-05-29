from clojure_metal.lang.lisp_reader import read_string
from clojure_metal.lang.cons import Cons
from clojure_metal.lang.numbers import WInt
import clojure_metal.lang.rt as RT

def test_read_int():
    i = read_string("1")
    assert isinstance(i, WInt)
    assert i._int_value == 1

def test_read_list():
    l = read_string("(1 2 3)")
    assert l
    assert isinstance(l, Cons)
    assert RT.count.invoke1(l)._int_value == 3