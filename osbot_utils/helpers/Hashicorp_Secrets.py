from osbot_utils.utils.Env                  import get_env
from osbot_utils.base_classes.Type_Safe     import Type_Safe
from osbot_utils.utils.Lists                import list_index_by
from osbot_utils.utils.Misc                 import list_set

ENV_VAR__HCP_ACCESS_TOKEN    = 'HCP_ACCESS_TOKEN'
ENV_VAR__HCP_APP_NAME        = 'HCP_APP_NAME'
ENV_VAR__HCP_CLIENT_ID       = 'HCP_CLIENT_ID'
ENV_VAR__HCP_CLIENT_SECRET   = 'HCP_CLIENT_SECRET'
ENV_VAR__HCP_ORGANIZATION_ID = 'HCP_ORGANIZATION_ID'
ENV_VAR__HCP_PROJECT_ID      = 'HCP_PROJECT_ID'

class Hashicorp_Secrets(Type_Safe):

    # helper methods
    def hcp__auth_details(self):
        client_id     = get_env(ENV_VAR__HCP_CLIENT_ID)
        client_secret = get_env(ENV_VAR__HCP_CLIENT_SECRET)
        return client_id, client_secret

    def hcp__access_token(self):                                                                    # todo: refactor to remove dependency on requests package (which is not part of the OSBOt_utils project)
        import requests

        access_token = get_env(ENV_VAR__HCP_ACCESS_TOKEN)                   # todo: add better way to detect when the access token as expired
        if not access_token:

            client_id, client_secret = self.hcp__auth_details()
            token_url               = 'https://auth.idp.hashicorp.com/oauth2/token'
            payload                 = { 'client_id'     : client_id                     ,
                                        'client_secret' : client_secret                 ,
                                        'grant_type'    : 'client_credentials'          ,
                                        'audience'      : 'https://api.hashicorp.cloud' }

            response = requests.post(token_url, data=payload)                                       # todo: refactor into requests_post method
            if response.status_code == 200:
                access_token = response.json().get('access_token')
        return access_token

    def hcp__enabled(self):
        if self.hcp__organization_id():
            if self.hcp__project_id():
                return True
        return False

    def hcp__app_name(self):
        return get_env(ENV_VAR__HCP_APP_NAME)

    def hcp__organization_id(self):
        return get_env(ENV_VAR__HCP_ORGANIZATION_ID)

    def hcp__project_id(self):
        return get_env(ENV_VAR__HCP_PROJECT_ID)

    def requests_get(self, path, data_field=None):
        import requests

        organization_id = self.hcp__organization_id()
        project_id      = self.hcp__project_id()
        headers         = {'Authorization': f"Bearer  { self.hcp__access_token()}" }
        url             = f"https://api.cloud.hashicorp.com/secrets/2023-06-13/organizations/{organization_id}/projects/{project_id}/{path}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            if data_field is None:
                data_field = path
            return json_data.get(data_field)
        return {}

    # API methods
    def app_secrets(self, app_name=None):
        if app_name is None:
            app_name = self.hcp__app_name()
        path_secrets = f'apps/{app_name}/secrets'
        app_secrets  = self.requests_get(path_secrets, 'secrets')
        return app_secrets

    def app_secrets_open(self, app_name=None):
        if app_name is None:
            app_name = self.hcp__app_name()
        path_secrets = f'apps/{app_name}/open'
        app_secrets  = self.requests_get(path_secrets, 'secrets')
        return app_secrets

    def app_secrets_names(self, app_name=None):
        app_secrets = self.app_secrets(app_name)
        return list_set(list_index_by(app_secrets, 'name'))

    def app_secrets_values(self, app_name=None):
        secrets_values = {}
        app_secrets    = self.app_secrets_open(app_name)
        for app_secret in app_secrets:
            secret_name                 = app_secret.get('name'       )
            secret_value                = app_secret.get('version', {}).get('value')
            secrets_values[secret_name] = secret_value
        return secrets_values



    def apps(self):
        return self.requests_get('apps')

