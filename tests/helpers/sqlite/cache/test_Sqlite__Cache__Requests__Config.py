from osbot_utils.helpers.sqlite.cache.TestCase__Sqlite__Cache__Requests import TestCase__Sqlite__Cache__Requests


class test_Sqlite__Cache__Requests__Config(TestCase__Sqlite__Cache__Requests):


    def test_disable(self):
        with self.sqlite_cache_requests as _:
            assert _.config.enabled is True
            _.disable()
            assert _.config.enabled is False
            _.enable()
            assert _.config.enabled is True

    def test_only_from_cache(self):
        with self.sqlite_cache_requests as _:
            assert _.config.cache_only_mode is False
            _.only_from_cache()
            assert _.config.cache_only_mode is True
            _.only_from_cache(False)
            assert _.config.cache_only_mode is False

    def test_update(self):
        with self.sqlite_cache_requests as _:
            assert _.config.update_mode is False
            _.update()
            assert _.config.update_mode is True
            _.update(False)
            assert _.config.update_mode is False
