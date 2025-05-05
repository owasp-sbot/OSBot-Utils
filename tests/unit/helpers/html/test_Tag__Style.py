from unittest                            import TestCase
from osbot_utils.helpers.html.Tag__Style import Tag__Style


class test_Tag__Style(TestCase):

    expected_css_html = ('        <style>\n'
                         '            .base64-image {\n'
                         '                width: 200px;\n'
                         '                height: auto;\n'
                         '                margin-bottom: 1rem;\n'
                         '            }\n'
                         '            .col {\n'
                         '                border: 2px solid #C0C0FF;\n'
                         '                padding: 10px;\n'
                         '            }\n'
                         '            .bg-dark {\n'
                         '                font-size: 15px;\n'
                         '            }\n'
                         '            .var_name {\n'
                         '                font-size: 12px;\n'
                         '            }\n'
                         '        </style>')
    def setUp(self):
        self.tag_style = Tag__Style()
        self.tag_style.indent=2

    def test_render(self):
        assert self.tag_style.render() == "        <style></style>"

    def test_render__via_json_data(self):
        css_data             = { ".base64-image" : { "width"         : "200px"           ,
                                                     "height"        : "auto"            ,
                                                     "margin-bottom" : "1rem"            },
                                 ".col"          : { "border"        : "2px solid #C0C0FF",
                                                     "padding"       : "10px"            },
                                 ".bg-dark"      : { "font-size"     : "15px"            },
                                 ".var_name"     : {"font-size"      : "12px"            }}
        self.tag_style.set_css(css_data)

        assert self.tag_style.render() == self.expected_css_html

    def test_add_css_entry(self):
        with self.tag_style as _:
            _.add_css_entry(selector=".base64-image", data={ "width"         : "200px"             ,
                                                             "height"        : "auto"              ,
                                                             "margin-bottom" : "1rem"              })
            _.add_css_entry(selector=".col"         , data={ "border"         : "2px solid #C0C0FF",
                                                             "padding"        : "10px"             })
            _.add_css_entry(selector=".bg-dark"     , data={ "font-size"      : "15px"             })
            _.add_css_entry(selector=".var_name"    , data={ "font-size"      : "12px"             })
            assert _.render() == self.expected_css_html
