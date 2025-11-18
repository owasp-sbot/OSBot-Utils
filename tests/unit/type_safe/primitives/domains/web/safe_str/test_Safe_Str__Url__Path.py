import pytest
from unittest                                                                        import TestCase
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Path       import Safe_Str__Url__Path, TYPE_SAFE_STR__URL__PATH__MAX_LENGTH
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Query      import Safe_Str__Url__Query
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Path_Query import Safe_Str__Url__Path_Query


class test_Safe_Str__Url__Path(TestCase):

    def test_init(self):
        assert Safe_Str__Url__Path() == ''

    def test_basic_paths(self):
        """Test basic path validation"""
        assert Safe_Str__Url__Path('/'                  ) == '/'
        assert Safe_Str__Url__Path('/api'               ) == '/api'
        assert Safe_Str__Url__Path('/api/v1'            ) == '/api/v1'
        assert Safe_Str__Url__Path('/users/123'         ) == '/users/123'
        assert Safe_Str__Url__Path('/path/to/resource'  ) == '/path/to/resource'

    def test_relative_paths(self):
        """Test relative paths (without leading slash)"""
        assert Safe_Str__Url__Path('api'        ) == 'api'
        assert Safe_Str__Url__Path('api/v1'     ) == 'api/v1'
        assert Safe_Str__Url__Path('users/123'  ) == 'users/123'

    def test_paths_with_file_extensions(self):
        """Test paths pointing to files"""
        assert Safe_Str__Url__Path('/index.html'            ) == '/index.html'
        assert Safe_Str__Url__Path('/docs/readme.md'        ) == '/docs/readme.md'
        assert Safe_Str__Url__Path('/images/photo.jpg'      ) == '/images/photo.jpg'
        assert Safe_Str__Url__Path('/static/css/style.css'  ) == '/static/css/style.css'

    def test_paths_with_special_characters(self):
        """Test paths with hyphens, underscores, and dots"""
        assert Safe_Str__Url__Path('/my-path'               ) == '/my-path'
        assert Safe_Str__Url__Path('/my_path'               ) == '/my_path'
        assert Safe_Str__Url__Path('/api/v1/user-profile'   ) == '/api/v1/user-profile'
        assert Safe_Str__Url__Path('/path/./current'        ) == '/path/./current'
        assert Safe_Str__Url__Path('/path/../parent'        ) == '/path/../parent'
        assert Safe_Str__Url__Path('/file.with.dots.txt'    ) == '/file.with.dots.txt'

    def test_paths_with_url_encoding(self):
        """Test paths with percent-encoded characters"""
        assert Safe_Str__Url__Path('/path%20with%20spaces'  ) == '/path%20with%20spaces'
        assert Safe_Str__Url__Path('/caf%C3%A9'             ) == '/caf%C3%A9'
        assert Safe_Str__Url__Path('/%7Euser'               ) == '/%7Euser'
        assert Safe_Str__Url__Path('/~user/docs'            ) == '/~user/docs'

    def test_whitespace_handling(self):
        """Test trimming of leading/trailing whitespace"""
        assert Safe_Str__Url__Path('  /api/v1  '   ) == '/api/v1'
        assert Safe_Str__Url__Path('\n/path\t'      ) == '/path'
        assert Safe_Str__Url__Path('  /users/123 '  ) == '/users/123'

    def test_empty_values(self):
        """Test that empty and None values are handled correctly"""
        assert Safe_Str__Url__Path(None) == ''
        assert Safe_Str__Url__Path(''  ) == ''

    def test_path_depth(self):
        """Test paths with various nesting levels"""
        assert Safe_Str__Url__Path('/a'         ) == '/a'
        assert Safe_Str__Url__Path('/a/b'       ) == '/a/b'
        assert Safe_Str__Url__Path('/a/b/c'     ) == '/a/b/c'
        assert Safe_Str__Url__Path('/a/b/c/d/e/f') == '/a/b/c/d/e/f'

        # Deep nesting
        deep_path = '/' + '/'.join([f'level{i}' for i in range(20)])
        assert Safe_Str__Url__Path(deep_path) == deep_path

    def test_invalid_paths(self):
        """Test that invalid paths are rejected"""
        # Query parameters not allowed in path
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Path('/api?query=test')
        assert "does not match required pattern" in str(exc_info.value)

        # Fragments not allowed
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Path('/page#section')
        assert "does not match required pattern" in str(exc_info.value)

        # Spaces without encoding
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Path('/path with spaces')
        assert "does not match required pattern" in str(exc_info.value)

        # Invalid special characters
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Path('/path<script>')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Path('/path?query')
        assert "does not match required pattern" in str(exc_info.value)

    def test_max_length_validation(self):
        """Test max length enforcement"""
        # Within limit
        long_path = '/' + 'a' * 2000
        assert len(Safe_Str__Url__Path(long_path)) > 0

        # Exceeds limit
        with pytest.raises(ValueError) as exc_info:
            very_long_path = '/' + 'a' * TYPE_SAFE_STR__URL__PATH__MAX_LENGTH
            Safe_Str__Url__Path(very_long_path)
        assert f"exceeds maximum length of {TYPE_SAFE_STR__URL__PATH__MAX_LENGTH}" in str(exc_info.value)

    def test_path_concatenation__path_plus_path(self):
        """Test Path + Path = Path with proper slash handling"""
        path1 = Safe_Str__Url__Path('/api/v1')
        path2 = Safe_Str__Url__Path('users')

        result = path1 + path2
        assert type(result) is Safe_Str__Url__Path
        assert str(result) == '/api/v1/users'

        # Both with slashes
        path3 = Safe_Str__Url__Path('/api/')
        path4 = Safe_Str__Url__Path('/users')
        result2 = path3 + path4
        assert str(result2) == '/api/users'

        # Concatenating absolute paths
        path5 = Safe_Str__Url__Path('/api')
        path6 = Safe_Str__Url__Path('/v1/users')
        result3 = path5 + path6
        assert str(result3) == '/api/v1/users'

    def test_path_concatenation__path_plus_query(self):
        """Test Path + Query = Path_Query"""
        path = Safe_Str__Url__Path('/api/v1/users')
        query = Safe_Str__Url__Query('page=1&limit=10')

        result = path + query
        assert type(result) is Safe_Str__Url__Path_Query
        assert str(result) == '/api/v1/users?page=1&limit=10'

        # Empty query
        result2 = path + Safe_Str__Url__Query('')
        assert type(result2) is Safe_Str__Url__Path_Query
        assert str(result2) == '/api/v1/users'

    def test_path_concatenation__path_plus_query_string(self):
        """Test Path + string starting with '?' = Path_Query"""
        path = Safe_Str__Url__Path('/search')

        result = path + '?q=test'
        assert type(result) is Safe_Str__Url__Path_Query
        assert str(result) == '/search?q=test'

        result2 = path + '?q=test&sort=desc'
        assert str(result2) == '/search?q=test&sort=desc'

    def test_path_concatenation__path_plus_string(self):
        """Test Path + regular string = Path"""
        path = Safe_Str__Url__Path('/api')

        result = path + '/users'
        assert type(result) is Safe_Str__Url__Path
        assert str(result) == '/api/users'

        result2 = path + '/v1/users'
        assert str(result2) == '/api/v1/users'

    def test_path_concatenation__string_plus_path(self):
        """Test string + Path = Path (reverse addition)"""
        base = '/api'
        path = Safe_Str__Url__Path('users')

        result = base + path
        assert type(result) is Safe_Str__Url__Path
        assert str(result) == '/api/users'

        # With trailing slash in base
        result2 = '/api/' + path
        assert str(result2) == '/api/users'

        # Base with slash, path with slash
        result3 = '/api/' + Safe_Str__Url__Path('/users')
        assert str(result3) == '/api/users'


    def test_api_path_patterns(self):
        """Test common API path patterns"""
        assert Safe_Str__Url__Path('/api/v1/users'                      ) == '/api/v1/users'
        assert Safe_Str__Url__Path('/api/v1/users/123'                  ) == '/api/v1/users/123'
        assert Safe_Str__Url__Path('/api/v1/users/123/posts'            ) == '/api/v1/users/123/posts'
        assert Safe_Str__Url__Path('/api/v2/organizations/456/members'  ) == '/api/v2/organizations/456/members'
        assert Safe_Str__Url__Path('/graphql'                           ) == '/graphql'
        assert Safe_Str__Url__Path('/webhooks/github'                   ) == '/webhooks/github'

    def test_file_path_patterns(self):
        """Test file-like paths"""
        assert Safe_Str__Url__Path('/static/css/style.css'      ) == '/static/css/style.css'
        assert Safe_Str__Url__Path('/static/js/app.min.js'      ) == '/static/js/app.min.js'
        assert Safe_Str__Url__Path('/images/logo.png'           ) == '/images/logo.png'
        assert Safe_Str__Url__Path('/docs/api-reference.pdf'    ) == '/docs/api-reference.pdf'

    def test_string_representation(self):
        """Test string conversion methods"""
        path = Safe_Str__Url__Path('/api/v1/users')

        assert str(path)  == '/api/v1/users'
        assert repr(path) == "Safe_Str__Url__Path('/api/v1/users')"
        assert f"Path: {path}" == "Path: /api/v1/users"

    def test_equality_and_comparison(self):
        """Test path equality"""
        path1 = Safe_Str__Url__Path('/api/v1/users')
        path2 = Safe_Str__Url__Path('/api/v1/users')
        path3 = Safe_Str__Url__Path('/api/v2/users')

        assert path1 == path2
        assert path1 == '/api/v1/users'
        assert path1 != path3

    def test_immutability(self):
        """Test that paths are immutable"""
        path1 = Safe_Str__Url__Path('/api/users')
        path2 = Safe_Str__Url__Path('/api/users')

        assert path1 == path2
        assert path1 is not path2
        assert hash(path1) == hash(path2)

    def test_edge_cases(self):
        """Test various edge cases"""
        # Root path
        assert Safe_Str__Url__Path('/') == '/'

        # Single character segments
        assert Safe_Str__Url__Path('/a/b/c') == '/a/b/c'

        # Trailing slash
        assert Safe_Str__Url__Path('/api/'      ) == '/api/'
        assert Safe_Str__Url__Path('/api/v1/'   ) == '/api/v1/'

        # Multiple consecutive slashes (allowed but unusual)
        assert Safe_Str__Url__Path('/api//users') == '/api//users'

    def test_path_concatenation__edge_cases(self):
        """Test concatenation edge cases"""
        # Empty + non-empty (preserve original)
        path1 = Safe_Str__Url__Path('/api')
        path2 = Safe_Str__Url__Path('')
        assert str(path1 + path2) == '/api'  # ✓

        path3 = Safe_Str__Url__Path('')
        path4 = Safe_Str__Url__Path('/users')
        assert str(path3 + path4) == '/users'

        # Root path + segment (preserve absolute path)
        root = Safe_Str__Url__Path('/')
        segment = Safe_Str__Url__Path('api')
        assert str(root + segment) == '/api'

        # Both empty
        empty1 = Safe_Str__Url__Path('')
        empty2 = Safe_Str__Url__Path('')
        assert str(empty1 + empty2) == ''

        # Multiple slashes get normalized
        path5 = Safe_Str__Url__Path('/api/')
        path6 = Safe_Str__Url__Path('/users')
        assert str(path5 + path6) == '/api/users'