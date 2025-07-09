# Html_Dict__To__Html_Document

## Overview

`Html_Dict__To__Html_Document` converts dictionary representations of HTML (from `Html__To__Html_Dict`) into type-safe schema objects. This converter bridges the gap between the raw parsed format and the structured schema system, enabling type-safe serialization and manipulation.

## Class Definition

```python
class Html_Dict__To__Html_Document(Type_Safe):
    html__dict    : dict                  = None
    html__document: Schema__Html_Document = None
```

## Purpose

This converter serves several critical functions:
1. **Type Safety**: Transforms untyped dictionaries into strongly-typed schema objects
2. **Position Assignment**: Adds position tracking to maintain element order
3. **Node Separation**: Splits mixed `nodes` arrays into separate `child_nodes` and `text_nodes`
4. **Validation**: Ensures proper structure during conversion

## Methods

### `convert() -> Schema__Html_Document`

Main conversion method that processes the dictionary and returns a document schema.

```python
converter = Html_Dict__To__Html_Document(html__dict=html_dict)
document = converter.convert()
```

### `parse_html_dict(target: Dict[str, Any]) -> Schema__Html_Document`

Creates the document wrapper with timestamp and root node.

### `parse_node(target: Dict[str, Any], position: int) -> Schema__Html_Node`

Recursively converts dictionary nodes to schema nodes, handling:
- Attribute preservation
- Child node separation
- Position assignment
- Type determination

## Conversion Process

### 1. Input Dictionary Format
```python
{
    'tag': 'div',
    'attrs': {'class': 'container'},
    'nodes': [
        {'type': 'TEXT', 'data': 'Hello'},
        {'tag': 'p', 'attrs': {}, 'nodes': [...]},
        {'type': 'TEXT', 'data': 'World'}
    ]
}
```

### 2. Output Schema Format
```python
Schema__Html_Node(
    tag='div',
    attrs={'class': 'container'},
    child_nodes=[
        Schema__Html_Node(tag='p', position=1, ...)
    ],
    text_nodes=[
        Schema__Html_Node__Data(data='Hello', position=0),
        Schema__Html_Node__Data(data='World', position=2)
    ],
    position=-1  # Root node
)
```

## Position Assignment

Positions are assigned to maintain the original order of mixed content:

```python
# Original: <div>Text1<p>Para</p>Text2</div>
# Positions: Text1(0), p(1), Text2(2)
```

- Root nodes get position `-1`
- Child positions start at `0` and increment
- Positions are relative to the parent node

## Usage Examples

### Basic Conversion

```python
from osbot_utils.helpers.html.Html__To__Html_Dict import Html__To__Html_Dict
from osbot_utils.helpers.html.Html_Dict__To__Html_Document import Html_Dict__To__Html_Document

# Parse HTML
html = "<div><p>Hello</p></div>"
html_dict = Html__To__Html_Dict(html).convert()

# Convert to document
converter = Html_Dict__To__Html_Document(html__dict=html_dict)
document = converter.convert()

# Access the structure
assert document.root_node.tag == 'div'
assert len(document.root_node.child_nodes) == 1
assert document.root_node.child_nodes[0].tag == 'p'
```

### Mixed Content Handling

```python
html = "<p>Start <strong>middle</strong> end</p>"
html_dict = Html__To__Html_Dict(html).convert()
document = Html_Dict__To__Html_Document(html__dict=html_dict).convert()

root = document.root_node
# Text nodes: "Start " (position 0), " end" (position 2)
# Child nodes: <strong> (position 1)
assert len(root.text_nodes) == 2
assert len(root.child_nodes) == 1
```

### With Serialization

```python
# Convert and serialize
document = Html_Dict__To__Html_Document(html__dict=html_dict).convert()
json_data = document.json()

# Can now be saved/transmitted
with open('document.json', 'w') as f:
    json.dump(json_data, f)
```

## Error Handling

```python
try:
    converter = Html_Dict__To__Html_Document(html__dict=invalid_dict)
    document = converter.convert()
except ValueError as e:
    print(f"Invalid HTML structure: {e}")
```

## Integration with Pipeline

```python
# Complete pipeline example
def html_to_document(html_string):
    # Step 1: Parse HTML to dict
    html_dict = Html__To__Html_Dict(html_string).convert()
    
    # Step 2: Convert to document
    document = Html_Dict__To__Html_Document(html__dict=html_dict).convert()
    
    return document
```

## Type Safety Benefits

The conversion provides several type safety advantages:

1. **Validated Structure**: All nodes have required fields
2. **Type Checking**: Can use type checkers like mypy
3. **Serialization**: Clean JSON serialization/deserialization
4. **IDE Support**: Better autocomplete and type hints

## Best Practices

1. **Validate Input**: Ensure the dictionary is from a valid HTML parse
2. **Handle Errors**: Wrap conversion in try-except for robustness
3. **Check Positions**: Verify position assignments for debugging
4. **Use Type Hints**: Leverage the type safety in your code

```python
def process_document(html_dict: dict) -> Schema__Html_Document:
    """Convert HTML dictionary to document with error handling."""
    if not html_dict:
        raise ValueError("Empty HTML dictionary")
        
    converter = Html_Dict__To__Html_Document(html__dict=html_dict)
    return converter.convert()
```

## Common Patterns

### Extracting All Text

```python
def get_all_text(node: Schema__Html_Node) -> List[str]:
    texts = []
    
    # Get text from text nodes
    for text_node in node.text_nodes:
        texts.append((text_node.position, text_node.data))
    
    # Recursively get text from child nodes
    for child in node.child_nodes:
        texts.extend(get_all_text(child))
    
    # Sort by position and extract text
    texts.sort(key=lambda x: x[0])
    return [text for _, text in texts]
```

### Finding Elements by Tag

```python
def find_by_tag(node: Schema__Html_Node, tag_name: str) -> List[Schema__Html_Node]:
    results = []
    
    if node.tag == tag_name:
        results.append(node)
    
    for child in node.child_nodes:
        results.extend(find_by_tag(child, tag_name))
    
    return results
```

## Performance Considerations

- **Memory Usage**: Schema objects use more memory than raw dicts
- **Conversion Time**: Linear with document size
- **Deep Nesting**: Very deep documents may hit recursion limits

## Limitations

1. **No HTML Validation**: Doesn't validate HTML semantics
2. **Memory Overhead**: Schema objects are larger than dicts
3. **Position Conflicts**: Manual position changes can break order
4. **No Streaming**: Requires full document in memory