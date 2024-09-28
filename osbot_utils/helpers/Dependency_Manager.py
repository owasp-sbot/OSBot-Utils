import inspect


class Dependency_Manager:
    def __init__(self):
        self._dependencies = {}

    def add_dependency(self, name: str, instance):                                          # Register a dependency by name.
        self._dependencies[name] = instance

    def get_dependency(self, name: str):                                                    # Retrieve a dependency by name.
        return self._dependencies.get(name, None)

    def resolve_dependencies(self, func, *args, **kwargs):                                  # Automatically inject dependencies based on function's parameters.
        sig             = inspect.signature(func)                                           # Get the function's signature and parameters
        bound_arguments = sig.bind_partial(*args, **kwargs)


        for param_name, param in sig.parameters.items():                                    # Check parameters to see if we need to inject a dependency
            if param_name not in bound_arguments.arguments:
                if param_name in self._dependencies:                                        # Inject dependency if available
                    bound_arguments.arguments[param_name] = self._dependencies[param_name]

        return bound_arguments.args, bound_arguments.kwargs

dependency_manager = Dependency_Manager()