from typing                                                         import List, Optional, Dict, Any
from osbot_utils.helpers.html.transformers.Html__To__Html_Document  import Html__To__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Document         import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node             import Schema__Html_Node
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class Html__Query(Type_Safe):
    html     : str
    document : Schema__Html_Document

    def __enter__(self):
        self.document = Html__To__Html_Document(html=self.html).convert()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def root(self) -> Schema__Html_Node:                                          # Get the root node
        return self.document.root_node

    @property
    def head(self) -> Optional[Schema__Html_Node]:                                # Get the head node
        return self.find_child_by_tag(self.root, 'head')

    @property
    def body(self) -> Optional[Schema__Html_Node]:                                # Get the body node
        return self.find_child_by_tag(self.root, 'body')

    @property
    def title(self) -> Optional[str]:                                             # Get the page title text
        if not self.head:
            return None
        title_node = self.find_child_by_tag(self.head, 'title')
        if title_node:
            return self.get_text_content(title_node).strip()
        return None

    @property
    def links(self) -> List[Dict[str, str]]:                                      # Get all link tags as list of attribute dicts
        if not self.head:
            return []
        return [node.attrs for node in self.head.child_nodes if node.tag == 'link']

    @property
    def link_hrefs(self) -> List[str]:                                            # Get all link hrefs
        return [link.get('href', '') for link in self.links if 'href' in link]

    @property
    def css_links(self) -> List[str]:                                             # Get all stylesheet link hrefs
        result = []
        for link in self.links:
            if link.get('rel') == 'stylesheet' and 'href' in link:
                result.append(link['href'])
        return result

    @property
    def script_sources(self) -> List[str]:                                        # Get all external script src URLs
        scripts = self.find_all_by_tag('script')
        return [s.attrs.get('src') for s in scripts if 'src' in s.attrs]

    @property
    def inline_scripts(self) -> List[str]:                                        # Get all inline script contents
        scripts = self.find_all_by_tag('script')
        result  = []
        for script in scripts:
            if 'src' not in script.attrs:                                         # Only inline scripts
                content = self.get_text_content(script)
                if content:
                    result.append(content)
        return result

    @property
    def meta_tags(self) -> List[Dict[str, str]]:                                  # Get all meta tags as list of attribute dicts
        if not self.head:
            return []
        return [node.attrs for node in self.head.child_nodes if node.tag == 'meta']

    @property
    def favicon(self) -> Optional[str]:                                           # Get favicon URL if present
        return (self.find_link_by_rel('shortcut icon') or
                self.find_link_by_rel('icon'))

    @property
    def stylesheets(self) -> List[str]:                                           # Alias for css_links
        return self.css_links

    # Query methods
    def has_link(self, href : str  = None ,                                       # Check if link exists with attributes
                       rel  : str  = None ,
                       **attrs
                 ) -> bool:
        for link in self.links:
            if href and link.get('href') != href:
                continue
            if rel and link.get('rel') != rel:
                continue
            if all(link.get(k) == v for k, v in attrs.items()):                  # Check any additional attributes
                return True
        return False

    def has_script(self, src      : str = None ,                                  # Check if script exists with src or text
                         contains : str = None
                   ) -> bool:
        scripts = self.find_all_by_tag('script')
        for script in scripts:
            if src and script.attrs.get('src') == src:
                return True
            if contains:
                content = self.get_text_content(script)
                if contains in content:
                    return True
        return False

    def has_meta(self, name    : str = None ,                                     # Check if meta tag exists with attributes
                       content : str = None ,
                       **attrs
                 ) -> bool:
        for meta in self.meta_tags:
            if name and meta.get('name') != name:
                continue
            if content and meta.get('content') != content:
                continue
            if all(meta.get(k) == v for k, v in attrs.items()):
                return True
        return False

    def find_by_id(self, element_id : str                                         # Find element by id attribute
                   ) -> Optional[Schema__Html_Node]:
        return self.find_by_attribute('id', element_id)

    def find_by_class(self, class_name : str                                      # Find all elements with a specific class
                      ) -> List[Schema__Html_Node]:
        result = []
        for node in self.find_all():
            classes = node.attrs.get('class', '').split()
            if class_name in classes:
                result.append(node)
        return result

    def find_by_tag(self, tag_name : str                                          # Find all elements with a specific tag
                    ) -> List[Schema__Html_Node]:
        return self.find_all_by_tag(tag_name)

    def get_attribute(self, element   : Schema__Html_Node ,                       # Get attribute value from an element
                            attr_name : str
                      ) -> Optional[str]:
        return element.attrs.get(attr_name)

    def get_text(self, element : Optional[Schema__Html_Node] = None               # Get text content of element or document
                 ) -> str:
        if element is None:
            element = self.root
        return self.get_text_content(element)


    # other helper methods
    def find_child_by_tag(self, parent : Schema__Html_Node,                      # Find first direct child with tag
                                tag    : str
                           ) -> Optional[Schema__Html_Node]:
        for child in parent.child_nodes:
            if child.tag == tag:
                return child
        return None

    def find_all_by_tag(self, tag  : str,                                       # Recursively find all nodes with tag
                              node : Optional[Schema__Html_Node] = None
                         ) -> List[Schema__Html_Node]:
        if node is None:
            node = self.root

        result = []
        if node.tag == tag:
            result.append(node)

        for child in node.child_nodes:
            result.extend(self.find_all_by_tag(tag, child))

        return result

    def find_by_attribute(self, attr_name  : str                                ,  # Find first node with attribute value
                                attr_value : str                                ,
                                node       : Optional[Schema__Html_Node] = None
                           ) -> Optional[Schema__Html_Node]:
        if node is None:
            node = self.root

        if node.attrs.get(attr_name) == attr_value:
            return node

        for child in node.child_nodes:
            result = self.find_by_attribute(attr_name, attr_value, child)
            if result:
                return result

        return None

    def find_all(self, node : Optional[Schema__Html_Node] = None                 # Get all nodes in the tree
                  ) -> List[Schema__Html_Node]:
        if node is None:
            node = self.root

        result = [node]
        for child in node.child_nodes:
            result.extend(self.find_all(child))

        return result

    def find_link_by_rel(self, rel_value: str) -> Optional[str]:
        for link in self.links:
            if link.get('rel') == rel_value:
                return link.get('href')
        return None

    def get_text_content(self, node : Schema__Html_Node                           # Get all text content from node
                         ) -> str:
        texts = []

        for text_node in node.text_nodes:                                         # Get text from this node's text_nodes
            texts.append(text_node.data)

        for child in node.child_nodes:                                            # Recursively get text from children
            texts.append(self.get_text_content(child))

        return ''.join(texts)