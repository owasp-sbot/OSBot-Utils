import pytest
from unittest                                                                     import TestCase
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id   import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Slug import Safe_Str__Slug


class test_Safe_Str__Slug(TestCase):

    def test__init__(self):                                      # Test basic initialization
        with Safe_Str__Slug() as _:
            assert type(_)                      is Safe_Str__Slug
            assert _.regex.pattern              == r'[^a-z0-9\-]'            # Only lowercase, numbers, hyphens
            assert _.to_lower_case              is True                      # CRITICAL: Forces lowercase
            assert _.allow_empty                is True
            assert _.trim_whitespace            is True
            assert _.allow_all_replacement_char is True

    def test_valid_slugs(self):                                 # Test valid slug patterns
        # Basic slugs
        assert str(Safe_Str__Slug('my-blog-post'            )) == 'my-blog-post'
        assert str(Safe_Str__Slug('product-name-2024'       )) == 'product-name-2024'
        assert str(Safe_Str__Slug('about-us'                )) == 'about-us'
        assert str(Safe_Str__Slug('contact'                 )) == 'contact'

        # URL-friendly slugs
        assert str(Safe_Str__Slug('hello-world'             )) == 'hello-world'
        assert str(Safe_Str__Slug('first-post'              )) == 'first-post'
        assert str(Safe_Str__Slug('blog-post-123'           )) == 'blog-post-123'
        assert str(Safe_Str__Slug('article-2024-03-15'      )) == 'article-2024-03-15'

        # Product slugs
        assert str(Safe_Str__Slug('iphone-15-pro'           )) == 'iphone-15-pro'
        assert str(Safe_Str__Slug('macbook-air-m2'          )) == 'macbook-air-m2'
        assert str(Safe_Str__Slug('samsung-galaxy-s24'      )) == 'samsung-galaxy-s24'

        # SEO-friendly slugs
        assert str(Safe_Str__Slug('how-to-learn-python'     )) == 'how-to-learn-python'
        assert str(Safe_Str__Slug('best-practices-2024'     )) == 'best-practices-2024'
        assert str(Safe_Str__Slug('ultimate-guide'          )) == 'ultimate-guide'

        # Version slugs
        assert str(Safe_Str__Slug('v1-0-0'                  )) == 'v1-0-0'
        assert str(Safe_Str__Slug('release-2-3-4'           )) == 'release-2-3-4'
        assert str(Safe_Str__Slug('beta-1'                  )) == 'beta-1'

        # Edge cases
        assert str(Safe_Str__Slug(None)) == ''
        assert str(Safe_Str__Slug(''  )) == ''

    def test_lowercase_conversion(self):                        # Test automatic lowercase conversion
        # Uppercase converted to lowercase
        assert str(Safe_Str__Slug('HELLO-WORLD'             )) == 'hello-world'
        assert str(Safe_Str__Slug('Blog-Post'               )) == 'blog-post'
        assert str(Safe_Str__Slug('MyBlogPost'              )) == 'myblogpost'
        assert str(Safe_Str__Slug('PRODUCT_NAME'            )) == 'product_name'

        # Mixed case converted
        assert str(Safe_Str__Slug('Hello-World-2024'        )) == 'hello-world-2024'
        assert str(Safe_Str__Slug('iPhone-15-Pro'           )) == 'iphone-15-pro'
        assert str(Safe_Str__Slug('MacBook-Air'             )) == 'macbook-air'
        assert str(Safe_Str__Slug('API-Documentation'       )) == 'api-documentation'

        # CamelCase becomes lowercase
        assert str(Safe_Str__Slug('CamelCaseString'         )) == 'camelcasestring'
        assert str(Safe_Str__Slug('PascalCase'              )) == 'pascalcase'
        assert str(Safe_Str__Slug('mixedCASE'               )) == 'mixedcase'

    def test_sanitization(self):                                # Test character replacement
        # Spaces replaced with underscores (due to replacement_char default)
        assert str(Safe_Str__Slug('hello world'             )) == 'hello_world'
        assert str(Safe_Str__Slug('my blog post'            )) == 'my_blog_post'
        assert str(Safe_Str__Slug('product name 2024'       )) == 'product_name_2024'

        # Underscores preserved (they're not in the regex)
        assert str(Safe_Str__Slug('hello_world'             )) == 'hello_world'
        assert str(Safe_Str__Slug('my_blog_post'            )) == 'my_blog_post'

        # Special characters replaced with underscore
        assert str(Safe_Str__Slug('hello@world'             )) == 'hello_world'
        assert str(Safe_Str__Slug('price:$100'              )) == 'price__100'
        assert str(Safe_Str__Slug('100% off'                )) == '100__off'
        assert str(Safe_Str__Slug('Q&A section'             )) == 'q_a_section'
        assert str(Safe_Str__Slug("it's working"            )) == 'it_s_working'

        # Dots replaced
        assert str(Safe_Str__Slug('version.1.0'             )) == 'version_1_0'
        assert str(Safe_Str__Slug('file.name.ext'           )) == 'file_name_ext'

        # Slashes replaced
        assert str(Safe_Str__Slug('path/to/page'            )) == 'path_to_page'
        assert str(Safe_Str__Slug('category\\subcategory'   )) == 'category_subcategory'

        # Unicode replaced and lowercased
        assert str(Safe_Str__Slug('Café Menu'               )) == 'caf__menu'
        assert str(Safe_Str__Slug('Résumé Tips'             )) == 'r_sum__tips'
        assert str(Safe_Str__Slug('Naïve Approach'          )) == 'na_ve_approach'
        assert str(Safe_Str__Slug('Hello 世界'              )) == 'hello___'

        # Multiple special chars become underscores
        assert str(Safe_Str__Slug('hello!!!world'           )) == 'hello___world'
        assert str(Safe_Str__Slug('price: $100 (sale)'      )) == 'price___100__sale_'

    def test_hyphen_handling(self):                             # Test hyphen preservation and handling
        # Single hyphens preserved
        assert str(Safe_Str__Slug('one-two-three'           )) == 'one-two-three'

        # Multiple consecutive hyphens preserved
        assert str(Safe_Str__Slug('one--two'                )) == 'one--two'
        assert str(Safe_Str__Slug('---'                     )) == '---'

        # Starting/ending with hyphens
        assert str(Safe_Str__Slug('-start'                  )) == '-start'
        assert str(Safe_Str__Slug('end-'                    )) == 'end-'
        assert str(Safe_Str__Slug('-both-'                  )) == '-both-'

        # Mixed with sanitization (uppercase becomes lowercase)
        assert str(Safe_Str__Slug('Hello-World'             )) == 'hello-world'
        assert str(Safe_Str__Slug('One_Two-Three'           )) == 'one_two-three'

    def test_trimming(self):                                    # Test whitespace trimming
        assert str(Safe_Str__Slug('  my-slug  '             )) == 'my-slug'
        assert str(Safe_Str__Slug('\tblog-post\t'           )) == 'blog-post'
        assert str(Safe_Str__Slug('\n product-name \n'      )) == 'product-name'
        assert str(Safe_Str__Slug('  UPPERCASE  '           )) == 'uppercase'

    def test_type_conversion(self):                             # Test conversion from other types
        # From integer
        assert str(Safe_Str__Slug(123      )) == '123'
        assert str(Safe_Str__Slug(0        )) == '0'

        # From float (dot replaced)
        assert str(Safe_Str__Slug(123.456  )) == '123_456'
        assert str(Safe_Str__Slug(1.0      )) == '1_0'

        # From boolean (lowercased)
        assert str(Safe_Str__Slug(True     )) == 'true'        # Lowercased!
        assert str(Safe_Str__Slug(False    )) == 'false'       # Lowercased!

    def test_in_type_safe_schema(self):                         # Test usage in Type_Safe classes
        class Schema__Page(Type_Safe):
            url_slug     : Safe_Str__Slug
            product_slug : Safe_Str__Slug
            category_slug: Safe_Str__Slug

        with Schema__Page() as _:
            # Auto-initialization
            assert type(_.url_slug     ) is Safe_Str__Slug
            assert type(_.product_slug ) is Safe_Str__Slug
            assert type(_.category_slug) is Safe_Str__Slug

            # Setting with raw strings (auto-conversion)
            _.url_slug = 'My Blog Post Title!'
            assert _.url_slug == 'my_blog_post_title_'         # Lowercased and sanitized

            # Setting with uppercase
            _.product_slug = 'iPhone 15 Pro Max'
            assert _.product_slug == 'iphone_15_pro_max'       # Spaces and case handled

            # Setting with Safe_Str__Slug
            _.category_slug = Safe_Str__Slug('Tech & Gadgets')
            assert _.category_slug == 'tech___gadgets'

            # JSON serialization
            json_data = _.json()
            assert json_data['url_slug'     ] == 'my_blog_post_title_'
            assert json_data['product_slug' ] == 'iphone_15_pro_max'
            assert json_data['category_slug'] == 'tech___gadgets'

    def test_common_slug_patterns(self):                        # Test real-world slug patterns
        # Blog post slugs
        assert str(Safe_Str__Slug('10 Tips for Better Code' )) == '10_tips_for_better_code'
        assert str(Safe_Str__Slug('Why Python is Awesome!'  )) == 'why_python_is_awesome_'
        assert str(Safe_Str__Slug('The Ultimate Guide (2024)')) == 'the_ultimate_guide__2024_'

        # E-commerce product slugs
        assert str(Safe_Str__Slug('Apple iPhone 15 Pro 256GB')) == 'apple_iphone_15_pro_256gb'
        assert str(Safe_Str__Slug('Nike Air Max 90'        )) == 'nike_air_max_90'
        assert str(Safe_Str__Slug('Sony WH-1000XM5'        )) == 'sony_wh-1000xm5'

        # Category slugs
        assert str(Safe_Str__Slug('Electronics & Gadgets'   )) == 'electronics___gadgets'
        assert str(Safe_Str__Slug('Home & Garden'           )) == 'home___garden'
        assert str(Safe_Str__Slug('Sports/Outdoors'         )) == 'sports_outdoors'

        # Documentation slugs
        assert str(Safe_Str__Slug('Getting Started'         )) == 'getting_started'
        assert str(Safe_Str__Slug('API Reference v2.0'      )) == 'api_reference_v2_0'
        assert str(Safe_Str__Slug('FAQ - Frequently Asked'  )) == 'faq_-_frequently_asked'

    def test_seo_friendly_slugs(self):                          # Test SEO best practices
        # Long titles become slugs
        long_title = 'The Complete Guide to Learning Python Programming in 2024'
        assert str(Safe_Str__Slug(long_title)) == 'the_complete_guide_to_learning_python_programming_in_2024'

        # Question titles
        assert str(Safe_Str__Slug('How to Learn Python?'    )) == 'how_to_learn_python_'
        assert str(Safe_Str__Slug('What is Type Safety?'    )) == 'what_is_type_safety_'
        assert str(Safe_Str__Slug('Why Use Safe_Str?'       )) == 'why_use_safe_str_'

        # List titles
        assert str(Safe_Str__Slug('Top 10 Python Libraries' )) == 'top_10_python_libraries'
        assert str(Safe_Str__Slug('5 Best Practices'        )) == '5_best_practices'

    def test_edge_cases(self):                                  # Test edge cases
        # Only hyphens
        assert str(Safe_Str__Slug('-'                       )) == '-'
        assert str(Safe_Str__Slug('--'                      )) == '--'
        assert str(Safe_Str__Slug('---'                     )) == '---'

        # Numbers only
        assert str(Safe_Str__Slug('123'                     )) == '123'
        assert str(Safe_Str__Slug('2024'                    )) == '2024'
        assert str(Safe_Str__Slug('404'                     )) == '404'

        # Single character
        assert str(Safe_Str__Slug('a'                       )) == 'a'
        assert str(Safe_Str__Slug('A'                       )) == 'a'  # Lowercased
        assert str(Safe_Str__Slug('1'                       )) == '1'
        assert str(Safe_Str__Slug('-'                       )) == '-'

    def test_max_length(self):                                  # Test length constraints
        # Should inherit from Safe_Str__Id (128)
        max_length = 128
        max_slug = 'a' * max_length
        assert str(Safe_Str__Slug(max_slug)) == max_slug
        assert len(Safe_Str__Slug(max_slug)) == max_length

        # Exceeds max length
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Slug('a' * (max_length + 1))
        assert f"value exceeds maximum length of {max_length}" in str(exc_info.value)

    def test_difference_from_safe_id(self):                     # Compare with parent Safe_Str__Id
        test_string = 'My_Blog_Post_2024'

        # Safe_Str__Slug forces lowercase
        slug = Safe_Str__Slug(test_string)
        assert str(slug) == 'my_blog_post_2024'                # Lowercase, underscores preserved

        # Safe_Str__Id preserves case
        id_val = Safe_Str__Id(test_string)
        assert str(id_val) == 'My_Blog_Post_2024'              # Case preserved

        # This distinction is important for:
        # - SEO-friendly URLs (slugs must be lowercase)
        # - Consistent URL patterns
        # - Better readability in URLs

    def test_url_compatibility(self):                           # Test URL-safe characteristics
        # No uppercase letters (URL case-insensitive)
        assert 'A' not in str(Safe_Str__Slug('ABC'))
        assert 'Z' not in str(Safe_Str__Slug('XYZ'))

        # Spaces become underscores (not %20)
        result = str(Safe_Str__Slug('hello world'))
        assert ' ' not in result
        assert result == 'hello_world'

        # No special URL characters
        result = str(Safe_Str__Slug('path?query=value'))
        assert '?' not in result
        assert '=' not in result

        result = str(Safe_Str__Slug('anchor#section'))
        assert '#' not in result

        result = str(Safe_Str__Slug('param&other'))
        assert '&' not in result

        # Safe for use in URLs without encoding
        slug = Safe_Str__Slug('My Blog Post: The Ultimate Guide!')
        url = f"https://example.com/blog/{slug}"
        assert url == "https://example.com/blog/my_blog_post__the_ultimate_guide_"

    def test_note_about_slug_behavior(self):                    # Document actual vs expected behavior
        # NOTE: The current implementation uses underscore as replacement_char
        # This is inherited from Safe_Str base class default
        # Traditional slugs typically use hyphens for spaces

        # Current behavior (underscore replacement)
        assert str(Safe_Str__Slug('hello world')) == 'hello_world'

        # If you want hyphen replacement for spaces, you'd need:
        # 1. Override replacement_char = '-' in Safe_Str__Slug
        # 2. Or handle space-to-hyphen conversion specially

        # The regex correctly excludes uppercase and allows hyphens
        # But spaces get replaced with the default underscore
        # This might be intentional for your use case