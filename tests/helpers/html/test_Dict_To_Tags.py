from unittest import TestCase

from osbot_utils.helpers.html.Dict_To_Tags import Dict_To_Tags
from osbot_utils.helpers.html.Html_To_Dict import Html_To_Dict
from osbot_utils.utils.Dev import pprint
from tests._test_data.Sample_Test_Files import Sample_Test_Files


class test_Dict_To_Tags(TestCase):


    def test_convert(self):
        sample_test_files = Sample_Test_Files()
        html              = sample_test_files.html_bootstrap_example()
        html_to_dict      = Html_To_Dict(html)
        root              = html_to_dict.convert()

        dict_to_tags      = Dict_To_Tags(root)
        root_tag          = dict_to_tags.convert()

        root_tag_html = root_tag.render()


        assert root_tag_html == """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8"></meta>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
        <title>Simple Bootstrap 5 Webpage</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" rel="stylesheet"/>
    </head>
</html>"""



        #pprint(root)
        #root['children'] = []
        #print()
        #print()
        #html_to_dict.print()