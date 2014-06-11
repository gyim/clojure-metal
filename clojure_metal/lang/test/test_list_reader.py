from clojure_metal.lang.lisp_reader import read_string
from clojure_metal.lang.cons import Cons
from clojure_metal.lang.numbers import WInt, WBigInt
import clojure_metal.lang.rt as RT

def test_read_int():
    def read_int(s):
        i = read_string(s)
        assert isinstance(i, WInt)
        return i._int_value

    assert read_int('0') == 0
    assert read_int('1') == 1
    assert read_int('+1') == 1
    assert read_int('-1') == -1
    assert read_int('0x10') == 16
    assert read_int('033') == 27
    assert read_int('16rff') == 255

def test_read_bigint():
    def read_bigint(s):
        i = read_string(s)
        assert isinstance(i, WBigInt)
        return i._bigint_value.tolong()

    assert read_bigint('0N') == 0L
    assert read_bigint('1N') == 1L
    assert read_bigint('+1N') == 1L
    assert read_bigint('-1N') == -1L
    assert read_bigint('0x10N') == 16L
    assert read_bigint('033N') == 27L

    assert read_bigint('99999999999999999999') == 99999999999999999999L
    assert read_bigint('+99999999999999999999') == 99999999999999999999L
    assert read_bigint('-99999999999999999999') == -99999999999999999999L
    assert read_bigint('0x10000000000000000') == 2**64
    assert read_bigint('02000000000000000000000') == 2**64
    assert read_bigint('16r10000000000000000') == 2**64

def test_read_list():
    l = read_string("(1 2 3)")
    assert l
    assert isinstance(l, Cons)
    assert RT.count.invoke1(l)._int_value == 3