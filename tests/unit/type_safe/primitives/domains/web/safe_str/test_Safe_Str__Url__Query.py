import pytest
from unittest                                                                       import TestCase
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Query     import Safe_Str__Url__Query, TYPE_SAFE_STR__URL__QUERY__MAX_LENGTH


class test_Safe_Str__Url__Query(TestCase):

    def test_init(self):
        assert Safe_Str__Url__Query() == ''

    def test_basic_queries(self):
        """Test basic query string validation"""
        assert Safe_Str__Url__Query('q=test'        ) == 'q=test'
        assert Safe_Str__Url__Query('search=hello'  ) == 'search=hello'
        assert Safe_Str__Url__Query('id=123'        ) == 'id=123'

    def test_multiple_parameters(self):
        """Test query strings with multiple parameters"""
        assert Safe_Str__Url__Query('page=1&limit=10'              ) == 'page=1&limit=10'
        assert Safe_Str__Url__Query('q=test&sort=desc&page=2'      ) == 'q=test&sort=desc&page=2'
        assert Safe_Str__Url__Query('a=1&b=2&c=3&d=4'              ) == 'a=1&b=2&c=3&d=4'

    def test_parameters_with_special_characters(self):
        """Test parameters with hyphens and underscores"""
        assert Safe_Str__Url__Query('user-id=123'                  ) == 'user-id=123'
        assert Safe_Str__Url__Query('user_id=456'                  ) == 'user_id=456'
        assert Safe_Str__Url__Query('created-at=2024-01-01'        ) == 'created-at=2024-01-01'
        assert Safe_Str__Url__Query('sort_by=name&order_by=asc'    ) == 'sort_by=name&order_by=asc'

    def test_url_encoding(self):
        """Test query strings with percent-encoded values"""
        assert Safe_Str__Url__Query('q=hello%20world'                      ) == 'q=hello%20world'
        assert Safe_Str__Url__Query('text=%22quoted%22'                    ) == 'text=%22quoted%22'
        assert Safe_Str__Url__Query('url=https%3A%2F%2Fexample.com'        ) == 'url=https%3A%2F%2Fexample.com'
        assert Safe_Str__Url__Query('email=user%40example.com'             ) == 'email=user%40example.com'

    def test_plus_signs(self):
        """Test plus signs as space encoding in query strings"""
        assert Safe_Str__Url__Query('q=hello+world'            ) == 'q=hello+world'
        assert Safe_Str__Url__Query('text=test+value+here'     ) == 'text=test+value+here'
        assert Safe_Str__Url__Query('search=python+tutorial'   ) == 'search=python+tutorial'

    def test_whitespace_handling(self):
        """Test trimming of leading/trailing whitespace"""
        assert Safe_Str__Url__Query('  q=test  '       ) == 'q=test'
        assert Safe_Str__Url__Query('\tpage=1\n'       ) == 'page=1'
        assert Safe_Str__Url__Query('  id=123  '       ) == 'id=123'

    def test_empty_values(self):
        """Test that empty and None values are handled correctly"""
        assert Safe_Str__Url__Query(None) == ''
        assert Safe_Str__Url__Query(''  ) == ''

    def test_parameter_formats(self):
        """Test different query parameter formats"""
        # Flag parameters (no value)
        assert Safe_Str__Url__Query('debug'             ) == 'debug'
        assert Safe_Str__Url__Query('verbose&debug'     ) == 'verbose&debug'

        # Empty values
        assert Safe_Str__Url__Query('param='            ) == 'param='
        assert Safe_Str__Url__Query('a=&b=2'            ) == 'a=&b=2'

        # Numeric values
        assert Safe_Str__Url__Query('count=100'         ) == 'count=100'
        assert Safe_Str__Url__Query('price=19.99'       ) == 'price=19.99'
        assert Safe_Str__Url__Query('page=1&limit=20&offset=40') == 'page=1&limit=20&offset=40'

    def test_special_encoded_values(self):
        """Test query strings with special encoded values"""
        # URLs as values
        assert Safe_Str__Url__Query('redirect=https%3A%2F%2Fexample.com') == 'redirect=https%3A%2F%2Fexample.com'

        # Dates
        assert Safe_Str__Url__Query('date=2024-01-01'                   ) == 'date=2024-01-01'
        assert Safe_Str__Url__Query('from=2024-01-01&to=2024-12-31'     ) == 'from=2024-01-01&to=2024-12-31'

    def test_array_parameters(self):
        """Test array/list parameter conventions"""
        # Same key multiple times
        assert Safe_Str__Url__Query('tags=python&tags=django'   ) == 'tags=python&tags=django'
        assert Safe_Str__Url__Query('ids=1&ids=2&ids=3'         ) == 'ids=1&ids=2&ids=3'
        assert Safe_Str__Url__Query('color=red&color=blue'      ) == 'color=red&color=blue'

    def test_invalid_queries(self):
        """Test that invalid query strings are rejected"""
        # Leading question mark (not part of query string itself)
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Query('?q=test')
        assert "does not match required pattern" in str(exc_info.value)

        # Fragment/hash
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Query('q=test#section')
        assert "does not match required pattern" in str(exc_info.value)

        # Unencoded spaces
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Query('q=hello world')
        assert "does not match required pattern" in str(exc_info.value)

        # Invalid special characters
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Query('q=<script>')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Query('param="quoted"')
        assert "does not match required pattern" in str(exc_info.value)

    def test_max_length_validation(self):
        """Test max length enforcement"""
        # Within limit
        long_query = 'param=' + 'a' * 2000
        assert len(Safe_Str__Url__Query(long_query)) > 0

        # Exceeds limit
        with pytest.raises(ValueError) as exc_info:
            very_long_query = 'param=' + 'a' * TYPE_SAFE_STR__URL__QUERY__MAX_LENGTH
            Safe_Str__Url__Query(very_long_query)
        assert f"exceeds maximum length of {TYPE_SAFE_STR__URL__QUERY__MAX_LENGTH}" in str(exc_info.value)

    def test_query_concatenation__query_plus_query(self):
        """Test Query + Query = Query with & separator"""
        query1 = Safe_Str__Url__Query('page=1')
        query2 = Safe_Str__Url__Query('limit=10')
        
        result = query1 + query2
        assert type(result) is Safe_Str__Url__Query
        assert str(result) == 'page=1&limit=10'

        # Multiple concatenations
        query3 = Safe_Str__Url__Query('sort=desc')
        result2 = query1 + query2 + query3
        assert str(result2) == 'page=1&limit=10&sort=desc'

    def test_query_concatenation__with_empty(self):
        """Test Query concatenation with empty strings"""
        query = Safe_Str__Url__Query('page=1')
        empty = Safe_Str__Url__Query('')
        
        result1 = query + empty
        assert str(result1) == 'page=1'

        result2 = empty + query
        assert str(result2) == 'page=1'

    def test_query_concatenation__query_plus_string(self):
        """Test Query + string = Query"""
        query = Safe_Str__Url__Query('page=1')
        
        result = query + '&limit=10'
        assert type(result) is Safe_Str__Url__Query
        assert str(result) == 'page=1&limit=10'

        result2 = query + '&sort=desc&order=asc'
        assert str(result2) == 'page=1&sort=desc&order=asc'

    def test_common_query_patterns(self):
        """Test common query string patterns"""
        # Pagination
        assert Safe_Str__Url__Query('page=1&per_page=25'       ) == 'page=1&per_page=25'
        assert Safe_Str__Url__Query('offset=0&limit=100'       ) == 'offset=0&limit=100'

        # Sorting
        assert Safe_Str__Url__Query('sort=name&order=asc'      ) == 'sort=name&order=asc'
        assert Safe_Str__Url__Query('sort_by=created_at&direction=desc') == 'sort_by=created_at&direction=desc'

        # Filtering
        assert Safe_Str__Url__Query('status=active&role=admin' ) == 'status=active&role=admin'
        assert Safe_Str__Url__Query('min_price=10&max_price=100') == 'min_price=10&max_price=100'

        # Search
        assert Safe_Str__Url__Query('q=python+tutorial'        ) == 'q=python+tutorial'
        assert Safe_Str__Url__Query('search=test&category=blog') == 'search=test&category=blog'

    def test_string_representation(self):
        """Test string conversion methods"""
        query = Safe_Str__Url__Query('page=1&limit=10')
        
        assert str(query)  == 'page=1&limit=10'
        assert repr(query) == "Safe_Str__Url__Query('page=1&limit=10')"
        assert f"Query: {query}" == "Query: page=1&limit=10"

    def test_equality_and_comparison(self):
        """Test query equality"""
        query1 = Safe_Str__Url__Query('page=1&limit=10')
        query2 = Safe_Str__Url__Query('page=1&limit=10')
        query3 = Safe_Str__Url__Query('page=2&limit=10')

        assert query1 == query2
        assert query1 == 'page=1&limit=10'
        assert query1 != query3

    def test_immutability(self):
        """Test that queries are immutable"""
        query1 = Safe_Str__Url__Query('page=1&limit=10')
        query2 = Safe_Str__Url__Query('page=1&limit=10')

        assert query1 == query2
        assert query1 is not query2
        assert hash(query1) == hash(query2)

    def test_edge_cases(self):
        """Test various edge cases"""
        # Single parameter
        assert Safe_Str__Url__Query('id=1') == 'id=1'

        # Parameter with no equals sign (flag)
        assert Safe_Str__Url__Query('flag') == 'flag'

        # Multiple ampersands (unusual but valid)
        assert Safe_Str__Url__Query('a=1&&b=2') == 'a=1&&b=2'

        # Trailing ampersand
        assert Safe_Str__Url__Query('page=1&') == 'page=1&'

        # Leading ampersand
        assert Safe_Str__Url__Query('&page=1') == '&page=1'