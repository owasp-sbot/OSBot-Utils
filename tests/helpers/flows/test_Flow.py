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

        print('\n\n\n')
        with self.flow as _:
            _.setup()
            _.create_flow()




