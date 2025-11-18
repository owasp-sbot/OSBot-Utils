import threading
from _thread                                                            import RLock                              # Reentrant lock for thread-safe access
from types                                                              import GeneratorType
from typing                                                             import Dict                               # Typing imports for type hints
from typing                                                             import Union
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe                          # Type_Safe base class for type-safe attributes
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid   import Random_Guid                        # Helper for generating unique IDs
from osbot_utils.helpers.generators.Generator_Context_Manager           import Generator_Context_Manager
from osbot_utils.helpers.generators.Model__Generator_State              import Model__Generator_State
from osbot_utils.helpers.generators.Model__Generator_Target             import Model__Generator_Target
from osbot_utils.utils.Lists                                            import list_group_by


class Generator_Manager(Type_Safe):                                                                        # Class for managing multiple generator targets
    generators: Dict[Random_Guid, Model__Generator_Target]                                                 # Dictionary mapping target IDs to generator targets
    lock      : RLock                               = None                                                 # Reentrant lock for thread-safe access to shared data

    def __init__(self, **kwargs):                                                                          # Constructor method
        super().__init__(**kwargs)
        self.lock = threading.RLock()                                                                      # return an object of type _thread.RLock


    def active(self) -> Dict[Random_Guid, Model__Generator_Target]:                                        # Method to get all active (running) generators
        with self.lock:                                                                                    # Acquire the lock for thread-safe access
            return {k: v for k, v in self.generators.items() if v.state == Model__Generator_State.RUNNING} # Return a dictionary of running generators

    def add(self, target: GeneratorType) -> Random_Guid:                                                   # Method to add a new generator to the manager
        with self.lock:                                                                                    # Acquire the lock for thread-safe access
            existing_target_id = self.target_id(target)                                                     # Check if the target already exists
            if existing_target_id:                                                                         # If the target already exists
                raise ValueError(f"In Generator_Manager.add_generator, "                                   # Raise an error with the ID of the existing target
                                 f"target already exists with ID: {existing_target_id}")

            generator = Model__Generator_Target(target=target, state=Model__Generator_State.RUNNING)       # Create a new Generator_Target with RUNNING state
            self.generators[generator.target_id] = generator                                               # Add the generator to the dictionary
            return generator.target_id                                                                     # Return the unique ID of the added generator

    def capture(self, generator_func: GeneratorType):                                                      # Use this method to manage a generator's lifecycle via a context manager.
        return Generator_Context_Manager(self, generator_func)

    def cleanup(self) -> int:                                                                              # Method to remove all completed or stopped generators
        with self.lock:                                                                                    # Acquire the lock for thread-safe access
            cleaned_count = 0                                                                              # Counter for the number of generators cleaned up
            for target_id in list(self.generators.keys()):                                                 # Iterate over the keys of the dictionary
                generator = self.generator(target_id)                                                      # Get the generator by its ID
                if generator and generator.state in [Model__Generator_State.STOPPED,
                                                     Model__Generator_State.COMPLETED]:                    # Check if the generator is stopped or completed
                    self.generators.pop(target_id, None)                                                   # Remove the generator from the dictionary
                    cleaned_count += 1                                                                     # Increment the cleaned count
            return cleaned_count                                                                           # Return the total number of cleaned generators

    def find_generator(self, target: GeneratorType) -> Model__Generator_Target:
        with self.lock:
            for generator in list(self.generators.values()):
                if generator.target == target:
                    return generator

    def generator(self, target_id: Random_Guid) -> Model__Generator_Target:                                # Method to get a generator by its ID
        with self.lock:                                                                                    # Acquire the lock for thread-safe access
            return self.generators.get(target_id)                                                          # Return the generator or None if it doesn't exist

    def remove(self, target_id: Random_Guid) -> bool:                                                      # Method to remove a generator if it is stopped or completed
        with self.lock:                                                                                    # Acquire the lock for thread-safe access
            generator = self.generator(target_id)                                                          # Get the generator by its ID
            if not generator:                                                                              # If the generator doesn't exist
                return False                                                                               # Silently return False
            if generator.state in [Model__Generator_State.STOPPED, Model__Generator_State.COMPLETED]:      # Check if the generator is in a removable state
                del self.generators[target_id]                                                             # Remove the generator from the dictionary
                return True                                                                                # Return True to indicate successful removal
            return False                                                                                   # Return False if the generator was not removable

    def should_stop(self, target_id: Random_Guid) -> bool:                                                 # Method to check if a generator should stop
        with self.lock:                                                                                    # Acquire the lock for thread-safe access
            generator = self.generator(target_id)                                                          # Get the generator by its ID
            if not generator:                                                                              # If the generator doesn't exist
                raise ValueError(f"In Generator_Manager.should_stop, "                                     # Raise an error indicating missing generator
                                 f"Generator with ID {target_id} does not exist.")
            return generator.state != Model__Generator_State.RUNNING                                       # Return True if the generator is not running

    def stop(self, target_id: Random_Guid) -> bool:                                                        # Method to stop a running generator
        with self.lock:                                                                                    # Acquire the lock for thread-safe access
            generator = self.generator(target_id)                                                          # Get the generator by its ID
            if generator and generator.state == Model__Generator_State.RUNNING:                            # If the generator is running
                generator.state = Model__Generator_State.STOPPING                                          # Set its state to STOPPING
                return True                                                                                # Return True to indicate the generator is stopping
            return False                                                                                   # Return False if the generator could not be stopped

    def stop_all(self) -> int:                                                                             # Method to stop all running generators
        with self.lock:                                                                                    # Acquire the lock for thread-safe access
            stopped_count = 0                                                                              # Counter for the number of generators stopped
            for target_id in list(self.generators.keys()):                                                 # Iterate over the keys of the dictionary
                if self.stop(target_id):                                                                   # Attempt to stop each generator
                    stopped_count += 1                                                                     # Increment the stopped count if successful
            return stopped_count                                                                           # Return the total number of stopped generators

    def status(self):
        items = []
        for _, generator in self.generators.items():
            item = dict(target_method_name = generator.target.__name__,
                        target_state       = generator.state.value,
                        target_id          = generator.target_id )
            items.append(item)
        items__by_state = list_group_by(items, 'target_state')
        result = {}
        for state, items in items__by_state.items():
            result[state] = len(items)
        result['data'] = items__by_state
        return result


    def target_id(self, target: GeneratorType) -> Union[Random_Guid, None]:                                # Method to get the ID of a specific generator
        with self.lock:                                                                                    # Acquire the lock for thread-safe access
            for generator in list(self.generators.values()):                                               # Iterate over the generator targets
                if generator.target == target:                                                             # Check if the target matches
                    return generator.target_id                                                             # Return the matching target's ID
