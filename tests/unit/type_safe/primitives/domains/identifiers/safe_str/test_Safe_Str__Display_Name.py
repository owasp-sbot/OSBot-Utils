import pytest
from unittest                                                                             import TestCase
from osbot_utils.type_safe.Type_Safe                                                      import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Display_Name import Safe_Str__Display_Name
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id           import Safe_Str__Id


class test_Safe_Str__Display_Name(TestCase):

    def test__init__(self):                                      # Test basic initialization
        with Safe_Str__Display_Name() as _:
            assert type(_)           is Safe_Str__Display_Name
            assert _.regex.pattern   == r'[^a-zA-Z0-9_\- ().\'#]' # More chars allowed than Safe_Str__Id
            assert _.allow_empty     is True
            assert _.trim_whitespace is True

    def test_valid_display_names(self):                         # Test valid display name patterns
        # Basic display names
        assert str(Safe_Str__Display_Name('John Smith'          )) == 'John Smith'
        assert str(Safe_Str__Display_Name('Mary-Jane Watson'    )) == 'Mary-Jane Watson'
        assert str(Safe_Str__Display_Name('Dr. Smith'           )) == 'Dr. Smith'
        assert str(Safe_Str__Display_Name("O'Brien"             )) == "O'Brien"

        # Team/Group names
        assert str(Safe_Str__Display_Name("John's Team"         )) == "John's Team"
        assert str(Safe_Str__Display_Name('Team Alpha'          )) == 'Team Alpha'
        assert str(Safe_Str__Display_Name('Group (A)'           )) == 'Group (A)'
        assert str(Safe_Str__Display_Name('Department #5'       )) == 'Department #5'

        # Project names
        assert str(Safe_Str__Display_Name('Project (2024)'      )) == 'Project (2024)'
        assert str(Safe_Str__Display_Name('Phase 1.5'           )) == 'Phase 1.5'
        assert str(Safe_Str__Display_Name('Sprint #15'          )) == 'Sprint #15'
        assert str(Safe_Str__Display_Name('v2.0 (Beta)'         )) == 'v2.0 (Beta)'

        # Product names
        assert str(Safe_Str__Display_Name('iPhone 15 Pro'       )) == 'iPhone 15 Pro'
        assert str(Safe_Str__Display_Name('Model X-200'         )) == 'Model X-200'
        assert str(Safe_Str__Display_Name('Product #123'        )) == 'Product #123'

        # Company/Organization names
        assert str(Safe_Str__Display_Name("Smith's Bakery"      )) == "Smith's Bakery"
        assert str(Safe_Str__Display_Name('ABC Corp.'           )) == 'ABC Corp.'
        assert str(Safe_Str__Display_Name('Tech Solutions Inc.' )) == 'Tech Solutions Inc.'

        # Edge cases
        assert str(Safe_Str__Display_Name(None)) == ''
        assert str(Safe_Str__Display_Name(''  )) == ''

    def test_special_characters_allowed(self):                  # Test that special display chars work
        # Parentheses
        assert str(Safe_Str__Display_Name('Name (Nickname)'     )) == 'Name (Nickname)'
        assert str(Safe_Str__Display_Name('(Important) Note'    )) == '(Important) Note'
        assert str(Safe_Str__Display_Name('Task (1 of 3)'       )) == 'Task (1 of 3)'

        # Apostrophes
        assert str(Safe_Str__Display_Name("It's Working"        )) == "It's Working"
        assert str(Safe_Str__Display_Name("Don't Stop"          )) == "Don't Stop"
        assert str(Safe_Str__Display_Name("User's Choice"       )) == "User's Choice"

        # Periods
        assert str(Safe_Str__Display_Name('Mr. Anderson'        )) == 'Mr. Anderson'
        assert str(Safe_Str__Display_Name('Version 1.2.3'       )) == 'Version 1.2.3'
        assert str(Safe_Str__Display_Name('U.S.A.'              )) == 'U.S.A.'

        # Hash/Pound
        assert str(Safe_Str__Display_Name('Item #1'             )) == 'Item #1'
        assert str(Safe_Str__Display_Name('#TeamAwesome'        )) == '#TeamAwesome'
        assert str(Safe_Str__Display_Name('Apartment #42B'      )) == 'Apartment #42B'

        # Combined
        assert str(Safe_Str__Display_Name("Mary's Team (2024)"  )) == "Mary's Team (2024)"
        assert str(Safe_Str__Display_Name('Dr. Smith #1'        )) == 'Dr. Smith #1'

    def test_sanitization(self):                                # Test character replacement
        # Characters that get replaced
        assert str(Safe_Str__Display_Name('Name@Email'          )) == 'Name_Email'
        assert str(Safe_Str__Display_Name('Price: $100'         )) == 'Price_ _100'
        assert str(Safe_Str__Display_Name('100% Complete'       )) == '100_ Complete'
        assert str(Safe_Str__Display_Name('A&B Company'         )) == 'A_B Company'
        assert str(Safe_Str__Display_Name('Question?'           )) == 'Question_'
        assert str(Safe_Str__Display_Name('Exclamation!'        )) == 'Exclamation_'

        # Quotes (double quotes replaced, single allowed)
        assert str(Safe_Str__Display_Name('"Quoted"'            )) == '_Quoted_'
        assert str(Safe_Str__Display_Name("'Single OK'"         )) == "'Single OK'"

        # Slashes and backslashes
        assert str(Safe_Str__Display_Name('A/B Test'            )) == 'A_B Test'
        assert str(Safe_Str__Display_Name('Path\\Name'          )) == 'Path_Name'

        # Unicode
        assert str(Safe_Str__Display_Name('Café Manager'        )) == 'Caf_ Manager'
        assert str(Safe_Str__Display_Name('Résumé Review'       )) == 'R_sum_ Review'
        assert str(Safe_Str__Display_Name('Team 🚀'             )) == 'Team _'

    def test_spaces_and_formatting(self):                       # Test space handling
        # Spaces preserved
        assert str(Safe_Str__Display_Name('First Last'          )) == 'First Last'
        assert str(Safe_Str__Display_Name('One Two Three'       )) == 'One Two Three'

        # Multiple spaces preserved
        assert str(Safe_Str__Display_Name('Name  (Double)'      )) == 'Name  (Double)'

        # Trimming
        assert str(Safe_Str__Display_Name('  John Doe  '        )) == 'John Doe'
        assert str(Safe_Str__Display_Name('\tTabbed Name\t'     )) == 'Tabbed Name'
        assert str(Safe_Str__Display_Name('\n New Line \n'      )) == 'New Line'

    def test_type_conversion(self):                             # Test conversion from other types
        # From integer
        assert str(Safe_Str__Display_Name(123      )) == '123'

        # From float (dot preserved in display names)
        assert str(Safe_Str__Display_Name(123.456  )) == '123.456'

        # From boolean
        assert str(Safe_Str__Display_Name(True     )) == 'True'
        assert str(Safe_Str__Display_Name(False    )) == 'False'

    def test_in_type_safe_schema(self):                         # Test usage in Type_Safe classes
        class Schema__Profile(Type_Safe):
            display_name  : Safe_Str__Display_Name
            team_name     : Safe_Str__Display_Name
            project_title : Safe_Str__Display_Name

        with Schema__Profile() as _:
            # Auto-initialization
            assert type(_.display_name ) is Safe_Str__Display_Name
            assert type(_.team_name    ) is Safe_Str__Display_Name
            assert type(_.project_title) is Safe_Str__Display_Name

            # Setting with raw strings
            _.display_name = "John's Profile"
            assert _.display_name == "John's Profile"

            # Setting with special chars (some sanitized)
            _.team_name = 'Team #1 (Alpha)'
            assert _.team_name == 'Team #1 (Alpha)'

            # Setting with invalid chars
            _.project_title = 'Project@2024 [Beta]'
            assert _.project_title == 'Project_2024 _Beta_'

            # JSON serialization
            json_data = _.json()
            assert json_data['display_name' ] == "John's Profile"
            assert json_data['team_name'    ] == 'Team #1 (Alpha)'
            assert json_data['project_title'] == 'Project_2024 _Beta_'

    def test_common_display_patterns(self):                     # Test real-world display patterns
        # User display names
        assert str(Safe_Str__Display_Name('John Doe'            )) == 'John Doe'
        assert str(Safe_Str__Display_Name('jane.doe'            )) == 'jane.doe'
        assert str(Safe_Str__Display_Name('user_123'            )) == 'user_123'
        assert str(Safe_Str__Display_Name('Admin (Support)'     )) == 'Admin (Support)'

        # Product/Version displays
        assert str(Safe_Str__Display_Name('Version 2.0'         )) == 'Version 2.0'
        assert str(Safe_Str__Display_Name('Beta (v1.5)'         )) == 'Beta (v1.5)'
        assert str(Safe_Str__Display_Name('Release #42'         )) == 'Release #42'

        # Status displays
        assert str(Safe_Str__Display_Name('In Progress'         )) == 'In Progress'
        assert str(Safe_Str__Display_Name('Done (100%)'         )) == 'Done (100_)'
        assert str(Safe_Str__Display_Name("Won't Fix"           )) == "Won't Fix"

        # File/Document names
        assert str(Safe_Str__Display_Name('Report_2024.pdf'     )) == 'Report_2024.pdf'
        assert str(Safe_Str__Display_Name('My Document (v2)'    )) == 'My Document (v2)'
        assert str(Safe_Str__Display_Name("User's Guide #1"     )) == "User's Guide #1"

    def test_edge_cases(self):                                  # Test edge cases
        # Only special allowed chars
        assert str(Safe_Str__Display_Name("'''"                 )) == "'''"
        assert str(Safe_Str__Display_Name('...'                 )) == '...'
        assert str(Safe_Str__Display_Name('###'                 )) == '###'
        assert str(Safe_Str__Display_Name('()()'                )) == '()()'

        # Mixed separators
        assert str(Safe_Str__Display_Name(".-_#'"                )) == ".-_#'"

        # Real-world edge cases
        assert str(Safe_Str__Display_Name("O'Neil-Smith #5"     )) == "O'Neil-Smith #5"
        assert str(Safe_Str__Display_Name('Team (A.K.A. "Winners")')) == 'Team (A.K.A. _Winners_)'

    def test_max_length(self):                                  # Test length constraints
        # Should inherit max_length from Safe_Str__Id (128)
        max_length = 128
        max_name = 'a' * max_length
        assert str(Safe_Str__Display_Name(max_name)) == max_name
        assert len(Safe_Str__Display_Name(max_name)) == max_length

        # Exceeds max length
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Display_Name('a' * (max_length + 1))
        assert f"value exceeds maximum length of {max_length}" in str(exc_info.value)

    def test_difference_from_safe_id(self):                     # Compare with parent Safe_Str__Id
        test_string = "John's Team (2024)"

        # Safe_Str__Display_Name preserves special chars
        display = Safe_Str__Display_Name(test_string)
        assert str(display) == "John's Team (2024)"            # Apostrophe and parens preserved

        # Safe_Str__Id would replace them
        id_val = Safe_Str__Id(test_string)
        assert str(id_val) == 'John_s_Team__2024_'            # Special chars replaced

        # This distinction is important for:
        # - User-facing names that need readability
        # - Preserving formatting in display text
        # - Supporting common name patterns