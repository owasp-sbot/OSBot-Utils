import traceback
import inspect
from typing import Any, Dict, List, Optional, Tuple


class Type_Safe__Exception_Detail:
    """Centralized detailed exception formatting for Type_Safe validation errors."""

    # Patterns that indicate type_safe internal code
    type_safe_patterns : List[str] = ['type_safe', 'Type_Safe', 'Safe_Str']

    # Patterns that indicate a test entry point
    test_patterns      : List[str] = ['setUpClass', 'setUp', 'tearDown', 'tearDownClass', 'test_']

    # Patterns for test framework internals to exclude
    framework_patterns : List[str] = ['site-packages/_pytest'  ,
                                      'site-packages/pluggy'   ,
                                      'site-packages/unittest' ,
                                      '_jb_pytest_runner'      ,
                                      'lib/python3'            ]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Public Methods - Error Creators
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def attribute_type_error(self, target        : Any            ,
                                   name          : str            ,
                                   expected_type : type           ,
                                   actual_type   : type           ,
                                   value         : Any   = None   ) -> ValueError:
        """Create detailed error for attribute type validation failures."""

        target_class                             = target.__class__.__name__
        expected_short, expected_full, expected_file, expected_line = self.get_type_info(expected_type)
        actual_short  , actual_full  , actual_file  , actual_line   = self.get_type_info(actual_type)
        mro_info                                 = self.get_mro_info(actual_type)
        is_subclass_issue                        = self.check_subclass_issue(actual_type, expected_type)
        value_preview                            = self.format_value_preview(value)
        suggestion                               = self.format_suggestion(is_subclass_issue , mro_info       ,
                                                                          actual_short      , expected_short ,
                                                                          actual_file       , actual_line    ,
                                                                          expected_file     , expected_line  )
        call_tree                                = self.build_filtered_call_tree()

        error_message = (
            f"\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
            f"Type Validation Error (Attribute)\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
            f"\n"
            f"Target class : {target_class}\n"
            f"Attribute    : '{name}'\n"
            f"\n"
            f"Expected type:\n"
            f"    Short : {expected_short}\n"
            f"    Full  : {expected_full}\n"
            f"\n"
            f"Actual type:\n"
            f"    Short : {actual_short}\n"
            f"    Full  : {actual_full}\n"
            f"\n"
            f"Inheritance chain of actual type:\n"
            f"{self.format_list(mro_info)}\n"
            f"\n"
            f"{value_preview}"
            f"{suggestion}"
            f"Call tree (from test to error):\n"
            f"{call_tree}\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
        )
        return ValueError(error_message)

    def parameter_type_error(self, param_name     : str  ,
                                   expected_type  : type ,
                                   actual_type    : type ,
                                   value          : Any  = None) -> ValueError:
        """Create detailed error for parameter type validation failures."""

        expected_short, expected_full, expected_file, expected_line = self.get_type_info(expected_type)
        actual_short  , actual_full  , actual_file  , actual_line   = self.get_type_info(actual_type)
        mro_info                                 = self.get_mro_info(actual_type)
        is_subclass_issue                        = self.check_subclass_issue(actual_type, expected_type)
        value_preview                            = self.format_value_preview(value)
        suggestion                               = self.format_suggestion(is_subclass_issue , mro_info       ,
                                                                          actual_short      , expected_short ,
                                                                          actual_file       , actual_line    ,
                                                                          expected_file     , expected_line  )
        call_tree                                = self.build_filtered_call_tree()

        error_message = (
            f"\n"
            f"\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
            f"Type Validation Error (Parameter)\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
            f"\n"
            f"Parameter    : '{param_name}'\n"
            f"\n"
            f"Expected type:\n"
            f"    Short : {expected_short}\n"
            f"    Full  : {expected_full}\n"
            f"\n"
            f"Actual type:\n"
            f"    Short : {actual_short}\n"
            f"    Full  : {actual_full}\n"
            f"\n"
            f"Inheritance chain of actual type:\n"
            f"{self.format_list(mro_info)}\n"
            f"\n"
            f"{value_preview}"
            f"{suggestion}"
            f"Call tree (from test to error):\n"
            f"{call_tree}\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
        )
        return ValueError(error_message)

    def regex_validation_error(self, cls           : type ,
                                     value         : str  ,
                                     pattern       : str  ,
                                     mode          : str  ) -> ValueError:
        """Create detailed error for regex/string validation failures."""

        class_name              = cls.__name__
        class_file, class_line  = self.get_class_location(cls)
        value_preview           = self.format_value_preview(value)
        call_tree               = self.build_filtered_call_tree()

        # Format class location as clickable link
        class_location = ""
        if class_file:
            class_location = (
                f"\nClass definition:\n"
                f'  File "{class_file}", line {class_line}, in {class_name}\n'
            )

        # Build mode-specific message
        if mode == 'match':
            mode_message = (
                f"Value does not match required pattern.\n"
                f"    Pattern : {pattern}\n"
                f"\n"
                f"{value_preview}"
            )
        else:  # sanitize mode
            mode_message = (
                f"Value contains forbidden characters.\n"
                f"    Pattern : {pattern}\n"
                f"\n"
                f"{value_preview}"
            )

        error_message = (
            f"\n"
            f"\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
            f"String Validation Error\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
            f"\n"
            f"Class        : {class_name}\n"
            f"Regex mode   : {mode}\n"
            f"{class_location}"
            f"\n"
            f"{mode_message}"
            f"Call tree (from test to error):\n"
            f"{call_tree}\n"
            f"═══════════════════════════════════════════════════════════════════════════════\n"
        )

        return ValueError(error_message)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Helper Methods - Type Info
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def get_type_info(self, t: Any) -> Tuple[str, str, Optional[str], Optional[int]]:
        """Extract short name, full path, file path, and line number for a type."""
        if t is None:
            return "None", "None", None, None
        if isinstance(t, str):
            return t, t, None, None

        short_name = getattr(t, '__name__', str(t))
        module     = getattr(t, '__module__', '')
        full_path  = f"{module}.{short_name}" if module else short_name

        file_path, line_no = self.get_class_location(t)

        return short_name, full_path, file_path, line_no

    def get_class_location(self, target: Any) -> Tuple[Optional[str], Optional[int]]:
        """Get file path and line number for a class/function, unwrapping decorators."""
        try:
            unwrapped = inspect.unwrap(target) if callable(target) else target
            file_path = inspect.getfile(unwrapped)
            line_no   = inspect.getsourcelines(unwrapped)[1]
            return file_path, line_no
        except (TypeError, OSError):
            return None, None

    def get_mro_info(self, actual_type: type) -> List[str]:
        """Get Method Resolution Order info, excluding self and object."""
        mro_info = []
        if hasattr(actual_type, '__mro__'):
            for cls in actual_type.__mro__[1:-1]:
                cls_name = getattr(cls, '__name__', str(cls))
                mro_info.append(cls_name)
        return mro_info

    def check_subclass_issue(self, actual_type: type, expected_type: type) -> bool:
        """Check if this looks like a missing inheritance issue."""
        if hasattr(actual_type, '__mro__') and hasattr(expected_type, '__name__'):
            expected_name = expected_type.__name__
            return expected_name not in [c.__name__ for c in actual_type.__mro__]
        return False

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Helper Methods - Formatting
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def format_list(self, items: List[str], indent: str = '    ') -> str:
        """Format a list with bullet points."""
        if not items:
            return f"{indent}(none)"
        return '\n'.join(f"{indent}- {item}" for item in items)

    def format_value_preview(self, value: Any) -> str:
        """Format a truncated value preview."""
        if value is None:
            return ""
        value_repr = repr(value)
        if len(value_repr) > 100:
            value_repr = value_repr[:97] + '...'
        return f"Value preview: {value_repr}\n\n"

    def format_suggestion(self, is_subclass_issue : bool          ,
                                mro_info          : List[str]     ,
                                actual_short      : str           ,
                                expected_short    : str           ,
                                actual_file       : Optional[str] ,
                                actual_line       : Optional[int] ,
                                expected_file     : Optional[str] ,
                                expected_line     : Optional[int] ) -> str:
        """Format suggestion with clickable class links."""
        if not (is_subclass_issue and mro_info):
            return ""

        lines = [
            "Suggestion:"                                                                      ,
            f"    The actual type '{actual_short}' does not inherit from '{expected_short}'." ,
            f"    Consider adding '{expected_short}' as a base class."                        ,
            ""                                                                                ,
            "    Related classes:"                                                            ,
        ]

        if actual_file:
            lineno = actual_line or 1
            lines.append(f'      File "{actual_file}", line {lineno}, in {actual_short}')

        if expected_file:
            lineno = expected_line or 1
            lines.append(f'      File "{expected_file}", line {lineno}, in {expected_short}')

        return '\n'.join(lines) + "\n\n"

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Helper Methods - Call Tree
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def build_filtered_call_tree(self, max_frames: int = 10) -> str:
        """Build filtered stack trace from test method to error, excluding type_safe internals."""

        stack            = traceback.extract_stack()
        test_entry_index = self.find_test_entry_index(stack)
        type_safe_start  = self.find_type_safe_start_index(stack)

        if test_entry_index is not None:
            start_index = test_entry_index
        else:
            start_index = max(0, type_safe_start - max_frames)

        end_index       = min(type_safe_start, len(stack))
        filtered_frames = self.filter_frames(stack, start_index, end_index)

        if len(filtered_frames) > max_frames:
            filtered_frames = filtered_frames[-max_frames:]

        if not filtered_frames:
            return "    (no relevant frames captured)"

        return self.format_frames(filtered_frames)

    def find_test_entry_index(self, stack: List) -> Optional[int]:
        """Find the index of the test entry point in the stack."""
        for i, frame in enumerate(stack):
            func_name = frame.name
            is_test   = any(func_name.startswith(p) or func_name == p for p in self.test_patterns)
            in_framework = any(fp in frame.filename for fp in self.framework_patterns)
            if is_test and not in_framework:
                return i
        return None

    def find_type_safe_start_index(self, stack: List) -> int:
        """Find where type_safe code starts (from the end of stack)."""
        for i in range(len(stack) - 1, -1, -1):
            frame        = stack[i]
            is_type_safe = any(p in frame.filename or p in frame.name for p in self.type_safe_patterns)
            if not is_type_safe:
                return i + 1
        return len(stack)

    def filter_frames(self, stack: List, start_index: int, end_index: int) -> List:
        """Filter frames, removing framework internals and internal methods."""
        filtered = []
        skip_funcs = ('attribute_type_error'       , 'parameter_type_error'    ,
                      'regex_validation_error'     , 'build_filtered_call_tree',
                      'create_detailed_type_error' , '_build_filtered_call_tree',
                      'validate_and_sanitize'      )

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
                if len(code_line) > 90:
                    code_line = code_line[:87] + '...'
                lines.append(f'    {code_line}')
        return '\n'.join(lines)


type_safe_exception_detail = Type_Safe__Exception_Detail()