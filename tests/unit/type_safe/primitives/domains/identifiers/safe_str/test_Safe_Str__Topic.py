import pytest
from unittest                                                                      import TestCase
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str                                import Safe_Str
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Topic import Safe_Str__Topic, TYPE_SAFE_STR__TOPIC__MAX_LENGTH


class test_Safe_Str__Topic(TestCase):

    def test__init__(self):                                      # Test basic initialization
        with Safe_Str__Topic() as _:
            assert type(_)                      is Safe_Str__Topic
            assert _.regex.pattern              == r'[^a-zA-Z0-9_\- ]'       # Alphanumerics, underscore, hyphen, space
            assert _.max_length                 == TYPE_SAFE_STR__TOPIC__MAX_LENGTH
            assert _.allow_empty                is True
            assert _.trim_whitespace            is True
            assert _.allow_all_replacement_char is True

    def test_valid_topics(self):                                # Test valid topic patterns
        # Basic valid topics
        assert str(Safe_Str__Topic('User Events'          )) == 'User Events'
        assert str(Safe_Str__Topic('order-processing'     )) == 'order-processing'
        assert str(Safe_Str__Topic('General Discussion'   )) == 'General Discussion'
        assert str(Safe_Str__Topic('Tech Support'         )) == 'Tech Support'
        assert str(Safe_Str__Topic('Product Updates'      )) == 'Product Updates'

        # Message queue topics
        assert str(Safe_Str__Topic('user events'          )) == 'user events'
        assert str(Safe_Str__Topic('order-events'         )) == 'order-events'
        assert str(Safe_Str__Topic('payment_processed'    )) == 'payment_processed'
        assert str(Safe_Str__Topic('inventory-updates'    )) == 'inventory-updates'

        # Forum/Discussion topics
        assert str(Safe_Str__Topic('How-to Guides'        )) == 'How-to Guides'
        assert str(Safe_Str__Topic('Best Practices'       )) == 'Best Practices'
        assert str(Safe_Str__Topic('Feature Requests'     )) == 'Feature Requests'
        assert str(Safe_Str__Topic('Bug Reports'          )) == 'Bug Reports'

        # Tag/Category names
        assert str(Safe_Str__Topic('python programming'   )) == 'python programming'
        assert str(Safe_Str__Topic('web-development'      )) == 'web-development'
        assert str(Safe_Str__Topic('machine_learning'     )) == 'machine_learning'
        assert str(Safe_Str__Topic('data science tips'    )) == 'data science tips'

        # Mixed formats
        assert str(Safe_Str__Topic('API_v2 Updates'       )) == 'API_v2 Updates'
        assert str(Safe_Str__Topic('Q4 2024 Planning'     )) == 'Q4 2024 Planning'
        assert str(Safe_Str__Topic('Team-A Sprint 15'     )) == 'Team-A Sprint 15'

        # Edge cases - empty and None
        assert str(Safe_Str__Topic(None)) == ''
        assert str(Safe_Str__Topic(''  )) == ''

    def test_sanitization(self):                                # Test character replacement
        # Special characters get replaced with underscore
        assert str(Safe_Str__Topic('user@events'          )) == 'user_events'
        assert str(Safe_Str__Topic('order#processing'     )) == 'order_processing'
        assert str(Safe_Str__Topic('feature.requests'     )) == 'feature_requests'
        assert str(Safe_Str__Topic('bug/reports'          )) == 'bug_reports'
        assert str(Safe_Str__Topic('Q&A Section'          )) == 'Q_A Section'
        assert str(Safe_Str__Topic('Price: $10.99'        )) == 'Price_ _10_99'
        assert str(Safe_Str__Topic('100% Complete'        )) == '100_ Complete'

        # Punctuation and symbols
        assert str(Safe_Str__Topic('Hello, World!'        )) == 'Hello_ World_'
        assert str(Safe_Str__Topic('What\'s New?'         )) == 'What_s New_'
        assert str(Safe_Str__Topic('"Breaking News"'      )) == '_Breaking News_'
        assert str(Safe_Str__Topic('[URGENT] Updates'     )) == '_URGENT_ Updates'
        assert str(Safe_Str__Topic('(Important) Notice'   )) == '_Important_ Notice'

        # Mixed valid and invalid characters
        assert str(Safe_Str__Topic('user-events!@#'       )) == 'user-events___'
        assert str(Safe_Str__Topic('Tech Support (24/7)'  )) == 'Tech Support _24_7_'
        assert str(Safe_Str__Topic('API v2.0 - Beta'      )) == 'API v2_0 - Beta'

        # Unicode characters
        assert str(Safe_Str__Topic('café discussions'     )) == 'caf_ discussions'
        assert str(Safe_Str__Topic('résumé tips'          )) == 'r_sum_ tips'
        assert str(Safe_Str__Topic('naïve questions'      )) == 'na_ve questions'
        assert str(Safe_Str__Topic('🚀 Launch News'       )) == '_ Launch News'
        assert str(Safe_Str__Topic('Updates 😀'           )) == 'Updates _'

    def test_spaces_preserved(self):                            # Test that spaces are preserved
        # Single spaces
        assert str(Safe_Str__Topic('one two three'        )) == 'one two three'
        assert str(Safe_Str__Topic('a b c d e'            )) == 'a b c d e'

        # Multiple spaces (preserved as-is)
        assert str(Safe_Str__Topic('one  two'             )) == 'one  two'
        assert str(Safe_Str__Topic('one   two'            )) == 'one   two'

        # Spaces with other valid chars
        assert str(Safe_Str__Topic('user-events topic'    )) == 'user-events topic'
        assert str(Safe_Str__Topic('topic_name here'      )) == 'topic_name here'
        assert str(Safe_Str__Topic('a-b_c d-e_f'          )) == 'a-b_c d-e_f'

    def test_trimming(self):                                    # Test whitespace trimming
        assert str(Safe_Str__Topic('  Topic Name  '       )) == 'Topic Name'
        assert str(Safe_Str__Topic('\tTech Support\t'     )) == 'Tech Support'
        assert str(Safe_Str__Topic('\nGeneral\n'          )) == 'General'
        assert str(Safe_Str__Topic('  \t Updates \n '     )) == 'Updates'

        # Internal spaces preserved after trimming
        assert str(Safe_Str__Topic('  one two  '          )) == 'one two'
        assert str(Safe_Str__Topic('\t one  two \n'       )) == 'one  two'

    def test_max_length(self):                                  # Test length constraints
        # At max length - should pass
        max_topic = 'a' * TYPE_SAFE_STR__TOPIC__MAX_LENGTH
        assert str(Safe_Str__Topic(max_topic)) == max_topic
        assert len(Safe_Str__Topic(max_topic)) == TYPE_SAFE_STR__TOPIC__MAX_LENGTH

        # Exceeds max length - should raise
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Topic('a' * (TYPE_SAFE_STR__TOPIC__MAX_LENGTH + 1))
        assert f"value exceeds maximum length of {TYPE_SAFE_STR__TOPIC__MAX_LENGTH}" in str(exc_info.value)

    def test_type_conversion(self):                             # Test conversion from other types
        # From integer
        assert str(Safe_Str__Topic(123      )) == '123'
        assert str(Safe_Str__Topic(0        )) == '0'

        # From float
        assert str(Safe_Str__Topic(123.456  )) == '123_456'   # Dot becomes underscore

        # From boolean
        assert str(Safe_Str__Topic(True     )) == 'True'
        assert str(Safe_Str__Topic(False    )) == 'False'

        # From another Safe_Str
        other = Safe_Str('test topic')
        assert str(Safe_Str__Topic(other)) == 'test_topic'

    def test_concatenation(self):                               # Test string concatenation behavior
        topic = Safe_Str__Topic('User Events')

        # Concatenation returns regular string, not Safe_Str__Topic
        result = topic + ' - Active'
        assert type(result) is Safe_Str__Topic                  # we didn't lose the type safety here
        assert result == 'User Events - Active'

        result = 'Topic: ' + topic
        assert type(result) is Safe_Str__Topic
        assert result == 'Topic_ User Events'

        # Using with format strings
        assert f"Topic: {topic}" == "Topic: User Events"
        assert "Topic: {}".format(topic) == "Topic: User Events"

    def test_repr_and_str(self):                                # Test string representations
        topic = Safe_Str__Topic('General Discussion')

        assert str(topic)  == 'General Discussion'
        assert repr(topic) == "Safe_Str__Topic('General Discussion')"

        # Empty topic
        empty = Safe_Str__Topic('')
        assert str(empty)   == ''
        assert repr(empty)  == "Safe_Str__Topic('')"

    def test_in_type_safe_schema(self):                         # Test usage in Type_Safe classes
        class Schema__Message(Type_Safe):
            topic       : Safe_Str__Topic
            channel     : Safe_Str__Topic
            category    : Safe_Str__Topic

        with Schema__Message() as _:
            # Auto-initialization
            assert type(_.topic   ) is Safe_Str__Topic
            assert type(_.channel ) is Safe_Str__Topic
            assert type(_.category) is Safe_Str__Topic

            # Setting with raw strings (auto-conversion)
            _.topic = 'User Registration'
            assert _.topic == 'User Registration'

            # Setting with special chars (sanitization)
            _.channel = 'support@channel#1'
            assert _.channel == 'support_channel_1'

            # Setting with Safe_Str__Topic
            _.category = Safe_Str__Topic('Tech Support')
            assert _.category == 'Tech Support'

            # JSON serialization
            json_data = _.json()
            assert json_data['topic'   ] == 'User Registration'
            assert json_data['channel' ] == 'support_channel_1'
            assert json_data['category'] == 'Tech Support'

            # Round-trip serialization
            restored = Schema__Message.from_json(json_data)
            assert restored.obj() == _.obj()

    def test_common_topic_patterns(self):                       # Test real-world topic patterns
        # Kafka/RabbitMQ topics
        assert str(Safe_Str__Topic('orders.created'       )) == 'orders_created'
        assert str(Safe_Str__Topic('users.updated'        )) == 'users_updated'
        assert str(Safe_Str__Topic('payments-processed'   )) == 'payments-processed'

        # Forum categories
        assert str(Safe_Str__Topic('Getting Started'      )) == 'Getting Started'
        assert str(Safe_Str__Topic('Advanced Topics'      )) == 'Advanced Topics'
        assert str(Safe_Str__Topic('Community Projects'   )) == 'Community Projects'

        # Event names
        assert str(Safe_Str__Topic('user_login_success'   )) == 'user_login_success'
        assert str(Safe_Str__Topic('order-placed'         )) == 'order-placed'
        assert str(Safe_Str__Topic('payment failed'       )) == 'payment failed'

        # Slack channels
        assert str(Safe_Str__Topic('general'              )) == 'general'
        assert str(Safe_Str__Topic('team-updates'         )) == 'team-updates'
        assert str(Safe_Str__Topic('dev_discussions'      )) == 'dev_discussions'

        # Tag names
        assert str(Safe_Str__Topic('machine-learning'     )) == 'machine-learning'
        assert str(Safe_Str__Topic('web development'      )) == 'web development'
        assert str(Safe_Str__Topic('data_science'         )) == 'data_science'

    def test_edge_cases(self):                                  # Test edge cases and corner scenarios
        # Only spaces
        assert str(Safe_Str__Topic('   '                  )) == ''  # Trimmed to empty

        # Only hyphens
        assert str(Safe_Str__Topic('---'                  )) == '---'

        # Only underscores
        assert str(Safe_Str__Topic('___'                  )) == '___'

        # Mix of valid separators
        assert str(Safe_Str__Topic('-_ _-'                )) == '-_ _-'

        # Numbers only
        assert str(Safe_Str__Topic('123456789'            )) == '123456789'

        # Single character
        assert str(Safe_Str__Topic('a'                    )) == 'a'
        assert str(Safe_Str__Topic('1'                    )) == '1'
        assert str(Safe_Str__Topic('-'                    )) == '-'
        assert str(Safe_Str__Topic('_'                    )) == '_'
        assert str(Safe_Str__Topic(' '                    )) == ''   # Single space trimmed

        # Start/end with separators (valid for topics)
        assert str(Safe_Str__Topic('-topic-'              )) == '-topic-'
        assert str(Safe_Str__Topic('_topic_'              )) == '_topic_'
        assert str(Safe_Str__Topic('-_topic_-'            )) == '-_topic_-'

        # Topics with numbers
        assert str(Safe_Str__Topic('2024 Updates'         )) == '2024 Updates'
        assert str(Safe_Str__Topic('Q1 Planning'          )) == 'Q1 Planning'
        assert str(Safe_Str__Topic('Sprint 15'            )) == 'Sprint 15'
        assert str(Safe_Str__Topic('v2 Features'          )) == 'v2 Features'

    def test_difference_from_safe_id(self):                     # Test key difference - spaces allowed
        test_string = 'user events topic'

        # Safe_Str__Topic preserves spaces
        topic = Safe_Str__Topic(test_string)
        assert str(topic) == 'user events topic'              # Spaces preserved

        # Safe_Str__Id would replace spaces (if we had it imported)
        # id_val = Safe_Str__Id(test_string)
        # assert str(id_val) == 'user_events_topic'          # Spaces replaced

        # This distinction is important for:
        # - Human-readable topic names
        # - Forum categories
        # - Display names
        # - Natural language labels