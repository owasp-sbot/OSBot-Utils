from unittest import TestCase

from osbot_utils.helpers.html.Dict_To_Css import Dict_To_Css



class test_Dict_To_Css(TestCase):

    expected_css_text = ('.base64-image {\n'
                         '    width: 200px;\n'
                         '    height: auto;\n'
                         '    margin-bottom: 1rem;\n'
                         '}\n'
                         '.col {\n'
                         '    border: 2px solid #C0C0FF;\n'
                         '    padding: 10px;\n'
                         '}\n'
                         '.bg-dark {\n'
                         '    font-size: 15px;\n'
                         '}\n'
                         '.var_name {\n'
                         '    font-size: 12px;\n'
                         '}')
    def setUp(self):
        self.dict_to_css = Dict_To_Css()

    def test_convert(self):
        assert self.dict_to_css.convert() == ''

    def test_convert__via_json_data(self):
        css_data             = { ".base64-image" : { "width"         : "200px"           ,
                                                     "height"        : "auto"            ,
                                                     "margin-bottom" : "1rem"            },
                                 ".col"          : { "border"        : "2px solid #C0C0FF",
                                                     "padding"       : "10px"            },
                                 ".bg-dark"      : { "font-size"     : "15px"            },
                                 ".var_name"     : {"font-size"      : "12px"            }}
        self.dict_to_css.css = css_data

        assert self.dict_to_css.convert() == self.expected_css_text

    def test_convert__via_obj_assigment(self):
        css_data             = {}
        self.dict_to_css.css = css_data

        css_data[".base64-image"] = { "width"         : "200px"            ,
                                      "height"        : "auto"             ,
                                      "margin-bottom" : "1rem"              }
        css_data[".col"         ] = { "border"        : "2px solid #C0C0FF",
                                     "padding"        : "10px"              }
        css_data[".bg-dark"     ] = {"font-size"      : "15px"              }
        css_data[".var_name"    ] = {"font-size"      : "12px"              }
        assert self.dict_to_css.convert() == self.expected_css_text

    def test_add_css_entry(self):
        with self.dict_to_css as _:
            _.add_css_entry(selector=".base64-image", data={ "width"         : "200px"             ,
                                                             "height"        : "auto"              ,
                                                             "margin-bottom" : "1rem"              })
            _.add_css_entry(selector=".col"         , data={ "border"         : "2px solid #C0C0FF",
                                                             "padding"        : "10px"             })
            _.add_css_entry(selector=".bg-dark"     , data={ "font-size"      : "15px"             })
            _.add_css_entry(selector=".var_name"    , data={ "font-size"      : "12px"             })
            assert _.convert() == self.expected_css_text

