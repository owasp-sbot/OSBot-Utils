# Html__Query Usage Guide

## 🎯 Purpose

`Html__Query` provides a **high-level, type-safe interface** for querying and analyzing HTML documents without using regex or string manipulation.

## 📦 Import

```python
from osbot_utils.helpers.html.utils.Html__Query import Html__Query
```

## 🔧 Basic Usage

### Context Manager Pattern (Recommended)

```python
html = "<html><head><title>Test</title></head><body><div id='main'>Content</div></body></html>"

with Html__Query(html=html) as query:
    title = query.title                    # "Test"
    main_div = query.find_by_id('main')   # Schema__Html_Node object
    text = query.get_text(main_div)       # "Content"
```

## 📊 Core Properties

### Document Structure

```python
with Html__Query(html=html) as query:
    query.root     # Root HTML node (Schema__Html_Node)
    query.head     # Head node or None
    query.body     # Body node or None
    query.title    # Page title text or None
```

### Link Elements

```python
with Html__Query(html=html) as query:
    query.links       # List of link attribute dicts
    query.link_hrefs  # List of href strings
    query.css_links   # List of stylesheet hrefs
    query.favicon     # Favicon URL or None
```

### Script Elements

```python
with Html__Query(html=html) as query:
    query.script_sources  # External script URLs
    query.inline_scripts  # Inline script contents
```

### Meta Tags

```python
with Html__Query(html=html) as query:
    query.meta_tags  # List of meta tag attribute dicts
```

## 🔍 Query Methods

### Check Element Existence

```python
# Check for links
query.has_link(href='/css/main.css')                    # Returns bool
query.has_link(rel='stylesheet')                        # Returns bool
query.has_link(href='/css/main.css', rel='stylesheet')  # Multiple conditions

# Check for scripts
query.has_script(src='/js/app.js')          # External script
query.has_script(contains='SwaggerUIBundle') # Inline script content

# Check for meta tags
query.has_meta(name='description')
query.has_meta(name='viewport', content='width=device-width')
```

### Find Elements

```python
# By ID
element = query.find_by_id('swagger-ui')  # Returns Schema__Html_Node or None

# By class
elements = query.find_by_class('container')  # Returns list of nodes

# By tag name
divs = query.find_by_tag('div')  # Returns list of all div nodes
```

### Extract Content

```python
# Get text from element
text = query.get_text()           # All document text
text = query.get_text(element)    # Text from specific element

# Get attributes
value = query.get_attribute(element, 'class')  # Returns attribute value or None
```

## 🧪 Testing Patterns

### FastAPI Documentation Testing

```python
def test_swagger_ui_setup(self):
    response = client.get('/docs')
    
    with Html__Query(html=response.text) as query:
        # Check page setup
        assert query.title == 'API - Swagger UI'
        
        # Verify resources
        assert query.has_link(href='/static/swagger-ui.css', rel='stylesheet')
        assert query.has_script(src='/static/swagger-ui-bundle.js')
        
        # Check configuration
        assert any('SwaggerUIBundle' in s for s in query.inline_scripts)
        
        # Verify structure
        swagger_div = query.find_by_id('swagger-ui')
        assert swagger_div is not None
```

### Form Validation Testing

```python
def test_login_form(self):
    with Html__Query(html=login_page_html) as query:
        # Find form elements
        username_input = query.find_by_id('username')
        password_input = query.find_by_id('password')
        submit_button = query.find_by_id('submit')
        
        # Verify attributes
        assert query.get_attribute(username_input, 'type') == 'text'
        assert query.get_attribute(password_input, 'type') == 'password'
        assert query.get_attribute(submit_button, 'type') == 'submit'
```

### CSS/JS Resource Testing

```python
def test_page_resources(self):
    with Html__Query(html=page_html) as query:
        # Check CSS files
        assert '/css/bootstrap.min.css' in query.css_links
        assert '/css/custom.css' in query.css_links
        
        # Check JavaScript files
        assert '/js/jquery.min.js' in query.script_sources
        assert '/js/app.js' in query.script_sources
        
        # Check favicon
        assert query.favicon == '/favicon.ico'
```

## 🏗️ Advanced Patterns

### Custom Traversal

```python
with Html__Query(html=html) as query:
    # Find all elements
    all_nodes = query.find_all()
    
    # Find by custom attribute
    node = query.find_by_attribute('data-testid', 'main-content')
    
    # Get all children of a node
    body = query.body
    for child in body.child_nodes:
        print(f"Tag: {child.tag}, ID: {child.attrs.get('id')}")
```

### Text Extraction

```python
with Html__Query(html=html) as query:
    # Extract all text from specific sections
    content_div = query.find_by_id('content')
    content_text = query.get_text_content(content_div)
    
    # Get text from multiple elements
    paragraphs = query.find_by_tag('p')
    texts = [query.get_text(p) for p in paragraphs]
```

### Nested Queries

```python
with Html__Query(html=html) as query:
    # Find container, then search within it
    container = query.find_by_class('container')[0]
    
    # Search within specific node
    headers = query.find_all_by_tag('h2', container)
    links = query.find_all_by_tag('a', container)
```

## 🔄 Data Access Patterns

### Direct Node Access

```python
with Html__Query(html=html) as query:
    node = query.find_by_id('main')
    
    # Access node properties
    node.tag          # 'div'
    node.attrs        # {'id': 'main', 'class': 'container'}
    node.child_nodes  # List of child Schema__Html_Node
    node.text_nodes   # List of Schema__Html_Node__Data
    node.position     # Position in parent
```

### Working with Attributes

```python
with Html__Query(html=html) as query:
    links = query.find_by_tag('a')
    
    for link in links:
        href = link.attrs.get('href', '')
        target = link.attrs.get('target', '_self')
        classes = link.attrs.get('class', '').split()
```

## ⚡ Performance Tips

1. **Use context manager** to ensure proper cleanup
2. **Cache query results** when checking multiple conditions
3. **Use specific queries** (find_by_id) over general ones (find_all)
4. **Avoid repeated parsing** - parse once, query many times

## 🚫 Common Pitfalls

```python
# ❌ Don't parse HTML multiple times
for element_id in element_ids:
    with Html__Query(html=html) as query:  # Parsing repeatedly
        element = query.find_by_id(element_id)

# ✅ Parse once, query multiple times
with Html__Query(html=html) as query:
    for element_id in element_ids:
        element = query.find_by_id(element_id)

# ❌ Don't use string methods on query results
element = query.find_by_id('main')
if 'container' in str(element):  # Wrong approach

# ✅ Use proper attribute access
element = query.find_by_id('main')
if 'container' in element.attrs.get('class', ''):
```

## 🔗 Related Classes

- `Html__To__Html_Document`: Lower-level parsing
- `Schema__Html_Node`: Node representation
- `Html__Query__Fast_API`: FastAPI-specific extensions