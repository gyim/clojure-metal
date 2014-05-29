from clojure_metal.lang.symbol import intern
from clojure_metal.lang.namespace import namespaces


def test_namespace_creation():
    assert namespaces.find_or_create_namespace(intern("foo"))
    assert namespaces.find_or_create_namespace(intern("foo")) is namespaces.find_or_create_namespace(intern("foo"))
    assert namespaces.find_or_create_namespace(intern("foo")) is not namespaces.find_or_create_namespace(intern("bar"))

def test_create_vars():
    ns = namespaces.find_or_create_namespace(intern("foo"))
    assert ns.find_or_create_var(intern("bar"))