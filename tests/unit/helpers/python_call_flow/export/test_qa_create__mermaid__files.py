# # ═══════════════════════════════════════════════════════════════════════════════
# # Mermaid Exporter Tests
# # ═══════════════════════════════════════════════════════════════════════════════
# import types
# from unittest                                                                       import TestCase
#
# from osbot_utils.helpers.python_call_flow.export.Call_Flow__Exporter__Mermaid import Call_Flow__Exporter__Mermaid
# from osbot_utils.helpers.python_call_flow.extract.Call_Flow__Analyzer import Call_Flow__Analyzer
# from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data import Sample__Simple_Class, QA__Call_Flow__Test_Data
# from osbot_utils.utils.Files import path_combine, file_save, folder_create
#
#
# #
# #
# class test_qa_create__mermaid__files(TestCase):                                   # Test Mermaid export
# #
#     @classmethod
#     def setUpClass(cls):                                                             # Shared setup
#         cls.qa_test_data  = QA__Call_Flow__Test_Data()
#         #cls.result       = cls.qa.create_result__self_calls()                              # Cached result
#         #cls.simple_class =  cls.qa.get_sample_class__simple()
# #
#     def test__save_simple_class(self):                                                          # Test exporter initialization
#         def create__call_flow__file__for_target(target):
#             if type(target) is type:
#                 file_name = target.__name__
#             elif type(target) is types.FunctionType:
#                 file_name = target.__name__
#             else:
#                 raise ValueError(f"unsupported target type: {type(target)}")
#             with Call_Flow__Analyzer() as call_flow_analyser:
#                 call_flow_analyser.current_depth = 3
#                 result   = call_flow_analyser.analyze(target)
#             exporter = Call_Flow__Exporter__Mermaid(result=result).setup()
#             html     = exporter.to_html()
#             target_folder = path_combine(__file__, '../_saved_html/5-Jan')
#             folder_create(target_folder)
#             target_file   = path_combine(target_folder, f'call-flow_{file_name}.html')
#             file_save(html, path=target_file)
#
#         with self.qa_test_data  as _:
#             from osbot_utils.type_safe.Type_Safe import Type_Safe
#             class An_Class(Type_Safe):
#                 an_str : str = '42'
#
#             #create__call_flow__file__for_target(_.get_sample_class__simple())
#             #create__call_flow__file__for_target(_.get_sample_class__self_calls())
#             #create__call_flow__file__for_target(_.get_sample_class__deep_calls())
#             #create__call_flow__file__for_target(_.get_sample_function__helper())
#             #create__call_flow__file__for_target(_.get_sample_function__standalone())
#             #create__call_flow__file__for_target(An_Class.__init__)



#from previous version

#         with graph_ids_for_tests():
#             with Call_Flow__Analyzer() as analyzer:
#
#                 def analyse_target(target, depth):
#                     analyzer.config.max_depth=depth
#                     graph = analyzer.analyze(Call_Flow__Analyzer)
#
#                     with Call_Flow__Exporter__Mermaid(graph=graph) as _:
#                         _.direction     = 'LR'
#                         _.max_label_len = 100
#                         _.font_size = 40
#                         html          = _.to_html()
#                         target_folder = path_combine(__file__, '../_saved_html')
#                         target_file   = path_combine(target_folder, f'call-flow__{target.__name__}__depth-{depth}' + '.html')
#
#                         file_save(html, path=target_file)
#                     #print(target_file)
#
#                 # analyse_target(An_Class__Python    , 0)
#                 # analyse_target(An_Class__Type__Safe, 0)
#                 # analyse_target(An_Class__Python    , 1)
#                 # analyse_target(An_Class__Type__Safe, 1)
#                 # analyse_target(An_Class__Python    , 2)
#                 # analyse_target(An_Class__Type__Safe, 2)
#                 analyse_target(Call_Flow__Analyzer, 1)
#                 analyse_target(Call_Flow__Analyzer, 2)
#
#                 # target = sample_function
#                 # target = Sample__Helper
#                 #target = test_Call_Flow__Exporter__Mermaid.test_create_mermaid_html
#                 #target  = Call_Flow__Analyzer
#                 #target = An_Class__Python
#
