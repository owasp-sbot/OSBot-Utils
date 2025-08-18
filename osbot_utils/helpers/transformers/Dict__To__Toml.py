from typing                                                           import Dict, Any, List, Set, Tuple, Union
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe        import type_safe


class Dict__To__Toml(Type_Safe):

    @type_safe
    def convert(self, data: Dict[str, Any]                                          # Dictionary to convert to TOML
                ) -> str:                                                           # Returns TOML formatted string
        toml_str = ""

        # First, process top-level simple values
        toml_str += self._process_simple_values(data, indent_level=0)

        # Process top-level arrays of simple types
        toml_str += self._process_simple_arrays(data, indent_level=0)

        # Process top-level dictionaries as sections
        toml_str += self._process_sections(data, parent_key="")

        # Process arrays of tables
        toml_str += self._process_array_of_tables(data, parent_key="")

        return toml_str

    @type_safe
    def _format_string_value(self, value: str                                      # String to format
                            ) -> str:                                              # Returns formatted TOML string
        """Format a string value for TOML output"""
        # For TOML basic strings, we need to handle:
        # 1. If string contains single quotes, use double quotes
        # 2. If string contains double quotes but no single quotes, use single quotes
        # 3. If string contains both, use triple quotes (multi-line literal)

        has_single = "'" in value
        has_double = '"' in value
        has_newline = '\n' in value or '\r' in value

        # Use triple quotes for complex strings (multilineelif has_single: or with both quote types)
        if has_newline or (has_single and has_double):
            # Use multi-line literal string (triple single quotes)
            # This preserves the exact content without escaping
            return f"'''\n{value}'''"
        elif has_single:
            # Use double quotes and escape any double quotes
            escaped = value.replace('"', '\\"')
            return f'"{escaped}"'
        else:
            # Use single quotes (default) - no escaping needed
            return f"'{value}'"

    @type_safe
    def _process_simple_values(self, data        : Dict[str, Any]        ,          # Data to process
                                     indent_level : int           = 0                # Current indentation level
                               ) -> str:                                            # Returns TOML for simple values
        toml_str = ""
        indent   = "    " * indent_level

        for key, value in data.items():
            if not isinstance(value, (dict, list, tuple, set)):
                if isinstance(value, str):
                    toml_str += f"{indent}{key} = {self._format_string_value(value)}\n"
                elif isinstance(value, bool):
                    toml_str += f"{indent}{key} = {str(value).lower()}\n"
                elif value is not None:
                    toml_str += f"{indent}{key} = {value}\n"

        return toml_str

    @type_safe
    def _process_simple_arrays(self, data        : Dict[str, Any]        ,          # Data to process
                                    indent_level : int           = 0                # Current indentation level
                              ) -> str:                                             # Returns TOML for simple arrays
        toml_str = ""
        indent   = "    " * indent_level

        for key, value in data.items():
            if isinstance(value, (list, tuple, set)):
                if not value:                                                       # Empty collection
                    toml_str += f"{indent}{key} = []\n"
                elif not any(isinstance(item, dict) for item in value):            # No dict items
                    toml_str += f"{indent}{key} = [\n"
                    for item in value:
                        if isinstance(item, str):
                            toml_str += f"{indent}    {self._format_string_value(item)},\n"
                        elif isinstance(item, bool):
                            toml_str += f"{indent}    {str(item).lower()},\n"
                        elif item is not None:
                            toml_str += f"{indent}    {item},\n"
                    toml_str += f"{indent}]\n"

        return toml_str

    @type_safe
    def _process_sections(self, data       : Dict[str, Any]       ,                 # Data to process
                               parent_key : str            = ""                    # Parent section key
                         ) -> str:                                                  # Returns TOML sections
        toml_str = ""

        for key, value in data.items():
            if isinstance(value, dict):
                section_key = f"{parent_key}.{key}" if parent_key else key
                toml_str   += f"[{section_key}]\n"
                toml_str   += self._process_section_content(value, section_key)

        return toml_str

    @type_safe
    def _process_section_content(self, section_data : Dict[str, Any]      ,         # Section data to process
                                       section_key  : str                           # Current section key
                                ) -> str:                                           # Returns section content
        toml_str = ""
        indent   = "    "

        # Process simple values in section
        for key, value in section_data.items():
            if isinstance(value, str):
                toml_str += f"{indent}{key} = {self._format_string_value(value)}\n"
            elif isinstance(value, bool):
                toml_str += f"{indent}{key} = {str(value).lower()}\n"
            elif isinstance(value, (int, float)) and value is not None:
                toml_str += f"{indent}{key} = {value}\n"
            elif isinstance(value, (list, tuple, set)) and not value:
                toml_str += f"{indent}{key} = []\n"
            elif isinstance(value, (list, tuple, set)):
                if not any(isinstance(item, dict) for item in value):
                    toml_str += f"{indent}{key} = [\n"
                    for item in value:
                        if isinstance(item, str):
                            toml_str += f"{indent}{indent}{self._format_string_value(item)},\n"
                        elif isinstance(item, bool):
                            toml_str += f"{indent}{indent}{str(item).lower()},\n"
                        elif item is not None:
                            toml_str += f"{indent}{indent}{item},\n"
                    toml_str += f"{indent}]\n"

        # Process arrays of tables within sections (NEW)
        for key, value in section_data.items():
            if isinstance(value, (list, tuple, set)):
                if value and all(isinstance(item, dict) for item in value):
                    for item in value:
                        toml_str += f"[[{section_key}.{key}]]\n"
                        for item_key, item_value in item.items():
                            if isinstance(item_value, str):
                                toml_str += f"{indent}{item_key} = {self._format_string_value(item_value)}\n"
                            elif isinstance(item_value, bool):
                                toml_str += f"{indent}{item_key} = {str(item_value).lower()}\n"
                            elif isinstance(item_value, (int, float)) and item_value is not None:
                                toml_str += f"{indent}{item_key} = {item_value}\n"

        # Process nested dictionaries
        for key, value in section_data.items():
            if isinstance(value, dict):
                nested_key = f"{section_key}.{key}"
                toml_str  += f"[{nested_key}]\n"
                toml_str  += self._process_section_content(value, nested_key)

        return toml_str

    @type_safe
    def _process_array_of_tables(self, data       : Dict[str, Any]       ,          # Data to process
                                       parent_key : str            = ""             # Parent section key
                                ) -> str:                                           # Returns array of tables
        toml_str = ""

        for key, value in data.items():
            if isinstance(value, (list, tuple, set)):
                if value and all(isinstance(item, dict) for item in value):
                    for item in value:
                        section_key = f"{parent_key}.{key}" if parent_key else key
                        toml_str   += f"[[{section_key}]]\n"
                        toml_str   += self._process_table_item(item, section_key)

        return toml_str

    @type_safe
    def _process_table_item(self, item        : Dict[str, Any]        ,             # Table item to process
                                  section_key : str                                 # Current section key
                           ) -> str:                                               # Returns formatted table item
        toml_str = ""
        indent   = "    "

        # Process simple values in table item
        for key, value in item.items():
            if isinstance(value, str):
                toml_str += f"{indent}{key} = {self._format_string_value(value)}\n"
            elif isinstance(value, bool):
                toml_str += f"{indent}{key} = {str(value).lower()}\n"
            elif isinstance(value, (int, float)) and value is not None:
                toml_str += f"{indent}{key} = {value}\n"
            elif isinstance(value, (list, tuple, set)) and not value:
                toml_str += f"{indent}{key} = []\n"
            elif isinstance(value, (list, tuple, set)):
                if not any(isinstance(sub_item, dict) for sub_item in value):
                    toml_str += f"{indent}{key} = [\n"
                    for sub_item in value:
                        if isinstance(sub_item, str):
                            toml_str += f"{indent}{indent}{self._format_string_value(sub_item)},\n"
                        else:
                            toml_str += f"{indent}{indent}{sub_item},\n"
                    toml_str += f"{indent}]\n"

        # Process nested dicts in table items
        for key, value in item.items():
            if isinstance(value, dict):
                nested_section = f"{section_key}.{key}"
                toml_str      += f"[{nested_section}]\n"
                toml_str      += self._process_section_content(value, nested_section)

        return toml_str