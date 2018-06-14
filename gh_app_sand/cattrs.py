import attr
import cattr

def _register_ignore_unknown_attribs(cls, converter=None):
    if converter is None:
        converter = cattr.global_converter

    if not attr.has(cls):
        raise TypeError("class does not have attrs: %s" % cls)

    prev_structure = converter._structure_func.dispatch(cls)

    def structure_ignoring_unknown(obj, cls):
        obj = obj.copy()
        attr_names = {f.name for f in attr.fields(cls)}
        for k in set(obj.keys()).difference(attr_names):
            del obj[k]
        return prev_structure(obj, cls)

    converter.register_structure_hook(cls, structure_ignoring_unknown)

def ignore_unknown_attribs(maybe_cls = None, converter=None):
    """Register a "tolerant" cattr.structure overload for the classk."""
    def bound(cls):
        _register_ignore_unknown_attribs(cls, converter = converter)
        return cls

    if maybe_cls:
        return bound(maybe_cls)
    else:
        return bound

