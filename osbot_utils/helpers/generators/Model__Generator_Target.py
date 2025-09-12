from types                                                  import GeneratorType
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                        import Random_Guid
from osbot_utils.helpers.generators.Model__Generator_State  import Model__Generator_State


class Model__Generator_Target(Type_Safe):                                   # Class representing a generator target and its metadata
    target_id : Random_Guid                                                 # Unique ID for the generator target
    target    : GeneratorType          = None                               # The generator instance being managed
    state     : Model__Generator_State = Model__Generator_State.CREATED     # Current state of the generator (default is CREATED)