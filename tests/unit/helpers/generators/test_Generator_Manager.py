import pytest
import _thread
import threading
from types                                                      import GeneratorType
from unittest                                                   import TestCase
from threading                                                  import Thread, Event
from time                                                       import sleep
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                            import Random_Guid
from osbot_utils.helpers.generators.Generator_Context_Manager   import Generator_Context_Manager
from osbot_utils.helpers.generators.Generator_Manager           import Generator_Manager
from osbot_utils.helpers.generators.Model__Generator_State      import Model__Generator_State
from osbot_utils.utils.Env                                      import not_in_github_action
from osbot_utils.utils.Misc                                     import is_guid


class test_Generator_Manager(TestCase):

    def setUp(self):
        self.manager = Generator_Manager()
        pass

    def test__init__(self):
        with self.manager as _:
           assert type(_) is Generator_Manager
           assert type(_.lock) is not threading.RLock                                               # confirm behaviour of threading.RLock()
           assert type(_.lock) is _thread.RLock                                                     # return an object of type _thread.RLock

    def test_add_and_get_generator(self):
        def sample_generator():
            yield 1

        gen = sample_generator()
        target_id = self.manager.add(gen)

        self.assertIsInstance(target_id, Random_Guid)
        self.assertEqual(len(self.manager.generators), 1)
        generator = self.manager.generator(target_id)
        self.assertEqual(generator.target, gen)
        self.assertEqual(generator.state, Model__Generator_State.RUNNING)


        assert self.manager.status() == { 'data': { 'running': [{ 'target_id'         : target_id        ,
                                                                  'target_state'      : 'running'         ,
                                                                  'target_method_name': 'sample_generator'}]},
                                         'running': 1}

    def test_add_duplicate_generator(self):
        def sample_generator():
            yield 1

        gen = sample_generator()
        self.manager.add(gen)

        with self.assertRaises(ValueError):
            self.manager.add(gen)

    def test_stop_generator(self):
        def sample_generator():
            yield 1

        target_id = self.manager.add(sample_generator())
        self.assertTrue(self.manager.stop(target_id))
        generator = self.manager.generator(target_id)
        self.assertEqual(generator.state, Model__Generator_State.STOPPING)

    def test_stop_all_generators(self):
        target_ids = []
        for _ in range(3):
            generator = (x for x in [1, 2, 3])
            target_id = self.manager.add(generator)
            target_ids.append(target_id)

        stopped = self.manager.stop_all()
        self.assertEqual(stopped, 3)

        for target_id in target_ids:
            generator = self.manager.generator(target_id)
            self.assertEqual(generator.state, Model__Generator_State.STOPPING)

    def test_cleanup_stopped_generators(self):
        target_ids = []
        for _ in range(3):
            generator = (x for x in [1, 2, 3])
            target_id = self.manager.add(generator)
            target_ids.append(target_id)

        for target_id in target_ids:
            generator = self.manager.generator(target_id)
            generator.state = Model__Generator_State.STOPPED

        cleaned = self.manager.cleanup()
        self.assertEqual(cleaned, 3)
        self.assertEqual(len(self.manager.generators), 0)

    def test_thread_safety(self):
        stop_event = Event()
        results = {'adds': 0, 'errors': 0}

        def worker():
            while not stop_event.is_set():
                try:
                    generator = (x for x in [1, 2, 3])
                    self.manager.add(generator)
                    results['adds'] += 1
                except ValueError:
                    results['errors'] += 1
                sleep(0.001)                                                        # Small delay to increase thread interleaving

        threads = [Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()

        sleep(0.001)                                                                  # Let threads run for a bit
        stop_event.set()

        for t in threads:
            t.join()

        self.assertTrue(results['adds'] > 0)
        self.assertEqual(len(self.manager.generators), results['adds'])

    def test_active_generators(self):
        target_ids = []
        for _ in range(3):
            generator = (x for x in [1, 2, 3])
            assert type(generator) is GeneratorType
            target_id = self.manager.add(generator)
            target_ids.append(target_id)

        active = self.manager.active()
        self.assertEqual(len(active), 3)

        generator = self.manager.generator(target_ids[0])
        generator.state = Model__Generator_State.STOPPED

        active = self.manager.active()
        self.assertEqual(len(active), 2)

    def test_empty_manager(self):
        self.assertEqual(len(self.manager.generators), 0)
        self.assertEqual(len(self.manager.active()), 0)
        self.assertEqual(self.manager.cleanup(), 0)
        self.assertFalse(self.manager.remove(Random_Guid()))

    def test_invalid_generator_type(self):
        with pytest.raises(ValueError, match="On Model__Generator_Target, invalid type for attribute 'target'. Expected '<class 'generator'>' but got '<class 'int'>'"):
            self.manager.add(123)  # Invalid type

        with pytest.raises(ValueError, match="On Model__Generator_Target, invalid type for attribute 'target'. Expected '<class 'generator'>' but got '<class 'str'>'"):
            self.manager.add("not a generator")  # Invalid type

    def test_capture(self):
        def sample_generator():
            yield 1
            yield 2
            yield 3

        values = []
        with self.manager.capture(sample_generator()) as gen:
            for value in gen:
                values.append(value)

        assert values                       == [1, 2, 3]
        assert len(self.manager.generators) == 1

        generator_target = list(self.manager.generators.values())[0]
        target_id        = generator_target.target_id

        assert generator_target.state  == Model__Generator_State.COMPLETED
        assert generator_target.target == gen

        assert is_guid(target_id)

        assert self.manager.target_id(gen) == target_id

    def test_capture_with_exception(self):
        def faulty_generator():
            yield 1
            raise ValueError("Intentional error")
            yield 2  # This won't be reached

        values = []
        with self.assertRaises(ValueError):
            with self.manager.capture(faulty_generator()) as gen:
                for value in gen:
                    values.append(value)

        assert values                                 == [1]
        assert len(self.manager.generators)           == 1
        assert self.manager.find_generator(gen).state == Model__Generator_State.COMPLETED

    def test_capture_with_early_exit(self):
        def long_generator():
            for i in range(10):
                yield i

        values = []
        with self.manager.capture(long_generator()) as gen:
            for value in gen:
                values.append(value)
                if value >= 3:                                          # Exit early after 4 iterations
                    break

        assert values                                 == [0, 1, 2, 3]
        assert len(self.manager.generators)           == 1
        assert self.manager.find_generator(gen).state == Model__Generator_State.COMPLETED

    def test_capture_with_concurrent_stop(self):
        stop_event = Event()
        values = []

        def slow_generator():
            i = 0
            while not stop_event.is_set():
                yield i
                i += 1
                sleep(0.0011)

        def stopper():
            sleep(0.003)  # Let the generator run for a bit
            stop_event.set()

        stop_thread = Thread(target=stopper)
        stop_thread.start()

        with self.manager.capture(slow_generator()) as gen:
            for value in gen:
                values.append(value)

        stop_thread.join()

        assert len(values)                           > 0
        assert len(values)                           < 10                               # Should not complete all iterations
        assert values                                == [0, 1, 2]
        assert len(self.manager.generators)          == 1
        assert self.manager.find_generator(gen).state == Model__Generator_State.COMPLETED

    def test_nested_capture(self):
        def outer_generator():
            yield 1
            yield 2

        def inner_generator():
            yield 'a'
            yield 'b'

        outer_values = []
        inner_values = []


        with self.manager.capture(outer_generator()) as outer_gen:
            for outer_value in outer_gen:
                outer_values.append(outer_value)
                with self.manager.capture(inner_generator()) as inner_gen:
                    for inner_value in inner_gen:
                        inner_values.append(inner_value)

        assert outer_values                                 == [1, 2]
        assert inner_values                                 == ['a', 'b', 'a', 'b']
        assert len(self.manager.generators)                 == 3
        assert self.manager.find_generator(outer_gen).state == Model__Generator_State.COMPLETED
        assert self.manager.find_generator(inner_gen).state == Model__Generator_State.COMPLETED


    def test_generator_completion(self):
        def sample_generator():
            yield 1
            yield 2

        gen = sample_generator()
        with Generator_Context_Manager(self.manager, gen):
            list(gen)  # Exhaust the generator

        generator = self.manager.find_generator(gen)
        assert generator.state == Model__Generator_State.COMPLETED

    def test__concurrent_add_and_stop(self):
        if not_in_github_action():
            pytest.skip("This test duration fluctuates quite a bit locally (from 100ms to 800ms)")
        stop_event = Event()
        results = {'adds': 0, 'stops': 0}

        def adder():
            while not stop_event.is_set():
                try:
                    generator = (x for x in [1, 2, 3])
                    self.manager.add(generator)
                    results['adds'] += 1
                except ValueError:
                    pass

        def stopper():
            while not stop_event.is_set():
                for target_id in list(self.manager.generators.keys()):
                    if self.manager.stop(target_id):
                        results['stops'] += 1
                #sleep(0.001)

        threads = [Thread(target=adder) for _ in range(3)] + [Thread(target=stopper) for _ in range(2)]

        for t in threads:
            t.start()

        stop_event.set()

        for t in threads:
            t.join()

        assert results['adds' ] > 0
        assert results['stops'] > 0

        assert len(self.manager.active())  == results['adds' ] - results['stops' ]
        assert len(self.manager.active()) != 0

    def test_capture_resource_cleanup(self):                            # Test  cleanup of resources when using capture
        resources_freed = False
        def generator_with_cleanup():
            nonlocal resources_freed
            try:
                yield 1
            finally:
                resources_freed = True

        with self.manager.capture(generator_with_cleanup()) as gen:
            list(gen)

        assert resources_freed is True

    def test_concurrent_state_transitions(self):                # Test concurrent state changes don't corrupt state
        def slow_generator():
            for i in range(10):
                yield i
                sleep(0.0001)

        gen = slow_generator()
        target_id = self.manager.add(gen)

        def state_changer():
            for _ in range(100):
                self.manager.stop(target_id)
                sleep(0.00001)

        threads = [Thread(target=state_changer) for _ in range(5)]
        [t.start() for t in threads]
        list(gen)                                                           # Exhaust generator
        [t.join() for t in threads]


        generator = self.manager.generator(target_id)                   # Verify final state is valid
        assert generator.state == Model__Generator_State.STOPPING

    def test_capture_reused_generator(self):
        """Test behavior when capturing same generator multiple times"""
        def reusable_generator():
            for i in range(3):
                yield i

        gen = reusable_generator()
        with self.manager.capture(gen):
            next(gen)

        # Attempting to capture partially consumed generator
        with pytest.raises(ValueError):
            with self.manager.capture(gen):
                pass

    def test_generator_state_consistency(self):
        """Test state transitions are consistent and atomic"""
        state_changes = []

        def state_tracking_generator():
            state_changes.append(('START', self.manager.generator(gen_id).state))
            yield 1
            state_changes.append(('YIELD', self.manager.generator(gen_id).state))
            return
            state_changes.append(('RETURN', self.manager.generator(gen_id).state))

        gen = state_tracking_generator()
        gen_id = self.manager.add(gen)

        # Consume generator
        list(gen)

        # Verify state changes were atomic and consistent
        assert state_changes == [('START', Model__Generator_State.RUNNING),
                                 ('YIELD', Model__Generator_State.RUNNING)]

        # Final state should be RUNNING since the generator was executed directly
        assert self.manager.generator(gen_id).state == Model__Generator_State.RUNNING

    def test_remove_with_running_generator(self):                                   # Test attempting to remove a generator in different states
        def sample_generator():
            yield 1
            yield 2

        # Test with RUNNING state
        gen = sample_generator()
        target_id = self.manager.add(gen)
        assert self.manager.generator(target_id).state == Model__Generator_State.RUNNING
        assert self.manager.remove(target_id) is False                  # Can't remove running generator
        assert self.manager.generator(target_id) is not None            # Generator should still exist

        # Test with STOPPING state
        self.manager.stop(target_id)
        assert self.manager.generator(target_id).state == Model__Generator_State.STOPPING
        assert self.manager.remove(target_id) is False               # Can't remove stopping generator
        assert self.manager.generator(target_id) is not None         # Generator should still exist

        # Test with COMPLETED state
        generator = self.manager.generator(target_id)
        generator.state = Model__Generator_State.COMPLETED
        assert self.manager.remove(target_id) is True                # Can remove completed generator
        assert self.manager.generator(target_id) is None             # Generator should be removed

        # Test with STOPPED state
        gen2 = sample_generator()
        target_id2 = self.manager.add(gen2)
        generator2 = self.manager.generator(target_id2)
        generator2.state = Model__Generator_State.STOPPED
        assert self.manager.remove(target_id2) is True               # Can remove stopped generator
        assert self.manager.generator(target_id2) is None            # Generator should be removed

    def test_should_stop_with_different_states(self):                # Test should_stop behavior with different generator states
        def sample_generator():
            yield 1

        # Test with non-existent generator
        non_existent_id = Random_Guid()
        with self.assertRaises(ValueError) as context:
            self.manager.should_stop(non_existent_id)
        assert str(context.exception) == f"In Generator_Manager.should_stop, Generator with ID {non_existent_id} does not exist."

        # Test with RUNNING state
        gen = sample_generator()
        target_id = self.manager.add(gen)
        generator = self.manager.generator(target_id)
        assert generator.state == Model__Generator_State.RUNNING
        assert self.manager.should_stop(target_id) is False          # Running generators should not stop

        # Test with STOPPING state
        generator.state = Model__Generator_State.STOPPING
        assert self.manager.should_stop(target_id) is True           # Stopping generators should stop

        # Test with STOPPED state
        generator.state = Model__Generator_State.STOPPED
        assert self.manager.should_stop(target_id) is True           # Stopped generators should stop

        # Test with COMPLETED state
        generator.state = Model__Generator_State.COMPLETED
        assert self.manager.should_stop(target_id) is True           # Completed generators should stop

        # Test state transition sequence
        gen2 = sample_generator()
        target_id2 = self.manager.add(gen2)

        assert self.manager.should_stop(target_id2) is False         # Initially running
        self.manager.stop(target_id2)                                # Request stop
        assert self.manager.should_stop(target_id2) is True          # Should stop after request

    def test_should_stop_concurrent_access(self):                   # Test should_stop behavior under concurrent access"""
        def slow_generator():
            for i in range(100):
                yield i
                sleep(0.0001)

        gen = slow_generator()
        target_id = self.manager.add(gen)
        stop_flag = Event()
        results = {'stop_requests': 0, 'stop_confirmed': 0}

        def checker():
            while not stop_flag.is_set():
                try:
                    if self.manager.should_stop(target_id):
                        results['stop_confirmed'] += 1
                except ValueError:
                    break  # Generator might be removed
                sleep(0.0001)

        def stopper():
            while not stop_flag.is_set():
                if self.manager.stop(target_id):
                    results['stop_requests'] += 1
                sleep(0.0001)

        threads = [Thread(target=checker), Thread(target=stopper)]
        [t.start() for t in threads]

        for value in gen:                # Consume generator
            if value >= 5:               # Stop after a few iterations
                break

        stop_flag.set()                  # Signal threads to stop
        [t.join() for t in threads]      # Wait for threads

        # Verify some stop requests were processed
        assert results['stop_requests'] > 0
        assert results['stop_confirmed'] > 0

        # Final state check
        generator = self.manager.generator(target_id)
        assert generator is not None
        assert generator.state in [Model__Generator_State.STOPPING, Model__Generator_State.COMPLETED]


    def test_simple_stream_control(self):   # Test simple stream control pattern

        def generate_events(wait_count, get_generator):
            generator = get_generator()
            while wait_count > 0:
                if generator.state != Model__Generator_State.RUNNING:
                    return  # Exit cleanly

                yield wait_count
                wait_count -= 1
                sleep(0.001)  # Simulate work

        def live_stream():

            def get_generator():
                nonlocal target_id
                generator = self.manager.generator(target_id)
                return generator


            gen       = generate_events(10, get_generator)
            target_id = self.manager.add(gen)

            return gen

        # Run the stream
        events           = []
        gen_live_stream  = live_stream()
        generator_target = self.manager.find_generator(gen_live_stream)

        # Simulate streaming
        for event in gen_live_stream:
            events.append(event)
            if event == 8:  # Stop after value 8
                generator_target.state = Model__Generator_State.STOPPING

        # Verify results
        assert events                        == [10, 9, 8]
        assert len(self.manager.generators) == 1
        assert generator_target.state       == Model__Generator_State.STOPPING

    def test_multiple_simple_streams(self):   # Test multiple concurrent simple streams
        manager = Generator_Manager()
        results = {}
        target_ids = {}

        def get_generator(stream_id):
            return manager.generator(target_ids[stream_id])

        def generate_events(stream_id, wait_count, get_generator):
            generator = get_generator(stream_id)
            while wait_count > 0:
                if generator.state != Model__Generator_State.RUNNING:
                    return

                yield f"{stream_id}:{wait_count}"
                wait_count -= 1
                sleep(0.001)

        def live_stream(stream_id):
            gen = generate_events(stream_id, 10, get_generator)
            target_ids[stream_id] = manager.add(gen)
            results[stream_id] = []

            for event in gen:
                results[stream_id].append(event)
                if len(results[stream_id]) >= 3:
                    generator = manager.generator(target_ids[stream_id])
                    generator.state = Model__Generator_State.STOPPING

        # Start multiple streams
        threads = []
        for i in range(3):
            stream_id = f"stream_{i}"
            thread = Thread(target=live_stream, args=(stream_id,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Verify results
        for i in range(3):
            stream_id = f"stream_{i}"
            assert len(results[stream_id]) == 3
            assert results[stream_id] == [ f"{stream_id}:10", f"{stream_id}:9", f"{stream_id}:8"]

            generator = manager.generator(target_ids[stream_id])
            assert generator.state == Model__Generator_State.STOPPING

    def test_error_handling_simple_stream(self): # Test error handling in simple stream pattern
        manager = Generator_Manager()
        events = []
        target_id = None

        def get_generator():
            return manager.generator(target_id)

        def generate_events(wait_count, get_generator):
            generator = get_generator()
            while wait_count > 0:
                if generator.state != Model__Generator_State.RUNNING:
                    return

                if wait_count == 8:
                    raise ValueError("Test error")

                yield wait_count
                wait_count -= 1

        def live_stream():
            nonlocal target_id
            gen = generate_events(10, get_generator)
            target_id = manager.add(gen)

            try:
                for event in gen:
                    events.append(event)
            except ValueError as e:
                events.append(f"Error: {str(e)}")
                generator = manager.generator(target_id)
                generator.state = Model__Generator_State.STOPPING
                raise

        # Run the stream
        with pytest.raises(ValueError):
            live_stream()

        # Verify results
        assert events == [10, 9, "Error: Test error"]
        assert len(manager.generators) == 1
        generator = manager.generator(target_id)
        assert generator.state == Model__Generator_State.STOPPING

    def test_cleanup_simple_stream(self): #        Test cleanup of completed streams
        manager = Generator_Manager()
        target_id = None

        def get_generator():
            return manager.generator(target_id)

        def generate_events(wait_count, get_generator):
            generator = get_generator()
            try:
                while wait_count > 0:
                    if generator.state != Model__Generator_State.RUNNING:
                        return

                    yield wait_count
                    wait_count -= 1
            finally:
                # Cleanup when generator exits
                generator = get_generator()
                if generator:
                    generator.state = Model__Generator_State.COMPLETED

        def live_stream():
            nonlocal target_id
            gen = generate_events(3, get_generator)
            target_id = manager.add(gen)

            for _ in gen:
                pass  # Consume all events

        # Run the stream
        live_stream()

        # Verify cleanup
        assert len(manager.generators) == 1
        generator = manager.generator(target_id)
        assert generator.state == Model__Generator_State.COMPLETED

        # Cleanup completed generators
        cleaned = manager.cleanup()
        assert cleaned == 1
        assert len(manager.generators) == 0