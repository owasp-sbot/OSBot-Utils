# ═══════════════════════════════════════════════════════════════════════════════
# Tests for Html_Generator__For_Benchmarks
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                               import TestCase
from osbot_utils.helpers.performance.testing.Html_Generator__For_Benchmarks import Html_Generator__For_Benchmarks
from osbot_utils.testing.Pytest                                             import skip__if_not__in_github_actions


class test_Html_Generator__For_Benchmarks(TestCase):

    @classmethod
    def setUpClass(cls):
        skip__if_not__in_github_actions()
        cls.generator = Html_Generator__For_Benchmarks()

    def test__init__(self):                                                     # Test auto-initialization
        with self.generator as _:
            assert type(_).__name__ == 'Html_Generator__For_Benchmarks'

    # ═══════════════════════════════════════════════════════════════════════════
    # Paragraph Generation
    # ═══════════════════════════════════════════════════════════════════════════

    def test_generate_with_paragraphs__default(self):                           # Default parameters
        with self.generator as _:
            html = _.generate_with_paragraphs()

            assert '<html>'  in html
            assert '<body>'  in html
            assert '<p>'     in html
            assert html.count('<p>') == 10                                      # Default 10 paragraphs

    def test_generate_with_paragraphs__custom(self):                            # Custom paragraph count
        with self.generator as _:
            html = _.generate_with_paragraphs(num_paragraphs=5, words_per_para=10)

            assert html.count('<p>') == 5

    # ═══════════════════════════════════════════════════════════════════════════
    # Target Node Generation
    # ═══════════════════════════════════════════════════════════════════════════

    def test_generate_with_target_nodes__small(self):                           # Target ~100 nodes
        with self.generator as _:
            html = _.generate_with_target_nodes(100)

            assert '<html>' in html
            assert '<body>' in html
            assert len(html) > 100                                              # Has content

    def test_generate_with_target_nodes__large(self):                           # Target ~1000 nodes
        with self.generator as _:
            html = _.generate_with_target_nodes(1000)

            assert len(html) > 1000                                             # Larger content

    def test_generate_with_target_nodes__minimum(self):                         # Target minimum nodes
        with self.generator as _:
            html = _.generate_with_target_nodes(1)                              # Very small target

            assert '<html>' in html
            assert html.count('<p>') >= 1                                       # At least 1 paragraph

    # ═══════════════════════════════════════════════════════════════════════════
    # Preset Sizes - All Variants
    # ═══════════════════════════════════════════════════════════════════════════

    def test_generate__1(self):                                                 # 1 paragraph preset
        with self.generator as _:
            html = _.generate__1()

            assert '<html>'          in html
            assert html.count('<p>') == 1

    def test_generate__5(self):                                                 # 5 paragraphs preset
        with self.generator as _:
            html = _.generate__5()

            assert '<html>'          in html
            assert html.count('<p>') == 5

    def test_generate__10(self):                                                # 10 paragraphs preset
        with self.generator as _:
            html = _.generate__10()

            assert '<html>'          in html
            assert html.count('<p>') == 10

    def test_generate__50(self):                                                # 50 paragraphs preset
        with self.generator as _:
            html = _.generate__50()

            assert '<html>'          in html
            assert html.count('<p>') == 50

    def test_generate__100(self):                                               # 100 paragraphs preset
        with self.generator as _:
            html = _.generate__100()

            assert '<html>'          in html
            assert html.count('<p>') == 100

    def test_generate__200(self):                                               # 200 paragraphs preset
        with self.generator as _:
            html = _.generate__200()

            assert '<html>'          in html
            assert html.count('<p>') == 200

    def test_generate__300(self):                                               # 300 paragraphs preset
        with self.generator as _:
            html = _.generate__300()

            assert '<html>'          in html
            assert html.count('<p>') == 300

    def test_generate__500(self):                                               # 500 paragraphs preset
        with self.generator as _:
            html = _.generate__500()

            assert '<html>'          in html
            assert html.count('<p>') == 500

    def test_generate__1_000(self):                                             # 1,000 paragraphs preset
        with self.generator as _:
            html = _.generate__1_000()

            assert '<html>'          in html
            assert html.count('<p>') == 1_000

    def test_generate__10_000(self):                                            # 10,000 paragraphs preset
        with self.generator as _:
            html = _.generate__10_000()

            assert '<html>'          in html
            assert html.count('<p>') == 10_000
            assert len(html)         > 100_000                                  # Substantial size

    def test_generate__100_000(self):                                           # 100,000 paragraphs preset
        with self.generator as _:
            html = _.generate__100_000()

            assert '<html>'          in html
            assert html.count('<p>') == 100_000
            assert len(html)         > 1_000_000                                # Very large

    # ═══════════════════════════════════════════════════════════════════════════
    # Special Structures
    # ═══════════════════════════════════════════════════════════════════════════

    def test_generate_with_nested_divs(self):                                   # Nested div structure
        with self.generator as _:
            html = _.generate_with_nested_divs(num_sections=3, items_per_sec=4)

            assert '<div class="section-0">' in html
            assert '<div class="section-2">' in html
            assert html.count('<p>') == 12                                      # 3 sections × 4 items

    def test_generate_with_nested_divs__default(self):                          # Default nested divs
        with self.generator as _:
            html = _.generate_with_nested_divs()

            assert '<div class="section-0">' in html
            assert '<div class="section-4">' in html
            assert html.count('<p>') == 25                                      # 5 sections × 5 items

    def test_generate_deep_nesting(self):                                       # Deep nesting
        with self.generator as _:
            html = _.generate_deep_nesting(depth=5)

            assert '<div><div><div><div><div>' in html
            assert 'Deep content' in html

    def test_generate_deep_nesting__default(self):                              # Default deep nesting
        with self.generator as _:
            html = _.generate_deep_nesting()

            assert '<div>' * 10 in html                                         # Default depth=10
            assert '</div>' * 10 in html
            assert 'Deep content' in html

    def test_generate_wide_structure(self):                                     # Wide (many siblings)
        with self.generator as _:
            html = _.generate_wide_structure(num_siblings=20)

            assert html.count('<span>') == 20

    def test_generate_wide_structure__default(self):                            # Default wide structure
        with self.generator as _:
            html = _.generate_wide_structure()

            assert html.count('<span>') == 50                                   # Default 50 siblings

    def test_generate_mixed_content(self):                                      # Mixed content types
        with self.generator as _:
            html = _.generate_mixed_content(num_paragraphs=9)

            assert '<h2>'  in html
            assert '<p>'   in html
            assert '<b>'   in html
            assert '<ul>'  in html
            assert '<li>'  in html

    def test_generate_mixed_content__default(self):                             # Default mixed content
        with self.generator as _:
            html = _.generate_mixed_content()

            assert '<h2>'  in html
            assert '<p>'   in html
            assert '<ul>'  in html

    # ═══════════════════════════════════════════════════════════════════════════
    # HTML Structure
    # ═══════════════════════════════════════════════════════════════════════════

    def test_wrap_in_html(self):                                                # HTML wrapper
        with self.generator as _:
            html = _.wrap_in_html("<p>Test</p>")

            assert html.startswith('<html>')
            assert '<head>'  in html
            assert '<title>' in html
            assert '<body>'  in html
            assert '<p>Test</p>' in html
            assert '</html>' in html

    def test_count_approximate_nodes(self):                                     # Node count estimation
        with self.generator as _:
            html  = "<html><body><p>Hello</p><p>World</p></body></html>"
            count = _.count_approximate_nodes(html)

            assert count > 0
            assert count < 20                                                   # Reasonable estimate

    def test_count_approximate_nodes__empty(self):                              # Empty HTML estimate
        with self.generator as _:
            count = _.count_approximate_nodes("<html></html>")

            assert count >= 0                                                   # Non-negative

    def test_count_approximate_nodes__no_text(self):                            # No text content
        with self.generator as _:
            html  = "<html><body><div><p></p></div></body></html>"
            count = _.count_approximate_nodes(html)

            assert count > 0