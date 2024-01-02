from unittest import TestCase, TestLoader

from osbot_utils.testing.Duration import Duration
from osbot_utils.utils import Misc
from osbot_utils.utils.Dev          import pprint
from osbot_utils.utils.Files import file_contents, parent_folder, folder_files
from osbot_utils.utils.Functions import python_file
from osbot_utils.utils.ast.Ast      import Ast
from osbot_utils.utils.ast.Ast_Visitor import Ast_Visitor
from tests.testing.test_Profiler       import An_Class


class test_Ast_Visit(TestCase):

    def setUp(self):
        self.ast      = Ast()



    def test_visit(self):

        target_file_1 = python_file(TestCase)
        target_file_2 = python_file(TestLoader)
        target_files = [target_file_1, target_file_2]
        #target_folder = parent_folder(parent_folder(parent_folder(target_file_2)))
        #target_files  = folder_files(target_folder, "*.py")
        #pprint(f"total files to process :{len(target_files)}")

        ast_visitor = Ast_Visitor()
        ast_visitor.add_files(target_files)

        stats         = ast_visitor.stats()
        classes_def   = stats.get('nodes').get('Ast_Class_Def'   )
        functions_def = stats.get('nodes').get('Ast_Function_Def')

        assert stats.get('node_count') == 9019
        assert len(stats.get('files_visited')) == 2
        assert classes_def   == 14
        assert functions_def == 136
        #pprint(stats)
