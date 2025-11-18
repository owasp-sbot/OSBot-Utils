import re

import pytest
from unittest                                                                           import TestCase
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Path_Query   import Safe_Str__Url__Path_Query, TYPE_SAFE_STR__URL__PATH_QUERY__MAX_LENGTH
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Query        import Safe_Str__Url__Query


class test_Safe_Str__Url__Path_Query(TestCase):

    def test_init(self):
        assert Safe_Str__Url__Path_Query() == ''

    def test_basic_path_query(self):
        """Test basic path with query validation"""
        assert Safe_Str__Url__Path_Query('/api/v1/users?page=1'        ) == '/api/v1/users?page=1'
        assert Safe_Str__Url__Path_Query('/search?q=test'               ) == '/search?q=test'
        assert Safe_Str__Url__Path_Query('/products/123?include=details') == '/products/123?include=details'

    def test_path_only(self):
        """Test paths without query parameters"""
        assert Safe_Str__Url__Path_Query('/'                ) == '/'
        assert Safe_Str__Url__Path_Query('/api'             ) == '/api'
        assert Safe_Str__Url__Path_Query('/api/v1/users'    ) == '/api/v1/users'
        assert Safe_Str__Url__Path_Query('/products/123'    ) == '/products/123'

    def test_complex_query_parameters(self):
        """Test paths with multiple query parameters"""
        assert Safe_Str__Url__Path_Query('/api/users?page=1&limit=10'                  ) == '/api/users?page=1&limit=10'
        assert Safe_Str__Url__Path_Query('/search?q=test&sort=desc&page=2'             ) == '/search?q=test&sort=desc&page=2'
        assert Safe_Str__Url__Path_Query('/products?category=electronics&min_price=100') == '/products?category=electronics&min_price=100'

    def test_url_encoding_in_query(self):
        """Test paths with encoded query parameters"""
        assert Safe_Str__Url__Path_Query('/search?q=hello%20world'                 ) == '/search?q=hello%20world'
        assert Safe_Str__Url__Path_Query('/search?q=test+value'                    ) == '/search?q=test+value'
        assert Safe_Str__Url__Path_Query('/api?url=https%3A%2F%2Fexample.com'      ) == '/api?url=https%3A%2F%2Fexample.com'
        assert Safe_Str__Url__Path_Query('/search?text=%22quoted%22'               ) == '/search?text=%22quoted%22'

    def test_url_encoding_in_path(self):
        """Test paths with encoded path segments"""
        assert Safe_Str__Url__Path_Query('/caf%C3%A9?menu=drinks'          ) == '/caf%C3%A9?menu=drinks'
        assert Safe_Str__Url__Path_Query('/path%20with%20spaces?param=value') == '/path%20with%20spaces?param=value'
        assert Safe_Str__Url__Path_Query('/%7Euser?page=home'              ) == '/%7Euser?page=home'

    def test_file_paths_with_queries(self):
        """Test file paths with query parameters"""
        assert Safe_Str__Url__Path_Query('/docs/readme.md?version=latest'  ) == '/docs/readme.md?version=latest'
        assert Safe_Str__Url__Path_Query('/static/css/style.css?v=2.0'     ) == '/static/css/style.css?v=2.0'
        assert Safe_Str__Url__Path_Query('/images/photo.jpg?size=large'    ) == '/images/photo.jpg?size=large'

    def test_whitespace_handling(self):
        """Test trimming of leading/trailing whitespace"""
        assert Safe_Str__Url__Path_Query('  /api/users?page=1  '   ) == '/api/users?page=1'
        assert Safe_Str__Url__Path_Query('\n/search?q=test\t'      ) == '/search?q=test'
        assert Safe_Str__Url__Path_Query('  /products?id=123  '    ) == '/products?id=123'

    def test_empty_values(self):
        """Test that empty and None values are handled correctly"""
        assert Safe_Str__Url__Path_Query(None) == ''
        assert Safe_Str__Url__Path_Query(''  ) == ''

    def test_empty_query_string(self):
        """Test paths with empty query string (just ?)"""
        assert Safe_Str__Url__Path_Query('/api/users?'  ) == '/api/users?'
        assert Safe_Str__Url__Path_Query('/search?'     ) == '/search?'

    def test_invalid_path_query(self):
        """Test that invalid path+query combinations are rejected"""
        # Fragment not allowed
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Path_Query('/page?q=test#section')
        assert "does not match required pattern" in str(exc_info.value)

        # Unencoded spaces in path
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Path_Query('/path with spaces?q=test')
        assert "does not match required pattern" in str(exc_info.value)

        # Unencoded spaces in query
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Path_Query('/search?q=hello world')
        assert "does not match required pattern" in str(exc_info.value)

        # Invalid characters
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Path_Query('/api?param=<script>')
        assert "does not match required pattern" in str(exc_info.value)

    def test_max_length_validation(self):
        """Test max length enforcement"""
        # Within limit
        long_path = '/api/' + 'a' * 2000 + '?param=value'
        assert len(Safe_Str__Url__Path_Query(long_path)) > 0

        # Exceeds limit
        with pytest.raises(ValueError) as exc_info:
            very_long = '/api/' + 'a' * TYPE_SAFE_STR__URL__PATH_QUERY__MAX_LENGTH
            Safe_Str__Url__Path_Query(very_long)
        assert f"exceeds maximum length of {TYPE_SAFE_STR__URL__PATH_QUERY__MAX_LENGTH}" in str(exc_info.value)

    def test_path_query_concatenation__with_query(self):
        """Test Path_Query + Query = Path_Query with proper separator"""
        base = Safe_Str__Url__Path_Query('/api/users?page=1')
        query = Safe_Str__Url__Query('limit=10')
        
        result = base + query
        assert type(result) is Safe_Str__Url__Path_Query
        assert str(result) == '/api/users?page=1&limit=10'

        # Path without query + Query
        base2 = Safe_Str__Url__Path_Query('/api/users')
        result2 = base2 + query
        assert str(result2) == '/api/users?limit=10'

        # Empty query
        result3 = base + Safe_Str__Url__Query('')
        assert str(result3) == '/api/users?page=1'

    def test_path_query_concatenation__with_string(self):
        """Test Path_Query + string = Path_Query"""
        base = Safe_Str__Url__Path_Query('/api/users?page=1')
        
        result = base + '&limit=10'
        assert type(result) is Safe_Str__Url__Path_Query
        assert str(result) == '/api/users?page=1&limit=10'

        # Path without query
        base2 = Safe_Str__Url__Path_Query('/api/users')
        result2 = base2 + '/more'
        assert str(result2) == '/api/users/more'

    def test_api_patterns(self):
        """Test common API path+query patterns"""
        # Pagination
        assert Safe_Str__Url__Path_Query('/api/users?page=1&per_page=25'           ) == '/api/users?page=1&per_page=25'
        assert Safe_Str__Url__Path_Query('/api/products?offset=0&limit=100'        ) == '/api/products?offset=0&limit=100'

        # Filtering
        assert Safe_Str__Url__Path_Query('/api/users?status=active&role=admin'     ) == '/api/users?status=active&role=admin'
        assert Safe_Str__Url__Path_Query('/api/products?category=electronics'      ) == '/api/products?category=electronics'

        # Sorting
        assert Safe_Str__Url__Path_Query('/api/users?sort=name&order=asc'          ) == '/api/users?sort=name&order=asc'
        assert Safe_Str__Url__Path_Query('/api/posts?sort_by=created_at&desc=true' ) == '/api/posts?sort_by=created_at&desc=true'

        # Search
        assert Safe_Str__Url__Path_Query('/search?q=python+tutorial&category=blog' ) == '/search?q=python+tutorial&category=blog'
        assert Safe_Str__Url__Path_Query('/api/search?query=test&limit=20'         ) == '/api/search?query=test&limit=20'

        # Includes/expansions
        assert Safe_Str__Url__Path_Query('/api/users/123?include=posts,comments'   ) == '/api/users/123?include=posts,comments'
        assert Safe_Str__Url__Path_Query('/api/products/456?expand=category,vendor') == '/api/products/456?expand=category,vendor'

    def test_deep_paths_with_queries(self):
        """Test deeply nested paths with query parameters"""
        assert Safe_Str__Url__Path_Query('/api/v1/organizations/123/teams/456/members?active=true') == \
               '/api/v1/organizations/123/teams/456/members?active=true'
        
        assert Safe_Str__Url__Path_Query('/api/v2/users/789/posts/101/comments?page=2&sort=date') == \
               '/api/v2/users/789/posts/101/comments?page=2&sort=date'

    def test_string_representation(self):
        """Test string conversion methods"""
        path_query = Safe_Str__Url__Path_Query('/api/users?page=1&limit=10')
        
        assert str(path_query)  == '/api/users?page=1&limit=10'
        assert repr(path_query) == "Safe_Str__Url__Path_Query('/api/users?page=1&limit=10')"
        assert f"Request: {path_query}" == "Request: /api/users?page=1&limit=10"

    def test_equality_and_comparison(self):
        """Test path_query equality"""
        pq1 = Safe_Str__Url__Path_Query('/api/users?page=1')
        pq2 = Safe_Str__Url__Path_Query('/api/users?page=1')
        pq3 = Safe_Str__Url__Path_Query('/api/users?page=2')

        assert pq1 == pq2
        assert pq1 == '/api/users?page=1'
        assert pq1 != pq3

    def test_immutability(self):
        """Test that path_query objects are immutable"""
        pq1 = Safe_Str__Url__Path_Query('/api/users?page=1')
        pq2 = Safe_Str__Url__Path_Query('/api/users?page=1')

        assert pq1 == pq2
        assert pq1 is not pq2
        assert hash(pq1) == hash(pq2)

    def test_edge_cases(self):
        """Test various edge cases"""
        # Root path with query
        assert Safe_Str__Url__Path_Query('/?lang=en') == '/?lang=en'

        # Multiple question marks (invalid but caught by regex)
        with pytest.raises(ValueError):
            Safe_Str__Url__Path_Query('/path?q1=test?q2=value')

        # Trailing slash with query
        assert Safe_Str__Url__Path_Query('/api/?page=1') == '/api/?page=1'

        # Empty query value
        assert Safe_Str__Url__Path_Query('/api?param='     ) == '/api?param='
        assert Safe_Str__Url__Path_Query('/api?a=&b=2'     ) == '/api?a=&b=2'

        # Query with no equals sign (flag)
        assert Safe_Str__Url__Path_Query('/api?debug'      ) == '/api?debug'
        assert Safe_Str__Url__Path_Query('/api?verbose&debug') == '/api?verbose&debug'