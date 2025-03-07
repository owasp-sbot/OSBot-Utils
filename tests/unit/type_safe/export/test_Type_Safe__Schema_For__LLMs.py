from typing                                                     import List, Dict, Optional, Union, Tuple, Set, Any
from unittest                                                   import TestCase
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from osbot_utils.type_safe.export.Type_Safe__Schema_For__LLMs   import Type_Safe__Schema_For__LLMs
from osbot_utils.type_safe.validators.Validator__Min            import Min
from osbot_utils.type_safe.validators.Validator__Max            import Max
from osbot_utils.type_safe.validators.Validator__Regex          import Regex
from osbot_utils.type_safe.validators.Validator__One_Of         import One_Of
from osbot_utils.helpers.python_compatibility.python_3_8        import Annotated
from osbot_utils.utils.Dev                                      import pprint


class test_Enhanced_Type_Safe__Schema_For__LLMs(TestCase):

    @classmethod
    def setUpClass(cls):

        cls.schema_for_llms = Type_Safe__Schema_For__LLMs()                                 # Initialize the schema generator

    def test_primitive_types(self):                                                         # Test schema generation for primitive types.

        class PrimitiveTypesClass(Type_Safe):
            """A class with primitive type attributes. (and a description)"""
            string_field: str           # A simple string field
            int_field   : int           # An integer field
            float_field : float         # A floating point number
            bool_field  : bool          # A boolean field

        schema = self.schema_for_llms.export(PrimitiveTypesClass)


        assert schema["type"] == "object"                                                   # Verify the schema
        assert "properties"   in schema

        properties = schema["properties"]
        assert properties["string_field"]["type"] == "string"
        assert properties["int_field"   ]["type"] == "integer"
        assert properties["float_field" ]["type"] == "number"
        assert properties["bool_field"  ]["type"] == "boolean"

        # Verify descriptions are included
        assert "description" in properties["string_field"]
        assert "A simple string field" in properties["string_field"]["description"]
        assert schema == { 'description': 'A class with primitive type attributes. (and a description)',
                           'properties' : { 'bool_field' : { 'description': 'A boolean field'        ,
                                                              'type'      : 'boolean'                },
                                           'float_field' : { 'description': 'A floating point number',
                                                            'type'       : 'number'                  },
                                           'int_field'   : { 'description': 'An integer field'       ,
                                                             'type'        : 'integer'               },
                                           'string_field': { 'description': 'A simple string field'  ,
                                                             'type'       : 'string'                 }},
                           'required'  : ['string_field', 'int_field', 'float_field', 'bool_field'],
                           'title'     : 'PrimitiveTypesClass'  ,
                           'type'      : 'object'               }

    def test_container_types(self):                             # Test schema generation for container types.

        class ContainerTypesClass(Type_Safe):
            """A class with container type attributes."""

            string_list     : List [str           ]             # A list of strings
            int_dict        : Dict [str, int      ]             # A dictionary with string keys and int values
            mixed_tuple     : Tuple[str, int, bool]             # A tuple with different types
            unique_strings  : Set  [str           ]             # A set of unique strings

        schema = self.schema_for_llms.export(ContainerTypesClass)

        # Verify list
        assert schema["properties"]["string_list"]["type"] == "array"
        assert schema["properties"]["string_list"]["items"]["type"] == "string"

        # Verify dict
        assert schema["properties"]["int_dict"]["type"] == "object"
        assert schema["properties"]["int_dict"]["additionalProperties"]["type"] == "integer"

        # Verify tuple
        assert schema["properties"]["mixed_tuple"]["type"] == "array"
        assert len(schema["properties"]["mixed_tuple"]["items"]) == 3
        assert schema["properties"]["mixed_tuple"]["items"][0]["type"] == "string"
        assert schema["properties"]["mixed_tuple"]["items"][1]["type"] == "integer"
        assert schema["properties"]["mixed_tuple"]["items"][2]["type"] == "boolean"

        # Verify set
        assert schema["properties"]["unique_strings"]["type"] == "array"
        assert schema["properties"]["unique_strings"]["items"]["type"] == "string"
        assert schema["properties"]["unique_strings"]["uniqueItems"] is True

        assert schema == { 'description': 'A class with container type attributes.',
                           'properties': { 'int_dict': { 'additionalProperties': {'type': 'integer'},
                                                         'description': 'A dictionary with string keys '
                                                                        'and int values',
                                                         'type': 'object'},
                                           'mixed_tuple': { 'description': 'A tuple with different '
                                                                           'types',
                                                            'items': [ {'type': 'string'},
                                                                       {'type': 'integer'},
                                                                       {'type': 'boolean'}],
                                                            'maxItems': 3,
                                                            'minItems': 3,
                                                            'type': 'array'},
                                           'string_list': { 'description': 'A list of strings',
                                                            'items': {'type': 'string'},
                                                            'type': 'array'},
                                           'unique_strings': { 'description': 'A set of unique strings',
                                                               'items': {'type': 'string'},
                                                               'type': 'array',
                                                               'uniqueItems': True}},
                           'required': ['string_list', 'int_dict', 'mixed_tuple', 'unique_strings'],
                           'title': 'ContainerTypesClass',
                           'type': 'object'}

    def test_optional_types(self):                                  # Test schema generation for optional types."""

        class OptionalTypesClass(Type_Safe):
            """A class with optional fields."""

            required_field: str                      # Required string field
            optional_field: Optional[int] = None     # Optional int field with default
            union_field: Union[str, int]             # Field that can be string or int

        schema = self.schema_for_llms.export(OptionalTypesClass)

        # Verify required field
        assert "required" in schema
        assert "required_field" in schema["required"]

        # Verify optional field
        assert "optional_field" not in schema["required"]
        assert schema["properties"]["optional_field"]["type"] == ["integer", "null"]

        # Verify union field
        assert "anyOf" in schema["properties"]["union_field"]
        assert len(schema["properties"]["union_field"]["anyOf"]) == 2

        assert schema == { 'description': 'A class with optional fields.',
                           'properties': { 'optional_field': { 'description': 'Optional int field with '
                                                                              'default',
                                                               'type': ['integer', 'null']},
                                           'required_field': { 'description': 'Required string field',
                                                               'type': 'string'},
                                           'union_field': { 'anyOf': [ {'type': 'string'},
                                                                       {'type': 'integer'}],
                                                            'description': 'Field that can be string or '
                                                                           'int'}},
                           'required': ['required_field', 'union_field'],
                           'title': 'OptionalTypesClass',
                           'type': 'object'}


    def test_nested_objects(self):      # Test schema generation for nested Type_Safe objects.

        class AddressClass(Type_Safe):
            """An address representation."""

            street: str
            city: str
            postal_code: str

        class PersonClass(Type_Safe):
            """A person with an address."""

            name: str
            age: int
            address: AddressClass

        schema = self.schema_for_llms.export(PersonClass)

        # Verify nested object
        assert schema["properties"]["address"]["type"] == "object"
        assert "properties" in schema["properties"]["address"]
        assert "street" in schema["properties"]["address"]["properties"]
        assert "city" in schema["properties"]["address"]["properties"]
        assert "postal_code" in schema["properties"]["address"]["properties"]

        assert schema == { 'description': 'A person with an address.',
                           'properties': { 'address': { 'description': 'An address representation.',
                                                        'properties': { 'city': {'type': 'string'},
                                                                        'postal_code': { 'type': 'string'},
                                                                        'street': {'type': 'string'}},
                                                        'required': ['street', 'city', 'postal_code'],
                                                        'title': 'AddressClass',
                                                        'type': 'object'},
                                           'age': {'type': 'integer'},
                                           'name': {'type': 'string'}},
                           'required': ['name', 'age', 'address'],
                           'title': 'PersonClass',
                           'type': 'object'}

    def test_validators(self):  # Test schema generation with validators."""

        class ValidatedClass(Type_Safe):
            """A class with validated fields."""

            # A string with minimum length 2 and maximum length 50
            username: Annotated[str, Min(2), Max(50)]

            # An integer between 0 and 100
            score: Annotated[int, Min(0), Max(100)]

            # A string matching a regex pattern
            email: Annotated[str, Regex(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                                       "Valid email address")]

            # A field with enumerated values
            status: Annotated[str, One_Of(["active", "inactive", "pending"])]

        schema = self.schema_for_llms.export(ValidatedClass)

        # Verify string validators
        assert schema["properties"]["username"]["minLength"] == 2
        assert schema["properties"]["username"]["maxLength"] == 50

        # Verify number validators
        assert schema["properties"]["score"]["minimum"] == 0
        assert schema["properties"]["score"]["maximum"] == 100

        # Verify regex validator
        assert "pattern" in schema["properties"]["email"]

        # Verify enum validator
        assert "enum" in schema["properties"]["status"]
        assert schema["properties"]["status"]["enum"] == ["active", "inactive", "pending"]

        assert schema == { 'description': 'A class with validated fields.',
                           'properties': { 'email': { 'description': 'Valid email address',
                                                      'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$',
                                                      'type': 'string'},
                                           'score': {'maximum': 100, 'minimum': 0, 'type': 'integer'},
                                           'status': { 'enum': ['active', 'inactive', 'pending'],
                                                       'type': 'string'},
                                           'username': { 'maxLength': 50,
                                                         'minLength': 2,
                                                         'type': 'string'}},
                           'required': ['username', 'score', 'email', 'status'],
                           'title': 'ValidatedClass',
                           'type': 'object'}

    def test_complex_structure(self):           # Test schema generation for a complex structure similar to the target example."""

        class RelationshipClass(Type_Safe):
            """Represents a relationship to another entity."""

            entity: str
            relationship_type: str
            strength: Annotated[float, Min(0), Max(1)]

        class DomainRelationshipClass(Type_Safe):
            """Represents a relationship to a domain concept."""

            concept: str
            relationship_type: str
            category: str
            strength: Annotated[float, Min(0), Max(1)]

        class EcosystemClass(Type_Safe):
            """Represents related ecosystem elements."""

            platforms: List[str]
            standards: List[str]
            technologies: List[str]

        class EntityClass(Type_Safe):
            """Represents an entity with relationships and properties."""
            name                : str                               # Core entity name
            primary_domains     : List[str]                         # Main domains this entity belongs to
            functional_roles    : List[str]                         # Specific functions/purposes
            ecosystem           : EcosystemClass                    # Related platforms, standards and technologies
            direct_relationships: List[RelationshipClass]           # Relationships with other entities
            domain_relationships: List[DomainRelationshipClass]     # Related concepts
            confidence          : Annotated[float, Min(0), Max(1)]  # Confidence level

        schema = self.schema_for_llms.export(EntityClass)

        # Verify overall structure
        assert schema["type"] == "object"
        assert len(schema["properties"]) == 7

        # Verify nested objects and arrays
        assert schema["properties"]["ecosystem"]["type"] == "object"
        assert schema["properties"]["direct_relationships"]["type"] == "array"
        assert schema["properties"]["direct_relationships"]["items"]["type"] == "object"

        # Verify all required fields
        assert set(schema["required"]) == {
            "name", "primary_domains", "functional_roles",
            "ecosystem", "direct_relationships", "domain_relationships", "confidence"
        }

        assert schema == { 'description': 'Represents an entity with relationships and properties.',
                           'properties': { 'confidence': { 'description': 'Confidence level',
                                                           'maximum': 1,
                                                           'minimum': 0,
                                                           'type': 'number'},
                                           'direct_relationships': { 'description': 'Relationships with '
                                                                                   'other entities',
                                                                    'items': { 'description': 'Represents '
                                                                                              'a '
                                                                                              'relationship '
                                                                                              'to '
                                                                                              'another '
                                                                                              'entity.',
                                                                               'properties': { 'entity': { 'type': 'string'},
                                                                                               'relationship_type': { 'type': 'string'},
                                                                                               'strength': { 'maximum': 1,
                                                                                                             'minimum': 0,
                                                                                                             'type': 'number'}},
                                                                               'required': [ 'entity',
                                                                                             'relationship_type',
                                                                                             'strength'],
                                                                               'title': 'RelationshipClass',
                                                                               'type': 'object'},
                                                                    'type': 'array'},
                                          'domain_relationships': { 'description': 'Related concepts',
                                                                    'items': { 'description': 'Represents '
                                                                                              'a '
                                                                                              'relationship '
                                                                                              'to a '
                                                                                              'domain '
                                                                                              'concept.',
                                                                               'properties': { 'category': { 'type': 'string'},
                                                                                               'concept': { 'type': 'string'},
                                                                                               'relationship_type': { 'type': 'string'},
                                                                                               'strength': { 'maximum': 1,
                                                                                                             'minimum': 0,
                                                                                                             'type': 'number'}},
                                                                               'required': [ 'concept',
                                                                                             'relationship_type',
                                                                                             'category',
                                                                                             'strength'],
                                                                               'title': 'DomainRelationshipClass',
                                                                               'type': 'object'},
                                                                    'type': 'array'},
                                          'ecosystem': { 'description': 'Related platforms, standards '
                                                                        'and technologies',
                                                         'properties': { 'platforms': { 'items': { 'type': 'string'},
                                                                                        'type': 'array'},
                                                                         'standards': { 'items': { 'type': 'string'},
                                                                                        'type': 'array'},
                                                                         'technologies': { 'items': { 'type': 'string'},
                                                                                           'type': 'array'}},
                                                         'required': [ 'platforms',
                                                                       'standards',
                                                                       'technologies'],
                                                         'title': 'EcosystemClass',
                                                         'type': 'object'},
                                          'functional_roles': { 'description': 'Specific '
                                                                               'functions/purposes',
                                                                'items': {'type': 'string'},
                                                                'type': 'array'},
                                          'name': {'description': 'Core entity name', 'type': 'string'},
                                          'primary_domains': { 'description': 'Main domains this '
                                                                              'entity belongs to',
                                                               'items': {'type': 'string'},
                                                               'type': 'array'}},
                          'required': [ 'name',
                                        'primary_domains',
                                        'functional_roles',
                                        'ecosystem',
                                        'direct_relationships',
                                        'domain_relationships',
                                        'confidence'],
                          'title': 'EntityClass',
                          'type': 'object'}