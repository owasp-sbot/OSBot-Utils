from unittest                                                import TestCase
from osbot_utils.type_safe.shared.Type_Safe__Json_Compressor import Type_Safe__Json_Compressor


class test_Type_Safe__Json_Compressor__Type_Registry(TestCase):

    def setUp(self):
        self.registry = Type_Safe__Json_Compressor().type_registry

    def test_create_reference_name(self):
        test_cases = [
            ("data.classes.Schema__First__Second__Third", "@schema_first_second_third"),
            ("data.classes.Schema__Alpha__Beta"         , "@schema_alpha_beta"        ),
            ("data.classes.Simple_Config"               , "@simple_config"            )
        ]

        for type_path, expected in test_cases:
            ref = self.registry.create_reference_name(type_path)
            assert ref == expected                                                    # Reference matches expected format
            assert ref.startswith('@')                                               # Starts with @
            assert ref.islower()                                                     # All lowercase

    def test_type_registry_operations(self):
        type_path_1 = "data.classes.Schema__First__Second__Third"
        type_path_2 = "data.classes.Schema__Alpha__Beta"

        ref_1 = self.registry.register_type(type_path_1)                            # Register first type
        ref_2 = self.registry.register_type(type_path_2)                            # Register second type

        assert ref_1 != ref_2                                                        # Different types get different refs
        assert self.registry.get_type(ref_1) == type_path_1                         # Can retrieve type paths
        assert self.registry.get_type(ref_2) == type_path_2

        ref_3 = self.registry.register_type(type_path_1)                            # Register same type again
        assert ref_3 == ref_1                                                        # Gets same reference

    def test_registry_clear(self):
        self.registry.register_type("some.type.path")
        self.registry.clear()

        assert len(self.registry.registry) == 0                                       # Registry cleared
        assert len(self.registry.reverse)  == 0                                       # Reverse mapping cleared
