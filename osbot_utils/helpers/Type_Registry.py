class Type_Registry:

    def __init__(self):
        self.types = {}

    def register(self, type_key, type):
        self.types[type_key] = type

    def resolve(self, type_key):
        return self.types.get(type_key)

    def resolve_key(self, value):
        return value

type_registry = Type_Registry()

