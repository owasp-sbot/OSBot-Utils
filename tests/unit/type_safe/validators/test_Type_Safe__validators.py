import sys
import pytest
from unittest                                                   import TestCase

if sys.version_info > (3, 8):
    from osbot_utils.helpers.python_compatibility.python_3_8    import Annotated
    from osbot_utils.type_safe.Type_Safe                        import Type_Safe
    from osbot_utils.type_safe.validators.Type_Safe__Validator  import Validate
    from osbot_utils.type_safe.validators.Validator__Max        import Max
    from osbot_utils.type_safe.validators.Validator__Min        import Min
    from osbot_utils.type_safe.validators.Validator__One_Of     import One_Of
    from osbot_utils.type_safe.validators.Validator__Regex      import Regex


class test_Type_Safe__validators(TestCase):

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 9):
            pytest.skip("Skipping tests that need FIXING on 3.8 or lower")

    def test_numeric_validators(self):
        class Person(Type_Safe):
            age  : Validate[int  , Min(0)  , Max(150  )]
            score: Validate[float, Min(0.0), Max(100.0)]

        # Valid cases
        person = Person(age=25, score=85.5)
        assert person.age   == 25
        assert person.score == 85.5

        # Invalid cases
        with pytest.raises(ValueError,match='age must be at least 0, got -1'):
            Person(age=-1)

        with pytest.raises(ValueError,match='age must be at most 150, got size 151'):
            Person(age=151)

        with pytest.raises(ValueError,match='score must be at least 0.0, got -0.1'):
            Person(score=-0.1)

    def test_string_validators(self):
        class User(Type_Safe):
            username: Annotated[str, Min(3), Max(20), Regex(r'^[a-zA-Z0-9_]+$')] = None
            status  : Annotated[str, One_Of(['active', 'inactive', 'pending'])]  = 'pending'

        user = User(username="john_doe", status="active")                           # Valid cases
        assert user.username == "john_doe"
        assert user.status  == "active"

        with self.assertRaises(ValueError) as context:                              # Invalid cases
            User(username="a")  # Too short
        assert "must have length at least 3" in str(context.exception)

        with self.assertRaises(ValueError) as context:
            User(username="invalid@username")  # Invalid character
        assert "must match pattern" in str(context.exception)

        with self.assertRaises(ValueError) as context:
            User(status="unknown")  # Invalid status
        assert "must be one of" in str(context.exception)

    def test_validator_descriptions(self):
        min_validator    = Min(0)
        max_validator    = Max(100)
        regex_validator  = Regex(r'^[a-zA-Z0-9]+$', "alphanumeric characters only")
        one_of_validator = One_Of(['red', 'green', 'blue'])

        assert min_validator.describe   () == "minimum value: 0"
        assert max_validator.describe   () == "maximum value: 100"
        assert regex_validator.describe () == "alphanumeric characters only"
        assert one_of_validator.describe() == "must be one of: ['red', 'green', 'blue']"