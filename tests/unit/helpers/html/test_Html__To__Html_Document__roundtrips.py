from unittest                                                   import TestCase
from osbot_utils.helpers.html.Html__To__Html_Dict               import Html__To__Html_Dict
from osbot_utils.helpers.html.Html_Dict__To__Html_Document      import Html_Dict__To__Html_Document
from osbot_utils.helpers.html.Html_Document__To__Html_Dict      import Html_Document__To__Html_Dict
from osbot_utils.helpers.html.schemas.Schema__Html_Document     import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node         import Schema__Html_Node
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data   import Schema__Html_Node__Data
from osbot_utils.helpers.html.Html_Dict__To__Html               import Html_Dict__To__Html


class test_Html__To__Html_Document__roundtrips(TestCase):                      # Tests that HTML structure and order is preserved through Type_Safe serialization

    def test_simple_roundtrip_with_schema_document(self):                       # Test basic roundtrip with Schema__Html_Document
        text_node = Schema__Html_Node__Data(data     = 'Hello World' ,
                                           position = 0              )
        p_node    = Schema__Html_Node      (tag         = 'p'        ,
                                           position    = 0           ,
                                           text_nodes  = [text_node] ,
                                           child_nodes = []          )

        data_node = Schema__Html_Node__Data(data     = 'some_data'   ,
                                           position = 1              )
        root_node = Schema__Html_Node      (tag         = 'div'      ,
                                           position    = -1          ,          # Root position
                                           child_nodes = [p_node]    ,
                                           text_nodes  = [data_node] )

        document = Schema__Html_Document(root_node = root_node)

        json_data         = document.json()
        document_restored = Schema__Html_Document.from_json(json_data)          # This should work now!

        assert document_restored.json()                              == json_data
        assert document_restored.root_node.tag                       == 'div'
        assert len(document_restored.root_node.child_nodes)          == 1
        assert len(document_restored.root_node.text_nodes)           == 1
        assert document_restored.root_node.child_nodes[0].tag        == 'p'
        assert document_restored.root_node.text_nodes[0].data        == 'some_data'

    def test_multiple_same_tags_order_preservation(self):                       # Test that multiple paragraphs/divs maintain their order
        html = """
        <div class="container">
            <p id="first">First paragraph</p>
            <p id="second">Second paragraph</p>
            <p id="third">Third paragraph</p>
            <div class="inner1">
                <p>Inner first</p>
                <p>Inner second</p>
            </div>
            <div class="inner2">
                <p>Another inner</p>
            </div>
            <p id="fourth">Fourth paragraph</p>
        </div>
        """

        html_dict         = Html__To__Html_Dict(html).convert()
        html_document     = Html_Dict__To__Html_Document(html__dict = html_dict).convert()

        json_data         = html_document.json()
        restored_document = Schema__Html_Document.from_json(json_data)

        assert restored_document.json() == json_data

        root = restored_document.root_node
        assert root.tag              == 'div'
        assert root.attrs['class']   == 'container'

        child_elements = root.child_nodes                                       # Now we can directly access child_nodes

        assert len(child_elements)                          == 6
        assert child_elements[0].tag                        == 'p'
        assert child_elements[0].attrs.get('id')            == 'first'
        assert child_elements[1].tag                        == 'p'
        assert child_elements[1].attrs.get('id')            == 'second'
        assert child_elements[2].tag                        == 'p'
        assert child_elements[2].attrs.get('id')            == 'third'
        assert child_elements[3].tag                        == 'div'
        assert child_elements[3].attrs.get('class')         == 'inner1'
        assert child_elements[4].tag                        == 'div'
        assert child_elements[4].attrs.get('class')         == 'inner2'
        assert child_elements[5].tag                        == 'p'
        assert child_elements[5].attrs.get('id')            == 'fourth'

    def test_complex_nested_structure_roundtrip(self):                          # Test complex nesting with mixed content
        html = """
        <article>
            <header>
                <h1>Title</h1>
                <h2>Subtitle</h2>
            </header>
            <section id="s1">
                <p>First section first para</p>
                <p>First section second para</p>
                <div>
                    <p>Nested para 1</p>
                    <p>Nested para 2</p>
                </div>
            </section>
            <section id="s2">
                <p>Second section first para</p>
                <p>Second section second para</p>
            </section>
        </article>
        """

        html_dict_1 = Html__To__Html_Dict(html).convert()
        document_1  = Html_Dict__To__Html_Document(html__dict = html_dict_1).convert()

        json_data   = document_1.json()
        document_2  = Schema__Html_Document.from_json(json_data)

        converter   = Html_Document__To__Html_Dict(html__document = document_2)
        html_dict_2 = converter.convert()

        assert html_dict_1 == html_dict_2

        sections = [n for n in document_2.root_node.child_nodes if n.tag == 'section']
        assert len(sections)              == 2
        assert sections[0].attrs['id']    == 's1'
        assert sections[1].attrs['id']    == 's2'

        s1_paras = [n for n in sections[0].child_nodes if n.tag == 'p']
        assert len(s1_paras) == 2

    def test_html_full_cycle_with_persistence(self):                            # Test the complete cycle: HTML → Parse → Save → Load → Render
        original_html = """<div>
    <p class="intro">Introduction paragraph</p>
    <ul>
        <li>First item</li>
        <li>Second item</li>
        <li>Third item</li>
    </ul>
    <p class="conclusion">Conclusion paragraph</p>
</div>"""

        html_dict       = Html__To__Html_Dict(original_html).convert()
        document        = Html_Dict__To__Html_Document(html__dict = html_dict).convert()

        saved_json      = document.json()
        loaded_document = Schema__Html_Document.from_json(saved_json)

        converter       = Html_Document__To__Html_Dict(html__document = loaded_document)
        restored_dict   = converter.convert()
        restored_html   = Html_Dict__To__Html(restored_dict).convert()

        final_dict      = Html__To__Html_Dict(restored_html).convert()

        assert html_dict == final_dict

        ul_node = None
        for node in loaded_document.root_node.child_nodes:
            if node.tag == 'ul':
                ul_node = node
                break

        assert ul_node is not None
        li_nodes = [n for n in ul_node.child_nodes if n.tag == 'li']
        assert len(li_nodes) == 3

        li_texts = []
        for li in li_nodes:
            for text_node in li.text_nodes:
                li_texts.append(text_node.data.strip())

        assert li_texts == ['First item', 'Second item', 'Third item']

    def test_schema_node_direct_serialization(self):                            # Test that Schema__Html_Node can be serialized and restored directly
        child_nodes = []
        text_nodes  = []

        for i in range(5):
            text   = Schema__Html_Node__Data(data     = f'Paragraph {i+1} content' ,
                                            position = 0                           )
            p_node = Schema__Html_Node      (tag         = 'p'                     ,
                                            attrs       = {'id': f'p{i+1}'}        ,
                                            text_nodes  = [text]                   ,
                                            child_nodes = []                       ,
                                            position    = i                        )
            child_nodes.append(p_node)

        root = Schema__Html_Node(tag         = 'div'                ,
                                attrs       = {'class': 'wrapper'}  ,
                                child_nodes = child_nodes           ,
                                text_nodes  = []                    ,
                                position    = -1                    )

        json_data     = root.json()
        restored_root = Schema__Html_Node.from_json(json_data)

        assert restored_root.json() == json_data

        for i, node in enumerate(restored_root.child_nodes):
            assert node.tag                    == 'p'
            assert node.attrs['id']            == f'p{i+1}'
            assert node.text_nodes[0].data     == f'Paragraph {i+1} content'

    def test_mixed_content_order_preservation(self):                            # Test that mixed text and element nodes maintain order
        html = """<div>
    Text before first
    <p>First para</p>
    Text between first and second
    <p>Second para</p>
    Text between second and third
    <p>Third para</p>
    Text after third
</div>"""

        html_dict = Html__To__Html_Dict(html).convert()
        document  = Html_Dict__To__Html_Document(html__dict = html_dict).convert()

        json_data = document.json()
        restored  = Schema__Html_Document.from_json(json_data)

        root = restored.root_node
        assert len(root.text_nodes)  == 4                                       # 4 text nodes
        assert len(root.child_nodes) == 3                                       # 3 paragraph nodes

        all_nodes = []
        for text in root.text_nodes:
            all_nodes.append((text.position, 'text', text))
        for child in root.child_nodes:
            all_nodes.append((child.position, 'element', child))

        all_nodes.sort(key = lambda x: x[0])

        assert len(all_nodes)                                 == 7
        assert all_nodes[0][1]                                == 'text'          # Text before first
        assert all_nodes[1][1]                                == 'element'       # First para
        assert all_nodes[1][2].tag                            == 'p'
        assert all_nodes[2][1]                                == 'text'          # Text between first and second
        assert all_nodes[3][1]                                == 'element'       # Second para
        assert all_nodes[3][2].tag                            == 'p'
        assert all_nodes[4][1]                                == 'text'          # Text between second and third
        assert all_nodes[5][1]                                == 'element'       # Third para
        assert all_nodes[5][2].tag                            == 'p'
        assert all_nodes[6][1]                                == 'text'          # Text after third

    def test_attribute_preservation(self):                                       # Test that all attributes are preserved through serialization
        html = """<div id="main" class="container responsive" data-value="123" custom-attr="test">
    <p id="p1" class="text-primary">First</p>
    <p id="p2" class="text-secondary" style="color: red;">Second</p>
    <p id="p3" data-index="3">Third</p>
</div>"""

        html_dict = Html__To__Html_Dict(html).convert()
        document  = Html_Dict__To__Html_Document(html__dict = html_dict).convert()

        json_data = document.json()
        restored  = Schema__Html_Document.from_json(json_data)

        root = restored.root_node
        assert root.attrs['id']            == 'main'
        assert root.attrs['class']         == 'container responsive'
        assert root.attrs['data-value']    == '123'
        assert root.attrs['custom-attr']   == 'test'

        p_nodes = [n for n in root.child_nodes if n.tag == 'p']
        assert p_nodes[0].attrs['id']      == 'p1'
        assert p_nodes[0].attrs['class']   == 'text-primary'
        assert p_nodes[1].attrs['id']      == 'p2'
        assert p_nodes[1].attrs['style']   == 'color: red;'
        assert p_nodes[2].attrs['data-index'] == '3'