from unittest import TestCase, TestLoader
from osbot_utils.utils.Functions import python_file
from osbot_utils.utils.ast.Ast      import Ast
from osbot_utils.utils.ast.Ast_Load import Ast_Load


class test_Ast_Load(TestCase):

    def setUp(self):
        self.ast      = Ast()

    def test_load_files(self):
        target_file_1 = python_file(TestCase)
        target_file_2 = python_file(TestLoader)
        target_files = [target_file_1, target_file_2]
        #target_folder = parent_folder(parent_folder(parent_folder(target_file_2)))
        #target_files  = folder_files(target_folder, "*.py")
        #pprint(f"total files to process :{len(target_files)}")

        ast_load = Ast_Load()
        ast_load.load_files(target_files)

        stats         = ast_load.stats()
        classes_def   = stats.get('nodes').get('Ast_Class_Def'   )
        functions_def = stats.get('nodes').get('Ast_Function_Def')

        assert stats.get('node_count') == 9019
        assert len(stats.get('files_visited')) == 2
        assert classes_def   == 14
        assert functions_def == 136
        #pprint(stats)

