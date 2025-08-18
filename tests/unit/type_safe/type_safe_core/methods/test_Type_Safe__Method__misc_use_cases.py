import pytest
import re
import unittest
from typing                                                         import List, Dict, Optional, Union, Any, Type, Callable, TypeVar, Generic
from dataclasses                                                    import dataclass
from enum                                                           import Enum
from osbot_utils.type_safe.type_safe_core.methods.Type_Safe__Method import Type_Safe__Method


# Test classes and types for integration testing
class Status(Enum):                                                                      # Example enum for testing
    ACTIVE   = "active"
    INACTIVE = "inactive"
    PENDING  = "pending"


@dataclass
class User:                                                                              # Example dataclass for testing
    id     : int
    name   : str
    email  : str
    status : Status = Status.ACTIVE


class ConfigBase: pass                                                                   # Base configuration class


class AppConfig(ConfigBase):                                                             # Application configuration
    def __init__(self, debug: bool = False):
        self.debug = debug


T = TypeVar('T')


class Container(Generic[T]):                                                             # Generic container for testing
    def __init__(self, items: List[T]):
        self.items = items


class test_Type_Safe__Method__misc_use_cases(unittest.TestCase):                             # Integration tests showing real-world usage of Type_Safe__Method

    def test_api_endpoint_validation(self):                                             # Test validation for a typical API endpoint function
        def create_user(name     : str                                     ,
                       email    : str                                      ,
                       age      : int                                      ,
                       roles    : List[str]                                ,
                       metadata : Optional[Dict[str, Any]] = None          ,
                       status   : Status                   = Status.PENDING
                  ) -> User:                                                            # Create a new user with validation
            return User(id     = 1    ,
                       name   = name ,
                       email  = email,
                       status = status)

        checker = Type_Safe__Method(create_user)

        # Valid request
        bound_args = checker.handle_type_safety(("John Doe", "john@example.com", 30, ["user", "admin"]),
                                                {"metadata": {"source": "api"}, "status": Status.ACTIVE})

        user = create_user(**bound_args.arguments)
        assert user.name   == "John Doe"
        assert user.status == Status.ACTIVE

        # Invalid age type
        with self.assertRaises(ValueError) as context:
            checker.handle_type_safety(("John Doe", "john@example.com", "thirty", ["user"]), {} )
        assert "Parameter 'age' expected type" in str(context.exception)

    def test_configuration_validation(self):                                             # Test validation for configuration loading
        def load_config(config_path  : str                                ,
                       environment  : str                                 ,
                       overrides    : Optional[Dict[str, Any]] = None     ,
                       validate     : bool                     = True     ,
                       config_class : Type[ConfigBase]         = AppConfig
                      ) -> ConfigBase:                                                   # Load configuration with type validation
            return config_class()

        checker = Type_Safe__Method(load_config)

        # Valid configuration
        bound_args = checker.handle_type_safety(("config.yml", "production"),
                                                { "overrides"   : {"debug": False}, "config_class": AppConfig })

        config = load_config(**bound_args.arguments)
        assert isinstance(config, AppConfig)

        # Invalid config class (not subclass of ConfigBase)
        with self.assertRaises(ValueError):
            checker.handle_type_safety(
                ("config.yml", "production"),
                {"config_class": str}                                                    # str is not a subclass of ConfigBase
            )

    def test_data_processing_pipeline__checks_not_implemented_error(self):                                             # Test validation for data processing functions
        def process_data(data            : List[Dict[str, Union[str, int, float]]],
                         transformations : List[Callable[[Any], Any]]        ,
                         options         : Dict[str, Any]                    ,
                         output_format   : str                        = "json"
                    ) -> List[Dict[str, Any]]:                                        # Process data through transformation pipeline
            result = data
            for transform in transformations:
                result = [transform(item) for item in result]
            return result

        checker = Type_Safe__Method(process_data)

        # Define transformations
        def uppercase_strings(item):
            return {k: v.upper() if isinstance(v, str) else v
                   for k, v in item.items()}

        def multiply_numbers(item):
            return {k: v * 2 if isinstance(v, (int, float)) else v
                   for k, v in item.items()}

        # Valid pipeline
        test_data = [ {"name": "alice", "score": 10, "rate": 0.5},
                      {"name": "bob"  , "score": 20, "rate": 0.8}]

        expected_error = "Validation for list items with subscripted type 'typing.Callable[[typing.Any], typing.Any]' is not yet supported in parameter 'transformations'."
        with pytest.raises(NotImplementedError, match=re.escape(expected_error)):
            checker.handle_type_safety((test_data, [uppercase_strings, multiply_numbers], {"debug": True}),{})
        # todo: should we add this as a bug?

        # result = process_data(**bound_args.arguments)
        # assert result[0]["name"]  == "ALICE"
        # assert result[0]["score"] == 20

    def test_database_query_builder(self):                                               # Test validation for a database query builder
        def build_query(table      : str                           ,
                       columns    : List[str]                      ,
                       conditions : Optional[Dict[str, Any]] = None,
                       joins      : Optional[List[Dict[str, str]]] = None ,
                       order_by   : Optional[List[Union[str, tuple]]] = None,
                       limit      : Optional[int]                     = None
                      ) -> str:                                                          # Build SQL query with type validation
            query = f"SELECT {', '.join(columns)} FROM {table}"
            if conditions:
                where  = " AND ".join(f"{k} = {v}" for k, v in conditions.items())
                query += f" WHERE {where}"
            if limit:
                query += f" LIMIT {limit}"
            return query

        checker = Type_Safe__Method(build_query)

        # Valid query
        bound_args = checker.handle_type_safety(
            ("users", ["id", "name", "email"]),
            { "conditions": {"status": "active"},
              "limit"     : 10                 }
        )

        query = build_query(**bound_args.arguments)
        assert "SELECT id, name, email" in query
        assert "LIMIT 10"               in query

        # Invalid columns type
        with self.assertRaises(ValueError):
            checker.handle_type_safety(
                ("users", "id, name"),                                                   # Should be list, not string
                {}
            )

    def test_generic_container_validation(self):                                         # Test validation with generic types
        def create_container(items          : List[int]           ,
                           container_type : Type[Container] = Container
                          ) -> Container[int]:                                           # Create a generic container
            return container_type(items)

        checker = Type_Safe__Method(create_container)

        # Valid container creation
        bound_args = checker.handle_type_safety(
            ([1, 2, 3, 4, 5],),
            {}
        )

        container = create_container(**bound_args.arguments)
        assert container.items == [1, 2, 3, 4, 5]

    def test_decorator_pattern(self):                                                    # Test using Type_Safe__Method as a decorator
        def type_safe(func):                                                             # Decorator to add type safety to functions
            checker = Type_Safe__Method(func)

            def wrapper(*args, **kwargs):
                bound_args = checker.handle_type_safety(args, kwargs)
                return func(**bound_args.arguments)

            return wrapper

        @type_safe
        def calculate_discount(price            : float       ,
                             discount_percent : float       ,
                             min_price        : float = 0.0
                            ) -> float:                                                  # Calculate discounted price
            discounted = price * (1 - discount_percent / 100)
            return max(discounted, min_price)

        # Valid calculation
        result = calculate_discount(100.0, 20.0)
        assert result == 80.0

        # Invalid type should raise
        with self.assertRaises(ValueError):
            calculate_discount("100", 20.0)

    def test_async_function_validation(self):                                            # Test validation with async functions
        async def fetch_data(url         : str                           ,
                           headers     : Optional[Dict[str, str]] = None ,
                           timeout     : float                    = 30.0 ,
                           retry_count : int                      = 3
                          ) -> Dict[str, Any]:                                           # Async function with type validation
            return {"url": url, "success": True}

        checker = Type_Safe__Method(fetch_data)

        # Validate async function parameters
        bound_args = checker.handle_type_safety(
            ("https://api.example.com",),
            { "headers": {"Authorization": "Bearer token"},
              "timeout": 10.0                             }
        )

        assert bound_args.arguments["url"]     == "https://api.example.com"
        assert bound_args.arguments["timeout"] == 10.0

    def test_complex_nested_validation__raises__not_implemented_error(self):                                            # Test deeply nested type validation
        def process_nested_data(data            : Dict[str, List[Dict[str, Union[int, str, List[float]]]]],
                               transformations : Optional[Dict[str, Callable]]                       = None
                              ) -> Dict[str, Any]:                                       # Process deeply nested data structures
            return {"processed": True}

        checker = Type_Safe__Method(process_nested_data)

        # Valid nested structure
        test_data = { "section1": [ {"id": 1, "name": "test" , "values": [1.0, 2.0, 3.0]},
                                   {"id": 2, "name": "test2", "values": [4.0, 5.0]}     ],
                     "section2": [ {"id": 3, "name": "test3", "values": []}             ]}

        expected_error = "Validation for subscripted value type 'typing.List[typing.Dict[str, typing.Union[int, str, typing.List[float]]]]' not yet supported in parameter 'data'"
        with pytest.raises(NotImplementedError, match=re.escape(expected_error)):
            bound_args = checker.handle_type_safety((test_data,), {})
            # result     = process_nested_data(**bound_args.arguments)
            # assert result["processed"] == True

            # # Invalid nested structure
            # invalid_data = { "section1": [ {"id": "not_an_int", "name": "test", "values": [1.0]}]}
            #
            # with self.assertRaises(ValueError):
            #     checker.handle_type_safety((invalid_data,), {})

    def test_multiple_inheritance_validation(self):                                      # Test validation with multiple inheritance
        class Serializable:
            def to_dict(self): pass

        class Timestamped:
            def get_timestamp(self): pass

        class Document(Serializable, Timestamped):
            pass

        def process_document(doc      : Document             ,
                           doc_type : Type[Document] = Document
                          ) -> Dict[str, Any]:                                           # Process a document with multiple inheritance
            return {"type": doc_type.__name__}

        checker = Type_Safe__Method(process_document)

        # Valid document
        doc        = Document()
        bound_args = checker.handle_type_safety((doc,), {})
        result     = process_document(**bound_args.arguments)
        assert result["type"] == "Document"

    def test_error_aggregation(self):                                                    # Test collecting multiple validation errors
        def complex_validation(numbers : List[int]      ,
                              names   : List[str]      ,
                              mapping : Dict[str, float],
                              config  : Dict[str, Any]
                         ) -> None:                                                   # Function with multiple parameters to validate
            pass

        checker = Type_Safe__Method(complex_validation)

        # Multiple invalid parameters
        errors = []
        params = [ (["not", "ints"], []        , {}         , {}),                      # Invalid numbers
                   ([1, 2]        , [1, 2, 3]  , {}         , {}),                      # Invalid names
                   ([1, 2]        , ["a", "b"] , {"k": "v"} , {})]                      # Invalid mapping

        for args in params:
            try:
                checker.handle_type_safety(args, {})
            except ValueError as e:
                errors.append(str(e))

        # Should have caught all three errors
        assert len(errors)    == 3
        assert errors == [ "List item at index 0 expected type <class 'int'>, but got <class 'str'>",
                           "List item at index 0 expected type <class 'str'>, but got <class 'int'>",
                           "Dict value for key 'k' expected type <class 'float'>, but got <class 'str'>"]


    def test_runtime_type_modification(self):                                            # Test behavior when types are modified at runtime
        class DynamicClass:
            pass

        def dynamic_func(obj: DynamicClass) -> None:
            pass

        checker = Type_Safe__Method(dynamic_func)

        # Initial validation
        obj        = DynamicClass()
        bound_args = checker.handle_type_safety((obj,), {})

        # Even if we modify the class, existing instances should validate
        DynamicClass.new_attribute = "added"
        bound_args                 = checker.handle_type_safety((obj,), {})

        # New instances should also work
        new_obj    = DynamicClass()
        bound_args = checker.handle_type_safety((new_obj,), {})