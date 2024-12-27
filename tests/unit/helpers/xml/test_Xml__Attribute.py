from unittest                               import TestCase
from osbot_utils.helpers.xml.Xml__Attribute import Xml__Attribute

class test_Xml__Attribute(TestCase):
    def test_create_attribute(self):                                            # Test attribute creation
        attribute = Xml__Attribute(name='test', value='value', namespace='ns')
        assert attribute.name == 'test'
        assert attribute.value == 'value'
        assert attribute.namespace == 'ns'

    def test_attribute_to_string(self):                                        # Test string representation
        attribute = Xml__Attribute(name='test', value='value', namespace='ns')
        assert attribute.json() == {'name': 'test', 'value': 'value', 'namespace': 'ns'}