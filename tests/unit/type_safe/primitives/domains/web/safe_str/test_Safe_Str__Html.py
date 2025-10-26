import re
import pytest
from unittest                                                             import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Str                       import Safe_Str
from osbot_utils.type_safe.Type_Safe__Primitive                           import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Html import Safe_Str__Html, TYPE_SAFE_STR__HTML__MAX_LENGTH, TYPE_SAFE_STR__HTML__REGEX
from osbot_utils.utils.Objects                                            import base_types
from osbot_utils.utils.Str                                                import trim


class test_Safe_Str__Html(TestCase):

    def test_Safe_Str__HTML_class(self):
        safe_str_html = Safe_Str__Html()
        assert type      (safe_str_html)      == Safe_Str__Html
        assert base_types(safe_str_html)      == [Safe_Str, Type_Safe__Primitive, str, object, object]
        assert safe_str_html.max_length       == TYPE_SAFE_STR__HTML__MAX_LENGTH
        assert safe_str_html.regex            == re.compile(TYPE_SAFE_STR__HTML__REGEX)
        assert safe_str_html.replacement_char == '_'


    def test_Safe_Str__Html_basic(self):
        # Basic HTML elements
        assert str(Safe_Str__Html("<html><body>Hello</body></html>")) == "<html><body>Hello</body></html>"
        assert str(Safe_Str__Html("<div>Content</div>")) == "<div>Content</div>"
        assert str(Safe_Str__Html("<p>Paragraph text</p>")) == "<p>Paragraph text</p>"

        # HTML with attributes
        assert str(Safe_Str__Html('<div class="container">Content</div>')) == '<div class="container">Content</div>'
        assert str(Safe_Str__Html('<a href="https://example.com">Link</a>')) == '<a href="https://example.com">Link</a>'
        assert str(Safe_Str__Html('<img src="image.jpg" alt="Image"/>')) == '<img src="image.jpg" alt="Image"/>'

        # HTML with special characters and entities
        assert str(Safe_Str__Html("<p>&lt;script&gt;&amp;&quot;&#39;</p>")) == "<p>&lt;script&gt;&amp;&quot;&#39;</p>"
        assert str(Safe_Str__Html("<p>Price: $100 &euro;50 &pound;75</p>")) == "<p>Price: $100 &euro;50 &pound;75</p>"

        # Complex HTML structure
        html_structure = """<div id="main" class="container">
    <h1>Title</h1>
    <p>Paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</div>"""
        assert str(Safe_Str__Html(html_structure)) == trim(html_structure)

    def test_Safe_Str__Html_whitespace_handling(self):
        # Trim outer whitespace (trim_whitespace = True)
        assert str(Safe_Str__Html("  <div>Content</div>  ")) == "<div>Content</div>"
        assert str(Safe_Str__Html("\n<html>\n</html>\n")) == "<html>\n</html>"

        # Preserve internal whitespace and formatting
        html_with_spaces = "<p>Text    with    spaces</p>"
        assert str(Safe_Str__Html(html_with_spaces)) == html_with_spaces

        # Preserve tabs for code formatting
        html_with_tabs = "<pre>\tIndented\tcode</pre>"
        assert str(Safe_Str__Html(html_with_tabs)) == html_with_tabs

    def test_Safe_Str__Html_newline_normalization(self):
        # Windows newlines (normalize_newlines = True)
        assert str(Safe_Str__Html("<div>\r\nContent\r\n</div>")) == "<div>\nContent\n</div>"

        # Mac newlines
        assert str(Safe_Str__Html("<div>\rContent\r</div>")) == "<div>\nContent\n</div>"

        # Mixed newlines
        assert str(Safe_Str__Html("<div>\nLine1\r\nLine2\rLine3</div>")) == "<div>\nLine1\nLine2\nLine3</div>"

        # Preserve multiple consecutive newlines
        assert str(Safe_Str__Html("<p>Para1</p>\n\n<p>Para2</p>")) == "<p>Para1</p>\n\n<p>Para2</p>"

    def test_Safe_Str__Html_empty_and_none(self):
        # Empty HTML (allow_empty = True)
        assert str(Safe_Str__Html("")) == ""
        assert str(Safe_Str__Html(None)) == ""
        assert str(Safe_Str__Html("   ")) == ""  # Spaces only (will be trimmed)

        # Empty tags are valid
        assert str(Safe_Str__Html("<div></div>")) == "<div></div>"
        assert str(Safe_Str__Html("<br/>")) == "<br/>"

    def test_Safe_Str__Html_control_chars(self):
        # HTML with control characters (should be filtered out)
        input_with_control = "<div>Text\x00with\x01control\x02chars</div>"
        expected = "<div>Text_with_control_chars</div>"
        assert str(Safe_Str__Html(input_with_control)) == expected

        # ANSI escape sequences in HTML
        input_with_escape = "<pre>\x1B[31mRed text\x1B[0m</pre>"
        expected = "<pre>_[31mRed text_[0m</pre>"
        assert str(Safe_Str__Html(input_with_escape)) == expected

        # DEL character
        input_with_del = "<div>Text\x7Fwith DEL</div>"
        expected = "<div>Text_with DEL</div>"
        assert str(Safe_Str__Html(input_with_del)) == expected

    def test_Safe_Str__Html_length_limits(self):
        # HTML at the limit
        html_at_limit = "<p>" + ("a" * (TYPE_SAFE_STR__HTML__MAX_LENGTH - 7)) + "</p>"
        assert len(str(Safe_Str__Html(html_at_limit))) == TYPE_SAFE_STR__HTML__MAX_LENGTH

        # HTML exceeding the limit
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Html("a" * (TYPE_SAFE_STR__HTML__MAX_LENGTH + 1))
        assert f"in Safe_Str__Html, value exceeds maximum length of {TYPE_SAFE_STR__HTML__MAX_LENGTH}" in str(exc_info.value)

    def test_Safe_Str__Html_complex_documents(self):
        # Complete HTML document
        html_doc = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Page</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 1200px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome</h1>
        <p>This is a test page.</p>
    </div>
    <script>
        console.log("Hello, world!");
    </script>
</body>
</html>"""
        assert str(Safe_Str__Html(html_doc)) == trim(html_doc)

    def test_Safe_Str__Html_html5_elements(self):
        # Modern HTML5 elements
        html5_elements = """<article>
    <header>
        <nav>
            <a href="#section1">Section 1</a>
        </nav>
    </header>
    <section id="section1">
        <figure>
            <img src="image.jpg" alt="Description">
            <figcaption>Image caption</figcaption>
        </figure>
    </section>
    <footer>
        <p>&copy; 2025 Company Name</p>
    </footer>
</article>"""
        assert str(Safe_Str__Html(html5_elements)) == trim(html5_elements)

    def test_Safe_Str__Html_embedded_content(self):
        # HTML with embedded SVG
        html_with_svg = """<div>
    <svg width="100" height="100">
        <circle cx="50" cy="50" r="40" stroke="black" fill="red"/>
    </svg>
</div>"""
        assert str(Safe_Str__Html(html_with_svg)) == trim(html_with_svg)

        # HTML with inline CSS
        html_with_css = '<div style="color: red; font-size: 14px;">Styled text</div>'
        assert str(Safe_Str__Html(html_with_css)) == html_with_css

        # HTML with data attributes
        html_with_data = '<div data-id="123" data-type="user">Content</div>'
        assert str(Safe_Str__Html(html_with_data)) == html_with_data

    def test_Safe_Str__Html_forms_and_inputs(self):
        # HTML forms
        html_form = """<form action="/submit" method="post">
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required>
    <input type="email" name="email" placeholder="email@example.com">
    <textarea name="message" rows="4" cols="50"></textarea>
    <button type="submit">Submit</button>
</form>"""
        assert str(Safe_Str__Html(html_form)) == trim(html_form)

    def test_Safe_Str__Html_tables(self):
        # HTML tables
        html_table = """<table>
    <thead>
        <tr>
            <th>Header 1</th>
            <th>Header 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Data 1</td>
            <td>Data 2</td>
        </tr>
    </tbody>
</table>"""
        assert str(Safe_Str__Html(html_table)) == trim(html_table)

    def test_Safe_Str__Html_comments_and_cdata(self):
        # HTML comments
        html_with_comments = """<div>
    <!-- This is a comment -->
    <p>Visible content</p>
    <!-- Another comment -->
</div>"""
        assert str(Safe_Str__Html(html_with_comments)) == trim(html_with_comments)

        # CDATA sections (common in XHTML/XML)
        html_with_cdata = """<script>
//<![CDATA[
    var x = 5 < 10;
//]]>
</script>"""
        assert str(Safe_Str__Html(html_with_cdata)) == trim(html_with_cdata)

    def test_Safe_Str__Html_unicode_and_international(self):
        # International characters in HTML
        html_intl = """<div>
    <p>English: Hello</p>
    <p>Español: Hola</p>
    <p>Français: Bonjour</p>
    <p>中文: 你好</p>
    <p>日本語: こんにちは</p>
    <p>العربية: مرحبا</p>
</div>"""
        assert str(Safe_Str__Html(html_intl)) == trim(html_intl)

        # Unicode symbols in HTML
        html_symbols = "<p>Symbols: ★ ♥ ☺ ☂ ☃ ♫ → ← ↑ ↓</p>"
        assert str(Safe_Str__Html(html_symbols)) == html_symbols

    def test_Safe_Str__Html_numeric_conversion(self):
        # Numeric values get converted to strings
        assert str(Safe_Str__Html(12345)) == "12345"
        assert str(Safe_Str__Html(0)) == "0"

        # But this is unusual for HTML - typically HTML is always string-based