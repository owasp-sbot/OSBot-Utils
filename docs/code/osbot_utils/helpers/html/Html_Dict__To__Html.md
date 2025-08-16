# Html_Dict__To__Html

## Overview

`Html_Dict__To__Html` converts dictionary representations back into HTML strings. It handles proper formatting, indentation, and special cases like self-closing tags and mixed content.

## Class Definition

```python
class Html_Dict__To__Html:
    def __init__(self, root, include_doctype=True, doctype=HTML_DEFAULT_DOCTYPE_VALUE):
        self.self_closing_tags = HTML_SELF_CLOSING_TAGS
        self.root              = root
        self.include_doctype   = include_doctype
        self.doctype           = doctype
```

## Key Features

- **Proper Indentation**: Generates readable HTML with consistent indentation
- **Attribute Handling**: Escapes quotes and handles special attribute values
- **Mixed Content Support**: Correctly formats elements with both text and child elements
- **Self-Closing Tags**: Recognizes and properly formats void elements
- **DOCTYPE Support**: Optionally includes DOCTYPE declaration

## Methods

### `convert() -> str`

Main method that converts the dictionary to an HTML string.

```python
html_dict = {'tag': 'div', 'attrs': {'class': 'container'}, 'nodes': []}
converter = Html_Dict__To__Html(html_dict)
html = converter.convert()
# Returns: "<!DOCTYPE html>\n<div class=\"container\"></div>\n"
```

### `convert_attrs(attrs: dict) -> str`

Converts attributes dictionary to HTML attribute string. Handles:
- Empty values
- None values  
- Quote escaping
- Special characters

```python
attrs = {'class': 'container', 'id': 'main', 'disabled': None}
# Returns: ' class="container" id="main" disabled'
```

### `convert_element(element: dict, indent_level: int) -> str`

Recursively converts dictionary elements to HTML with proper indentation.

### `convert_children(nodes: list, indent_level: int) -> str`

Processes child nodes with appropriate indentation.

## Formatting Rules

### 1. Empty Elements
```python
{'tag': 'div', 'attrs': {}, 'nodes': []}
# Output: <div></div>
```

### 2. Elements with Only Child Elements
```python
{
    'tag': 'ul',
    'nodes': [
        {'tag': 'li', 'nodes': [{'type': 'TEXT', 'data': 'Item'}]}
    ]
}
# Output:
# <ul>
#     <li>Item</li>
# </ul>
```

### 3. Mixed Content (Text + Elements)
```python
{
    'tag': 'p',
    'nodes': [
        {'type': 'TEXT', 'data': 'Hello '},
        {'tag': 'strong', 'nodes': [{'type': 'TEXT', 'data': 'World'}]},
        {'type': 'TEXT', 'data': '!'}
    ]
}
# Output: <p>Hello <strong>World</strong>!</p>
```

### 4. Self-Closing Tags
```python
{'tag': 'br', 'attrs': {}, 'nodes': []}
# Output: <br />
```

## Usage Examples

### Basic Conversion

```python
from osbot_utils.helpers.html.transformers.Html_Dict__To__Html import Html_Dict__To__Html

html_dict = {
    'tag': 'html',
    'attrs': {'lang': 'en'},
    'nodes': [
        {
            'tag': 'head',
            'attrs': {},
            'nodes': [
                {
                    'tag': 'title',
                    'attrs': {},
                    'nodes': [{'type': 'TEXT', 'data': 'My Page'}]
                }
            ]
        }
    ]
}

converter = Html_Dict__To__Html(html_dict)
html = converter.convert()
```

### Without DOCTYPE

```python
converter = Html_Dict__To__Html(html_dict, include_doctype=False)
html = converter.convert()  # No DOCTYPE declaration
```

### Custom DOCTYPE

```python
custom_doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN">\n'
converter = Html_Dict__To__Html(html_dict, doctype=custom_doctype)
```

## Attribute Handling Details

### Quote Escaping

The converter intelligently handles quotes in attribute values:

```python
# Double quotes present: uses single quotes
{'href': 'javascript:alert("Hello")'}
# Output: href='javascript:alert("Hello")'

# Both quotes present: escapes double quotes
{'onclick': 'alert("It\'s working")'}
# Output: onclick="alert(&quot;It's working&quot;)"
```

### Special Attribute Values

```python
# None values: attribute without value
{'disabled': None} → 'disabled'

# Empty strings: empty attribute
{'alt': ''} → 'alt=""'
```

## Indentation

- Uses 4 spaces per indent level
- Elements-only content gets newlines and indentation
- Mixed content stays on one line
- Closing tags align with opening tags

## Constants

```python
HTML_SELF_CLOSING_TAGS = {'area', 'base', 'br', 'col', 'command', 'embed', 
                         'hr', 'img', 'input', 'link', 'meta', 'param', 
                         'source', 'track', 'wbr'}
HTML_DEFAULT_DOCTYPE_VALUE = "<!DOCTYPE html>\n"
```

## Best Practices

1. **Consistent Structure**: Ensure dictionary structure matches expected format
2. **Text Nodes**: Always include 'type': 'TEXT' for text content
3. **Attributes**: Use None for boolean attributes, empty string for empty values
4. **Validation**: Validate dictionary structure before conversion

## Limitations

- Does not validate HTML semantics
- Does not check for required attributes
- Does not enforce HTML5 vs XHTML rules
- Attribute order is preserved from dictionary (Python 3.7+)