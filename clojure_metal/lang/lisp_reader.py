import rpython.rlib.rsre.rsre_re as re
from numbers import wrap_int, wrap_bigint
from fn import AFn, wrap_fn
from cons import create_from_list as create_list
from rpython.rlib.rbigint import rbigint
from rpython.rlib.rarithmetic import LONG_BIT

int_pat = re.compile("^([-+]?)(?:(0)|([1-9][0-9]*)|0[xX]([0-9A-Fa-f]+)|0([0-7]+)|([1-9][0-9]?)[rR]([0-9A-Za-z]+)|0[0-9]+)(N)?$")

def is_whitespace(ch):
    return ch in '\n\r ,\t'

def is_digit(ch):
    return ch in '0123456789'



def read(r, eof_is_error, eof_value, is_recursive):
    while True:
        ch = r.read()

        while is_whitespace(ch):
            ch = r.read()

        if ch == "":
            if eof_is_error:
                raise RuntimeError("EOF while reading")
            return eof_value

        if is_digit(ch):
            n = read_number(r, ch)
            return n

        macro_fn = macros.get(ch, None)
        if macro_fn is not None:
            ret = macro_fn.invoke(r, ch)
            if ret is None:
                continue
            return ret

        if ch in ("+", "-"):
            ch2 = r.read()
            if is_digit(ch2):
                r.unread(ch2)
                n = read_number(r, ch)
                return n
            r.unread(ch2)

def match_number(s):
    m = int_pat.match(s)
    if m:
        if m.group(2) is not None:
            if m.group(8) is not None:
                return wrap_bigint(rbigint.fromint(0))
            return wrap_int(0)
        sign = -1 if m.group(1) == '-' else 1

        radix = 10
        n = m.group(3)
        if n is not None:
            radix = 10
        if n is None:
            n = m.group(4)
            if n is not None:
                radix = 16
        if n is None:
            n = m.group(5)
            if n is not None:
                radix = 8
        if n is None:
            n = m.group(7)
            if n is not None:
                radix = int(m.group(6))
        if n is None:
            return None

        bn = rbigint.fromstr(n, radix) # throws rpython.rlib.rstring.InvalidBaseError
        bn.sign = sign

        if m.group(8) is not None:
            return wrap_bigint(bn)
        elif bn.bit_length() < LONG_BIT:
            return wrap_int(bn.toint())
        else:
            return wrap_bigint(bn)
    else:
        assert False, "TODO: implement other number types"

    return None

def read_number(r, initch):
    sb = [initch]

    while True:
        ch = r.read()
        if ch == "" or is_whitespace(ch) or ch in macros:
            r.unread(ch)
            break
        sb.append(ch)

    s = "".join(sb)
    n = match_number(s)
    if n is None:
        raise ValueError("Invalid Number: " + s)

    return n



class MacroReader(object):
    def invoke(self, r, ch):
        pass

class ListReader(MacroReader):
    def invoke(self, r, leftparen):
        line = -1
        column = -1

        line = r.get_line_number()
        column = r.get_column_number() - 1
        list = read_delimited_list(")", r, True)

        s = create_list(list)
        ## TODO add meta
        return s

class UnmatchedDelimiterReader(MacroReader):
    def invoke(self, r, ch):
        raise SyntaxError("Unmatched delimiter: " + ch)


def read_delimited_list(delim, r, is_recursive):
    firstline = r.get_line_number()
    a = []

    while True:
        ch = r.read()
        while is_whitespace(ch):
            ch = r.read()

        if ch == "":
            raise ValueError("EOF while reading, starting at line " + str(firstline))

        if ch == delim:
            break

        macro = macros.get(ch, None)
        if macro is not None:
            mret = macro.invoke(r, ch)

            if mret is not None:
                a.append(mret)

        else:
            r.unread(ch)
            o = read(r, True, None, is_recursive)
            if o is not None:
                a.append(o)

    return a




macros = {"(": ListReader(),
          ")": UnmatchedDelimiterReader()}


import StringIO
def read_string(s):
    from pushback_reader import LineNumberingReader, StringReader
    io = StringReader(s)
    rdr = LineNumberingReader(io)

    return read(rdr, True, None, False)