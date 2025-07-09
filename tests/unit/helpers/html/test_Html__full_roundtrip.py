from unittest                                                import TestCase
from osbot_utils.helpers.html.Html__To__Html_Dict            import Html__To__Html_Dict
from osbot_utils.helpers.html.Html_Dict__To__Html_Document   import Html_Dict__To__Html_Document
from osbot_utils.helpers.html.Html_Document__To__Html_Dict   import Html_Document__To__Html_Dict
from osbot_utils.helpers.html.Html_Dict__To__Html            import Html_Dict__To__Html
from osbot_utils.helpers.html.schemas.Schema__Html_Document  import Schema__Html_Document
from tests._test_data.Sample_Test_Files                      import Sample_Test_Files


class test_Html__Full_Roundtrip(TestCase):                                      # Test complete HTML → Document → HTML roundtrip

    def test_simple_html_roundtrip(self):                                       # Test basic HTML structure roundtrip
        original_html = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Test Page</title>
    </head>
    <body>
        <h1>Hello World</h1>
        <p>This is a test paragraph.</p>
    </body>
</html>"""

        # HTML → Dict → Document → Dict → HTML
        html_dict_1    = Html__To__Html_Dict(original_html).convert()
        html_document  = Html_Dict__To__Html_Document(html__dict = html_dict_1).convert()
        html_dict_2    = Html_Document__To__Html_Dict(html__document = html_document).convert()
        final_html     = Html_Dict__To__Html(html_dict_2).convert()

        # Verify dict structures match
        assert html_dict_1 == html_dict_2

        # Parse final HTML back to verify structure
        final_dict = Html__To__Html_Dict(final_html).convert()
        assert final_dict == html_dict_1

    def test_mixed_content_roundtrip(self):                                     # Test HTML with mixed text and elements
        original_html = """<!DOCTYPE html>
<div>
    Text before <strong>bold text</strong> text after
    <p>Paragraph with <em>emphasis</em> and more text</p>
    Final text
</div>"""

        html_dict_1    = Html__To__Html_Dict(original_html).convert()
        html_document  = Html_Dict__To__Html_Document(html__dict     = html_dict_1).convert()
        html_dict_2    = Html_Document__To__Html_Dict(html__document = html_document).convert()
        final_html     = Html_Dict__To__Html(html_dict_2).convert()

        assert html_dict_1 == html_dict_2
        assert html_dict_1 == Html__To__Html_Dict(final_html).convert()                 # confirm full roundtrip

        # Verify the structure is preserved
        root = html_document.root_node
        assert root.tag == 'div'
        assert len(root.text_nodes)  == 3  # "Text before ", "text after", and "Final text"
        assert len(root.child_nodes) == 2  # <strong> and <p>

        # Verify order using positions
        all_nodes = [(n.position, 'text', n) for n in root.text_nodes]
        all_nodes.extend([(n.position, 'elem', n) for n in root.child_nodes])
        all_nodes.sort(key = lambda x: x[0])

        assert all_nodes[0][1] == 'text'  # "Text before "
        assert all_nodes[1][1] == 'elem'  # <strong>
        assert all_nodes[2][1] == 'text'  # " text after"
        assert all_nodes[3][1] == 'elem'  # <p>
        assert all_nodes[4][1] == 'text'  # "Final text"

    def test_complex_nested_roundtrip(self):                                    # Test complex nested HTML structure
        original_html = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Complex Page</title>
        <link rel="stylesheet" href="styles.css" />
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id="content">
                <h1>Main Title</h1>
                <p>First paragraph with <strong>bold</strong> text.</p>
                <p>Second paragraph with <em>italic</em> text.</p>
            </section>
        </main>
        <footer>
            <p>&copy; 2024 Test Site</p>
        </footer>
    </body>
</html>"""

        html_dict_1    = Html__To__Html_Dict(original_html).convert()
        html_document  = Html_Dict__To__Html_Document(html__dict = html_dict_1).convert()
        html_dict_2    = Html_Document__To__Html_Dict(html__document = html_document).convert()
        final_html     = Html_Dict__To__Html(html_dict_2).convert()

        assert html_dict_1 == html_dict_2
        assert html_dict_1 == Html__To__Html_Dict(final_html).convert()  # confirm full roundtrip

        # Verify complex structure
        root = html_document.root_node
        assert root.tag            == 'html'
        assert root.attrs['lang']  == 'en'
        assert len(root.child_nodes) == 2  # head and body

        head = root.child_nodes[0]
        body = root.child_nodes[1]
        assert head.tag == 'head'
        assert body.tag == 'body'

        # Verify body structure
        assert len(body.child_nodes) == 3  # header, main, footer
        header, main, footer = body.child_nodes
        assert header.tag == 'header'
        assert main.tag   == 'main'
        assert footer.tag == 'footer'

    def test_self_closing_tags_roundtrip(self):                                # Test self-closing tags preservation
        original_html = """<!DOCTYPE html>
<div>
    <img src="image.jpg" alt="Test Image" />
    <br />
    <input type="text" name="test" />
    <hr />
    <meta charset="UTF-8" />
</div>"""

        html_dict_1    = Html__To__Html_Dict(original_html).convert()
        html_document  = Html_Dict__To__Html_Document(html__dict = html_dict_1).convert()
        html_dict_2    = Html_Document__To__Html_Dict(html__document = html_document).convert()
        final_html     = Html_Dict__To__Html(html_dict_2).convert()

        assert html_dict_1 == html_dict_2
        assert html_dict_1 == Html__To__Html_Dict(final_html).convert()  # confirm full roundtrip

        # Verify self-closing tags
        root = html_document.root_node
        assert len(root.child_nodes) == 5
        assert root.child_nodes[0].tag == 'img'
        assert root.child_nodes[1].tag == 'br'
        assert root.child_nodes[2].tag == 'input'
        assert root.child_nodes[3].tag == 'hr'
        assert root.child_nodes[4].tag == 'meta'

    def test_attributes_preservation_roundtrip(self):                           # Test that all attributes are preserved
        original_html = """<!DOCTYPE html>
<div id="main" class="container responsive" data-value="123" custom-attr="test">
    <p id="p1" class="text-primary" style="color: blue;">Text</p>
    <span data-toggle="tooltip" title="Help text">Hover me</span>
    <a href="https://example.com" target="_blank" rel="noopener">Link</a>
</div>"""

        html_dict_1    = Html__To__Html_Dict(original_html).convert()
        html_document  = Html_Dict__To__Html_Document(html__dict = html_dict_1).convert()
        html_dict_2    = Html_Document__To__Html_Dict(html__document = html_document).convert()
        final_html     = Html_Dict__To__Html(html_dict_2).convert()

        assert html_dict_1 == html_dict_2
        assert html_dict_1 == Html__To__Html_Dict(final_html).convert()  # confirm full roundtrip

        # Verify attributes
        root = html_document.root_node
        assert root.attrs['id']          == 'main'
        assert root.attrs['class']       == 'container responsive'
        assert root.attrs['data-value']  == '123'
        assert root.attrs['custom-attr'] == 'test'

        # Check child attributes
        p_elem    = root.child_nodes[0]
        span_elem = root.child_nodes[1]
        a_elem    = root.child_nodes[2]

        assert p_elem.attrs['id']         == 'p1'
        assert p_elem.attrs['class']      == 'text-primary'
        assert p_elem.attrs['style']      == 'color: blue;'

        assert span_elem.attrs['data-toggle'] == 'tooltip'
        assert span_elem.attrs['title']       == 'Help text'

        assert a_elem.attrs['href']      == 'https://example.com'
        assert a_elem.attrs['target']    == '_blank'
        assert a_elem.attrs['rel']       == 'noopener'

    def test_bootstrap_example_roundtrip(self):                                # Test with real Bootstrap HTML example
        sample_files   = Sample_Test_Files()
        original_html  = sample_files.html_bootstrap_example()

        html_dict_1    = Html__To__Html_Dict(original_html).convert()
        html_document  = Html_Dict__To__Html_Document(html__dict = html_dict_1).convert()

        # Test serialization/deserialization
        json_data              = html_document.json()
        html_document_restored = Schema__Html_Document.from_json(json_data)

        assert html_document_restored.json() == json_data

        # Complete the roundtrip
        html_dict_2    = Html_Document__To__Html_Dict(html__document = html_document_restored).convert()
        final_html     = Html_Dict__To__Html(html_dict_2).convert()

        assert html_dict_1 == html_dict_2

        # Parse final HTML to verify
        final_dict = Html__To__Html_Dict(final_html).convert()
        assert final_dict == html_dict_1

    def test_whitespace_handling_roundtrip(self):                              # Test whitespace preservation in mixed content
        original_html = """<!DOCTYPE html>
<div>
    <p>Line one</p>
    <p>Line two</p>
    Text between paragraphs
    <p>Line three</p>
</div>"""

        html_dict_1    = Html__To__Html_Dict(original_html).convert()
        html_document  = Html_Dict__To__Html_Document(html__dict = html_dict_1).convert()
        html_dict_2    = Html_Document__To__Html_Dict(html__document = html_document).convert()
        final_html     = Html_Dict__To__Html(html_dict_2).convert()

        assert html_dict_1 == html_dict_2
        assert html_dict_1 == Html__To__Html_Dict(final_html).convert()  # confirm full roundtrip

        # Check the text node between paragraphs
        root = html_document.root_node
        text_nodes = root.text_nodes

        # Find the text node with "Text between paragraphs"
        between_text = None
        for text_node in text_nodes:
            if 'Text between paragraphs' in text_node.data:
                between_text = text_node
                break

        assert between_text is not None
        assert 'Text between paragraphs' in between_text.data

    def test_empty_elements_roundtrip(self):                                    # Test empty elements handling
        original_html = """<!DOCTYPE html>
<div>
    <p></p>
    <div></div>
    <span></span>
    <p>Not empty</p>
</div>"""

        html_dict_1    = Html__To__Html_Dict(original_html).convert()
        html_document  = Html_Dict__To__Html_Document(html__dict = html_dict_1).convert()
        html_dict_2    = Html_Document__To__Html_Dict(html__document = html_document).convert()
        final_html     = Html_Dict__To__Html(html_dict_2).convert()

        assert html_dict_1 == html_dict_2
        assert html_dict_1 == Html__To__Html_Dict(final_html).convert()  # confirm full roundtrip

        # Verify empty elements
        root = html_document.root_node
        assert len(root.child_nodes) == 4
        assert root.child_nodes[0].tag == 'p'
        assert len(root.child_nodes[0].child_nodes) == 0
        assert len(root.child_nodes[0].text_nodes) == 0