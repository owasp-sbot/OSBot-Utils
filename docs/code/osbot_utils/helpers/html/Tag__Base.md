# Tag__Base

## Overview

`Tag__Base` is the foundational class for all HTML tag representations in the object-oriented tag system. It provides core functionality for rendering, attribute management, and element hierarchy, serving as the base class for specific tag implementations.

## Class Definition

```python
class Tag__Base(Type_Safe):
    attributes               : dict
    elements                 : list
    end_tag                  : bool = True
    indent                   : int
    tag_name                 : str
    tag_classes              : list
    inner_html               : str
    new_line_before_elements : bool = True
```

## Key Features

- **Attribute Management**: Flexible attribute handling with special class support
- **Element Hierarchy**: Parent-child relationships with proper nesting
- **Rendering Engine**: Converts tag objects to HTML with formatting
- **Type Safety**: Inherits from Type_Safe for validation
- **Indentation Control**: Configurable indentation for readable output

## Properties

### `attributes`
- **Type**: `dict`
- **Purpose**: HTML attributes (id, style, data-*, etc.)
- **Example**: `{'id': 'main', 'data-value': '123'}`

### `elements`
- **Type**: `list`
- **Purpose**: Child elements (Tag__Base instances or Tag__Text)
- **Default**: `[]`

### `end_tag`
- **Type**: `bool`
- **Purpose**: Whether to render closing tag
- **Default**: `True` (False for void elements)

### `indent`
- **Type**: `int`
- **Purpose**: Indentation level for rendering
- **Default**: `0`

### `tag_name`
- **Type**: `str`
- **Purpose**: HTML element name
- **Example**: `'div'`, `'p'`, `'span'`

### `tag_classes`
- **Type**: `list`
- **Purpose**: CSS classes (merged into class attribute)
- **Example**: `['container', 'active']`

### `inner_html`
- **Type**: `str`
- **Purpose**: Direct HTML content (before child elements)
- **Default**: `''`

### `new_line_before_elements`
- **Type**: `bool`
- **Purpose**: Add newline before child elements
- **Default**: `True`

## Methods

### `append(*elements)`

Adds elements to the children list.

```python
div = Tag__Base(tag_name='div')
p1 = Tag__Base(tag_name='p', inner_html='First')
p2 = Tag__Base(tag_name='p', inner_html='Second')
div.append(p1, p2)
```

### `render() -> str`

Renders the tag and all children to HTML.

```python
div = Tag__Base(
    tag_name='div',
    attributes={'id': 'container'},
    tag_classes=['main', 'wide']
)
html = div.render()
# <div id="container" class="main wide"></div>
```

### `render_attributes() -> str`

Renders attributes including merged classes.

```python
tag = Tag__Base(
    attributes={'id': 'test'},
    tag_classes=['active', 'highlight']
)
attrs = tag.render_attributes()
# 'id="test" class="active highlight"'
```

### `render_element() -> str`

Core rendering logic with indentation and formatting.

### `render_elements() -> str`

Renders all child elements.

### `attributes_values(*attributes_names) -> dict`

Extracts specific attributes by name.

```python
link = Tag__Link(href='https://example.com', rel='stylesheet')
attrs = link.attributes_values('href', 'rel')
# {'href': 'https://example.com', 'rel': 'stylesheet'}
```

### `elements__by_tag_name() -> dict`

Groups child elements by tag name.

```python
div = Tag__Base(tag_name='div')
div.append(
    Tag__Base(tag_name='p'),
    Tag__Base(tag_name='p'),
    Tag__Base(tag_name='span')
)
grouped = div.elements__by_tag_name()
# {'p': [<p>, <p>], 'span': [<span>]}
```

### `elements__with_tag_name(tag_name) -> list`

Gets all child elements with specific tag.

```python
paragraphs = div.elements__with_tag_name('p')
# [<p>, <p>]
```

### `save(file_path) -> str`

Renders and saves to file.

```python
html = Tag__Html()
html.save('output.html')
```

## Usage Examples

### Creating Basic Elements

```python
# Simple div
div = Tag__Base(
    tag_name='div',
    attributes={'id': 'content'},
    inner_html='Hello World'
)

# Paragraph with classes
p = Tag__Base(
    tag_name='p',
    tag_classes=['text-large', 'intro'],
    inner_html='Welcome to our site'
)
```

### Building Hierarchies

```python
# Create structure
container = Tag__Base(tag_name='div', attributes={'class': 'container'})
header = Tag__Base(tag_name='header')
nav = Tag__Base(tag_name='nav')
ul = Tag__Base(tag_name='ul')

# Build hierarchy
container.append(header)
header.append(nav)
nav.append(ul)

# Add list items
for item in ['Home', 'About', 'Contact']:
    li = Tag__Base(tag_name='li')
    a = Tag__Base(
        tag_name='a',
        attributes={'href': f'#{item.lower()}'},
        inner_html=item
    )
    li.append(a)
    ul.append(li)
```

### Custom Tag Classes

```python
class Tag__Card(Tag__Base):
    def __init__(self, title='', content='', **kwargs):
        super().__init__(**kwargs)
        self.tag_name = 'div'
        self.tag_classes = ['card']
        
        # Add title
        if title:
            title_elem = Tag__Base(
                tag_name='h3',
                tag_classes=['card-title'],
                inner_html=title
            )
            self.append(title_elem)
        
        # Add content
        if content:
            content_elem = Tag__Base(
                tag_name='div',
                tag_classes=['card-content'],
                inner_html=content
            )
            self.append(content_elem)

# Use custom tag
card = Tag__Card(
    title='Welcome',
    content='This is a card component',
    attributes={'id': 'welcome-card'}
)
```

### Mixed Content Handling

```python
# Paragraph with mixed content
p = Tag__Base(tag_name='p')
p.inner_html = 'This is '

# Add strong element
strong = Tag__Base(
    tag_name='strong',
    inner_html='important'
)
p.append(strong)

# Add text node
text = Tag__Text(' information')
p.append(text)

# Renders: <p>This is <strong>important</strong> information</p>
```

## Rendering Details

### Indentation Rules

```python
# Set indent level
outer = Tag__Base(tag_name='div', indent=0)
inner = Tag__Base(tag_name='p', indent=1)
outer.append(inner)

# Renders with 4-space indentation:
# <div>
#     <p></p>
# </div>
```

### Formatting Control

```python
# Control newlines
div = Tag__Base(
    tag_name='div',
    new_line_before_elements=False
)
# Children render on same line as opening tag

# Self-closing tags
img = Tag__Base(
    tag_name='img',
    end_tag=False,
    attributes={'src': 'image.jpg'}
)
# Renders: <img src="image.jpg"/>
```

## Advanced Patterns

### Dynamic Attribute Building

```python
def build_data_attributes(data_dict):
    """Convert dict to data-* attributes."""
    attrs = {}
    for key, value in data_dict.items():
        attrs[f'data-{key}'] = str(value)
    return attrs

tag = Tag__Base(
    tag_name='div',
    attributes=build_data_attributes({
        'id': 123,
        'category': 'products',
        'active': True
    })
)
# <div data-id="123" data-category="products" data-active="True"></div>
```

### Conditional Rendering

```python
class ConditionalTag(Tag__Base):
    def __init__(self, condition=True, **kwargs):
        super().__init__(**kwargs)
        self.condition = condition
    
    def render(self):
        if self.condition:
            return super().render()
        return ''  # Don't render if condition is false

# Usage
tag = ConditionalTag(
    condition=user_is_admin,
    tag_name='div',
    inner_html='Admin panel'
)
```

### Template Integration

```python
class TemplateTag(Tag__Base):
    def __init__(self, template_vars=None, **kwargs):
        super().__init__(**kwargs)
        self.template_vars = template_vars or {}
    
    def render(self):
        # Replace template variables
        if self.inner_html and self.template_vars:
            for key, value in self.template_vars.items():
                self.inner_html = self.inner_html.replace(
                    f'{{{key}}}', str(value)
                )
        return super().render()

# Usage
welcome = TemplateTag(
    tag_name='h1',
    inner_html='Welcome, {username}!',
    template_vars={'username': 'John'}
)
# Renders: <h1>Welcome, John!</h1>
```

## Performance Optimization

### Element Caching

```python
class CachedTag(Tag__Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._render_cache = None
        self._cache_valid = True
    
    def append(self, *elements):
        self._cache_valid = False
        return super().append(*elements)
    
    def render(self):
        if self._cache_valid and self._render_cache:
            return self._render_cache
        
        self._render_cache = super().render()
        self._cache_valid = True
        return self._render_cache
```

## Best Practices

1. **Use Specific Tag Classes**: Prefer Tag__Div over Tag__Base
2. **Set Meaningful IDs**: Use attributes for identification
3. **Manage Classes Properly**: Use tag_classes for CSS
4. **Control Indentation**: Set indent for readable output
5. **Handle Mixed Content**: Use inner_html for text before elements

## Common Pitfalls

1. **Circular References**: Don't create parent-child loops
2. **Attribute Conflicts**: tag_classes vs attributes['class']
3. **Memory Leaks**: Large element trees consume memory
4. **Rendering Order**: inner_html renders before elements
5. **Indentation Accumulation**: Reset indent when needed

## Integration with Schema System

```python
# Convert from schema to tags
def schema_to_tag(schema_node):
    tag = Tag__Base(
        tag_name=schema_node.tag,
        attributes=schema_node.attrs
    )
    
    # Add text content
    for text_node in sorted(schema_node.text_nodes, key=lambda x: x.position):
        if text_node.position == 0:
            tag.inner_html = text_node.data
        else:
            tag.append(Tag__Text(text_node.data))
    
    # Add child elements
    for child in schema_node.child_nodes:
        tag.append(schema_to_tag(child))
    
    return tag
```