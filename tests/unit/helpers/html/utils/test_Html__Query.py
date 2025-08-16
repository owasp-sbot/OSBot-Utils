from unittest                                                import TestCase
from osbot_utils.helpers.html.utils.Html__Query              import Html__Query
from osbot_utils.helpers.html.schemas.Schema__Html_Document  import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node      import Schema__Html_Node
from osbot_utils.testing.test_data.const__test__data__html   import TEST__DATA__HTML__SIMPLE, TEST__DATA__HTML__SWAGGER, TEST__DATA__HTML__MIXED_CONTENT


class test_Html__Query(TestCase):

    @classmethod
    def setUpClass(cls):                                                              # Setup test HTML samples
        cls.html_simple        = TEST__DATA__HTML__SIMPLE
        cls.html_swagger       = TEST__DATA__HTML__SWAGGER
        cls.html_mixed_content = TEST__DATA__HTML__MIXED_CONTENT


    def test__init__(self):                                                       # Test initialization
        with Html__Query(html=self.html_simple) as query:
            assert type(query.html    ) is str
            assert type(query.document) is Schema__Html_Document
            assert query.html           == self.html_simple


    def test__context_manager(self):                                              # Test context manager behavior
        with Html__Query(html=self.html_simple) as query:
            assert type(query         )         is Html__Query
            assert type(query.document)         is Schema__Html_Document
            assert query.document.root_node.tag == 'html'


    # Property tests
    def test_root(self):                                                          # Test root property
        with Html__Query(html=self.html_simple) as query:
            assert type(query.root) is Schema__Html_Node
            assert query.root.tag   == 'html'


    def test_head_and_body(self):                                                 # Test head and body properties
        with Html__Query(html=self.html_simple) as query:
            assert query.head      is not None
            assert query.body      is not None
            assert query.head.tag  == 'head'
            assert query.body.tag  == 'body'

        with Html__Query(html='<div>No head or body</div>') as query:            # Test when no head/body
            assert query.head is None
            assert query.body is None


    def test_title(self):                                                         # Test title extraction
        with Html__Query(html=self.html_simple) as query:
            assert query.title == 'Test Page'

        with Html__Query(html=self.html_swagger) as query:
            assert query.title == 'Fast_API - Swagger UI'

        with Html__Query(html='<html><head></head></html>') as query:            # No title
            assert query.title is None


    def test_links_and_link_hrefs(self):                                          # Test link extraction
        with Html__Query(html=self.html_simple) as query:
            assert len(query.links     ) == 2
            assert len(query.link_hrefs) == 2
            assert '/css/main.css'       in query.link_hrefs
            assert '/favicon.ico'        in query.link_hrefs

            link_1 = query.links[0]
            link_2 = query.links[1]
            assert link_1['rel' ] == 'stylesheet'
            assert link_1['href'] == '/css/main.css'
            assert link_2['rel' ] == 'shortcut icon'
            assert link_2['href'] == '/favicon.ico'


    def test_css_links(self):                                                     # Test CSS link extraction
        with Html__Query(html=self.html_simple) as query:
            assert len(query.css_links) == 1
            assert query.css_links[0]   == '/css/main.css'

        with Html__Query(html=self.html_swagger) as query:
            assert len(query.css_links) == 1
            assert query.css_links[0]   == '/static/swagger-ui/swagger-ui.css'


    def test_script_sources(self):                                                # Test script source extraction
        with Html__Query(html=self.html_simple) as query:
            assert len(query.script_sources) == 1
            assert query.script_sources[0]   == '/js/app.js'

        with Html__Query(html=self.html_swagger) as query:
            assert len(query.script_sources) == 1
            assert query.script_sources[0]   == '/static/swagger-ui/swagger-ui-bundle.js'


    def test_inline_scripts(self):                                                # Test inline script extraction
        with Html__Query(html=self.html_simple) as query:
            assert len(query.inline_scripts) == 1
            assert "console.log('inline');"  in query.inline_scripts[0]

        with Html__Query(html=self.html_swagger) as query:
            assert len(query.inline_scripts) == 1
            assert 'SwaggerUIBundle'          in query.inline_scripts[0]
            assert '/openapi.json'            in query.inline_scripts[0]


    def test_meta_tags(self):                                                     # Test meta tag extraction
        with Html__Query(html=self.html_simple) as query:
            assert len(query.meta_tags) == 1
            meta = query.meta_tags[0]
            assert meta['name'   ] == 'description'
            assert meta['content'] == 'Test description'


    def test_favicon(self):                                                       # Test favicon detection
        with Html__Query(html=self.html_simple) as query:
            assert query.favicon == '/favicon.ico'

        with Html__Query(html=self.html_swagger) as query:
            assert query.favicon == '/static/swagger-ui/favicon.png'

        with Html__Query(html='<html><head></head></html>') as query:
            assert query.favicon is None


    def test_stylesheets(self):                                                   # Test stylesheets alias
        with Html__Query(html=self.html_simple) as query:
            assert query.stylesheets == query.css_links
            assert query.stylesheets == ['/css/main.css']

    # Query method tests
    def test_has_link(self):                                                      # Test has_link method
        with Html__Query(html=self.html_simple) as query:
            assert query.has_link(href='/css/main.css'                 ) is True
            assert query.has_link(href='/css/main.css', rel='stylesheet') is True
            assert query.has_link(href='/nonexistent.css'              ) is False
            assert query.has_link(rel='stylesheet'                     ) is True
            assert query.has_link(rel='nonexistent'                    ) is False


    def test_has_script(self):                                                    # Test has_script method
        with Html__Query(html=self.html_simple) as query:
            assert query.has_script(src='/js/app.js'       ) is True
            assert query.has_script(src='/nonexistent.js'  ) is False
            assert query.has_script(contains='console.log' ) is True
            assert query.has_script(contains='nonexistent' ) is False


    def test_has_meta(self):                                                      # Test has_meta method
        with Html__Query(html=self.html_simple) as query:
            assert query.has_meta(name='description'                        ) is True
            assert query.has_meta(content='Test description'                ) is True
            assert query.has_meta(name='description', content='Test description') is True
            assert query.has_meta(name='keywords'                           ) is False


    def test_find_by_id(self):                                                    # Test find_by_id method
        with Html__Query(html=self.html_simple) as query:
            main_div = query.find_by_id('main')
            assert main_div      is not None
            assert main_div.tag  == 'div'
            assert main_div.attrs['id'] == 'main'

            assert query.find_by_id('nonexistent') is None

        with Html__Query(html=self.html_swagger) as query:
            swagger_div = query.find_by_id('swagger-ui')
            assert swagger_div      is not None
            assert swagger_div.tag  == 'div'


    def test_find_by_class(self):                                                 # Test find_by_class method
        with Html__Query(html=self.html_mixed_content) as query:
            containers = query.find_by_class('container')
            paragraphs = query.find_by_class('paragraph')
            highlights = query.find_by_class('highlight')

            assert len(containers) == 1
            assert len(paragraphs) == 1
            assert len(highlights) == 1

            assert containers[0].tag == 'div'
            assert paragraphs[0].tag == 'p'
            assert highlights[0].tag == 'span'

            assert len(query.find_by_class('nonexistent')) == 0


    def test_find_by_tag(self):                                                   # Test find_by_tag method
        with Html__Query(html=self.html_simple) as query:
            scripts = query.find_by_tag('script')
            links   = query.find_by_tag('link')
            divs    = query.find_by_tag('div')

            assert len(scripts) == 2
            assert len(links  ) == 2
            assert len(divs   ) == 1


    def test_get_attribute(self):                                                 # Test get_attribute method
        with Html__Query(html=self.html_simple) as query:
            main_div = query.find_by_id('main')
            assert query.get_attribute(main_div, 'id'   ) == 'main'
            assert query.get_attribute(main_div, 'class') is None


    def test_get_text(self):                                                      # Test get_text method
        with Html__Query(html=self.html_mixed_content) as query:
            full_text = query.get_text()
            assert 'Text before'       in full_text
            assert 'Paragraph content' in full_text
            assert 'Highlighted'       in full_text
            assert 'Text after'        in full_text

            p_nodes = query.find_by_tag('p')
            p_text  = query.get_text(p_nodes[0])
            assert p_text == 'Paragraph content'


    # Helper method tests
    def test_find_child_by_tag(self):                                             # Test find_child_by_tag helper
        with Html__Query(html=self.html_simple) as query:
            head = query.find_child_by_tag(query.root, 'head')
            body = query.find_child_by_tag(query.root, 'body')

            assert head      is not None
            assert body      is not None
            assert head.tag  == 'head'
            assert body.tag  == 'body'

            assert query.find_child_by_tag(query.root, 'div') is None


    def test_find_all_by_tag(self):                                               # Test find_all_by_tag helper
        with Html__Query(html=self.html_simple) as query:
            all_scripts = query.find_all_by_tag('script')
            all_links   = query.find_all_by_tag('link')

            assert len(all_scripts) == 2
            assert len(all_links  ) == 2

            all_scripts_from_head = query.find_all_by_tag('script', query.head)
            assert len(all_scripts_from_head) == 0


    def test_find_by_attribute(self):                                             # Test find_by_attribute helper
        with Html__Query(html=self.html_simple) as query:
            element = query.find_by_attribute('id', 'main')
            assert element      is not None
            assert element.tag  == 'div'

            element = query.find_by_attribute('rel', 'stylesheet')
            assert element      is not None
            assert element.tag  == 'link'


    def test_find_all(self):                                                      # Test find_all helper
        with Html__Query(html=self.html_simple) as query:
            all_nodes = query.find_all()
            assert len(all_nodes) > 0
            assert all_nodes[0].tag == 'html'

            tag_names = [node.tag for node in all_nodes]
            assert 'html'   in tag_names
            assert 'head'   in tag_names
            assert 'body'   in tag_names
            assert 'title'  in tag_names
            assert 'script' in tag_names


    def test_get_text_content(self):                                              # Test get_text_content helper
        with Html__Query(html=self.html_mixed_content) as query:
            text = query.get_text_content(query.root)
            assert 'Text before'       in text
            assert 'Paragraph content' in text
            assert 'Text middle'       in text
            assert 'Highlighted'       in text
            assert 'Text after'        in text
