# Html_Document__To__Html_Dict

## Overview

`Html_Document__To__Html_Dict` reverses the schema conversion process, transforming type-safe `Schema__Html_Document` objects back into dictionary representations. This enables the complete roundtrip from HTML to schema and back to HTML.

## Class Definition

```python
class Html_Document__To__Html_Dict(Type_Safe):
    html__document : Schema__Html_Document = None
    html__dict     : dict                  = None
```

## Purpose

This converter is essential for:
1. **Completing the Roundtrip**: Schema → Dict → HTML
2. **Position Merging**: Reconstructs mixed content using positions
3. **Format Compatibility**: Outputs the same format as `Html__To__Html_Dict`
4. **Serialization Bridge**: Converts from type-safe to parseable format

## Methods

### `convert() -> dict`

Main method that converts a schema document back to dictionary format.

```python
converter = Html_Document__To__Html_Dict(html__document=document)
html_dict = converter.convert()
```

### `node_to_dict(node: Schema__Html_Node) -> Dict[str, Any]`

Recursively converts schema nodes to dictionary format, handling:
- Merging child_nodes and text_nodes by position
- Recreating the mixed content structure
- Converting attributes back to dict format

## Conversion Process

### 1. Input Schema Format
```python
Schema__Html_Node(
    tag='div',
    attrs={'class': 'container'},
    child_nodes=[
        Schema__Html_Node(tag='p', position=1, ...)
    ],
    text_nodes=[
        Schema__Html_Node__Data(data='Before', position=0),
        Schema__Html_Node__Data(data='After', position=2)
    ]
)
```

### 2. Position-Based Merging
The converter:
1. Collects all nodes with their positions
2. Sorts by position
3. Rebuilds the original mixed array

### 3. Output Dictionary Format
```python
{
    'tag': 'div',
    'attrs': {'class': 'container'},
    'nodes': [
        {'type': 'TEXT', 'data': 'Before'},
        {'tag': 'p', 'attrs': {}, 'nodes': [...]},
        {'type': 'TEXT', 'data': 'After'}
    ]
}
```

## Usage Examples

### Basic Conversion

```python
from osbot_utils.helpers.html.schemas.Schema__Html_Document import Schema__Html_Document
from osbot_utils.helpers.html.Html_Document__To__Html_Dict import Html_Document__To__Html_Dict

# Assume we have a document
document = Schema__Html_Document.from_json(json_data)

# Convert back to dict
converter = Html_Document__To__Html_Dict(html__document=document)
html_dict = converter.convert()

# Now can render to HTML
html = Html_Dict__To__Html(html_dict).convert()
```

### Complete Roundtrip

```python
# Original HTML
original_html = "<div>Hello <strong>World</strong>!</div>"

# Parse to dict
dict1 = Html__To__Html_Dict(original_html).convert()

# Convert to document
document = Html_Dict__To__Html_Document(html__dict=dict1).convert()

# Convert back to dict
dict2 = Html_Document__To__Html_Dict(html__document=document).convert()

# Should be identical
assert dict1 == dict2

# Convert back to HTML
final_html = Html_Dict__To__Html(dict2).convert()
```

### Handling Complex Structures

```python
# Document with nested mixed content
document = create_complex_document()

# Convert maintaining structure
converter = Html_Document__To__Html_Dict(html__document=document)
html_dict = converter.convert()

# Verify structure preserved
def verify_mixed_content(node_dict):
    nodes = node_dict.get('nodes', [])
    for i, node in enumerate(nodes):
        if node.get('type') == 'TEXT':
            print(f"Position {i}: Text '{node['data']}'")
        else:
            print(f"Position {i}: Element <{node['tag']}>")
```

## Position Resolution Algorithm

```python
# The algorithm for merging nodes:
all_nodes = []

# Add child nodes with positions
for child in node.child_nodes:
    all_nodes.append((child.position, 'child', child))

# Add text nodes with positions  
for text in node.text_nodes:
    all_nodes.append((text.position, 'text', text))

# Sort by position
all_nodes.sort(key=lambda x: x[0])

# Build nodes array
nodes = []
for position, node_type, node_obj in all_nodes:
    if node_type == 'text':
        nodes.append({
            'type': 'TEXT',
            'data': node_obj.data
        })
    else:
        nodes.append(self.node_to_dict(node_obj))
```

## Error Handling

```python
def safe_convert(document):
    """Safely convert document to dict with error handling."""
    if not document:
        return None
        
    try:
        converter = Html_Document__To__Html_Dict(html__document=document)
        return converter.convert()
    except Exception as e:
        print(f"Conversion error: {e}")
        return None
```

## Integration Patterns

### With Modification Pipeline

```python
def modify_and_convert(document):
    """Modify document and convert back."""
    # Modify the document
    for node in document.root_node.child_nodes:
        if node.tag == 'p':
            node.attrs['class'] = 'modified'
    
    # Convert back to dict
    return Html_Document__To__Html_Dict(
        html__document=document
    ).convert()
```

### Validation After Conversion

```python
def validate_roundtrip(original_dict, document):
    """Ensure roundtrip maintains structure."""
    # Convert back
    converter = Html_Document__To__Html_Dict(html__document=document)
    result_dict = converter.convert()
    
    # Compare
    if original_dict != result_dict:
        # Find differences
        return find_dict_differences(original_dict, result_dict)
    
    return None  # Success
```

## Performance Optimization

### Batch Processing

```python
def batch_convert_documents(documents):
    """Convert multiple documents efficiently."""
    results = []
    
    for document in documents:
        converter = Html_Document__To__Html_Dict(html__document=document)
        results.append(converter.convert())
    
    return results
```

### Caching Conversion

```python
class CachedConverter:
    def __init__(self):
        self._cache = {}
    
    def convert(self, document):
        # Use document timestamp as cache key
        cache_key = f"{id(document)}_{document.timestamp}"
        
        if cache_key not in self._cache:
            converter = Html_Document__To__Html_Dict(
                html__document=document
            )
            self._cache[cache_key] = converter.convert()
        
        return self._cache[cache_key]
```

## Testing Patterns

```python
def test_position_preservation():
    """Test that positions correctly reconstruct order."""
    # Create test structure
    text1 = Schema__Html_Node__Data(data='A', position=0)
    elem = Schema__Html_Node(tag='b', position=1)
    text2 = Schema__Html_Node__Data(data='B', position=2)
    
    node = Schema__Html_Node(
        tag='div',
        text_nodes=[text1, text2],
        child_nodes=[elem]
    )
    
    # Convert
    result = node_to_dict(node)
    
    # Verify order
    assert result['nodes'][0]['data'] == 'A'
    assert result['nodes'][1]['tag'] == 'b'
    assert result['nodes'][2]['data'] == 'B'
```

## Common Issues and Solutions

### Missing Positions
```python
# Problem: Nodes without positions
# Solution: Assign positions during creation
def fix_positions(node):
    all_items = [(n, 'child') for n in node.child_nodes]
    all_items.extend([(n, 'text') for n in node.text_nodes])
    
    for i, (item, type_) in enumerate(all_items):
        if item.position == -1:  # Unset
            item.position = i
```

### Position Conflicts
```python
# Problem: Multiple nodes with same position
# Solution: Re-index positions
def reindex_positions(node):
    all_positions = []
    for child in node.child_nodes:
        all_positions.append((child.position, child, 'child'))
    for text in node.text_nodes:
        all_positions.append((text.position, text, 'text'))
    
    # Sort and reassign
    all_positions.sort(key=lambda x: x[0])
    for i, (_, item, _) in enumerate(all_positions):
        item.position = i
```

## Best Practices

1. **Verify Positions**: Always check position consistency
2. **Handle Empty Nodes**: Account for nodes without children
3. **Preserve Attributes**: Ensure all attributes are maintained
4. **Test Roundtrips**: Verify dict1 == dict2 after roundtrip
5. **Document Changes**: Track any modifications during conversion