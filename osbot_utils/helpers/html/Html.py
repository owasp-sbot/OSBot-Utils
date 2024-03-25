from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

TAG_HTML = 'html'

class Html(Kwargs_To_Self):
    doc_type: bool = True
    lang    : str

    def render(self):
        if self.doc_type:
            html = "<!DOCTYPE html>\n"
        else:
            html = ""
        attributes = {}
        if self.lang:
            attributes['lang'] = self.lang
        attributes = self.render_attributes(attributes)
        html += self.render_element(TAG_HTML, attributes)
        return html

    def render_attributes(self, attributes):
        attributes = ' '.join([f'{key}="{value}"' for key, value in attributes.items()])
        return attributes

    def render_element(self, html_tag, attributes):
        if attributes:
            return f"<{html_tag} {attributes}></{html_tag}>"
        return f"<{html_tag}></{html_tag}>"


