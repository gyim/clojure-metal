

class Object(object):
    def type(self):
        assert False

class TypeIDGen(object):
    def __init__(self):
        self.curr_id = 1
    def next_id(self):
        self.curr_id += 1
        return self.curr_id



id_gen = TypeIDGen()

class Nil(Object):
    _type = id_gen.next_id()
    def type(self):
        return Nil._type

nil = Nil()

class Bool(Object):
    _type = id_gen.next_id()
    def type(self):
        return Bool._type

    def __init__(self, is_true):
        self.is_true = is_true

false = Bool(False)
true = Bool(True)
