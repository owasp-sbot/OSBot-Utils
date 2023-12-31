# todo add tests
def obj_base_classes(obj):
    return type_base_classes(type(obj))

def type_base_classes(cls):
    base_classes = cls.__bases__
    all_base_classes = list(base_classes)
    for base in base_classes:
        all_base_classes.extend(type_base_classes(base))
    return all_base_classes

def obj_base_classes_names(obj, show_module=False):
    names = []
    for base in obj_base_classes(obj):
        if show_module:
            names.append(base.__module__ + '.' + base.__name__)
        else:
            names.append(base.__name__)
    return names
