# Schema__Html_Node__Data

## Overview

`Schema__Html_Node__Data` represents text content within HTML elements. It's a type-safe wrapper for text nodes that includes position tracking for maintaining order within mixed content.

## Class Definition

```python
class Schema__Html_Node__Data(Type_Safe):
    data     : str                                           # Text content
    type     : Schema__Html_Node__Data__Type = Schema__Html_Node__Data__Type.TEXT
    position : int = 0                                       # Position in parent
```

## Purpose

This class serves to:
1. **Type Safety**: Provides a strongly-typed text node representation
2. **Position Tracking**: Maintains text position among sibling nodes
3. **Clear Semantics**: Explicitly identifies text vs element nodes
4. **Serialization**: Enables clean JSON serialization of text content

## Properties

### `data`
- **Type**: `str`
- **Purpose**: The actual text content
- **Default**: `""`
- **Examples**: `"Hello World"`, `"Click here"`, `"\n    "`

### `type`
- **Type**: `Schema__Html_Node__Data__Type`
- **Purpose**: Identifies this as a text node
- **Default**: `Schema__Html_Node__Data__Type.TEXT`
- **Value**: Always `'TEXT'` in serialized form

### `position`
- **Type**: `int`
- **Purpose**: Position within parent's children
- **Default**: `0`
- **Range**: 0 to n-1 for n total children

## Usage Examples

### Basic Text Node

```python
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data import Schema__Html_Node__Data

# Simple text node
text_node = Schema__Html_Node__Data(
    data="Hello World",
    position=0
)

# Accessing properties
print(text_node.data)       # "Hello World"
print(text_node.position)   # 0
print(text_node.type.value) # "TEXT"
```

### Within HTML Structure

```python
# Creating a paragraph with text
# <p>This is a paragraph.</p>

text = Schema__Html_Node__Data(
    data="This is a paragraph.",
    position=0
)

p_node = Schema__Html_Node(
    tag='p',
    text_nodes=[text],
    child_nodes=[],
    position=0
)
```

### Mixed Content

```python
# HTML: <p>Hello <em>beautiful</em> world!</p>

# Text nodes
text1 = Schema__Html_Node__Data(data="Hello ", position=0)
text2 = Schema__Html_Node__Data(data=" world!", position=2)

# Em node with its own text
em_text = Schema__Html_Node__Data(data="beautiful", position=0)
em_node = Schema__Html_Node(
    tag='em',
    text_nodes=[em_text],
    child_nodes=[],
    position=1
)

# Paragraph containing mixed content
p_node = Schema__Html_Node(
    tag='p',
    text_nodes=[text1, text2],
    child_nodes=[em_node],
    position=0
)
```

## Special Cases

### Whitespace Preservation

```python
# Preserving formatting whitespace
formatted_text = Schema__Html_Node__Data(
    data="\n    Indented text\n    ",
    position=0
)

# Empty text nodes (sometimes needed for formatting)
empty_text = Schema__Html_Node__Data(
    data="",
    position=1
)
```

### Special Characters

```python
# HTML entities and special characters
entity_text = Schema__Html_Node__Data(
    data="Price: $19.99 & tax",
    position=0
)

# Unicode content
unicode_text = Schema__Html_Node__Data(
    data="Hello 世界 🌍",
    position=0
)

# Line breaks and tabs
formatted = Schema__Html_Node__Data(
    data="Line 1\nLine 2\tTabbed",
    position=0
)
```

## Serialization

### JSON Format

```python
text_node = Schema__Html_Node__Data(
    data="Sample text",
    position=3
)

# Serialize to JSON
json_data = text_node.json()
# {
#     "data": "Sample text",
#     "type": "TEXT",
#     "position": 3
# }

# Deserialize from JSON
restored = Schema__Html_Node__Data.from_json(json_data)
assert restored.data == "Sample text"
assert restored.position == 3
```

### In Document Context

```python
# As part of a larger structure
document_json = {
    "root_node": {
        "tag": "p",
        "attrs": {},
        "child_nodes": [],
        "text_nodes": [
            {
                "data": "Paragraph text",
                "type": "TEXT",
                "position": 0
            }
        ],
        "position": 0
    },
    "timestamp": "2024-01-01T00:00:00"
}
```

## Common Operations

### Text Manipulation

```python
def clean_text(text_node):
    """Clean and normalize text content."""
    # Remove extra whitespace
    cleaned = ' '.join(text_node.data.split())
    
    # Create new node with cleaned text
    return Schema__Html_Node__Data(
        data=cleaned,
        position=text_node.position
    )

def truncate_text(text_node, max_length):
    """Truncate text to maximum length."""
    if len(text_node.data) <= max_length:
        return text_node
    
    truncated = text_node.data[:max_length-3] + "..."
    return Schema__Html_Node__Data(
        data=truncated,
        position=text_node.position
    )
```

### Text Analysis

```python
def analyze_text_node(text_node):
    """Analyze text node properties."""
    return {
        'length': len(text_node.data),
        'word_count': len(text_node.data.split()),
        'has_whitespace': text_node.data != text_node.data.strip(),
        'is_empty': text_node.data == '',
        'position': text_node.position
    }

def contains_pattern(text_node, pattern):
    """Check if text contains a pattern."""
    import re
    return bool(re.search(pattern, text_node.data))
```

### Position Management

```python
def insert_text_node(parent, new_text, position):
    """Insert a text node at specific position."""
    # Create new text node
    new_node = Schema__Html_Node__Data(
        data=new_text,
        position=position
    )
    
    # Adjust positions of existing nodes
    for text in parent.text_nodes:
        if text.position >= position:
            text.position += 1
    
    for child in parent.child_nodes:
        if child.position >= position:
            child.position += 1
    
    # Add new node
    parent.text_nodes.append(new_node)
    
    # Sort by position
    parent.text_nodes.sort(key=lambda x: x.position)
```

## Integration with Parent Nodes

### Building Complete Structures

```python
def create_paragraph_with_formatting(text_parts):
    """Create paragraph with multiple text nodes."""
    p_node = Schema__Html_Node(
        tag='p',
        attrs={},
        child_nodes=[],
        text_nodes=[],
        position=0
    )
    
    for i, text in enumerate(text_parts):
        text_node = Schema__Html_Node__Data(
            data=text,
            position=i
        )
        p_node.text_nodes.append(text_node)
    
    return p_node
```

### Extracting All Text

```python
def extract_all_text(node):
    """Extract all text from a node hierarchy."""
    texts = []
    
    # Combine text and child nodes by position
    all_content = []
    for text in node.text_nodes:
        all_content.append((text.position, text.data))
    
    for child in node.child_nodes:
        child_text = extract_all_text(child)
        all_content.append((child.position, child_text))
    
    # Sort by position and join
    all_content.sort(key=lambda x: x[0])
    return ''.join(str(content[1]) for content in all_content)
```

## Type Safety Benefits

```python
from typing import List

def process_text_nodes(text_nodes: List[Schema__Html_Node__Data]) -> str:
    """Type-safe text processing."""
    # IDE knows these are text nodes
    combined = ""
    for node in text_nodes:
        # Type checker ensures 'data' exists
        combined += node.data
    
    return combined

# Type checking prevents errors
def invalid_usage(node: Schema__Html_Node__Data):
    # This would be caught by type checker
    # node.tag  # Error: 'Schema__Html_Node__Data' has no attribute 'tag'
    pass
```

## Best Practices

1. **Always Set Position**: Even for single text nodes
2. **Preserve Whitespace**: Don't strip unless intentional
3. **Handle Empty Text**: Empty strings are valid
4. **Use Type Enum**: Always use the enum for type field
5. **Validate Positions**: Ensure no position conflicts

## Common Patterns

### Text Replacement

```python
def replace_text_content(node, old_text, new_text):
    """Replace text in all text nodes."""
    for text_node in node.text_nodes:
        if old_text in text_node.data:
            text_node.data = text_node.data.replace(old_text, new_text)
```

### Text Formatting

```python
def format_as_title(text_node):
    """Convert text to title case."""
    return Schema__Html_Node__Data(
        data=text_node.data.title(),
        position=text_node.position
    )
```

## Performance Notes

- **String Immutability**: Text changes create new strings
- **Memory Usage**: Each node has overhead beyond the text
- **Large Texts**: Consider chunking very large text content
- **Position Sorting**: O(n log n) when reordering

## Limitations

1. **No Formatting**: Just plain text, no built-in formatting
2. **No Validation**: Doesn't validate HTML entities
3. **Memory Overhead**: Wrapper adds memory beyond raw string
4. **No Streaming**: Entire text must be in memory