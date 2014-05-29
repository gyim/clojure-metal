from base_types import Object, id_gen, nil
from string import String
from symbol import Symbol
import util as UT

class Namespace(Object):
    _type = id_gen.next_id()
    def type(self):
        return Namespace._type

    def __init__(self, name):
        assert isinstance(name, Symbol)
        self._name = name
        self._vars = {}

    def _str_for_name(self, name):
        assert isinstance(name, Symbol)
        return UT.name(name)._str_value

    def find_var(self, name):
        assert isinstance(name, Symbol)
        if UT.namespace(name) is not nil:
            raise ValueError("Var names cannot have namespaces")

        return self._vars.get(name, self._str_for_name(name))

    def find_or_create_var(self, name):
        assert isinstance(name, Symbol)
        var = self.find_var(name)
        if var is not None:
            return var

        sname = self._str_for_name(name)
        var = Var(name)
        self._vars[sname] = var

        return var

class Var(Object):
    _type = id_gen.next_id()
    def type(self):
        return Var._type

    def __init__(self, sym):
        self._sym = sym
        self._root = None


class NamespaceRegistry(object):
    def __init__(self):
        self._namespaces = {}

    def _str_for_name(self, name):
        assert isinstance(name, Symbol)
        return UT.name(name)._str_value

    def find_namespace(self, name):
        assert isinstance(name, Symbol)
        if UT.namespace(name) is not nil:
            raise ValueError("Namespace names cannot have namespaces")

        return self._namespaces.get(self._str_for_name(name), None)

    def find_or_create_namespace(self, name):
        assert isinstance(name, Symbol)
        ns = self.find_namespace(name)
        if ns is not None:
            return ns

        sname = self._str_for_name(name)
        ns = Namespace(name)
        self._namespaces[sname] = ns

        return ns


namespaces = NamespaceRegistry()
