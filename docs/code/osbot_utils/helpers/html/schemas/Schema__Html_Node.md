# Schema__Html_Node

## Overview

`Schema__Html_Node` represents an HTML element in the type-safe schema system. It separates child elements and text content into distinct lists with position tracking, solving the Union type serialization challenge while maintaining document structure.

## Class Definition

```python
class Schema__Html_Node(Type_Safe):
    attrs       : Dict[str, Optional[str]]     # HTML attributes
    child_nodes : List['Schema__Html_Node']    # Element nodes only
    text_nodes  : List['Schema__Html_Node__Data']  # Text nodes only  
    tag         : str                          # HTML tag name
    position    : int = -1                     # Position in parent (-1 for root)
```

## Design Rationale

The separation of `child_nodes` and `text_nodes` addresses several challenges:

1. **Type Safety**: Eliminates `Union` types that cause serialization issues
2. **Clear Semantics**: Explicitly distinguishes elements from text
3. **Position Tracking**: Maintains original order through position fields
4. **Clean Serialization**: Each list has a single, known type

## Properties

### `attrs`
- **Type**: `Dict[str, Optional[str]]`
- **Purpose**: Stores HTML attributes
- **Examples**: `{'class': 'container', 'id': 'main'}`
- **Note**: `None` values represent boolean attributes

### `child_nodes`
- **Type**: `List[Schema__Html_Node]`
- **Purpose**: Contains only element children
- **Ordering**: Use position field to maintain order with text nodes

### `text_nodes`
- **Type**: `List[Schema__Html_Node__Data]`
- **Purpose**: Contains only text content
- **Ordering**: Use position field for placement among elements

### `tag`
- **Type**: `str`
- **Purpose**: HTML element name
- **Examples**: `'div'`, `'p'`, `'span'`

### `position`
- **Type**: `int`
- **Default**: `-1` (for root nodes)
- **Purpose**: Maintains node order within parent
- **Range**: 0 to n-1 for n children

## Usage Examples

### Creating Element Nodes

```python
from osbot_utils.helpers.html.schemas.Schema__Html_Node import Schema__Html_Node
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data import Schema__Html_Node__Data

# Simple element
div_node = Schema__Html_Node(
    tag='div',
    attrs={'class': 'container'},
    child_nodes=[],
    text_nodes=[],
    position=0
)

# Element with text
p_node = Schema__Html_Node(
    tag='p',
    attrs={},
    text_nodes=[
        Schema__Html_Node__Data(data='Hello World', position=0)
    ],
    child_nodes=[],
    position=0
)
```

### Mixed Content Example

```python
# HTML: <p>Hello <strong>World</strong>!</p>

# Create text nodes
text1 = Schema__Html_Node__Data(data='Hello ', position=0)
text2 = Schema__Html_Node__Data(data='!', position=2)

# Create strong element
strong_text = Schema__Html_Node__Data(data='World', position=0)
strong_node = Schema__Html_Node(
    tag='strong',
    text_nodes=[strong_text],
    child_nodes=[],
    position=1
)

# Create paragraph with mixed content
p_node = Schema__Html_Node(
    tag='p',
    text_nodes=[text1, text2],
    child_nodes=[strong_node],
    position=0
)
```

### Nested Structure

```python
# Create nested structure: <div><ul><li>Item</li></ul></div>

# List item
li_text = Schema__Html_Node__Data(data='Item', position=0)
li_node = Schema__Html_Node(
    tag='li',
    text_nodes=[li_text],
    child_nodes=[],
    position=0
)

# Unordered list
ul_node = Schema__Html_Node(
    tag='ul',
    child_nodes=[li_node],
    text_nodes=[],
    position=0
)

# Container div
div_node = Schema__Html_Node(
    tag='div',
    child_nodes=[ul_node],
    text_nodes=[],
    position=-1  # Root node
)
```

## Position Management

### Understanding Positions

Positions are relative to the parent node and include both text and element children:

```python
# HTML: <div>A<p>B</p>C<span>D</span>E</div>
# Positions: A=0, p=1, C=2, span=3, E=4

div_node = Schema__Html_Node(
    tag='div',
    text_nodes=[
        Schema__Html_Node__Data(data='A', position=0),
        Schema__Html_Node__Data(data='C', position=2),
        Schema__Html_Node__Data(data='E', position=4)
    ],
    child_nodes=[
        Schema__Html_Node(tag='p', position=1, ...),
        Schema__Html_Node(tag='span', position=3, ...)
    ]
)
```

### Reconstructing Order

```python
def get_ordered_content(node):
    """Get all children in position order."""
    all_content = []
    
    # Add text nodes
    for text in node.text_nodes:
        all_content.append((text.position, 'text', text))
    
    # Add child nodes
    for child in node.child_nodes:
        all_content.append((child.position, 'child', child))
    
    # Sort by position
    all_content.sort(key=lambda x: x[0])
    
    return all_content
```

## Serialization

### JSON Representation

```python
node = Schema__Html_Node(
    tag='div',
    attrs={'id': 'main'},
    position=0
)

json_data = node.json()
# {
#     "tag": "div",
#     "attrs": {"id": "main"},
#     "child_nodes": [],
#     "text_nodes": [],
#     "position": 0
# }

# Deserialize
restored = Schema__Html_Node.from_json(json_data)
```

### Deep Serialization

```python
# Complex structure serialization
root = create_complex_structure()
json_data = root.json()

# Save to file
with open('structure.json', 'w') as f:
    json.dump(json_data, f, indent=2)

# Load and restore
with open('structure.json', 'r') as f:
    data = json.load(f)
    restored = Schema__Html_Node.from_json(data)
```

## Common Operations

### Finding Nodes

```python
def find_by_tag(node, tag_name):
    """Find all nodes with specific tag."""
    results = []
    
    if node.tag == tag_name:
        results.append(node)
    
    for child in node.child_nodes:
        results.extend(find_by_tag(child, tag_name))
    
    return results
```

### Modifying Attributes

```python
def add_class(node, class_name):
    """Add a CSS class to the node."""
    current_class = node.attrs.get('class', '')
    if current_class:
        node.attrs['class'] = f"{current_class} {class_name}"
    else:
        node.attrs['class'] = class_name
```

### Extracting Text

```python
def get_text_content(node):
    """Extract all text content from node and children."""
    texts = []
    
    # Get direct text nodes in order
    ordered = get_ordered_content(node)
    
    for pos, type_, content in ordered:
        if type_ == 'text':
            texts.append(content.data)
        else:  # child node
            texts.append(get_text_content(content))
    
    return ''.join(texts)
```

## Validation

### Structure Validation

```python
def validate_node(node):
    """Validate node structure."""
    errors = []
    
    # Check required fields
    if not node.tag:
        errors.append("Missing tag name")
    
    # Check position conflicts
    positions = []
    for child in node.child_nodes:
        positions.append(('child', child.position))
    for text in node.text_nodes:
        positions.append(('text', text.position))
    
    # Check for duplicates
    position_values = [p[1] for p in positions]
    if len(position_values) != len(set(position_values)):
        errors.append("Duplicate positions found")
    
    # Validate children recursively
    for child in node.child_nodes:
        errors.extend(validate_node(child))
    
    return errors
```

### Position Normalization

```python
def normalize_positions(node):
    """Ensure positions are sequential from 0."""
    # Collect all children with positions
    all_children = []
    for child in node.child_nodes:
        all_children.append(('child', child.position, child))
    for text in node.text_nodes:
        all_children.append(('text', text.position, text))
    
    # Sort by current position
    all_children.sort(key=lambda x: x[1])
    
    # Reassign sequential positions
    for i, (type_, _, child) in enumerate(all_children):
        child.position = i
```

## Performance Considerations

1. **Memory Usage**: Each node stores references to children
2. **Deep Nesting**: Very deep structures may hit recursion limits
3. **Large Documents**: Consider streaming for very large HTML
4. **Position Lookups**: O(n) to find nodes by position

## Best Practices

1. **Always Set Positions**: Ensure all nodes have valid positions
2. **Validate Structure**: Check for position conflicts
3. **Use Type Hints**: Leverage type safety in your code
4. **Handle Deep Recursion**: Add depth limits for safety
5. **Cache Computed Values**: Cache expensive operations like text extraction

## Common Pitfalls

1. **Position Conflicts**: Multiple nodes with same position
2. **Missing Positions**: Forgetting to set positions
3. **Circular References**: Nodes referencing ancestors
4. **Type Mismatches**: Mixing node types incorrectly
5. **Mutation Issues**: Modifying shared node instances