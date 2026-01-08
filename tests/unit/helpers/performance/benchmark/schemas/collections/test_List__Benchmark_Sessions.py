# ═══════════════════════════════════════════════════════════════════════════════
# test_List__Benchmark_Sessions - Tests for benchmark sessions list
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                       import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Sessions         import List__Benchmark_Sessions
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Session   import Schema__Perf__Benchmark__Session
from osbot_utils.helpers.performance.benchmark.testing.QA__Benchmark__Test_Data                     import QA__Benchmark__Test_Data
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                               import Type_Safe__List


class test_List__Benchmark_Sessions(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.test_data = QA__Benchmark__Test_Data()

    def test__init__(self):                                                      # Test initialization
        with List__Benchmark_Sessions() as _:
            assert type(_) is List__Benchmark_Sessions
            assert isinstance(_, Type_Safe__List)
            assert len(_)  == 0

    def test_type_constraint(self):                                              # Test type definition
        assert List__Benchmark_Sessions.expected_type is Schema__Perf__Benchmark__Session

    def test_append(self):                                                       # Test appending items
        sessions = List__Benchmark_Sessions()
        session  = self.test_data.create_session(title='Session 1')

        sessions.append(session)

        assert len(sessions) == 1

    def test_access_by_index(self):                                              # Test index access
        sessions = List__Benchmark_Sessions()
        session  = self.test_data.create_session(title='Session 1')

        sessions.append(session)
        retrieved = sessions[0]

        assert retrieved is session
        assert type(retrieved) is Schema__Perf__Benchmark__Session

    def test_multiple_sessions(self):                                            # Test multiple sessions
        sessions = List__Benchmark_Sessions()

        for i in range(3):
            session = self.test_data.create_session(title=f'Session {i+1}')
            sessions.append(session)

        assert len(sessions)        == 3
        assert str(sessions[0].title) == 'Session 1'
        assert str(sessions[1].title) == 'Session 2'
        assert str(sessions[2].title) == 'Session 3'

    def test_iteration(self):                                                    # Test iterating over list
        sessions = List__Benchmark_Sessions()

        for i in range(2):
            session = self.test_data.create_session(title=f'Session {i+1}')
            sessions.append(session)

        count = 0
        for session in sessions:
            assert type(session) is Schema__Perf__Benchmark__Session
            count += 1

        assert count == 2

    def test_len(self):                                                          # Test length
        sessions = List__Benchmark_Sessions()

        assert len(sessions) == 0

        sessions.append(self.test_data.create_session())
        assert len(sessions) == 1

        sessions.append(self.test_data.create_session())
        assert len(sessions) == 2

    def test_negative_index(self):                                               # Test negative indexing
        sessions = List__Benchmark_Sessions()

        sessions.append(self.test_data.create_session(title='First'))
        sessions.append(self.test_data.create_session(title='Last'))

        assert str(sessions[-1].title) == 'Last'
        assert str(sessions[-2].title) == 'First'

    def test_slice(self):                                                        # Test slicing
        sessions = List__Benchmark_Sessions()

        for i in range(4):
            sessions.append(self.test_data.create_session(title=f'Session {i+1}'))

        sliced = sessions[1:3]
        assert len(sliced) == 2

    def test_contains(self):                                                     # Test membership check
        sessions = List__Benchmark_Sessions()
        session  = self.test_data.create_session()

        sessions.append(session)

        assert session in sessions

    def test_empty_list_operations(self):                                        # Test empty list
        sessions = List__Benchmark_Sessions()

        assert len(sessions)      == 0
        assert list(sessions)     == []
        assert bool(sessions)     is False                                       # Empty list is falsy
