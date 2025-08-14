import unittest
from datetime                                                                  import datetime
from osbot_utils.helpers.Safe_Id                                               import Safe_Id
from osbot_utils.helpers.llms.cache.LLM_Cache__Path_Generator                  import LLM_Cache__Path_Generator
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Path import Safe_Str__File__Path


class test_LLM_Cache__Path_Generator(unittest.TestCase):
    path_generator: LLM_Cache__Path_Generator

    def setUp(self):
        self.path_generator = LLM_Cache__Path_Generator()

    def test_generate_path__with_only_domains(self):
        domains = [Safe_Id("domain1"), Safe_Id("domain2")]
        path = self.path_generator.generate_path(domains=domains)
        assert "domain1/domain2" == path

    def test_generate_path__with_only_areas(self):
        areas = [Safe_Id("area1"), Safe_Id("area2")]
        path = self.path_generator.generate_path(areas=areas)
        assert "area1/area2" == path

    def test_generate_path__with_only_time(self):
        path = self.path_generator.generate_path(year=2023, month=4, day=15, hour=12)
        assert "2023/04/15/12" == path

    def test_generate_path__with_partial_time(self):
        # Year only
        path = self.path_generator.generate_path(year=2023)
        assert  "2023" == path

        # Year and month only
        path = self.path_generator.generate_path(year=2023, month=4)
        assert "2023/04"== path

        # Month only
        path = self.path_generator.generate_path(month=4)
        assert "04"== path

        # Day only
        path = self.path_generator.generate_path(day=15)
        assert "15"== path

        # Hour only
        path = self.path_generator.generate_path(hour=12)
        assert "12"== path

        # Mixed (skipping components)
        path = self.path_generator.generate_path(year=2023, day=15)
        assert "2023/15"== path

    def test_generate_path__with_all_components(self):
        domains   = [Safe_Id("domain1"), Safe_Id("domain2")]
        areas     = [Safe_Id("area1"), Safe_Id("area2")]
        file_id   = Safe_Id("test-file")
        extension = "json"

        path = self.path_generator.generate_path(year=2023, month=4, day=15, hour=12,
                                                 domains=domains, areas=areas,
                                                file_id=file_id, extension=extension)

        assert "domain1/domain2/2023/04/15/12/area1/area2/test-file.json" == path

    def test_generate_path__with_file_components(self):
        file_id   = Safe_Id("test-file")
        extension = "json"
        path      = self.path_generator.generate_path(file_id=file_id, extension=extension)
        assert "test-file.json"== path

        # With domains and file
        domains = [Safe_Id("domain1")]
        path    = self.path_generator.generate_path(domains=domains, file_id=file_id, extension=extension)
        assert "domain1/test-file.json"== path

    def test_from_date_time(self):
        date_time = datetime(2023, 4, 15, 12, 30, 45)
        domains   = [Safe_Id("domain1" )]
        areas     = [Safe_Id("area1"   )]
        file_id   = Safe_Id("test-file")
        extension = "json"

        path = self.path_generator.from_date_time(date_time = date_time,
                                                  domains   = domains   , areas     = areas    ,
                                                  file_id   = file_id   , extension = extension)

        assert "domain1/2023/04/15/12/area1/test-file.json"== path

    def test_now(self):
        test_time = datetime(2023, 4, 15, 12, 30, 45)                               # Test with a specific timestamp (to make testing deterministic)
        domains   = [Safe_Id("domain1")]
        areas     = [Safe_Id("area1")]
        file_id   = Safe_Id("test-file")
        extension = "json"

        path = self.path_generator.now(domains = domains  , areas     = areas    ,
                                       file_id = file_id  , extension = extension,
                                       now     = test_time)

        assert "domain1/2023/04/15/12/area1/test-file.json"== path



        path = self.path_generator.now(domains=domains, areas=areas,                # Test without providing timestamp (harder to test deterministically)
                                       file_id=file_id, extension=extension)

        assert type(path) is Safe_Str__File__Path                                   # Just ensure it doesn't error and returns a Safe_Str__File__Path
        assert len(path)  >  0