import inspect
import traceback
from typing import List, Optional


class Dependency_Manager:

    # Patterns for filtering call tree
    type_safe_patterns  : List[str] = ['type_safe', 'Type_Safe', 'Dependency_Manager']
    test_patterns       : List[str] = ['setUpClass', 'setUp', 'tearDown', 'tearDownClass', 'test_']
    framework_patterns  : List[str] = ['site-packages/_pytest'  ,
                                       'site-packages/pluggy'   ,
                                       'site-packages/unittest' ,
                                       '_jb_pytest_runner'      ,
                                       'lib/python3'            ]

    def __init__(self):
        self._dependencies = {}

    def add_dependency(self, name: str, instance):                                          # Register a dependency by name.
        self._dependencies[name] = instance

    def get_dependency(self, name: str):                                                    # Retrieve a dependency by name.
        return self._dependencies.get(name, None)

    def resolve_dependencies(self, func, *args, **kwargs):                                  # Automatically inject dependencies based on function's parameters.
        sig             = inspect.signature(func)                                           # Get the function's signature and parameters
        try:
            bound_arguments = sig.bind_partial(*args, **kwargs)
        except TypeError as e:
            raise self.create_detailed_error__for_sig_bind_exception(func, sig, args, kwargs, e) from None

        for param_name, param in sig.parameters.items():                                    # Check parameters to see if we need to inject a dependency
            if param_name not in bound_arguments.arguments:
                if param_name in self._dependencies:                                        # Inject dependency if available
                    bound_arguments.arguments[param_name] = self._dependencies[param_name]

        return bound_arguments.args, bound_arguments.kwargs

    def create_detailed_error__for_sig_bind_exception(self          ,                   # Create detailed error for debugging
                                                      func          ,
                                                      sig           ,
                                                      args   : tuple,
                                                      kwargs : dict ,
                                                      original_error: TypeError
                                                 ) -> TypeError:
        func_name   = getattr(func, '__name__'  , str(func))
        func_module = getattr(func, '__module__', '<unknown>')

        # Get function file location
        func_file, func_line = self.get_function_location(func)

        # Build expected parameters info
        expected_params = []
        for name, param in sig.parameters.items():
            param_info = name
            if param.annotation != inspect.Parameter.empty:
                ann_name    = getattr(param.annotation, '__name__', str(param.annotation))
                param_info += f": {ann_name}"
            if param.default != inspect.Parameter.empty:
                param_info += f" = {param.default!r}"
            expected_params.append(param_info)

        # Build received arguments info (truncate long reprs)
        received_args   = []
        for i, arg in enumerate(args):
            arg_repr = repr(arg)
            if len(arg_repr) > 80:
                arg_repr = arg_repr[:77] + '...'
            received_args.append(f"args[{i}]: {type(arg).__name__} = {arg_repr}")

        received_kwargs = []
        for k, v in kwargs.items():
            val_repr = repr(v)
            if len(val_repr) > 80:
                val_repr = val_repr[:77] + '...'
            received_kwargs.append(f"{k}: {type(v).__name__} = {val_repr}")

        # Build available dependencies info
        available_deps = [f"{k:15}: {type(v).__name__}" for k, v in self._dependencies.items()]

        # Build call tree
        call_tree = self.build_filtered_call_tree()

        # Format function location as clickable link
        func_location = ""
        if func_file:
            func_location = (
                f"\nFunction definition:\n"
                f'  File "{func_file}", line {func_line}, in {func_name}\n'
            )

        error_message = (
            f"\n"
            f"\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
            f"Dependency Resolution Error: {original_error}\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
            f"\n"
            f"Function: {func_module}.{func_name}\n"
            f"{func_location}"
            f"\n"
            f"Expected parameters ({len(expected_params)}):\n"
            f"{self.format_list(expected_params)}\n"
            f"\n"
            f"Received positional args ({len(args)}):\n"
            f"{self.format_list(received_args)}\n"
            f"\n"
            f"Received keyword args ({len(kwargs)}):\n"
            f"{self.format_list(received_kwargs)}\n"
            f"\n"
            f"Available dependencies ({len(self._dependencies)}):\n"
            f"{self.format_list(available_deps)}\n"
            f"\n"
            f"Call tree (from test to error):\n"
            f"{call_tree}\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
        )

        return TypeError(error_message)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Helper Methods
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def format_list(self, items: List[str], indent: str = '    ') -> str:
        """Format a list with bullet points."""
        if not items:
            return f"{indent}(none)"
        return '\n'.join(f"{indent}- {item}" for item in items)

    def get_function_location(self, func) -> tuple: # Get file path and line number for a function, unwrapping decorators."""
        try:
            # Unwrap decorated functions to get the original function
            unwrapped = inspect.unwrap(func)
            file_path = inspect.getfile(unwrapped)
            _, line_no = inspect.getsourcelines(unwrapped)
            return file_path, line_no
        except (TypeError, OSError):
            # Fallback: try without unwrapping
            try:
                file_path = inspect.getfile(func)
                _, line_no = inspect.getsourcelines(func)
                return file_path, line_no
            except (TypeError, OSError):
                return None, None

    def build_filtered_call_tree(self, max_frames: int = 10) -> str:
        """Build filtered stack trace from test method to error, excluding internals."""

        stack            = traceback.extract_stack()
        test_entry_index = self.find_test_entry_index(stack)
        internal_start   = self.find_internal_start_index(stack)

        if test_entry_index is not None:
            start_index = test_entry_index
        else:
            start_index = max(0, internal_start - max_frames)

        end_index       = min(internal_start, len(stack))
        filtered_frames = self.filter_frames(stack, start_index, end_index)

        if len(filtered_frames) > max_frames:
            filtered_frames = filtered_frames[-max_frames:]

        if not filtered_frames:
            return "    (no relevant frames captured)"

        return self.format_frames(filtered_frames)

    def find_test_entry_index(self, stack: List) -> Optional[int]:
        """Find the index of the test entry point in the stack."""
        for i, frame in enumerate(stack):
            func_name    = frame.name
            is_test      = any(func_name.startswith(p) or func_name == p for p in self.test_patterns)
            in_framework = any(fp in frame.filename for fp in self.framework_patterns)
            if is_test and not in_framework:
                return i
        return None

    def find_internal_start_index(self, stack: List) -> int:
        """Find where internal code starts (from the end of stack)."""
        for i in range(len(stack) - 1, -1, -1):
            frame       = stack[i]
            is_internal = any(p in frame.filename or p in frame.name for p in self.type_safe_patterns)
            if not is_internal:
                return i + 1
        return len(stack)

    def filter_frames(self, stack: List, start_index: int, end_index: int) -> List:
        """Filter frames, removing framework internals and internal methods."""
        filtered   = []
        skip_funcs = ('create_detailed_error__for_sig_bind_exception',
                      'build_filtered_call_tree'                     ,
                      'resolve_dependencies'                         )

        for i in range(start_index, end_index):
            frame = stack[i]
            if any(fp in frame.filename for fp in self.framework_patterns):
                continue
            if frame.name in skip_funcs:
                continue
            filtered.append(frame)
        return filtered

    def format_frames(self, frames: List) -> str:
        """Format frames using Python's standard traceback format for PyCharm clickability."""
        lines = []
        for frame in frames:
            lines.append(f'  File "{frame.filename}", line {frame.lineno}, in {frame.name}')
            if frame.line:
                code_line = frame.line.strip()
                # if len(code_line) > 90:
                #     code_line = code_line[:87] + '...'

                lines.append(f'    {code_line}')
        return '\n'.join(lines)


dependency_manager = Dependency_Manager()