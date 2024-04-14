from osbot_utils.helpers.html.Dict_To_Css import Dict_To_Css
from osbot_utils.helpers.html.Tag__Base import Tag__Base, INDENT_SIZE


class Tag__Style(Tag__Base):
    tag_name    : str = 'style'
    dict_to_css : Dict_To_Css

    def add_css_entry(self, selector, data):
        self.dict_to_css.add_css_entry(selector,data)
        return self

    def css(self):
        return self.dict_to_css.css

    def render(self):
        if self.dict_to_css.css:
            css_indent          = self.indent +1
            css_indent_text     = " " * css_indent * INDENT_SIZE
            element_indent_text = " " * self.indent * INDENT_SIZE
            self.inner_html = '\n' + self.dict_to_css.convert(indent=css_indent_text) + '\n' + element_indent_text
        return super().render()

    def set_css(self, css):
        self.dict_to_css.css = css