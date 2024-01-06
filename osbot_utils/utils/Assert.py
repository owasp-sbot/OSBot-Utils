import re
import datetime

from osbot_utils.utils.Objects import class_name


class Assert:
    def __init__(self ,target):
        self.target = target

    def is_class(self, name):
        assert class_name(self.target) in name

    def contains(self, text):
        assert text in self.target

    def field_is_equal(self, field_name, expected_value=None):
        field_value = self.target.get(field_name)
        assert  field_value == expected_value , "{0} != {1}".format(field_value, expected_value)
        return self

    def is_bigger_than(self, value):
        if type(self.target) is list:
            list_len = len(self.target)
            assert  list_len > value   , "array with len {0} was not bigger than {1}".format(list_len, value)
        else:
            assert self.target > value , "value {0} was not bigger than {1}".format(self.target, value)
        return self

    def is_smaller_than(self, value):
        if type(self.target) is list:
            list_len = len(self.target)
            assert  list_len < value   , "array with len {0} was not smaller than {1}".format(list_len, value)
        else:
            assert self.target < value , "value {0} was not smaller than {1}".format(self.target, value)
        return self

    def is_equal(self, to):
        assert self.target == to

    def is_today(self):
        assert type(self.target) == datetime.datetime
        assert str(self.target.date())  == str(datetime.datetime.utcnow().date())

    def match_regex(self, regex):
        assert re.compile(regex).match(self.target) is not None

    def size_is(self, to):
        assert len(self.target) == to

    def regex_not_match(self,regex):
        assert re.compile(regex).match(self.target) is None
