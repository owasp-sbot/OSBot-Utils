import pytest
from unittest                                                                           import TestCase
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Cache_Control import Safe_Str__Http__Cache_Control


class test_Safe_Str__Http__Cache_Control(TestCase):

    def test__init__(self):                                                             # Test Safe_Str__Http__Cache_Control initialization
        cache = Safe_Str__Http__Cache_Control('no-cache')
        assert type(cache)            is Safe_Str__Http__Cache_Control
        assert str(cache)             == 'no-cache'
        assert cache                  == 'no-cache'

    def test__simple_directives(self):                                                  # Test simple cache directive values
        assert Safe_Str__Http__Cache_Control('no-cache'      ) == 'no-cache'
        assert Safe_Str__Http__Cache_Control('no-store'      ) == 'no-store'
        assert Safe_Str__Http__Cache_Control('public'        ) == 'public'
        assert Safe_Str__Http__Cache_Control('private'       ) == 'private'
        assert Safe_Str__Http__Cache_Control('must-revalidate') == 'must-revalidate'
        assert Safe_Str__Http__Cache_Control('proxy-revalidate') == 'proxy-revalidate'
        assert Safe_Str__Http__Cache_Control('no-transform'  ) == 'no-transform'
        assert Safe_Str__Http__Cache_Control('immutable'     ) == 'immutable'
        assert Safe_Str__Http__Cache_Control('only-if-cached') == 'only-if-cached'

    def test__directives_with_values(self):                                             # Test cache directives with time values
        assert Safe_Str__Http__Cache_Control('max-age=3600'  ) == 'max-age=3600'
        assert Safe_Str__Http__Cache_Control('s-maxage=86400') == 's-maxage=86400'
        assert Safe_Str__Http__Cache_Control('max-stale=600' ) == 'max-stale=600'
        assert Safe_Str__Http__Cache_Control('min-fresh=300' ) == 'min-fresh=300'
        assert Safe_Str__Http__Cache_Control('stale-while-revalidate=86400') == 'stale-while-revalidate=86400'
        assert Safe_Str__Http__Cache_Control('stale-if-error=259200') == 'stale-if-error=259200'

    def test__multiple_directives(self):                                                # Test multiple cache directives combined
        assert Safe_Str__Http__Cache_Control('public, max-age=3600') == 'public, max-age=3600'
        assert Safe_Str__Http__Cache_Control('private, must-revalidate') == 'private, must-revalidate'
        assert Safe_Str__Http__Cache_Control('no-cache, no-store, must-revalidate') == 'no-cache, no-store, must-revalidate'
        assert Safe_Str__Http__Cache_Control('public, max-age=31536000, immutable') == 'public, max-age=31536000, immutable'

    def test__common_response_directives(self):                                         # Test common response Cache-Control patterns
        assert Safe_Str__Http__Cache_Control('max-age=0'     ) == 'max-age=0'
        assert Safe_Str__Http__Cache_Control('no-cache, no-store, must-revalidate') == 'no-cache, no-store, must-revalidate'
        assert Safe_Str__Http__Cache_Control('public, max-age=31536000, immutable') == 'public, max-age=31536000, immutable'
        assert Safe_Str__Http__Cache_Control('private, max-age=0, no-cache') == 'private, max-age=0, no-cache'

    def test__common_request_directives(self):                                          # Test common request Cache-Control patterns
        assert Safe_Str__Http__Cache_Control('max-age=0'     ) == 'max-age=0'
        assert Safe_Str__Http__Cache_Control('no-cache'      ) == 'no-cache'
        assert Safe_Str__Http__Cache_Control('max-stale'     ) == 'max-stale'
        assert Safe_Str__Http__Cache_Control('only-if-cached') == 'only-if-cached'

    def test__complex_combinations(self):                                               # Test complex real-world combinations
        assert Safe_Str__Http__Cache_Control('max-age=604800, stale-while-revalidate=86400') == 'max-age=604800, stale-while-revalidate=86400'
        assert Safe_Str__Http__Cache_Control('s-maxage=600, max-age=300') == 's-maxage=600, max-age=300'
        assert Safe_Str__Http__Cache_Control('public, max-age=3600, stale-if-error=86400') == 'public, max-age=3600, stale-if-error=86400'

    def test__age_values(self):                                                         # Test various max-age time values
        assert Safe_Str__Http__Cache_Control('max-age=60'    ) == 'max-age=60'         # 1 minute
        assert Safe_Str__Http__Cache_Control('max-age=3600'  ) == 'max-age=3600'       # 1 hour
        assert Safe_Str__Http__Cache_Control('max-age=86400' ) == 'max-age=86400'      # 1 day
        assert Safe_Str__Http__Cache_Control('max-age=604800') == 'max-age=604800'     # 1 week
        assert Safe_Str__Http__Cache_Control('max-age=2592000') == 'max-age=2592000'   # 30 days
        assert Safe_Str__Http__Cache_Control('max-age=31536000') == 'max-age=31536000' # 1 year

    def test__whitespace_handling(self):                                                # Test trim_whitespace = True
        assert Safe_Str__Http__Cache_Control('  no-cache  '  ) == 'no-cache'
        assert Safe_Str__Http__Cache_Control('public, max-age=3600  ') == 'public, max-age=3600'
        assert Safe_Str__Http__Cache_Control('  max-age=60' ) == 'max-age=60'

    def test__numeric_conversion(self):                                                 # Test conversion from numeric types
        assert Safe_Str__Http__Cache_Control(12345           ) == '12345'
        assert Safe_Str__Http__Cache_Control(999             ) == '999'

    def test__invalid_characters(self):                                                 # Test regex character replacement
        assert Safe_Str__Http__Cache_Control('no-cache<script>') == 'no-cache_script_'
        assert Safe_Str__Http__Cache_Control('max-age@3600'  ) == 'max-age_3600'
        assert Safe_Str__Http__Cache_Control('public/private') == 'public_private'
        assert Safe_Str__Http__Cache_Control('no-cache:test' ) == 'no-cache_test'

    def test__empty_values(self):                                                       # Test allow_empty = True
        assert Safe_Str__Http__Cache_Control(None            ) == ''
        assert Safe_Str__Http__Cache_Control(''              ) == ''
        assert Safe_Str__Http__Cache_Control('   '           ) == ''                    # Spaces only (will be trimmed)

    def test__max_length(self):                                                         # Test TYPE_SAFE_STR__HTTP__CACHE_CONTROL__MAX_LENGTH = 256
        valid_256   = 'a' * 256
        invalid_257 = 'a' * 257

        assert Safe_Str__Http__Cache_Control(valid_256       ) == valid_256

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Cache_Control(invalid_257)
        assert "in Safe_Str__Http__Cache_Control, value exceeds maximum length of 256" in str(exc_info.value)

    def test__cdn_patterns(self):                                                       # Test CDN-specific cache patterns
        assert Safe_Str__Http__Cache_Control('public, max-age=31536000, immutable') == 'public, max-age=31536000, immutable'
        assert Safe_Str__Http__Cache_Control('public, max-age=86400, s-maxage=604800') == 'public, max-age=86400, s-maxage=604800'

    def test__api_patterns(self):                                                       # Test API response cache patterns
        assert Safe_Str__Http__Cache_Control('private, no-store') == 'private, no-store'
        assert Safe_Str__Http__Cache_Control('no-cache, no-store, must-revalidate, max-age=0') == 'no-cache, no-store, must-revalidate, max-age=0'

    def test__static_asset_patterns(self):                                              # Test static asset cache patterns
        assert Safe_Str__Http__Cache_Control('public, max-age=31536000') == 'public, max-age=31536000'
        assert Safe_Str__Http__Cache_Control('public, max-age=604800, immutable') == 'public, max-age=604800, immutable'

    def test__str_and_repr(self):                                                       # Test string representations
        cache = Safe_Str__Http__Cache_Control('no-cache')

        assert str(cache)             == 'no-cache'
        assert f"{cache}"             == 'no-cache'
        assert f"Cache-Control: {cache}" == 'Cache-Control: no-cache'