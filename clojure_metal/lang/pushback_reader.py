
class StringReader(object):
    def __init__(self, s):
        self._idx = 0
        self._s = s
    def read(self):
        if self._idx < len(self._s):
            c = self._s[self._idx]
            self._idx += 1
            return c
        return ""


class PushbackReader(object):
    def __init__(self, stream):
        self._stream = stream
        self._has_unread = False

    def read(self):
        if self._has_unread:
            ret = self._unread_char
            self._has_unread = False
        else:
            ret = self._stream.read()

        return ret

    def unread(self, ch):
        assert not self._has_unread

        self._unread_char = ch
        self._has_unread = True


class LineNumberingReader(PushbackReader):
    def __init__(self, stream):
        PushbackReader.__init__(self, stream)
        self._lineNumber = 1
        self._prevColumnNumber = 0
        self._columnNumber = 0
        self._prevLineStart = True
        self._atLineStart = True
        self._index = 0

    def read(self):
        ret = PushbackReader.read(self)

        self._prevLineStart = self._atLineStart

        if ret == "":
            self._atLineStart = True
            return ret

        self._index += 1
        self._atLineStart = False
        self._columnNumber += 1

        if ret == '\n':
            self.note_line_advance()

        return ret

    def note_line_advance(self):
        self._atLineStart = True
        self._lineNumber += 1
        self._prevColumnNumber = self._columnNumber - 1
        self._columnNumber = 0

    def unread(self, ch):
        PushbackReader.unread(self, ch)
        self._index -= 1
        self._columnNumber -= 1
        if ch == '\n':
            self._lineNumber -= 1
            self._columnNumber = self._prevColumnNumber
            self._atLineStart = self._prevLineStart

    def get_line_number(self):
        return self._lineNumber

    def get_column_number(self):
        return self._columnNumber
