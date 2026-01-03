from unittest                                                                      import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb import Safe_Str__Ontology__Verb


class test_Safe_Str__Ontology__Verb(TestCase):                                       # Test ontology verb

    def test__init__(self):                                                          # Test initialization
        with Safe_Str__Ontology__Verb('defines') as _:
            assert str(_) == 'defines'

    def test__lowercase_only(self):                                                  # Test lowercase constraint
        with Safe_Str__Ontology__Verb('inherits_from') as _:
            assert str(_) == 'inherits_from'

    def test__sanitizes_uppercase(self):                                             # Test uppercase is sanitized
        with Safe_Str__Ontology__Verb('DEFINES') as _:
            assert str(_) == '_______'                                               # Uppercase chars replaced

    def test__allows_underscores(self):                                              # Test underscores allowed
        with Safe_Str__Ontology__Verb('is_related_to') as _:
            assert str(_) == 'is_related_to'

    def test__comparison(self):                                                      # Test string comparison
        verb = Safe_Str__Ontology__Verb('has')
        assert verb == 'has'
        assert str(verb) == 'has'
