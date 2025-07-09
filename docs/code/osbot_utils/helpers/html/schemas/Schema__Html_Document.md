# Schema__Html_Document

## Overview

`Schema__Html_Document` is the root schema class that represents a complete HTML document. It provides type-safe serialization and includes a timestamp for tracking document creation or modification time.

## Class Definition

```python
class Schema__Html_Document(Type_Safe):
    root_node : Schema__Html_Node
    timestamp : Timestamp_Now
```

## Inheritance

Inherits from `Type_Safe`, which provides:
- Type validation
- JSON serialization/deserialization
- Object introspection methods

## Properties

### `root_node`
- **Type**: `Schema__Html_Node`
- **Description**: The root element of the HTML document (typically the `<html>` tag)
- **Required**: Yes

### `timestamp`
- **Type**: `Timestamp_Now`
- **Description**: Automatically generated timestamp when the document is created
- **Default**: Current timestamp

## Methods

### Inherited from Type_Safe

#### `json() -> dict`
Serializes the document to a JSON-compatible dictionary.

```python
document = Schema__Html_Document(root_node=html_node)
json_data = document.json()
```

#### `from_json(json_data: dict) -> Schema__Html_Document`
Deserializes a document from JSON data.

```python
json_data = {'root_node': {...}, 'timestamp': '2024-01-01T00:00:00Z'}
document = Schema__Html_Document.from_json(json_data)
```

#### `obj() -> object`
Returns a simplified object representation.

```python
doc_obj = document.obj()
```

## Usage Examples

### Creating a Document

```python
from osbot_utils.helpers.html.schemas.Schema__Html_Document import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node import Schema__Html_Node

# Create root HTML node
root_node = Schema__Html_Node(
    tag='html',
    attrs={'lang': 'en'},
    child_nodes=[],
    text_nodes=[],
    position=-1
)

# Create document
document = Schema__Html_Document(root_node=root_node)
```

### Serialization and Persistence

```python
# Serialize to JSON
json_data = document.json()

# Save to file (hypothetical)
with open('document.json', 'w') as f:
    json.dump(json_data, f)

# Load and deserialize
with open('document.json', 'r') as f:
    loaded_data = json.load(f)
    
restored_document = Schema__Html_Document.from_json(loaded_data)
```

### Complete Roundtrip Example

```python
from osbot_utils.helpers.html.Html__To__Html_Dict import Html__To__Html_Dict
from osbot_utils.helpers.html.Html_Dict__To__Html_Document import Html_Dict__To__Html_Document

# Parse HTML to document
html = "<html><body><p>Hello World</p></body></html>"
html_dict = Html__To__Html_Dict(html).convert()
document = Html_Dict__To__Html_Document(html__dict=html_dict).convert()

# Serialize and restore
json_data = document.json()
restored = Schema__Html_Document.from_json(json_data)

# Verify
assert restored.json() == json_data
```

## JSON Structure

A serialized document has this structure:

```json
{
    "root_node": {
        "tag": "html",
        "attrs": {"lang": "en"},
        "child_nodes": [...],
        "text_nodes": [...],
        "position": -1
    },
    "timestamp": "2024-01-01T12:00:00.000000"
}
```

## Integration Points

### With Converters

1. **Created by**: `Html_Dict__To__Html_Document`
2. **Consumed by**: `Html_Document__To__Html_Dict`

### With Parser Pipeline

```
HTML String 
    → Html__To__Html_Dict 
    → Html_Dict__To__Html_Document 
    → Schema__Html_Document
```

## Design Considerations

1. **Timestamp**: Automatically captured for audit trails and caching
2. **Single Root**: Enforces valid HTML structure with one root element
3. **Type Safety**: Full type checking through Type_Safe base class
4. **Serialization**: Clean JSON format for storage and transmission

## Best Practices

1. **Root Node Position**: Always set root node position to -1
2. **Validation**: Ensure root node is properly structured before creating document
3. **Timestamp Usage**: Use timestamp for cache invalidation or versioning
4. **Error Handling**: Wrap deserialization in try-except for invalid JSON

## Common Patterns

### Document Creation from HTML

```python
def create_document_from_html(html_string):
    html_dict = Html__To__Html_Dict(html_string).convert()
    return Html_Dict__To__Html_Document(html__dict=html_dict).convert()
```

### Document Validation

```python
def is_valid_document(document):
    return (
        document.root_node is not None and
        document.root_node.tag == 'html' and
        document.timestamp is not None
    )
```

## Limitations

- No built-in HTML validation beyond structure
- Timestamp is not timezone-aware by default
- No versioning support built-in
- No compression for large documents