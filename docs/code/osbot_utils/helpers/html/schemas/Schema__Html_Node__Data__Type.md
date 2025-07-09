# Schema__Html_Node__Data__Type

## Overview

`Schema__Html_Node__Data__Type` is an enumeration that identifies the type of data nodes in the HTML schema system. Currently, it supports only text nodes, but the design allows for future expansion to other data types.

## Class Definition

```python
from enum import Enum

class Schema__Html_Node__Data__Type(Enum):
    TEXT : str = 'text'
```

## Purpose

This enum serves to:
1. **Type Identification**: Clearly identify text nodes vs element nodes
2. **Serialization Support**: Provide consistent type values in JSON
3. **Type Safety**: Prevent invalid type assignments
4. **Future Extensibility**: Allow for additional node types if needed

## Enum Values

### `TEXT`
- **Value**: `'text'`
- **Purpose**: Identifies text content nodes
- **Usage**: Default and currently only supported type

## Usage Examples

### Basic Usage

```python
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data__Type import Schema__Html_Node__Data__Type

# Access enum value
text_type = Schema__Html_Node__Data__Type.TEXT
print(text_type.value)  # 'text'
print(text_type.name)   # 'TEXT'
```

### In Schema__Html_Node__Data

```python
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data import Schema__Html_Node__Data
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data__Type import Schema__Html_Node__Data__Type

# Create text node with explicit type
text_node = Schema__Html_Node__Data(
    data="Hello World",
    type=Schema__Html_Node__Data__Type.TEXT,
    position=0
)

# Check node type
if text_node.type == Schema__Html_Node__Data__Type.TEXT:
    print(f"Text content: {text_node.data}")
```

### Type Checking

```python
def process_node_data(node_data):
    """Process node data based on type."""
    if node_data.type == Schema__Html_Node__Data__Type.TEXT:
        # Handle text node
        return node_data.data.strip()
    else:
        # Future: Handle other types
        raise ValueError(f"Unknown node data type: {node_data.type}")
```

## Serialization

### JSON Representation

```python
# When serialized, the enum value is used
text_node = Schema__Html_Node__Data(
    data="Sample text",
    type=Schema__Html_Node__Data__Type.TEXT
)

json_data = text_node.json()
# {
#     "data": "Sample text",
#     "type": "TEXT",  # Note: Uses the string value
#     "position": 0
# }
```

### Deserialization

```python
# From JSON back to object
json_data = {
    "data": "Sample text",
    "type": "TEXT",
    "position": 0
}

# The enum is automatically reconstructed
restored_node = Schema__Html_Node__Data.from_json(json_data)
assert restored_node.type == Schema__Html_Node__Data__Type.TEXT
```

## Integration Points

### With Html__To__Html_Dict

```python
# The parser uses the string value for text nodes
STRING__SCHEMA_TEXT = 'TEXT'  # Matches enum name

# In parsed dictionary
{
    'type': 'TEXT',  # This matches Schema__Html_Node__Data__Type.TEXT.name
    'data': 'Text content'
}
```

### Type Discrimination

```python
def is_text_node(node_dict):
    """Check if dictionary represents a text node."""
    return node_dict.get('type') == Schema__Html_Node__Data__Type.TEXT.name

def is_element_node(node_dict):
    """Check if dictionary represents an element node."""
    return 'tag' in node_dict and node_dict.get('type') != Schema__Html_Node__Data__Type.TEXT.name
```

## Validation Patterns

### Enum Validation

```python
def validate_node_type(type_value):
    """Validate that type value is valid."""
    try:
        # Try to get enum by value
        for member in Schema__Html_Node__Data__Type:
            if member.value == type_value:
                return True
        return False
    except:
        return False

# Usage
assert validate_node_type('text') == True
assert validate_node_type('invalid') == False
```

### Type Conversion

```python
def string_to_node_type(type_string):
    """Convert string to node type enum."""
    if type_string == 'TEXT' or type_string == 'text':
        return Schema__Html_Node__Data__Type.TEXT
    
    raise ValueError(f"Invalid node type: {type_string}")
```

## Future Extensibility

The enum design allows for future node types:

```python
# Potential future additions (example only)
class Schema__Html_Node__Data__Type(Enum):
    TEXT    : str = 'text'
    COMMENT : str = 'comment'  # HTML comments
    CDATA   : str = 'cdata'    # CDATA sections
    PI      : str = 'pi'       # Processing instructions
```

## Best Practices

1. **Always Use Enum**: Don't hardcode type strings
2. **Type Checking**: Use enum for type comparisons
3. **Serialization**: Be aware of name vs value in JSON
4. **Future Proof**: Design code to handle potential new types
5. **Validation**: Validate types when deserializing

## Common Patterns

### Type Switching

```python
def render_node_data(node_data):
    """Render node data based on type."""
    type_handlers = {
        Schema__Html_Node__Data__Type.TEXT: lambda n: n.data
        # Future types would be added here
    }
    
    handler = type_handlers.get(node_data.type)
    if handler:
        return handler(node_data)
    else:
        raise ValueError(f"No handler for type: {node_data.type}")
```

### Type Guards

```python
from typing import TypeGuard

def is_text_node_data(node_data: any) -> TypeGuard[Schema__Html_Node__Data]:
    """Type guard for text node data."""
    return (
        hasattr(node_data, 'type') and
        node_data.type == Schema__Html_Node__Data__Type.TEXT
    )
```

### Factory Pattern

```python
class NodeDataFactory:
    @staticmethod
    def create(data_type: Schema__Html_Node__Data__Type, **kwargs):
        """Create node data based on type."""
        if data_type == Schema__Html_Node__Data__Type.TEXT:
            return Schema__Html_Node__Data(
                type=data_type,
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported type: {data_type}")

# Usage
text_node = NodeDataFactory.create(
    Schema__Html_Node__Data__Type.TEXT,
    data="Hello",
    position=0
)
```

## Testing

```python
def test_enum_values():
    """Test enum values and properties."""
    text_type = Schema__Html_Node__Data__Type.TEXT
    
    # Test value
    assert text_type.value == 'text'
    
    # Test name
    assert text_type.name == 'TEXT'
    
    # Test string representation
    assert str(text_type) == 'Schema__Html_Node__Data__Type.TEXT'
    
    # Test membership
    assert Schema__Html_Node__Data__Type.TEXT in Schema__Html_Node__Data__Type
    
    # Test iteration
    all_types = list(Schema__Html_Node__Data__Type)
    assert len(all_types) == 1
    assert all_types[0] == Schema__Html_Node__Data__Type.TEXT
```

## Performance Notes

1. **Enum Comparison**: Very fast (identity comparison)
2. **Value Access**: Constant time
3. **Memory**: Minimal overhead
4. **Serialization**: Slight overhead for enum reconstruction

## Limitations

1. **Single Type**: Currently only supports TEXT
2. **No Metadata**: Enum doesn't carry additional metadata
3. **String Values**: JSON serialization uses strings, not enum objects
4. **No Inheritance**: Enums can't be extended through inheritance