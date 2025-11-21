import pytest
import re
import unittest
from typing                                                         import List, Dict, Optional, Union, Any, Type, Callable, TypeVar, Generic, Tuple, Set
from dataclasses                                                    import dataclass
from enum                                                           import Enum
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
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

        checker = Type_Safe__Method(create_user).setup()

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

        checker = Type_Safe__Method(load_config).setup()

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

        checker = Type_Safe__Method(build_query).setup()

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

        checker = Type_Safe__Method(create_container).setup()

        # Valid container creation
        bound_args = checker.handle_type_safety(
            ([1, 2, 3, 4, 5],),
            {}
        )

        container = create_container(**bound_args.arguments)
        assert container.items == [1, 2, 3, 4, 5]

    def test_decorator_pattern(self):                                                    # Test using Type_Safe__Method as a decorator
        def type_safe(func):                                                             # Decorator to add type safety to functions
            checker = Type_Safe__Method(func).setup()

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

        checker = Type_Safe__Method(fetch_data).setup()

        # Validate async function parameters
        bound_args = checker.handle_type_safety(
            ("https://api.example.com",),
            { "headers": {"Authorization": "Bearer token"},
              "timeout": 10.0                             }
        )

        assert bound_args.arguments["url"]     == "https://api.example.com"
        assert bound_args.arguments["timeout"] == 10.0

    def test__bug__complex_nested_validation__raises__not_implemented_error(self):                                            # Test deeply nested type validation
        def process_nested_data(data            : Dict[str, List[Dict[str, Union[int, str, List[float]]]]],
                               transformations : Optional[Dict[str, Callable]]                       = None
                              ) -> Dict[str, Any]:                                       # Process deeply nested data structures
            return {"processed": True}

        checker = Type_Safe__Method(process_nested_data).setup()

        # Valid nested structure
        test_data = { "section1": [ {"id": 1, "name": "test" , "values": [1.0, 2.0, 3.0]},
                                   {"id": 2, "name": "test2", "values": [4.0, 5.0]}     ],
                     "section2": [ {"id": 3, "name": "test3", "values": []}             ]}

        # expected_error = "Validation for subscripted value type 'typing.List[typing.Dict[str, typing.Union[int, str, typing.List[float]]]]' not yet supported in parameter 'data'"
        # with pytest.raises(NotImplementedError, match=re.escape(expected_error)):
        #     bound_args = checker.handle_type_safety((test_data,), {})         # BUG
        bound_args = checker.handle_type_safety((test_data,), {})               # FIXED
        result     = process_nested_data(**bound_args.arguments)
        assert result["processed"] == True

    def test_nested_dict_validation__simple(self):
        """Test validation of Dict[str, List[int]]"""
        def process_data(data: Dict[str, List[int]]) -> int:
            return sum(sum(v) for v in data.values())

        checker = Type_Safe__Method(process_data).setup()

        # Valid nested structure
        test_data = {"a": [1, 2, 3], "b": [4, 5]}
        bound_args = checker.handle_type_safety((test_data,), {})
        result = process_data(**bound_args.arguments)
        assert result == 15

        # Invalid: string instead of list
        with pytest.raises(ValueError, match=re.escape("Dict value for key 'a' in parameter 'data': Expected 'list[int]', but got 'str'")):
            checker.handle_type_safety(({"a": "not a list"},), {})

        # Invalid: list contains wrong type
        with pytest.raises(ValueError, match=re.escape(
            "In list at index 1: Expected 'int', but got 'str'"
        )):
            checker.handle_type_safety(({"a": [1, "two", 3]},), {})


    def test_nested_dict_validation__with_type_safe_classes(self):
        """Test validation of Dict[str, CustomClass]"""
        from osbot_utils.type_safe.Type_Safe import Type_Safe

        class Person(Type_Safe):
            name: str
            age: int

        def process_people(people: Dict[str, Person]) -> List[str]:
            return [p.name for p in people.values()]

        checker = Type_Safe__Method(process_people).setup()

        # Valid: Type_Safe instances
        john = Person(name="John", age=30)
        jane = Person(name="Jane", age=25)
        bound_args = checker.handle_type_safety(({"john": john, "jane": jane},), {})
        result = process_people(**bound_args.arguments)
        assert result == ["John", "Jane"]

        # Invalid: string instead of Person
        with pytest.raises(ValueError, match=re.escape(
            "Dict value for key 'john' in parameter 'people': Expected 'Person', but got 'str'"
        )):
            checker.handle_type_safety(({"john": "not a person"},), {})


    def test_nested_dict_validation__three_levels_deep(self):
        """Test validation of Dict[str, Dict[str, List[int]]]"""
        def process_nested(data: Dict[str, Dict[str, List[int]]]) -> int:
            total = 0
            for outer_dict in data.values():
                for inner_list in outer_dict.values():
                    total += sum(inner_list)
            return total

        checker = Type_Safe__Method(process_nested).setup()

        # Valid three-level structure
        test_data = {
            "section1": {"a": [1, 2], "b": [3, 4]},
            "section2": {"c": [5, 6], "d": [7, 8]}
        }
        bound_args = checker.handle_type_safety((test_data,), {})
        result = process_nested(**bound_args.arguments)
        assert result == 36

        # Invalid at level 2: list instead of dict
        with pytest.raises(ValueError, match=re.escape("Dict value for key 'section1' in parameter 'data': Expected 'dict[str, list[int]]', but got 'list'")):
            checker.handle_type_safety(({"section1": [1, 2, 3]},), {})

        # Invalid at level 3: string in list
        with pytest.raises(ValueError, match=re.escape(
            "In list at index 0: Expected 'int', but got 'str'"
        )):
            checker.handle_type_safety(({
                "section1": {"a": ["wrong", 2]}
            },), {})


    def test_nested_dict_validation__with_unions(self):
        """Test validation of Dict[str, Union[int, str, List[float]]]"""
        def process_mixed(data: Dict[str, Union[int, str, List[float]]]) -> Dict[str, str]:
            result = {}
            for k, v in data.items():
                if isinstance(v, list):
                    result[k] = f"list of {len(v)} items"
                else:
                    result[k] = str(v)
            return result

        checker = Type_Safe__Method(process_mixed).setup()

        # Valid mixed types
        test_data = {
            "count": 42,
            "name": "test",
            "values": [1.0, 2.0, 3.0]
        }
        bound_args = checker.handle_type_safety((test_data,), {})
        result = process_mixed(**bound_args.arguments)
        assert result == {
            "count": "42",
            "name": "test",
            "values": "list of 3 items"
        }

        # Invalid: dict not in union
        with pytest.raises(ValueError, match=re.escape(
            "Dict value for key 'invalid' in parameter 'data': Expected 'Union[int, str, list[float]]', but got 'dict'"
        )):
            checker.handle_type_safety(({"invalid": {"nested": "dict"}},), {})


    def test_nested_dict_validation__with_optional(self):
        """Test validation of Dict[str, Optional[List[int]]]"""
        def process_optional(data: Dict[str, Optional[List[int]]]) -> int:
            return sum(sum(v) for v in data.values() if v is not None)

        checker = Type_Safe__Method(process_optional).setup()

        # Valid with None values
        test_data = {"a": [1, 2, 3], "b": None, "c": [4, 5]}
        bound_args = checker.handle_type_safety((test_data,), {})
        result = process_optional(**bound_args.arguments)
        assert result == 15

        # Invalid: string instead of list or None
        with pytest.raises(ValueError, match=re.escape(
            "Dict value for key 'a' in parameter 'data': Expected 'Union[list[int], NoneType]', but got 'str'"
        )):
            checker.handle_type_safety(({"a": "not valid"},), {})


    def test_nested_dict_validation__error_shows_full_path(self):
        """Test that error messages show the complete path to the invalid value"""
        def process_data(data: Dict[str, List[Dict[str, int]]]) -> None:
            pass

        checker = Type_Safe__Method(process_data).setup()

        # Create deeply nested invalid data
        test_data = {
            "users": [
                {"id": 1, "count": 10},
                {"id": 2, "count": "invalid"}  # Wrong type here
            ]
        }

        # Error should show the path: dict key 'users' -> list index 1 -> dict key 'count'
        with pytest.raises(ValueError) as exc_info:
            checker.handle_type_safety((test_data,), {})

        error_msg = str(exc_info.value)
        # Should mention the parameter name
        assert "parameter 'data'" in error_msg
        # Should mention it's in a dict value
        assert "Dict value" in error_msg or "dict" in error_msg.lower()
        # Should mention the list index
        assert "index 1" in error_msg or "index" in error_msg


    def test_nested_dict_validation__with_tuples(self):
        """Test validation of Dict[str, Tuple[int, str, float]]"""
        def process_tuples(data: Dict[str, Tuple[int, str, float]]) -> List[str]:
            return [f"{v[1]}: {v[0]} ({v[2]})" for v in data.values()]

        checker = Type_Safe__Method(process_tuples).setup()

        # Valid tuples
        test_data = {
            "item1": (1, "first", 1.5),
            "item2": (2, "second", 2.5)
        }
        bound_args = checker.handle_type_safety((test_data,), {})
        result = process_tuples(**bound_args.arguments)
        assert result == ["first: 1 (1.5)", "second: 2 (2.5)"]

        # Invalid: wrong tuple length
        with pytest.raises(ValueError, match=re.escape(
            "Expected tuple of length 3, but got 2"
        )):
            checker.handle_type_safety(({"item1": (1, "missing_float")},), {})

        # Invalid: wrong type in tuple
        with pytest.raises(ValueError, match=re.escape(
            "In tuple at index 0: Expected 'int', but got 'str'"
        )):
            checker.handle_type_safety(({"item1": ("wrong", "second", 1.5)},), {})


    def test_nested_dict_validation__empty_collections(self):
        """Test that empty nested collections are valid"""
        def process_data(data: Dict[str, List[int]]) -> int:
            return len(data)

        checker = Type_Safe__Method(process_data).setup()

        # Empty dict is valid
        bound_args = checker.handle_type_safety(({},), {})
        assert process_data(**bound_args.arguments) == 0

        # Empty lists in dict are valid
        test_data = {"a": [], "b": [], "c": []}
        bound_args = checker.handle_type_safety((test_data,), {})
        assert process_data(**bound_args.arguments) == 3


    def test_nested_dict_validation__with_sets(self):
        """Test validation of Dict[str, Set[int]]"""
        def process_sets(data: Dict[str, Set[int]]) -> int:
            return sum(len(s) for s in data.values())

        checker = Type_Safe__Method(process_sets).setup()

        # Valid sets
        test_data = {"a": {1, 2, 3}, "b": {4, 5}}
        bound_args = checker.handle_type_safety((test_data,), {})
        result = process_sets(**bound_args.arguments)
        assert result == 5

        # Invalid: set contains wrong type
        with pytest.raises(ValueError) as exc_info:
            checker.handle_type_safety(({"a": {1, "two", 3}},), {})

        error_msg = str(exc_info.value)
        assert "parameter 'data'" in error_msg


    def test_nested_dict_validation__module_qualname_noy_in_errors(self):

        class OuterClass:
            class InnerClass(Type_Safe):
                value: int

        def process_nested_class(data: Dict[str, OuterClass.InnerClass]) -> None:
            pass

        checker = Type_Safe__Method(process_nested_class).setup()

        # Invalid: wrong type
        with pytest.raises(ValueError) as exc_info:
            checker.handle_type_safety(({"key": "not_inner_class"},), {})

        error_msg = str(exc_info.value)
        # Should show nested class structure
        assert "InnerClass" in error_msg
        assert error_msg == "Dict value for key 'key' in parameter 'data': Expected 'InnerClass', but got 'str'"


    def test_nested_dict_validation__performance_with_large_data(self):
        """Test that validation doesn't have exponential complexity"""
        import time

        def process_large(data: Dict[str, List[int]]) -> int:
            return sum(sum(v) for v in data.values())

        checker = Type_Safe__Method(process_large).setup()

        # Create progressively larger datasets
        sizes = [1, 10, 50]                         # this also works for 1000, but no need to run it :)
        times = []

        for size in sizes:
            test_data = {f"key{i}": list(range(100)) for i in range(size)}

            start = time.time()
            bound_args = checker.handle_type_safety((test_data,), {})
            elapsed = time.time() - start
            times.append(elapsed)

        # Validation time should scale roughly linearly, not exponentially
        # If it's exponential, time[2]/time[1] >> time[1]/time[0]
        if len(times) >= 2:
            ratio1 = times[1] / times[0] if times[0] > 0 else 0
            ratio2 = times[2] / times[1] if times[1] > 0 else 0
            # Allow for some variance, but not exponential growth
            assert ratio2 < ratio1 * 5, f"Validation appears to have exponential complexity: {times}"

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

        checker = Type_Safe__Method(process_document).setup()

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

        checker = Type_Safe__Method(complex_validation).setup()

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
                            "Dict value for key 'k' in parameter 'mapping': Expected 'float', but got 'str'"]


    def test_runtime_type_modification(self):                                            # Test behavior when types are modified at runtime
        class DynamicClass:
            pass

        def dynamic_func(obj: DynamicClass) -> None:
            pass

        checker = Type_Safe__Method(dynamic_func).setup()

        # Initial validation
        obj        = DynamicClass()
        bound_args = checker.handle_type_safety((obj,), {})

        # Even if we modify the class, existing instances should validate
        DynamicClass.new_attribute = "added"
        bound_args                 = checker.handle_type_safety((obj,), {})

        # New instances should also work
        new_obj    = DynamicClass()
        bound_args = checker.handle_type_safety((new_obj,), {})