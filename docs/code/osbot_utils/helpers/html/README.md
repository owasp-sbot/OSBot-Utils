# OSBot_Utils HTML Parser Documentation

## Overview

The OSBot_Utils HTML parser provides a robust system for parsing, manipulating, and serializing HTML documents. It features a type-safe schema system that enables reliable roundtrip conversion between HTML strings and Python objects, with full support for mixed content, attributes preservation, and complex nested structures.

## Key Features

- **Full HTML Parsing**: Converts HTML strings to dictionary representations
- **Type-Safe Schema**: Structured data models with serialization support
- **Roundtrip Conversion**: HTML → Dict → Schema → Dict → HTML with perfect fidelity
- **Mixed Content Support**: Handles intermixed text and element nodes
- **Position Tracking**: Maintains element order through explicit positioning
- **CSS Support**: Includes CSS dictionary to string conversion
- **Tag Classes**: Object-oriented representation of HTML elements

## Architecture

```
HTML String
    ↓
Html__To__Html_Dict (Parser)
    ↓
Dictionary Representation
    ↓
Html_Dict__To__Html_Document (Converter)
    ↓
Schema Objects (Type-Safe)
    ↓
Html_Document__To__Html_Dict (Converter)
    ↓
Dictionary Representation
    ↓
Html_Dict__To__Html (Renderer)
    ↓
HTML String
```

## Core Components

### Parsers and Converters

- [Html__To__Html_Dict](Html__To__Html_Dict.md) - Parses HTML strings to dictionary format
- [Html_Dict__To__Html](Html_Dict__To__Html.md) - Converts dictionaries back to HTML strings
- [Html_Dict__To__Html_Document](Html_Dict__To__Html_Document.md) - Converts dictionaries to schema objects
- [Html_Document__To__Html_Dict](Html_Document__To__Html_Dict.md) - Converts schema objects back to dictionaries
- [Html__To__Html_Document](Html__To__Html_Document.md) - Direct HTML to schema document conversion
- [Html_Dict__To__Html_Tags](Html_Dict__To__Html_Tags.md) - Converts dictionaries to tag objects
- [Html__To__Html_Tag](Html__To__Html_Tag.md) - Direct HTML to tag object conversion

### Schema Classes

- [Schema__Html_Document](Schema__Html_Document.md) - Root document schema with timestamp
- [Schema__Html_Node](Schema__Html_Node.md) - Element node representation
- [Schema__Html_Node__Data](Schema__Html_Node__Data.md) - Text node representation
- [Schema__Html_Node__Data__Type](Schema__Html_Node__Data__Type.md) - Enumeration for node types

### Tag Classes

- [Tag__Base](Tag__Base.md) - Base class for all HTML tags
- [Tag__Html](Tag__Html.md) - HTML root element
- [Tag__Head](Tag__Head.md) - Head element with metadata support
- [Tag__Body](Tag__Body.md) - Body element
- [Tag__Div](Tag__Div.md) - Div element
- [Tag__Link](Tag__Link.md) - Link element for stylesheets
- [Tag__Style](Tag__Style.md) - Style element with CSS support
- [Tag__Text](Tag__Text.md) - Text node representation
- [Tag__H](Tag__H.md) - Heading elements (h1-h6)
- [Tag__HR](Tag__HR.md) - Horizontal rule element

### CSS Support

- [CSS_Dict__To__Css](CSS_Dict__To__Css.md) - Converts CSS dictionaries to string format

## Quick Start

### Basic HTML Parsing

```python
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict import Html__To__Html_Dict

html = "<div><p>Hello World</p></div>"
parser = Html__To__Html_Dict(html)
html_dict = parser.convert()
```

### Full Roundtrip Conversion

```python
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict import Html__To__Html_Dict
from osbot_utils.helpers.html.transformers.Html_Dict__To__Html_Document import Html_Dict__To__Html_Document
from osbot_utils.helpers.html.transformers.Html_Document__To__Html_Dict import Html_Document__To__Html_Dict
from osbot_utils.helpers.html.transformers.Html_Dict__To__Html import Html_Dict__To__Html

# Parse HTML to dictionary
html_dict = Html__To__Html_Dict(html).convert()

# Convert to type-safe schema
document = Html_Dict__To__Html_Document(html__dict=html_dict).convert()

# Serialize and deserialize
json_data = document.json()
restored = Schema__Html_Document.from_json(json_data)

# Convert back to HTML
dict_back = Html_Document__To__Html_Dict(html__document=restored).convert()
html_back = Html_Dict__To__Html(dict_back).convert()
```

### Creating HTML with Tag Classes

```python
from osbot_utils.helpers.html.tags.Tag__Html import Tag__Html
from osbot_utils.helpers.html.tags.Tag__Div import Tag__Div

html = Tag__Html()
html.head.title = "My Page"
div = Tag__Div()
div.inner_html = "Hello World"
html.body.append(div)

rendered_html = html.render()
```

## Dictionary Format

The dictionary representation uses this structure:

```python
{
    'tag': 'element_name',
    'attrs': {'attribute': 'value'},
    'nodes': [
        {'type': 'TEXT', 'data': 'text content'},
        {'tag': 'child', 'attrs': {}, 'nodes': []}
    ]
}
```

## Schema Format

The schema format separates text and element nodes:

```python
Schema__Html_Node(
    tag='div',
    attrs={'class': 'container'},
    child_nodes=[...],  # Element nodes only
    text_nodes=[...],   # Text nodes only
    position=0          # Position in parent
)
```

## Design Decisions

1. **Position-Based Ordering**: Uses explicit position fields to maintain node order during serialization
2. **Separated Node Types**: Avoids Union type issues by separating text and element nodes
3. **Type Safety**: Full type annotations and Type_Safe base class for reliable serialization
4. **Attribute Preservation**: Maintains attribute order and all values through roundtrip
5. **Mixed Content Handling**: Special handling for elements containing both text and child elements

## Common Use Cases

- HTML parsing and manipulation
- Web scraping with structure preservation
- HTML generation from data
- Template processing
- HTML validation and cleanup
- Converting between HTML and structured data formats

## Testing

The library includes comprehensive tests for:
- Basic HTML parsing
- Complex nested structures
- Mixed content handling
- Attribute preservation
- Roundtrip fidelity
- Edge cases (empty elements, self-closing tags, etc.)

## Contributing

When contributing to the HTML parser:
1. Maintain backward compatibility
2. Add tests for new features
3. Follow the existing code style
4. Update documentation
5. Ensure roundtrip tests pass