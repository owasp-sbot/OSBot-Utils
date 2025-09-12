import re
import pytest
from unittest                                                                                import TestCase
from osbot_utils.type_safe.Type_Safe                                                         import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                              import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Str                                          import Safe_Str
from osbot_utils.type_safe.primitives.domains.llm.safe_str.Safe_Str__LLM__Message__Assistant import Safe_Str__LLM__Message__Assistant
from osbot_utils.utils.Objects                                                               import __, base_classes



class test_Safe_Str__LLM__Message__Assistant(TestCase):

    def test__init__(self):                                                              # Test initialization
        with Safe_Str__LLM__Message__Assistant() as _:
            assert type(_)         is Safe_Str__LLM__Message__Assistant
            assert base_classes(_) == [Safe_Str, Type_Safe__Primitive, str, object, object]
            assert _               == ''
            assert _.max_length    == 32768                                             # Full context for responses
            assert _.regex.pattern == r'[\x00-\x08\x0B\x0C\x0E-\x1F]'                 # Preserves tabs/newlines

    def test_assistant_responses_preserved(self):                                       # Test typical assistant messages
        # Simple responses
        assert Safe_Str__LLM__Message__Assistant('Hello! How can I help?') == 'Hello! How can I help?'
        assert Safe_Str__LLM__Message__Assistant('The answer is 42.')      == 'The answer is 42.'

        # Detailed explanation
        explanation = """Python is a high-level programming language known for:
1. Simple, readable syntax
2. Dynamic typing
3. Extensive standard library
4. Large ecosystem of packages

Here's a simple example:
```python
def greet(name):
    return f"Hello, {name}!"
```"""

        result = Safe_Str__LLM__Message__Assistant(explanation)
        assert result == explanation                                            # All formatting preserved
        assert '```python' in result
        assert '\n' in result

    def test_code_responses(self):                                                     # Test code in responses
        # Python code
        python_code = """Here's the solution:

```python
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

This iterative approach is O(n) time complexity."""

        assert Safe_Str__LLM__Message__Assistant(python_code) == python_code

        # JSON response
        json_response = '{"status": "success", "result": [1, 2, 3], "metadata": null}'
        assert Safe_Str__LLM__Message__Assistant(json_response) == json_response

    def test_markdown_formatting(self):                                               # Test markdown in responses
        markdown = """# Solution

## Step 1: Understanding
The problem requires us to **find** the *optimal* solution.

## Step 2: Implementation
- First, we initialize variables
- Then, we iterate through the data
- Finally, we return the result

> Note: This approach has O(n log n) complexity.

For more details, see [documentation](https://example.com)."""

        result = Safe_Str__LLM__Message__Assistant(markdown)
        assert result == markdown
        assert '**find**' in result
        assert '*optimal*' in result
        assert '[documentation]' in result

    def test_whitespace_preservation(self):                                          # Test whitespace handling
        # Tabs preserved
        assert Safe_Str__LLM__Message__Assistant('A\tB\tC')         == 'A\tB\tC'

        # Newlines preserved
        assert Safe_Str__LLM__Message__Assistant('Line1\nLine2')    == 'Line1\nLine2'

        # Indentation preserved
        indented = """    def function():
        return True"""
        assert Safe_Str__LLM__Message__Assistant(indented) == indented

    def test_control_char_replacement(self):                                            # Test control character removal
        # Control chars removed
        assert Safe_Str__LLM__Message__Assistant('Text\x00Null')    == 'Text_Null'
        assert Safe_Str__LLM__Message__Assistant('Bell\x07Ring')    == 'Bell_Ring'

        # Vertical tab and form feed removed
        assert Safe_Str__LLM__Message__Assistant('V\x0BTab')        == 'V_Tab'
        assert Safe_Str__LLM__Message__Assistant('Form\x0CFeed')    == 'Form_Feed'

    def test_special_content(self):                                                 # Test special content types
        # Math notation
        math = 'The derivative of x² is 2x, and ∫x²dx = x³/3 + C'
        assert Safe_Str__LLM__Message__Assistant(math) == math

        # Tables
        table = """| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |
| Value 3  | Value 4  |"""
        assert Safe_Str__LLM__Message__Assistant(table) == table

        # Lists with emojis
        emoji_list = """Tasks completed:
✅ Task 1
✅ Task 2
❌ Task 3 (failed)
⏳ Task 4 (pending)"""
        assert Safe_Str__LLM__Message__Assistant(emoji_list) == emoji_list

    def test_max_length_enforcement(self):                                         # Test 32KB limit
        # At max length
        long_response = 'A' * 32768
        assert Safe_Str__LLM__Message__Assistant(long_response) == long_response

        # Exceeds max length
        too_long = 'A' * 32769
        error_message = "in Safe_Str__LLM__Message__Assistant, value exceeds maximum length of 32768"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__LLM__Message__Assistant(too_long)

    def test_usage_in_type_safe(self):                                            # Test Type_Safe integration
        class Schema__AI__Response(Type_Safe):
            response     : Safe_Str__LLM__Message__Assistant
            confidence   : float = 0.0

        with Schema__AI__Response() as _:
            assert type(_.response) is Safe_Str__LLM__Message__Assistant
            assert _.response == ''

            _.response = """Based on my analysis:
1. The code is correct
2. Performance can be improved
3. Consider adding error handling"""

            assert '1. The code' in _.response
            assert '\n' in _.response

    def test_json_serialization(self):                                           # Test JSON round-trip
        class Schema__Assistant__Reply(Type_Safe):
            answer      : Safe_Str__LLM__Message__Assistant
            explanation : Safe_Str__LLM__Message__Assistant

        with Schema__Assistant__Reply() as original:
            original.answer = 'The capital of France is Paris.'
            original.explanation = 'Paris has been the capital since 987 AD.'

            json_data = original.json()
            assert json_data == {
                'answer': 'The capital of France is Paris.',
                'explanation': 'Paris has been the capital since 987 AD.'
            }

            with Schema__Assistant__Reply.from_json(json_data) as restored:
                assert restored.obj() == original.obj()
                assert type(restored.answer) is Safe_Str__LLM__Message__Assistant

    def test_realistic_assistant_responses(self):                                # Test real-world examples
        # Detailed technical response
        technical = """I'll help you implement authentication in FastAPI. Here's a complete solution:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
        return username
    except JWTError:
        raise HTTPException(status_code=401)
```

This implementation includes:
- JWT token generation
- Token validation middleware
- Secure password handling
- 30-minute token expiration

Would you like me to explain any part in more detail?"""

        assert Safe_Str__LLM__Message__Assistant(technical) ==  technical