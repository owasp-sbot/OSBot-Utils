import pytest
from unittest                                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id         import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Namespace  import Safe_Str__Namespace


class test_Safe_Str__Namespace(TestCase):

    def test__init__(self):                                      # Test basic initialization
        with Safe_Str__Namespace() as _:
            assert type(_)                      is Safe_Str__Namespace
            assert _.regex.pattern              == r'[^a-zA-Z0-9.\-]'   # Allows alphanumerics, dots, hyphens
            assert _.allow_empty                is True
            assert _.trim_whitespace            is True
            assert _.allow_all_replacement_char is True

    def test_valid_namespaces(self):                            # Test valid namespace patterns
        # Java-style namespaces
        assert str(Safe_Str__Namespace('com.example.app'        )) == 'com.example.app'
        assert str(Safe_Str__Namespace('org.apache.commons'     )) == 'org.apache.commons'
        assert str(Safe_Str__Namespace('io.github.project'      )) == 'io.github.project'
        assert str(Safe_Str__Namespace('net.company.product'    )) == 'net.company.product'

        # Python-style namespaces
        assert str(Safe_Str__Namespace('osbot_utils.type_safe'  )) == 'osbot_utils.type_safe'
        assert str(Safe_Str__Namespace('django.contrib.auth'    )) == 'django.contrib.auth'
        assert str(Safe_Str__Namespace('numpy.linalg.decomp'    )) == 'numpy.linalg.decomp'

        # DNS-style namespaces
        assert str(Safe_Str__Namespace('api.example.com'        )) == 'api.example.com'
        assert str(Safe_Str__Namespace('staging.app.company.io' )) == 'staging.app.company.io'
        assert str(Safe_Str__Namespace('v2.service.domain.net'  )) == 'v2.service.domain.net'

        # Hyphenated namespaces
        assert str(Safe_Str__Namespace('org-department-team'    )) == 'org-department-team'
        assert str(Safe_Str__Namespace('region-us-west-2'       )) == 'region-us-west-2'
        assert str(Safe_Str__Namespace('env-production'         )) == 'env-production'

        # Mixed dots and hyphens
        assert str(Safe_Str__Namespace('com.my-company.app'     )) == 'com.my-company.app'
        assert str(Safe_Str__Namespace('org.open-source.lib'    )) == 'org.open-source.lib'
        assert str(Safe_Str__Namespace('api.v2-beta.endpoint'   )) == 'api.v2-beta.endpoint'

        # Version namespaces
        assert str(Safe_Str__Namespace('v1.api.service'         )) == 'v1.api.service'
        assert str(Safe_Str__Namespace('app.v2.0.1'             )) == 'app.v2.0.1'
        assert str(Safe_Str__Namespace('release-1.2.3'          )) == 'release-1.2.3'

        # Edge cases
        assert str(Safe_Str__Namespace(None)) == ''
        assert str(Safe_Str__Namespace(''  )) == ''

    def test_dots_in_namespaces(self):                          # Test dot handling
        # Single level
        assert str(Safe_Str__Namespace('app'                    )) == 'app'

        # Multi-level
        assert str(Safe_Str__Namespace('a.b'                    )) == 'a.b'
        assert str(Safe_Str__Namespace('a.b.c'                  )) == 'a.b.c'
        assert str(Safe_Str__Namespace('a.b.c.d.e.f'            )) == 'a.b.c.d.e.f'

        # Starting/ending with dots
        assert str(Safe_Str__Namespace('.hidden'                )) == '.hidden'
        assert str(Safe_Str__Namespace('trailing.'              )) == 'trailing.'
        assert str(Safe_Str__Namespace('.both.'                 )) == '.both.'

        # Multiple consecutive dots (valid for some namespace styles)
        assert str(Safe_Str__Namespace('a..b'                   )) == 'a..b'
        assert str(Safe_Str__Namespace('...'                    )) == '...'

    def test_hyphens_in_namespaces(self):                       # Test hyphen handling
        # Kebab-case style
        assert str(Safe_Str__Namespace('my-namespace'           )) == 'my-namespace'
        assert str(Safe_Str__Namespace('org-team-project'       )) == 'org-team-project'

        # Starting/ending with hyphens
        assert str(Safe_Str__Namespace('-start'                 )) == '-start'
        assert str(Safe_Str__Namespace('end-'                   )) == 'end-'
        assert str(Safe_Str__Namespace('-both-'                 )) == '-both-'

        # Multiple consecutive hyphens
        assert str(Safe_Str__Namespace('a--b'                   )) == 'a--b'
        assert str(Safe_Str__Namespace('---'                    )) == '---'

    def test_sanitization(self):                                # Test character replacement
        # Spaces replaced (namespaces shouldn't have spaces)
        assert str(Safe_Str__Namespace('my namespace'           )) == 'my_namespace'
        assert str(Safe_Str__Namespace('com example app'        )) == 'com_example_app'

        # Underscores replaced (not typical in namespaces)
        assert str(Safe_Str__Namespace('my_namespace'           )) == 'my_namespace'
        assert str(Safe_Str__Namespace('com_example_app'        )) == 'com_example_app'

        # Special characters replaced
        assert str(Safe_Str__Namespace('com@example'            )) == 'com_example'
        assert str(Safe_Str__Namespace('org#team'               )) == 'org_team'
        assert str(Safe_Str__Namespace('app:module'             )) == 'app_module'
        assert str(Safe_Str__Namespace('path/to/module'         )) == 'path_to_module'
        assert str(Safe_Str__Namespace('key=value'              )) == 'key_value'

        # Unicode replaced
        assert str(Safe_Str__Namespace('café.app'               )) == 'caf_.app'
        assert str(Safe_Str__Namespace('résumé.module'          )) == 'r_sum_.module'
        assert str(Safe_Str__Namespace('org.🚀.project'         )) == 'org._.project'

        # Mixed valid and invalid
        assert str(Safe_Str__Namespace('com.example@2024'       )) == 'com.example_2024'
        assert str(Safe_Str__Namespace('org-team#prod'          )) == 'org-team_prod'

    def test_trimming(self):                                    # Test whitespace trimming
        assert str(Safe_Str__Namespace('  com.example  '        )) == 'com.example'
        assert str(Safe_Str__Namespace('\torg.project\t'        )) == 'org.project'
        assert str(Safe_Str__Namespace('\n namespace.app \n'    )) == 'namespace.app'

    def test_type_conversion(self):                             # Test conversion from other types
        # From integer
        assert str(Safe_Str__Namespace(123      )) == '123'

        # From float (dots preserved)
        assert str(Safe_Str__Namespace(123.456  )) == '123.456'
        assert str(Safe_Str__Namespace(1.0      )) == '1.0'

        # From boolean
        assert str(Safe_Str__Namespace(True     )) == 'True'
        assert str(Safe_Str__Namespace(False    )) == 'False'

    def test_in_type_safe_schema(self):                         # Test usage in Type_Safe classes
        class Schema__Module(Type_Safe):
            namespace   : Safe_Str__Namespace  # Will actually be Safe_Str__Key due to bug
            package     : Safe_Str__Namespace
            module_path : Safe_Str__Namespace

        with Schema__Module() as _:
            # Auto-initialization (type check will show Safe_Str__Key due to bug)
            # assert type(_.namespace) is Safe_Str__Namespace  # Would fail

            # Setting with raw strings
            _.namespace = 'com.company.product'
            assert _.namespace == 'com.company.product'

            # Setting with hyphens
            _.package = 'org-team-project'
            assert _.package == 'org-team-project'

            # Setting with invalid chars
            _.module_path = 'app/module@v2'
            assert _.module_path == 'app_module_v2'

            # JSON serialization
            json_data = _.json()
            assert json_data['namespace'  ] == 'com.company.product'
            assert json_data['package'    ] == 'org-team-project'
            assert json_data['module_path'] == 'app_module_v2'

    def test_common_namespace_patterns(self):                   # Test real-world namespace patterns
        # Maven/Java packages
        assert str(Safe_Str__Namespace('org.springframework.boot')) == 'org.springframework.boot'
        assert str(Safe_Str__Namespace('com.google.common.base' )) == 'com.google.common.base'
        assert str(Safe_Str__Namespace('javax.servlet.http'     )) == 'javax.servlet.http'

        # .NET namespaces
        assert str(Safe_Str__Namespace('System.Collections.Generic')) == 'System.Collections.Generic'
        assert str(Safe_Str__Namespace('Microsoft.AspNetCore.Mvc')) == 'Microsoft.AspNetCore.Mvc'

        # Kubernetes namespaces
        assert str(Safe_Str__Namespace('kube-system'            )) == 'kube-system'
        assert str(Safe_Str__Namespace('istio-system'           )) == 'istio-system'
        assert str(Safe_Str__Namespace('cert-manager'           )) == 'cert-manager'

        # AWS ARN components
        assert str(Safe_Str__Namespace('arn.aws.s3'             )) == 'arn.aws.s3'
        assert str(Safe_Str__Namespace('arn.aws.lambda'         )) == 'arn.aws.lambda'

        # Docker registry paths
        assert str(Safe_Str__Namespace('docker.io'              )) == 'docker.io'
        assert str(Safe_Str__Namespace('gcr.io'                 )) == 'gcr.io'
        assert str(Safe_Str__Namespace('registry.gitlab.com'    )) == 'registry.gitlab.com'

    def test_edge_cases(self):                                  # Test edge cases
        # Only dots
        assert str(Safe_Str__Namespace('.'                      )) == '.'
        assert str(Safe_Str__Namespace('..'                     )) == '..'
        assert str(Safe_Str__Namespace('...'                    )) == '...'

        # Only hyphens
        assert str(Safe_Str__Namespace('-'                      )) == '-'
        assert str(Safe_Str__Namespace('--'                     )) == '--'
        assert str(Safe_Str__Namespace('---'                    )) == '---'

        # Mixed separators
        assert str(Safe_Str__Namespace('.-'                     )) == '.-'
        assert str(Safe_Str__Namespace('-.'                     )) == '-.'
        assert str(Safe_Str__Namespace('.-.-'                   )) == '.-.-'

        # Numeric only
        assert str(Safe_Str__Namespace('123.456.789'            )) == '123.456.789'
        assert str(Safe_Str__Namespace('1-2-3'                  )) == '1-2-3'

    def test_max_length(self):                                  # Test length constraints
        # Should inherit from Safe_Str__Id (128)
        max_length = 128
        max_ns = 'a' * max_length
        assert str(Safe_Str__Namespace(max_ns)) == max_ns
        assert len(Safe_Str__Namespace(max_ns)) == max_length

        # Exceeds max length
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Namespace('a' * (max_length + 1))
        assert f"value exceeds maximum length of {max_length}" in str(exc_info.value)

    def test_difference_from_safe_id(self):                     # Compare with parent Safe_Str__Id
        test_string = 'com.example.app'

        # Safe_Str__Namespace preserves dots
        namespace = Safe_Str__Namespace(test_string)
        assert str(namespace) == 'com.example.app'              # Dots preserved

        # Safe_Str__Id would replace dots
        id_val = Safe_Str__Id(test_string)
        assert str(id_val) == 'com_example_app'                 # Dots replaced

        # This distinction is important for:
        # - Package/module namespaces
        # - DNS-style naming
        # - Hierarchical organization