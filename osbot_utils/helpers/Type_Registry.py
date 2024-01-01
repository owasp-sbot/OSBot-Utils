class Type_Registry:

    def __init__(self):
        self.types = {}

    def register(self, type_key, type):
        key = self.resolve_key(type_key)
        self.types[key] = type

    def resolve(self, type_key):
        key = self.resolve_key(type_key)
        return self.types.get(key)

    def resolve_key(self, value):
        return value
        #return str(value)               # todo: see if we need this

type_registry = Type_Registry()