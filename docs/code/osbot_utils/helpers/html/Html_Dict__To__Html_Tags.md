# Html_Dict__To__Html_Tags

## Overview

`Html_Dict__To__Html_Tags` converts dictionary representations of HTML into object-oriented tag instances. This converter bridges the gap between parsed HTML dictionaries and the tag-based rendering system, enabling programmatic HTML manipulation through tag objects.

## Class Definition

```python
class Html_Dict__To__Html_Tags:
    def __init__(self, root):
        self.root = root
```

## Purpose

This converter enables:
1. **Object-Oriented HTML**: Work with HTML as objects rather than dictionaries
2. **Type-Specific Tags**: Creates appropriate tag classes (Tag__Html, Tag__Head, etc.)
3. **Programmatic Manipulation**: Modify HTML structure through object methods
4. **Alternative Rendering**: Use tag system instead of direct dict-to-HTML conversion

## Methods

### `convert() -> Tag__Base`

Main conversion method that returns the root tag object.

```python
converter = Html_Dict__To__Html_Tags(html_dict)
root_tag = converter.convert()
```

### `convert_element(element: dict) -> Tag__Base`

Routes elements to appropriate conversion methods based on tag type.

### `convert_to__tag(target_tag, element, indent) -> Tag__Base`

Generic conversion for any tag type, handling:
- Attribute mapping
- Text content extraction
- Child element recursion
- Proper indentation

### `convert_to__tag__html(element) -> Tag__Html`

Specialized conversion for HTML root elements.

### `convert_to__tag__head(element, indent) -> Tag__Head`

Specialized conversion for head elements, handling:
- Title extraction
- Link elements
- Meta tags
- Style elements

### `convert_to__tag__link(element) -> Tag__Link`

Creates Tag__Link instances with proper attributes.

### `collect_inner_text(element) -> str`

Extracts all text content from text nodes within an element.

## Conversion Process

### 1. Dictionary Analysis
The converter analyzes the dictionary structure to determine:
- Tag type for specialized handling
- Presence of text nodes
- Child element structure

### 2. Tag Selection
```python
if tag_name == 'html':
    return self.convert_to__tag__html(element)
elif tag_name == 'head':
    return self.convert_to__tag__head(element, indent)
elif tag_name == 'link':
    return self.convert_to__tag__link(element)
else:
    return self.convert_to__tag(Tag__Base, element, indent)
```

### 3. Content Processing
- Text nodes are collected as inner_html
- Element nodes become child tags
- Attributes are preserved
- Indentation is calculated

## Usage Examples

### Basic Conversion

```python
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict import Html__To__Html_Dict
from osbot_utils.helpers.html.transformers.Html_Dict__To__Html_Tags import Html_Dict__To__Html_Tags

# Parse HTML to dict
html = "<div class='container'><p>Hello World</p></div>"
html_dict = Html__To__Html_Dict(html).convert()

# Convert to tags
converter = Html_Dict__To__Html_Tags(html_dict)
root_tag = converter.convert()

# Work with tag objects
print(root_tag.tag_name)  # 'div'
print(root_tag.attributes['class'])  # 'container'
print(len(root_tag.elements))  # 1
```

### Complex HTML Structure

```python
html = """
<html lang="en">
    <head>
        <title>My Page</title>
        <link rel="stylesheet" href="styles.css">
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Welcome</h1>
        <p>Content goes here</p>
    </body>
</html>
"""

# Convert to tags
html_dict = Html__To__Html_Dict(html).convert()
html_tag = Html_Dict__To__Html_Tags(html_dict).convert()

# Access structured elements
assert isinstance(html_tag, Tag__Html)
assert html_tag.lang == 'en'
assert html_tag.head.title == 'My Page'
assert len(html_tag.head.links) == 1
assert html_tag.head.links[0].href == 'styles.css'
```

### Modifying Structure

```python
# Convert HTML to tags
html_dict = Html__To__Html_Dict(html).convert()
root_tag = Html_Dict__To__Html_Tags(html_dict).convert()

# Modify through tag objects
if isinstance(root_tag, Tag__Html):
    # Add CSS to head
    root_tag.head.add_css_bootstrap()
    
    # Add new element to body
    new_div = Tag__Div()
    new_div.inner_html = "New content"
    new_div.tag_classes = ['alert', 'alert-info']
    root_tag.body.append(new_div)

# Render modified HTML
modified_html = root_tag.render()
```

## Special Tag Handling

### HTML Tag
```python
def convert_to__tag__html(self, element):
    attrs = element.get("attrs", {})
    lang = attrs.get("lang")
    
    tag_html = Tag__Html(
        attributes=attrs,
        lang=lang,
        doc_type=False  # DOCTYPE handled separately
    )
    
    # Process head and body
    for node in element.get('nodes', []):
        if node.get('tag') == 'head':
            tag_html.head = self.convert_to__tag__head(node, 1)
        elif node.get('tag') == 'body':
            tag_html.body = self.convert_to__tag(Tag__Body, node, 1)
```

### Head Tag
```python
def convert_to__tag__head(self, element, indent):
    tag_head = Tag__Head(indent=indent + 1)
    
    for node in element.get('nodes', []):
        tag_name = node.get('tag')
        
        if tag_name == 'title':
            tag_head.title = self.collect_inner_text(node)
        elif tag_name == 'link':
            tag_head.links.append(self.convert_to__tag__link(node))
        elif tag_name == 'meta':
            tag_head.elements.append(
                self.convert_to__tag(Tag__Base, node, indent + 1)
            )
```

## Mixed Content Handling

The converter handles mixed text and element content:

```python
# HTML: <p>Hello <strong>World</strong>!</p>
# Dict structure has mixed nodes

# Conversion process:
# 1. First text node becomes inner_html
# 2. Element nodes become children
# 3. Subsequent text nodes become Tag__Text elements
```

## Integration Patterns

### With HTML Parser Pipeline

```python
def html_to_tags(html_string):
    """Complete pipeline from HTML to tags."""
    # Parse HTML
    html_dict = Html__To__Html_Dict(html_string).convert()
    
    # Convert to tags
    return Html_Dict__To__Html_Tags(html_dict).convert()
```

### Tag Manipulation Utilities

```python
class TagManipulator:
    def __init__(self, html):
        self.root_tag = html_to_tags(html)
    
    def add_css_class(self, selector, class_name):
        """Add CSS class to elements matching selector."""
        elements = self.find_by_selector(selector)
        for elem in elements:
            if hasattr(elem, 'tag_classes'):
                elem.tag_classes.append(class_name)
    
    def set_attribute(self, selector, attr_name, attr_value):
        """Set attribute on matching elements."""
        elements = self.find_by_selector(selector)
        for elem in elements:
            elem.attributes[attr_name] = attr_value
    
    def render(self):
        """Render modified HTML."""
        return self.root_tag.render()
```

### Validation After Conversion

```python
def validate_tag_structure(root_tag):
    """Validate converted tag structure."""
    errors = []
    
    # Check HTML structure
    if isinstance(root_tag, Tag__Html):
        if not root_tag.head:
            errors.append("Missing head element")
        if not root_tag.body:
            errors.append("Missing body element")
    
    # Validate recursively
    def check_tag(tag, path=""):
        current_path = f"{path}/{tag.tag_name}"
        
        # Check for required attributes
        if tag.tag_name == 'img' and 'src' not in tag.attributes:
            errors.append(f"Missing src attribute at {current_path}")
        
        # Check children
        for child in tag.elements:
            if hasattr(child, 'tag_name'):
                check_tag(child, current_path)
    
    check_tag(root_tag)
    return errors
```

## Advanced Usage

### Custom Tag Creation

```python
def create_custom_tags(element_dict):
    """Create custom tag classes based on data attributes."""
    if element_dict.get('attrs', {}).get('data-component') == 'card':
        return Tag__Card(element_dict)
    elif element_dict.get('attrs', {}).get('data-component') == 'modal':
        return Tag__Modal(element_dict)
    else:
        return Html_Dict__To__Html_Tags(element_dict).convert()
```

### Performance Optimization

```python
class OptimizedTagConverter:
    def __init__(self):
        self.tag_cache = {}
    
    def convert_with_cache(self, element_dict):
        """Cache converted tags for reuse."""
        # Create cache key from element
        cache_key = self._create_cache_key(element_dict)
        
        if cache_key in self.tag_cache:
            return self.tag_cache[cache_key]
        
        # Convert and cache
        converter = Html_Dict__To__Html_Tags(element_dict)
        tag = converter.convert()
        self.tag_cache[cache_key] = tag
        
        return tag
```

## Error Handling

```python
def safe_convert_to_tags(element_dict):
    """Safely convert with error handling."""
    try:
        converter = Html_Dict__To__Html_Tags(element_dict)
        return converter.convert(), None
    except Exception as e:
        # Return a fallback tag with error info
        error_tag = Tag__Div()
        error_tag.tag_classes = ['conversion-error']
        error_tag.inner_html = f"Conversion error: {str(e)}"
        return error_tag, str(e)
```

## Testing Patterns

```python
def test_tag_conversion():
    """Test dictionary to tag conversion."""
    test_dict = {
        'tag': 'div',
        'attrs': {'id': 'test'},
        'nodes': [
            {'type': 'TEXT', 'data': 'Hello '},
            {'tag': 'span', 'attrs': {}, 'nodes': [
                {'type': 'TEXT', 'data': 'World'}
            ]}
        ]
    }
    
    converter = Html_Dict__To__Html_Tags(test_dict)
    tag = converter.convert()
    
    assert tag.tag_name == 'div'
    assert tag.attributes['id'] == 'test'
    assert tag.inner_html == 'Hello '
    assert len(tag.elements) == 1
    assert tag.elements[0].tag_name == 'span'
```

## Best Practices

1. **Check Tag Types**: Use isinstance() for specialized tags
2. **Preserve Structure**: Maintain the original HTML structure
3. **Handle Missing Elements**: Provide defaults for required elements
4. **Validate Results**: Check converted tags for completeness
5. **Memory Management**: Be aware of object creation overhead

## Limitations

1. **Memory Usage**: Tag objects use more memory than dicts
2. **Performance**: Object creation has overhead
3. **Circular References**: Avoid creating parent references
4. **Type Matching**: Not all HTML elements have specialized classes
5. **Mixed Content**: Complex mixed content may need special handling