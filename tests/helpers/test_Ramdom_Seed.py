from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.helpers.Random_Seed import Random_Seed, DEFAULT_VALUE__RANDOM_SEED
from osbot_utils.utils.Misc import random_int, random_text, random_uuid, random_password, random_port, random_filename, \
    random_bytes


class test_Ramdom_Seed(TestCase):

    def test__init__(self):
        seed = random_int()
        assert Random_Seed(seed).seed == seed

        assert Random_Seed().seed == DEFAULT_VALUE__RANDOM_SEED

    def test_next_ints(self):
        expected_next_int         = 41906
        expected_next_ints        = [7297, 1640, 48599, 18025]
        seed  = 42
        size  = 4

        def check_random_but_deterministic_values():
            with Random_Seed(seed) as _:
                assert _.next_int()             == expected_next_int
                assert list(_.next_ints(size))  == expected_next_ints
                assert random_int ()            == 16050                                            # these should now be deterministic
                assert random_text()            == "text_I0Y6DPBHSAHX"
                assert random_password()        == 'Zu$]a_.Fo5Fij_%__Y7JZ^_|'
                assert random_port()            == 57837
                assert random_filename()        == 'gcx1945nq4.tmp'
                # assert random_uuid()            == 'eee90437-216d-4a23-95f6-6fd570100714'                             # not impacted by random.seed
                # assert random_bytes()           == b'\x9cLg\xcc\xe1yuj\xa2M\xdf\x96\x85\x1b\xc26\x8b\x99iq]I\x93\x1f'

        check_random_but_deterministic_values()                                                 # run once

        assert random_int() != 26447                                                            # these should (again) be random
        assert random_text() != "text_6TXUMC47BQ0W"

        check_random_but_deterministic_values()                                                 # run couple more tims to confirm that even after multiple excecutions
        check_random_but_deterministic_values()                                                 # we still get the same values (random but deterministic)


