import re
import pytest
from unittest                                                                           import TestCase
from osbot_utils.utils.Objects                                                          import base_classes
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                         import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Str                                     import Safe_Str
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Message__Tool import Safe_Str__LLM__Message__Tool



class test_Safe_Str__LLM__Message__Tool(TestCase):

    def test__init__(self):                                                         # Test initialization
        with Safe_Str__LLM__Message__Tool() as _:
            assert type(_)         is Safe_Str__LLM__Message__Tool
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 16384                                        # Shorter than full messages
            assert _.regex.pattern == r'[\x00-\x08\x0B\x0C\x0E-\x1F]'            # Preserves tabs/newlines

    def test_tool_responses_preserved(self):                                       # Test typical tool/function responses
        # JSON response from tool
        json_response = '{"status": "success", "data": {"temperature": 22, "humidity": 45}}'
        assert Safe_Str__LLM__Message__Tool(json_response) == json_response

        # Structured data response
        data_response = """Result from database query:
ID | Name     | Status
1  | Item A   | Active
2  | Item B   | Pending
3  | Item C   | Complete"""

        assert Safe_Str__LLM__Message__Tool(data_response) == data_response

        # API response
        api_response = '{"endpoint": "/api/users", "method": "GET", "response_code": 200}'
        assert Safe_Str__LLM__Message__Tool(api_response) == api_response

    def test_function_call_results(self):                                          # Test function call outputs
        # Calculator function
        calc_result = '{"function": "calculate", "input": "2+2", "output": 4}'
        assert Safe_Str__LLM__Message__Tool(calc_result) == calc_result

        # Search function
        search_result = """Search Results:
1. "Python Tutorial" - https://example.com/python
2. "Learn Python" - https://example.com/learn
3. "Python Docs" - https://python.org/docs"""

        assert Safe_Str__LLM__Message__Tool(search_result) == search_result

        # Database query
        db_result = """Query executed successfully.
Rows affected: 5
Result: [
    {"id": 1, "value": "A"},
    {"id": 2, "value": "B"}
]"""

        assert Safe_Str__LLM__Message__Tool(db_result) == db_result

    def test_error_messages(self):                                                # Test tool error responses
        # Error JSON
        error_json = '{"error": "Invalid parameters", "code": 400, "details": "Missing required field: user_id"}'
        assert Safe_Str__LLM__Message__Tool(error_json) == error_json

        # Stack trace (simplified)
        stack_trace = """Error: Division by zero
  at calculate() line 15
  at process() line 8
  at main() line 3"""

        assert Safe_Str__LLM__Message__Tool(stack_trace) == stack_trace

    def test_whitespace_preservation(self):                                       # Test whitespace handling
        # Tabs preserved for structured data
        tabbed = "Column1\tColumn2\tColumn3\nValue1\tValue2\tValue3"
        assert Safe_Str__LLM__Message__Tool(tabbed) == tabbed

        # Newlines preserved
        multiline = "Line 1\nLine 2\nLine 3"
        assert Safe_Str__LLM__Message__Tool(multiline) == multiline

        # JSON formatting preserved
        formatted_json = """{
    "key1": "value1",
    "key2": {
        "nested": true
    }
}"""
        assert Safe_Str__LLM__Message__Tool(formatted_json) == formatted_json

    def test_control_char_removal(self):                                         # Test control character removal
        # Control chars removed
        assert Safe_Str__LLM__Message__Tool('Data\x00Null')     == 'Data_Null'
        assert Safe_Str__LLM__Message__Tool('Alert\x07Bell')    == 'Alert_Bell'

        # Vertical tab and form feed removed
        assert Safe_Str__LLM__Message__Tool('V\x0BTab')         == 'V_Tab'
        assert Safe_Str__LLM__Message__Tool('Page\x0CBreak')    == 'Page_Break'

    def test_special_formats(self):                                             # Test various data formats
        # CSV-like data
        csv_data = """name,age,city
John,30,NYC
Jane,25,LA
Bob,35,Chicago"""
        assert Safe_Str__LLM__Message__Tool(csv_data) == csv_data

        # XML response
        xml_data = '<response><status>ok</status><count>42</count></response>'
        assert Safe_Str__LLM__Message__Tool(xml_data) == xml_data

        # URL with parameters
        url_data = 'https://api.example.com/data?id=123&format=json&key=abc-xyz'
        assert Safe_Str__LLM__Message__Tool(url_data) == url_data

    def test_max_length_enforcement(self):                                      # Test 16KB limit
        # At max length
        long_response = 'A' * 16384
        assert Safe_Str__LLM__Message__Tool(long_response) == long_response

        # Exceeds max length
        too_long = 'A' * 16385
        error_message = "in Safe_Str__LLM__Message__Tool, value exceeds maximum length of 16384"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__LLM__Message__Tool(too_long)

    def test_usage_in_type_safe(self):                                         # Test Type_Safe integration
        class Schema__Tool__Response(Type_Safe):
            tool_output : Safe_Str__LLM__Message__Tool
            tool_name   : str
            success     : bool = True

        with Schema__Tool__Response() as _:
            assert type(_.tool_output) is Safe_Str__LLM__Message__Tool
            assert _.tool_output == ''

            _.tool_output = '{"result": "calculated", "value": 42}'
            _.tool_name = 'calculator'

            assert '"result"' in _.tool_output
            assert _.success is True

    def test_json_serialization(self):                                        # Test JSON round-trip
        class Schema__Function__Call(Type_Safe):
            function_result : Safe_Str__LLM__Message__Tool
            execution_time  : float

        with Schema__Function__Call() as original:
            original.function_result = '{"computed": true, "result": [1, 2, 3]}'
            original.execution_time = 0.123

            json_data = original.json()
            assert json_data == {
                'function_result': '{"computed": true, "result": [1, 2, 3]}',
                'execution_time': 0.123
            }

            with Schema__Function__Call.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.function_result) is Safe_Str__LLM__Message__Tool

    def test_realistic_tool_outputs(self):                                    # Test real-world examples
        # Web search tool
        web_search = """Web Search Results for "Python FastAPI tutorial":

1. **Official FastAPI Documentation**
   URL: https://fastapi.tiangolo.com/tutorial/
   Description: Complete tutorial covering all FastAPI features
   
2. **Real Python - FastAPI Tutorial**
   URL: https://realpython.com/fastapi-python-web-apis/
   Description: Build modern web APIs with Python and FastAPI
   
3. **FastAPI Quick Start Guide**
   URL: https://github.com/tiangolo/fastapi#example
   Description: Quick examples to get started with FastAPI

Total results: 1,234
Search time: 0.42 seconds"""

        assert web_search == Safe_Str__LLM__Message__Tool(web_search)

        # Code execution tool
        code_exec = """Execution Result:
stdout:
Hello, World!
Processing item 1...
Processing item 2...
Done!

stderr:
(empty)

Return code: 0
Execution time: 0.003s"""

        assert code_exec == Safe_Str__LLM__Message__Tool(code_exec)

        # Database query tool
        db_query = """Query: SELECT * FROM users WHERE active = true LIMIT 3;

Results:
[
  {"id": 1, "name": "Alice", "email": "alice@example.com", "active": true},
  {"id": 3, "name": "Charlie", "email": "charlie@example.com", "active": true},
  {"id": 5, "name": "Eve", "email": "eve@example.com", "active": true}
]

Rows returned: 3
Query time: 15ms"""

        assert db_query == Safe_Str__LLM__Message__Tool(db_query)