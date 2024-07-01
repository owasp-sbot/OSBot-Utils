from unittest                                   import TestCase

import pytest

from osbot_utils.helpers.Hashicorp_Secrets import Hashicorp_Secrets
from osbot_utils.utils.Env                      import load_dotenv
from osbot_utils.utils.Misc                     import list_set

class test_Hashicorp_Secrets(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.hc_secrets = Hashicorp_Secrets()
        if cls.hc_secrets.hcp__enabled() is False:
            pytest.skip("Skipping Hashicorp_Secrets since required env vars are not setup")

    def test_hcp__access_token(self):
        with self.hc_secrets as _:
            access_token = _.hcp__access_token()
            assert access_token is not None

    def test_app_secrets(self):
        with self.hc_secrets as _:
            app_secrets = _.app_secrets()
            assert len(app_secrets) > 0
            for app_secret in app_secrets:
                assert list_set(app_secret) == ['created_at', 'created_by', 'latest_version', 'name', 'sync_status', 'version']

    def test_app_secrets_open(self):
        with self.hc_secrets as _:
            app_secrets = _.app_secrets_open()
            assert len(app_secrets) > 0
            for app_secret in app_secrets:
                secret_version = app_secret.get('version')
                assert list_set(app_secret)     == ['created_at', 'created_by', 'created_by_id', 'latest_version', 'name', 'sync_status', 'version']
                assert list_set(secret_version) == ['created_at', 'created_by', 'created_by_id', 'type', 'value', 'version']

    def test_app_secrets_names(self):
        with self.hc_secrets as _:
            secrets_names = _.app_secrets_names()
            assert len(secrets_names) > 0
            for secret_name in secrets_names:
                assert type(secret_name) is str

    def test_app_secrets_values(self):
        with self.hc_secrets as _:
            secrets_values = _.app_secrets_values()
            assert len(secrets_values) > 0
            for secret_name, secret_value in secrets_values.items():
                assert type(secret_name ) is str
                assert type(secret_value) is str

    def test_apps(self):
        with self.hc_secrets as _:
            apps = _.apps()
            assert len(apps) > 0
            for app in apps :
                assert list_set(app) == ['created_at', 'created_by', 'description',
                                         'location', 'name', 'secret_count',
                                         'sync_integrations', 'updated_at', 'updated_by']