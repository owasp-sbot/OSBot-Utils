from unittest import TestCase

import pytest

from osbot_utils.helpers.CFormat import CFormat, f_black, f_red, f_blue, f_cyan, f_grey, f_green, f_none, f_magenta, \
    f_white, f_yellow, f_bright_black, f_bright_red, f_bright_green, f_bright_yellow, f_bright_blue, f_bright_magenta, \
    f_bright_cyan, f_bright_white, f_dark_red


class Test_CFormat(TestCase):

    cformat : CFormat

    @classmethod
    def setUpClass(cls):
        cls.cformat =  CFormat()

    def test__init__(self):
        with self.cformat as _:
            assert _.apply_colors is True

    def test_colors(self):
        with self.cformat  as _:
            assert _.black          ("test") == "\033[30mtest\033[0m"
            assert _.blue           ("test") == "\033[34mtest\033[0m"
            assert _.cyan           ("test") == "\033[36mtest\033[0m"
            assert _.grey           ("test") == "\033[38;5;15mtest\033[0m"
            assert _.green          ("test") == "\033[32mtest\033[0m"
            assert _.none           ("test") == '\x1b[0mtest\x1b[0m'
            assert _.magenta        ("test") == "\033[35mtest\033[0m"
            assert _.red            ("test") == "\033[31mtest\033[0m"
            assert _.white          ("test") == "\033[38;5;15mtest\033[0m"
            assert _.yellow         ("test") == "\033[33mtest\033[0m"
            assert _.bright_black   ("test") == "\033[90mtest\033[0m"
            assert _.bright_red     ("test") == "\033[91mtest\033[0m"
            assert _.bright_green   ("test") == "\033[92mtest\033[0m"
            assert _.bright_yellow  ("test") == "\033[93mtest\033[0m"
            assert _.bright_blue    ("test") == "\033[94mtest\033[0m"
            assert _.bright_magenta ("test") == "\033[95mtest\033[0m"
            assert _.bright_cyan    ("test") == "\033[96mtest\033[0m"
            assert _.bright_white   ("test") == "\033[97mtest\033[0m"
            assert _.dark_red       ("test") == "\033[38;5;124mtest\033[0m"

            result = _.apply_color_to_text("red", "test")
            assert result == "\033[31mtest\033[0m"

            result = _.apply_color_code_to_text("31", "test")
            assert result == "\033[31mtest\033[0m"

            result = _.text_with_colors("31", "test")
            assert result == "\033[31mtest\033[0m"

            _.apply_colors = False
            result = _.text_with_colors("31", "test")
            assert result == "test"
            _.apply_colors = True

    def test_colors__using_static_methods(self):
        text = 'some text'

        with self.cformat  as _:
            assert f_black         (text) == _.black         (text)
            assert f_blue          (text) == _.blue          (text)
            assert f_cyan          (text) == _.cyan          (text)
            assert f_grey          (text) == _.grey          (text)
            assert f_green         (text) == _.green         (text)
            assert f_none          (text) == _.none          (text)
            assert f_magenta       (text) == _.magenta       (text)
            assert f_red           (text) == _.red           (text)
            assert f_white         (text) == _.white         (text)
            assert f_yellow        (text) == _.yellow        (text)
            assert f_bright_black  (text) == _.bright_black  (text)
            assert f_bright_red    (text) == _.bright_red    (text)
            assert f_bright_green  (text) == _.bright_green  (text)
            assert f_bright_yellow (text) == _.bright_yellow (text)
            assert f_bright_blue   (text) == _.bright_blue   (text)
            assert f_bright_magenta(text) == _.bright_magenta(text)
            assert f_bright_cyan   (text) == _.bright_cyan   (text)
            assert f_bright_white  (text) == _.bright_white  (text)
            assert f_dark_red      (text) == _.dark_red      (text)

    def test_auto_bold(self):
        cformat = self.cformat
        cformat.auto_bold = True
        text = 'some text'
        with self.cformat as _:
            result = _.red(text)
            assert result == "\033[1m\033[31m" + text + "\033[0m\033[0m"

        cformat.auto_bold = False
        with self.cformat as _:
            result = _.red(text)
            assert result == "\033[31m" + text + "\033[0m"


    def test_rgb(self):
        text = 'some text'
        with self.cformat as _:
            result = _.rgb(255, 0, 0, text)
            assert result == "\033[38;2;255;0;0m" + text + "\033[0m"

    def test_bg_rgb(self):
        text = 'some text'
        with self.cformat as _:
            result = _.bg_rgb(0, 255, 0, text)
            assert result == "\033[48;2;0;255;0m" + text + "\033[0m"

    def test_cmyk(self):
        text = 'some text'
        with self.cformat as _:
            result = _.cmyk(0, 100, 100, 0, text)
            assert result == "\033[38;2;255;0;0m" + text + "\033[0m"

    def test_bg_cmyk(self):
        text = 'some text'
        with self.cformat as _:
            result = _.bg_cmyk(100, 0, 0, 0, text)
            assert result == "\033[48;2;0;255;255m" + text + "\033[0m"

    def test_hex_color(self):
        cformat = self.cformat
        text = 'some text'
        with self.cformat as _:
            result = _.hex("#1122BA", text)
            assert result == "\033[38;2;17;34;186m" + text + "\033[0m"

    def test_bg_hex_color(self):
        cformat = self.cformat
        text = 'some text'
        with self.cformat as _:
            result = _.bg_hex("#1122BA", text)
            assert result == "\033[48;2;17;34;186m" + text + "\033[0m"