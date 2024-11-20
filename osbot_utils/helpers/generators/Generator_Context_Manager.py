from osbot_utils.helpers.generators.Model__Generator_State import Model__Generator_State


class Generator_Context_Manager:
    def __init__(self, manager, generator_func):
        self.manager = manager
        self.generator_func = generator_func
        self.target_id = None

    def __enter__(self):
        self.target_id = self.manager.add(self.generator_func)                  # Add the generator to the manager
        return self.manager.generator(self.target_id).target                    # Return the generator's reference

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self.manager.lock:
            generator = self.manager.generator(self.target_id)
            if generator and generator.state == Model__Generator_State.RUNNING:
                generator.state = Model__Generator_State.COMPLETED


        #self.manager.cleanup()
