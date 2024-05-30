from unittest import TestCase

import osbot_utils
from osbot_utils.helpers.ssh.SSH import SSH
from osbot_utils.utils.Env import load_dotenv
from osbot_utils.utils.Files import path_combine

ENV_FILE__WITH_ENV_VARS           = "../.ssh.env"

class TestCase__SSH(TestCase):
    ssh : SSH

    @classmethod
    def setUpClass(cls):
        cls.load_dotenv()
        cls.ssh = SSH().setup()

    @staticmethod
    def load_dotenv():
        env_file_path = path_combine(osbot_utils.path, ENV_FILE__WITH_ENV_VARS)
        load_dotenv(dotenv_path=env_file_path)