from os                                             import environ
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.helpers.sqlite.Sqlite__Database    import Sqlite__Database
from osbot_utils.utils.Files                        import current_temp_folder, path_combine

ENV_NAME_PATH_LOCAL_DBS        = 'PATH_LOCAL_DBS'

class Sqlite__DB__Local(Sqlite__Database):
    db_name     : str

    def __init__(self, db_path=None):
        super().__init__(db_path=db_path or self.path_local_db())

    def path_db_folder(self):
        return environ.get(ENV_NAME_PATH_LOCAL_DBS) or current_temp_folder()

    def path_local_db(self):
        return path_combine(self.path_db_folder(), self.db_name)
