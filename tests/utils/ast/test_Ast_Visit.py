from unittest import TestCase

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
        print()
        # with Duration(prefix='ast_module'):
        #     ast_module = self.ast.ast_module__from(TestCase)

        #ast_module = self.ast.ast_module__from(An_Class)

        with Duration(prefix='list_files'):
            target_file_1 = python_file(TestCase)
            target_file_2 = python_file(Misc)
            #target_folder = parent_folder(parent_folder(parent_folder(target_file_2)))
            target_folder = parent_folder(target_file_2)
            target_files  = folder_files(target_folder, "*.py")
            pprint(f"total files to process :{len(target_files)}")

            #target_files = target_files[800:1300]
            #pprint(f"files to proces :{len(target_files)}")

        ast_visitor = Ast_Visitor()
        #ast_visitor.add_file(target_file_1)
        #ast_visitor.add_file(target_file_2)

        with Duration(prefix='add_files'):
            ast_visitor.add_files(target_files)
        # ast_visitor.visit(ast_module_1.node)
        # ast_visitor.visit(ast_module_2.node)

        with Duration(prefix='stats'):
            stats = ast_visitor.stats()
            pprint('node_count', stats.get('node_count'))
            pprint('files_visited', len(stats.get('files_visited')))
            pprint(stats)
