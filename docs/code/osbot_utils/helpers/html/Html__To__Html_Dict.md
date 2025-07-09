# Html__To__Html_Dict

## Overview

`Html__To__Html_Dict` is the core HTML parser that converts HTML strings into dictionary representations. It extends Python's built-in `HTMLParser` to create a structured dictionary format that preserves the complete HTML structure including elements, attributes, and text content.

## Class Definition

```python
class Html__To__Html_Dict(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.root            = None
        self.current         = None
        self.stack           = []
        self.html            = html or ''
        self.void_elements   = HTML_SELF_CLOSING_TAGS
        self.strip_text_data = True
```

## Key Features

- **Hierarchical Parsing**: Maintains parent-child relationships
- **Mixed Content Support**: Handles elements containing both text and child elements
- **Self-Closing Tag Recognition**: Properly handles void elements like `<br>`, `<img>`, etc.
- **Stack-Based Navigation**: Uses a stack to track nesting depth
- **Pretty Printing**: Can output a visual tree representation

## Constants

```python
HTML_SELF_CLOSING_TAGS = {'area', 'base', 'br', 'col', 'command', 'embed', 
                         'hr', 'img', 'input', 'link', 'meta', 'param', 
                         'source', 'track', 'wbr'}
STRING__SCHEMA_TEXT    = 'TEXT'
STRING__SCHEMA_NODES   = 'nodes'
```

## Methods

### `convert() -> dict`

Main method that parses the HTML and returns the root dictionary.

```python
parser = Html__To__Html_Dict("<div>Hello</div>")
result = parser.convert()
# Returns: {'tag': 'div', 'attrs': {}, 'nodes': [{'type': 'TEXT', 'data': 'Hello'}]}
```

### `handle_starttag(tag: str, attrs: list)`

Handles opening HTML tags. Creates a new dictionary node and manages the parsing stack.

### `handle_endtag(tag: str)`

Handles closing HTML tags. Properly manages the stack even with malformed HTML.

### `handle_data(data: str)`

Handles text content between tags. Ignores pure whitespace unless significant.

### `print(just_return_lines: bool = False)`

Outputs a visual tree representation of the parsed HTML.

```python
parser = Html__To__Html_Dict(html)
parser.convert()
parser.print()
# Output:
# html (lang="en")
#     ├── head
#     │   └── title
#     │       └── TEXT: My Page
#     └── body
```

## Dictionary Format

The parser produces dictionaries with this structure:

### Element Nodes
```python
{
    'tag': 'div',
    'attrs': {'class': 'container', 'id': 'main'},
    'nodes': [...]  # Child nodes
}
```

### Text Nodes
```python
{
    'type': 'TEXT',
    'data': 'Text content'
}
```

## Usage Examples

### Basic Parsing

```python
from osbot_utils.helpers.html.Html__To__Html_Dict import Html__To__Html_Dict

html = """
<div class="container">
    <p>Hello <strong>World</strong></p>
</div>
"""

parser = Html__To__Html_Dict(html)
result = parser.convert()
```

### Handling Mixed Content

```python
html = "<p>Text before <span>inline</span> text after</p>"
parser = Html__To__Html_Dict(html)
result = parser.convert()

# Result structure:
# {
#     'tag': 'p',
#     'attrs': {},
#     'nodes': [
#         {'type': 'TEXT', 'data': 'Text before '},
#         {'tag': 'span', 'attrs': {}, 'nodes': [{'type': 'TEXT', 'data': 'inline'}]},
#         {'type': 'TEXT', 'data': ' text after'}
#     ]
# }
```

### Working with Attributes

```python
html = '<div id="main" class="container" data-value="123">'
parser = Html__To__Html_Dict(html)
result = parser.convert()
# result['attrs'] = {'id': 'main', 'class': 'container', 'data-value': '123'}
```

## Helper Function

The module also provides a convenience function:

```python
def html_to_dict(html_code: str) -> dict:
    """
    Quick parsing function that returns None on parse errors.
    """
    try:
        return Html__To__Html_Dict(html_code).convert()
    except:
        return None
```

## Error Handling

- Malformed HTML is handled gracefully
- Missing closing tags are managed by the stack mechanism  
- Parse errors in `html_to_dict()` return `None`

## Implementation Notes

1. **Void Elements**: Self-closing tags are recognized and don't expect closing tags
2. **Whitespace**: Pure whitespace between elements is ignored by default
3. **Stack Management**: The parser maintains proper nesting even with malformed HTML
4. **Text Stripping**: Text content can be stripped of leading/trailing whitespace via `strip_text_data`

## Limitations

- Does not preserve comments
- Does not handle CDATA sections
- Does not preserve DOCTYPE information (handled separately)
- Attribute order may not be preserved exactly as in source