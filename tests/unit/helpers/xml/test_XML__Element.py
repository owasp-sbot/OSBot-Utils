from unittest                               import TestCase
from osbot_utils.helpers.xml.Xml__Attribute import Xml__Attribute
from osbot_utils.helpers.xml.Xml__Element   import XML__Element


class test_XML__Element(TestCase):
    def setUp(self):
        self.basic_element = XML__Element(                                      # Create basic element for tests
            tag='test',
            attributes={},
            children=['text content']
        )

    def test_create_element(self):                                             # Test element creation
        assert self.basic_element.tag == 'test'
        assert self.basic_element.children == ['text content']
        assert isinstance(self.basic_element.attributes, dict)

    def test_element_with_attributes(self):                                    # Test element with attributes
        attribute = Xml__Attribute(name='attr', value='val', namespace='')
        element = XML__Element(
            tag='test',
            attributes={'attr': attribute},
            children=[]
        )
        assert element.attributes['attr'].value == 'val'

    def test_element_with_nested_children(self):                               # Test nested elements
        child = XML__Element(tag='child', attributes={}, children=['child text'])
        parent = XML__Element(tag='parent',
                              attributes={},
                              children=[child] )
        assert isinstance(parent.children[0], XML__Element)
        assert parent.children[0].tag == 'child'
        assert parent.children[0].children[0] == 'child text'