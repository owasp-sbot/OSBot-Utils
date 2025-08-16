from unittest                                                            import TestCase
from osbot_utils.utils.Objects                                           import __
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict           import Html__To__Html_Dict
from osbot_utils.helpers.html.transformers.Html_Dict__To__Html_Document  import Html_Dict__To__Html_Document
from osbot_utils.helpers.html.transformers.Html_Document__To__Html_Dict  import Html_Document__To__Html_Dict
from osbot_utils.helpers.html.schemas.Schema__Html_Document              import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node                  import Schema__Html_Node
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data            import Schema__Html_Node__Data

class test_Html_Document__To__Html_Dict(TestCase):                                  # Test Html_Document__To__Html_Dict and the multiple roundtrip possibilities


    def test_simple_roundtrip_with_positions(self):                                 # Test basic roundtrip with the new schema structure

        text_node = Schema__Html_Node__Data(data        ='Hello World'  ,           # Create nodes with positions
                                            position    = 0             )           # todo: question: shouldn't this be position 1
        p_node    = Schema__Html_Node      (tag         = 'p'           ,
                                            position    = 0             ,
                                            text_nodes  = [text_node]   ,
                                            child_nodes = []            )
        data_node = Schema__Html_Node__Data(data        ='some_data'    ,
                                            position    = 1             )
        root_node = Schema__Html_Node      (tag         = 'div'       ,
                                            position    = -1,             # Root position
                                            child_nodes = [p_node],
                                            text_nodes  = [data_node])

        document = Schema__Html_Document(root_node=root_node)

        # Convert to JSON and back
        json_data = document.json()
        document_restored = Schema__Html_Document.from_json(json_data)                  # Verify exact match
        assert document_restored.json()                         == json_data
        assert document_restored.root_node.tag                  == 'div'
        assert len(document_restored.root_node.child_nodes)     == 1
        assert len(document_restored.root_node.text_nodes)      == 1
        assert document_restored.root_node.child_nodes  [0].tag == 'p'
        assert document_restored.root_node.text_nodes   [0].data == 'some_data'
        assert json_data == { 'root_node'  : { 'attrs'      : {},
                                               'child_nodes': [{ 'attrs'      : {},
                                                                 'child_nodes': [],
                                                                 'position'   : 0,
                                                                 'tag'        : 'p',
                                                                 'text_nodes': [{'data'    : 'Hello World',
                                                                                 'position': 0,
                                                                                 'type'    : 'TEXT'}]}],
                                               'position'   : -1,
                                               'tag'        : 'div',
                                               'text_nodes' : [{'data'    : 'some_data',
                                                                'position': 1          ,
                                                                'type'    : 'TEXT'     }]},
                              'timestamp': document.timestamp }

    def test_mixed_content_with_positions(self):                                        # Test mixed text and element content maintains order
        html      = """<div>Text before<p>Paragraph</p>Text after</div>"""
        html_dict = Html__To__Html_Dict(html).convert()                                 # Parse HTML to dict
        document  = Html_Dict__To__Html_Document(html__dict=html_dict).convert()        # Convert to new schema with positions
        root      = document.root_node                                                  # Check the root node

        assert root.tag              == 'div'
        assert len(root.text_nodes ) == 2
        assert len(root.child_nodes) == 1

        assert root.obj()            == __(position    = -1,
                                           attrs       = __(),
                                           child_nodes = [ __(position    = 1,
                                                              attrs       = __(),
                                                              child_nodes = [],
                                                              text_nodes  = [__(type='TEXT', data='Paragraph', position=0)],
                                                              tag         = 'p')],
                                           text_nodes  = [ __(type='TEXT', data='Text before', position=0),
                                                           __(type='TEXT', data='Text after' , position=2)],
                                           tag         = 'div')

        text_before = next(t for t in root.text_nodes  if t.position == 0)              # Verify positions
        p_element   = next(c for c in root.child_nodes if c.position == 1)
        text_after  = next(t for t in root.text_nodes  if t.position == 2)

        assert text_before.data.strip() == 'Text before'
        assert p_element.tag == 'p'
        assert text_after.data.strip() == 'Text after'

        # Test JSON roundtrip
        json_data = document.json()
        restored  = Schema__Html_Document.from_json(json_data)
        assert restored.json() == json_data

    def test_complex_nested_with_positions(self):                                       # Test complex nesting preserves structure"""
        html = """
        <div>
            Start text
            <p>First para</p>
            Middle text
            <div>
                Nested start
                <span>Span content</span>
                Nested end
            </div>
            End text
        </div>
        """


        html_dict = Html__To__Html_Dict(html).convert()                             # Full cycle with new schema
        document  = Html_Dict__To__Html_Document(html__dict=html_dict).convert()

        # Serialize and restore
        json_data = document.json()
        restored  = Schema__Html_Document.from_json(json_data)


        # Verify structure is preserved
        assert restored.json() == json_data

        assert restored.obj() == document.obj()
        assert document.obj() == __(root_node=__(position    = -1,
                                                 attrs       = __(),
                                                 child_nodes = [__(position     = 1,
                                                                   attrs        = __(),
                                                                   child_nodes  = [],
                                                                   text_nodes   = [__(type='TEXT', data='First para', position=0)],
                                                                   tag          = 'p' ),
                                                                __(position     = 3,
                                                                   attrs        =__(),
                                                                   child_nodes  = [__(position    = 1,
                                                                                      attrs       = __(),
                                                                                      child_nodes = [],
                                                                                      text_nodes  = [__(type='TEXT',data='Span content', position=0)],
                                                                                   tag='span')],
                                                                   text_nodes   = [__(type     = 'TEXT',
                                                                                      data     = '\n'
                                                                                                 '                Nested '
                                                                                                 'start\n'
                                                                                                 '                ',
                                                                                      position = 0),
                                                                                   __(type     = 'TEXT',
                                                                                      data     = '\n'
                                                                                                 '                Nested '
                                                                                                 'end\n'
                                                                                                 '            ',
                                                                                      position  = 2)],
                                                                   tag          = 'div')],
                                                 text_nodes = [__(type='TEXT', data='\n            Start text\n            ' , position=0 ),
                                                               __(type='TEXT', data='\n            Middle text\n            ', position=2 ),
                                                               __(type='TEXT', data='\n            End text\n        '       , position=4 )],
                                                 tag        = 'div'),
                                   timestamp=document.timestamp)

        # Check nested div
        root       = restored.root_node
        nested_div = next(c for c in root.child_nodes if c.tag == 'div')
        assert len(nested_div.text_nodes)  == 2  # "Nested start" and "Nested end"
        assert len(nested_div.child_nodes) == 1  # span

        assert type(document.root_node.child_nodes[0].text_nodes[0]) is Schema__Html_Node__Data
        assert type(restored.root_node.child_nodes[0].text_nodes[0]) is Schema__Html_Node__Data
        assert type(nested_div.child_nodes[0]                      ) is Schema__Html_Node

        # Verify positions in nested div
        assert any(t.position == 0 for t in nested_div.text_nodes)                       # Before span
        assert nested_div.child_nodes[0].position == 1                                   # Span
        assert any(t.position == 2 for t in nested_div.text_nodes)                       # After span

    def test_html_dict_roundtrip(self):                                                         # Test converting from document back to html dict"""
        original_html      = """<div>Text1<p>Para1</p>Text2<p>Para2</p>Text3</div>"""
        original_dict      = Html__To__Html_Dict(original_html).convert()                       # Parse to dict
        document           = Html_Dict__To__Html_Document(html__dict=original_dict).convert()   # Convert to document
        converter          = Html_Document__To__Html_Dict(html__document=document)              # Convert back to dict
        reconstructed_dict = converter.convert()

        assert reconstructed_dict == original_dict                                              # Should match the original

        nodes = reconstructed_dict['nodes']                                                     # Verify the nodes are in correct order
        assert len(nodes)       == 5
        assert nodes[0]['type'] == 'TEXT' and 'Text1' in nodes[0]['data']
        assert nodes[1]['tag' ] == 'p'
        assert nodes[2]['type'] == 'TEXT' and 'Text2' in nodes[2]['data']
        assert nodes[3]['tag' ] == 'p'
        assert nodes[4]['type'] == 'TEXT' and 'Text3' in nodes[4]['data']

    def test_multiple_same_tags_with_positions(self):                   # Test multiple paragraphs maintain order through position tracking
        html = """
        <article>
            <p id="p1">First</p>
            <p id="p2">Second</p>
            <p id="p3">Third</p>
            Some text
            <p id="p4">Fourth</p>
        </article>
        """

        html_dict = Html__To__Html_Dict(html).convert()                              # Full roundtrip
        document  = Html_Dict__To__Html_Document(html__dict=html_dict).convert()
        root      = document.root_node                                               # Verify positions are assigned correctly
        p_nodes   = sorted(root.child_nodes, key=lambda x: x.position)

        assert len(p_nodes) == 4
        assert p_nodes[0].attrs['id'] == 'p1' and p_nodes[0].position == 0
        assert p_nodes[1].attrs['id'] == 'p2' and p_nodes[1].position == 1
        assert p_nodes[2].attrs['id'] == 'p3' and p_nodes[2].position == 2
        assert p_nodes[3].attrs['id'] == 'p4' and p_nodes[3].position == 4          # position 3 is the text

        json_data = document.json()                                                 # Test serialization
        restored  = Schema__Html_Document.from_json(json_data)
        assert restored.json() == json_data