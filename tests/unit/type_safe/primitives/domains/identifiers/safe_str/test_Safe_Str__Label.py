import pytest
from unittest                                                                      import TestCase
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label import Safe_Str__Label
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Topic import Safe_Str__Topic


class test_Safe_Str__Label(TestCase):

    def test__init__(self):                                      # Test basic initialization
        with Safe_Str__Label() as _:
            assert type(_)                      is Safe_Str__Label
            assert _.regex.pattern              == r'[^a-zA-Z0-9_\-.: ]'     # Allows dots, colons, spaces (from Topic)
            assert _.allow_empty                is True
            assert _.trim_whitespace            is True
            assert _.allow_all_replacement_char is True

    def test_valid_labels(self):                                # Test valid label patterns
        # Basic labels
        assert str(Safe_Str__Label('app.module.component'   )) == 'app.module.component'
        assert str(Safe_Str__Label('category:subcategory'   )) == 'category:subcategory'
        assert str(Safe_Str__Label('namespace.class.method' )) == 'namespace.class.method'
        assert str(Safe_Str__Label('type:subtype:detail'    )) == 'type:subtype:detail'

        # Hierarchical labels with spaces
        assert str(Safe_Str__Label('Project: Alpha Team'    )) == 'Project: Alpha Team'
        assert str(Safe_Str__Label('Status: In Progress'    )) == 'Status: In Progress'
        assert str(Safe_Str__Label('Priority: High'         )) == 'Priority: High'
        assert str(Safe_Str__Label('Version: 2.0.1'         )) == 'Version: 2.0.1'

        # Module/Package paths
        assert str(Safe_Str__Label('com.example.app'        )) == 'com.example.app'
        assert str(Safe_Str__Label('org.project.module'     )) == 'org.project.module'
        assert str(Safe_Str__Label('io.github.repo'         )) == 'io.github.repo'

        # Classification labels
        assert str(Safe_Str__Label('department:engineering' )) == 'department:engineering'
        assert str(Safe_Str__Label('team:backend'           )) == 'team:backend'
        assert str(Safe_Str__Label('env:production'         )) == 'env:production'
        assert str(Safe_Str__Label('region:us-west-2'       )) == 'region:us-west-2'

        # Time-based labels
        assert str(Safe_Str__Label('2024:Q1:January'        )) == '2024:Q1:January'
        assert str(Safe_Str__Label('year.month.day'         )) == 'year.month.day'
        assert str(Safe_Str__Label('hour:minute:second'     )) == 'hour:minute:second'

        # Mixed formats
        assert str(Safe_Str__Label('app.v2:beta release'    )) == 'app.v2:beta release'
        assert str(Safe_Str__Label('service.api:v3.endpoint')) == 'service.api:v3.endpoint'
        assert str(Safe_Str__Label('Task 1.2: Complete'     )) == 'Task 1.2: Complete'

        # Edge cases
        assert str(Safe_Str__Label(None)) == ''
        assert str(Safe_Str__Label(''  )) == ''

    def test_dots_and_colons(self):                             # Test dots and colons work together
        # Dots for hierarchical separation
        assert str(Safe_Str__Label('level1.level2.level3'   )) == 'level1.level2.level3'
        assert str(Safe_Str__Label('a.b.c.d.e'              )) == 'a.b.c.d.e'

        # Colons for key-value style
        assert str(Safe_Str__Label('key:value'              )) == 'key:value'
        assert str(Safe_Str__Label('type:subtype'           )) == 'type:subtype'

        # Combined dots and colons
        assert str(Safe_Str__Label('app.module:config'      )) == 'app.module:config'
        assert str(Safe_Str__Label('service:api.v2'         )) == 'service:api.v2'
        assert str(Safe_Str__Label('a.b:c.d'                )) == 'a.b:c.d'

        # Multiple consecutive
        assert str(Safe_Str__Label('a..b'                   )) == 'a..b'
        assert str(Safe_Str__Label('a::b'                   )) == 'a::b'
        assert str(Safe_Str__Label('.::'                    )) == '.::'

        # Starting/ending with dots or colons
        assert str(Safe_Str__Label('.hidden:label'          )) == '.hidden:label'
        assert str(Safe_Str__Label(':priority'              )) == ':priority'
        assert str(Safe_Str__Label('trailing.'              )) == 'trailing.'
        assert str(Safe_Str__Label('ending:'                )) == 'ending:'

    def test_spaces_preserved(self):                            # Test that spaces work with dots/colons
        # Labels with spaces
        assert str(Safe_Str__Label('Label Name'             )) == 'Label Name'
        assert str(Safe_Str__Label('Multi Word Label'       )) == 'Multi Word Label'

        # Spaces with dots
        assert str(Safe_Str__Label('app.name: My App'       )) == 'app.name: My App'
        assert str(Safe_Str__Label('version 1.0.0'          )) == 'version 1.0.0'

        # Spaces with colons
        assert str(Safe_Str__Label('Status: In Review'      )) == 'Status: In Review'
        assert str(Safe_Str__Label('Priority: Very High'    )) == 'Priority: Very High'

        # Multiple spaces preserved
        assert str(Safe_Str__Label('Label  with  spaces'    )) == 'Label  with  spaces'

    def test_sanitization(self):                                # Test character replacement
        # Invalid characters replaced
        assert str(Safe_Str__Label('label@domain'           )) == 'label_domain'
        assert str(Safe_Str__Label('item#123'               )) == 'item_123'
        assert str(Safe_Str__Label('price=$100'             )) == 'price__100'
        assert str(Safe_Str__Label('50% complete'           )) == '50_ complete'
        assert str(Safe_Str__Label('user/admin'             )) == 'user_admin'
        assert str(Safe_Str__Label('key=value'              )) == 'key_value'

        # Quotes replaced
        assert str(Safe_Str__Label('"quoted"'               )) == '_quoted_'
        assert str(Safe_Str__Label("'single'"               )) == '_single_'

        # Brackets and braces
        assert str(Safe_Str__Label('[category]'             )) == '_category_'
        assert str(Safe_Str__Label('{type}'                 )) == '_type_'
        assert str(Safe_Str__Label('(group)'                )) == '_group_'

        # Unicode
        assert str(Safe_Str__Label('café:menu'              )) == 'caf_:menu'
        assert str(Safe_Str__Label('résumé.section'         )) == 'r_sum_.section'
        assert str(Safe_Str__Label('Label 🏷️'              )) == 'Label __'

    def test_type_conversion(self):                             # Test conversion from other types
        # From integer
        assert str(Safe_Str__Label(123      )) == '123'

        # From float (dots preserved)
        assert str(Safe_Str__Label(123.456  )) == '123.456'
        assert str(Safe_Str__Label(1.0      )) == '1.0'

        # From boolean
        assert str(Safe_Str__Label(True     )) == 'True'
        assert str(Safe_Str__Label(False    )) == 'False'

    def test_in_type_safe_schema(self):                         # Test usage in Type_Safe classes
        class Schema__Tagged(Type_Safe):
            category    : Safe_Str__Label
            namespace   : Safe_Str__Label
            metadata    : Safe_Str__Label

        with Schema__Tagged() as _:
            # Auto-initialization
            assert type(_.category  ) is Safe_Str__Label
            assert type(_.namespace ) is Safe_Str__Label
            assert type(_.metadata  ) is Safe_Str__Label

            # Setting with raw strings
            _.category = 'type:document'
            assert _.category == 'type:document'

            # Setting with hierarchical labels
            _.namespace = 'com.company.product.module'
            assert _.namespace == 'com.company.product.module'

            # Setting with spaces and special chars
            _.metadata = 'Created: 2024-03-15 @ 10:30'
            assert _.metadata == 'Created: 2024-03-15 _ 10:30'

            # JSON serialization
            json_data = _.json()
            assert json_data['category' ] == 'type:document'
            assert json_data['namespace'] == 'com.company.product.module'
            assert json_data['metadata' ] == 'Created: 2024-03-15 _ 10:30'

    def test_common_label_patterns(self):                       # Test real-world label patterns
        # Kubernetes labels (Note: / will be replaced)
        assert str(Safe_Str__Label('app.kubernetes.io_name' )) == 'app.kubernetes.io_name'
        assert str(Safe_Str__Label('app.kubernetes.io_version')) == 'app.kubernetes.io_version'
        assert str(Safe_Str__Label('environment:production' )) == 'environment:production'

        # Docker labels
        assert str(Safe_Str__Label('com.docker.compose.project')) == 'com.docker.compose.project'
        assert str(Safe_Str__Label('org.label-schema.version')) == 'org.label-schema.version'

        # Semantic versioning labels
        assert str(Safe_Str__Label('version:1.2.3'          )) == 'version:1.2.3'
        assert str(Safe_Str__Label('release:v2.0.0-beta'    )) == 'release:v2.0.0-beta'

        # Jira/Issue tracking
        assert str(Safe_Str__Label('project:PROJ'           )) == 'project:PROJ'
        assert str(Safe_Str__Label('issue.type:bug'         )) == 'issue.type:bug'
        assert str(Safe_Str__Label('priority:P1'            )) == 'priority:P1'
        assert str(Safe_Str__Label('status:in progress'     )) == 'status:in progress'

        # Logging/Monitoring
        assert str(Safe_Str__Label('log.level:error'        )) == 'log.level:error'
        assert str(Safe_Str__Label('metric.type:counter'    )) == 'metric.type:counter'
        assert str(Safe_Str__Label('alert:critical'         )) == 'alert:critical'

    def test_edge_cases(self):                                  # Test edge cases
        # Only special chars
        assert str(Safe_Str__Label(':::'                    )) == ':::'
        assert str(Safe_Str__Label('...'                    )) == '...'
        assert str(Safe_Str__Label('.:.'                    )) == '.:.'
        assert str(Safe_Str__Label(': : :'                  )) == ': : :'

        # Complex patterns
        assert str(Safe_Str__Label('a.b:c d-e_f'            )) == 'a.b:c d-e_f'
        assert str(Safe_Str__Label('1.2.3:alpha-4'          )) == '1.2.3:alpha-4'
        assert str(Safe_Str__Label('service.v2:endpoint.api')) == 'service.v2:endpoint.api'

    def test_max_length(self):                                  # Test length constraints
        # Should inherit from Safe_Str__Topic (512)
        max_length = 512
        max_label = 'a' * max_length
        assert str(Safe_Str__Label(max_label)) == max_label
        assert len(Safe_Str__Label(max_label)) == max_length

        # Exceeds max length
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Label('a' * (max_length + 1))
        assert f"value exceeds maximum length of {max_length}" in str(exc_info.value)

    def test_difference_from_safe_topic(self):                  # Compare with parent Safe_Str__Topic
        test_string = 'app.module:config setting'

        # Safe_Str__Label preserves dots and colons
        label = Safe_Str__Label(test_string)
        assert str(label) == 'app.module:config setting'        # Dots and colons preserved

        # Safe_Str__Topic would replace dots and colons
        topic = Safe_Str__Topic(test_string)
        assert str(topic) == 'app_module_config setting'        # Dots and colons replaced

        # This distinction is important for:
        # - Hierarchical labeling systems
        # - Namespace separation
        # - Key-value style labels