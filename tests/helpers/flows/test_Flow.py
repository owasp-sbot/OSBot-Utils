from unittest import TestCase

from osbot_utils.helpers.flows.Flow import Flow


class test_Flow(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flow = Flow()

    def test_random_flow_id(self):
        with self.flow as _:
            assert _.flow_id == self.flow.flow_id
            #assert _.flow_id.startswith('FLOW_ID__PREFIX_')

    def test_create_flow(self):

        def an_flow():
            print('this is inside the flow')

        print('\n\n\n')
        with self.flow as _:
            _.setup()
            _.set_flow_target(an_flow)
            _.set_flow_target(self.test_create_flow)
            _.create_flow()
            _.execute_flow()




