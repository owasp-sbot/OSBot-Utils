# Html__To__Html_Tag

## Overview

`Html__To__Html_Tag` provides a direct conversion path from HTML strings to tag objects. It combines HTML parsing and tag object creation into a single operation, streamlining the process of working with HTML in an object-oriented manner.

## Class Definition

```python
class Html__To__Html_Tag:
    def __init__(self, html):
        self.html_to_dict = Html__To__Html_Dict(html)

    def __enter__(self):
        return self.convert()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def convert(self):
        html_dict = self.html_to_dict.convert()
        html_tag = Html_Dict__To__Html_Tags(html_dict).convert()
        return html_tag
```

## Purpose

This class simplifies the two-step process:
1. HTML string → Dictionary (via `Html__To__Html_Dict`)
2. Dictionary → Tag objects (via `Html_Dict__To__Html_Tags`)

Into a single, convenient operation with context manager support.

## Methods

### `convert() -> Tag__Base`

Performs the complete conversion from HTML to tag objects.

```python
converter = Html__To__Html_Tag(html)
root_tag = converter.convert()
```

### Context Manager Methods

Supports Python's context manager protocol:

```python
with Html__To__Html_Tag(html) as tag:
    # Work with tag
    tag.attributes['id'] = 'modified'
    print(tag.render())
```

## Usage Examples

### Basic Conversion

```python
from osbot_utils.helpers.html.Html__To__Html_Tag import Html__To__Html_Tag

html = "<div class='container'><h1>Title</h1><p>Content</p></div>"

# Direct conversion
converter = Html__To__Html_Tag(html)
root_tag = converter.convert()

# Access tag properties
print(root_tag.tag_name)  # 'div'
print(root_tag.attributes['class'])  # 'container'
print(len(root_tag.elements))  # 2
```

### Using Context Manager

```python
html = """
<html lang="en">
    <head>
        <title>My Page</title>
    </head>
    <body>
        <h1>Welcome</h1>
    </body>
</html>
"""

with Html__To__Html_Tag(html) as html_tag:
    # Modify the structure
    html_tag.head.title = "Updated Title"
    
    # Add new elements
    new_p = Tag__Base(tag_name='p', inner_html='New paragraph')
    html_tag.body.append(new_p)
    
    # Render modified HTML
    modified_html = html_tag.render()
```

### Quick HTML Manipulation

```python
def add_bootstrap_to_html(html_string):
    """Add Bootstrap CSS to any HTML."""
    with Html__To__Html_Tag(html_string) as tag:
        if isinstance(tag, Tag__Html):
            tag.head.add_css_bootstrap()
        return tag.render()
    return html_string  # Return original if not valid HTML

# Usage
original_html = "<html><head><title>Plain</title></head><body>Content</body></html>"
bootstrap_html = add_bootstrap_to_html(original_html)
```

## Integration Patterns

### HTML Transformation Pipeline

```python
class HtmlTransformer:
    def __init__(self, html):
        self.original_html = html
        self.tag = None
    
    def load(self):
        """Load HTML into tag structure."""
        with Html__To__Html_Tag(self.original_html) as tag:
            self.tag = tag
        return self
    
    def transform(self, transformation_func):
        """Apply transformation function to tag."""
        if self.tag:
            transformation_func(self.tag)
        return self
    
    def render(self):
        """Render transformed HTML."""
        return self.tag.render() if self.tag else self.original_html

# Usage
transformer = HtmlTransformer(html)
result = (transformer
    .load()
    .transform(lambda tag: tag.attributes.update({'data-processed': 'true'}))
    .transform(add_timestamps)
    .transform(optimize_images)
    .render()
)
```

### Batch Processing

```python
def process_html_files(file_paths, processor_func):
    """Process multiple HTML files."""
    results = []
    
    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        try:
            with Html__To__Html_Tag(html) as tag:
                processor_func(tag)
                processed_html = tag.render()
                
                results.append({
                    'path': path,
                    'success': True,
                    'html': processed_html
                })
        except Exception as e:
            results.append({
                'path': path,
                'success': False,
                'error': str(e)
            })
    
    return results
```

### Validation and Conversion

```python
def validate_and_fix_html(html_string):
    """Validate HTML and fix common issues."""
    issues = []
    
    with Html__To__Html_Tag(html_string) as tag:
        # Check if it's a complete HTML document
        if not isinstance(tag, Tag__Html):
            # Wrap in HTML structure
            html_tag = Tag__Html()
            html_tag.body.append(tag)
            tag = html_tag
            issues.append("Wrapped content in HTML structure")
        
        # Check for missing elements
        if not tag.head.title:
            tag.head.title = "Untitled"
            issues.append("Added missing title")
        
        # Check for lang attribute
        if not tag.lang:
            tag.lang = "en"
            issues.append("Added lang attribute")
        
        return tag.render(), issues
```

## Advanced Usage

### Custom Tag Processing

```python
class HtmlProcessor:
    def __init__(self):
        self.processors = {}
    
    def register_processor(self, tag_name, processor_func):
        """Register a processor for specific tag type."""
        self.processors[tag_name] = processor_func
    
    def process_html(self, html_string):
        """Process HTML with registered processors."""
        with Html__To__Html_Tag(html_string) as root_tag:
            self._process_tag(root_tag)
            return root_tag.render()
    
    def _process_tag(self, tag):
        """Recursively process tags."""
        # Apply processor if registered
        if tag.tag_name in self.processors:
            self.processors[tag.tag_name](tag)
        
        # Process children
        if hasattr(tag, 'elements'):
            for child in tag.elements:
                if hasattr(child, 'tag_name'):
                    self._process_tag(child)

# Usage
processor = HtmlProcessor()
processor.register_processor('img', lambda tag: tag.attributes.setdefault('loading', 'lazy'))
processor.register_processor('a', lambda tag: tag.attributes.setdefault('rel', 'noopener'))

processed_html = processor.process_html(original_html)
```

### Memory-Efficient Processing

```python
def stream_process_html(html_string, chunk_processor):
    """Process HTML in chunks (conceptual)."""
    # Note: Full HTML parsing requires complete document
    # This shows the pattern for memory-conscious processing
    
    with Html__To__Html_Tag(html_string) as tag:
        # Process top-level elements one at a time
        if hasattr(tag, 'elements'):
            for i, element in enumerate(tag.elements):
                # Process element
                chunk_processor(element)
                
                # Clear processed elements to free memory
                if i > 0:
                    tag.elements[i-1] = None
        
        return tag.render()
```

## Error Handling

### Safe Conversion

```python
def safe_html_to_tag(html_string, default_tag=None):
    """Safely convert HTML with fallback."""
    try:
        converter = Html__To__Html_Tag(html_string)
        return converter.convert()
    except Exception as e:
        print(f"Conversion failed: {e}")
        
        if default_tag:
            return default_tag
        
        # Return error message as tag
        error_tag = Tag__Div()
        error_tag.tag_classes = ['error']
        error_tag.inner_html = f"Failed to parse HTML: {str(e)}"
        return error_tag
```

### Detailed Error Reporting

```python
class HtmlConversionResult:
    def __init__(self, html_string):
        self.html_string = html_string
        self.tag = None
        self.errors = []
        self.warnings = []
        self.success = False
    
    def convert(self):
        """Attempt conversion with detailed reporting."""
        try:
            with Html__To__Html_Tag(self.html_string) as tag:
                self.tag = tag
                self.success = True
                self._validate_tag()
        except Exception as e:
            self.errors.append(f"Conversion error: {str(e)}")
        
        return self
    
    def _validate_tag(self):
        """Validate converted tag structure."""
        if not self.tag:
            return
        
        # Add validation warnings
        if hasattr(self.tag, 'tag_name'):
            if self.tag.tag_name != 'html':
                self.warnings.append("Root element is not <html>")
```

## Performance Considerations

```python
import time

class PerformanceMonitor:
    def __init__(self):
        self.timings = []
    
    def convert_with_timing(self, html_string):
        """Convert HTML and track timing."""
        start_time = time.time()
        
        with Html__To__Html_Tag(html_string) as tag:
            parse_time = time.time() - start_time
            
            render_start = time.time()
            rendered = tag.render()
            render_time = time.time() - render_start
        
        self.timings.append({
            'parse_time': parse_time,
            'render_time': render_time,
            'total_time': parse_time + render_time,
            'html_size': len(html_string),
            'rendered_size': len(rendered)
        })
        
        return tag
    
    def get_average_timing(self):
        """Get average conversion timing."""
        if not self.timings:
            return None
        
        avg_parse = sum(t['parse_time'] for t in self.timings) / len(self.timings)
        avg_render = sum(t['render_time'] for t in self.timings) / len(self.timings)
        
        return {
            'avg_parse_time': avg_parse,
            'avg_render_time': avg_render,
            'samples': len(self.timings)
        }
```

## Testing Utilities

```python
def create_test_html(title="Test", body_content="Test content"):
    """Create test HTML quickly."""
    html = f"""
    <html lang="en">
        <head>
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            <p>{body_content}</p>
        </body>
    </html>
    """
    
    with Html__To__Html_Tag(html) as tag:
        return tag

def assert_valid_conversion(html_string):
    """Assert HTML converts successfully."""
    with Html__To__Html_Tag(html_string) as tag:
        assert tag is not None, "Conversion returned None"
        assert hasattr(tag, 'tag_name'), "Result missing tag_name"
        assert hasattr(tag, 'render'), "Result missing render method"
        
        # Try rendering
        rendered = tag.render()
        assert rendered, "Rendered HTML is empty"
        
    return tag
```

## Best Practices

1. **Use Context Manager**: Leverage the with statement for clean code
2. **Check Tag Types**: Verify expected tag types after conversion
3. **Handle Errors**: Always wrap conversions in try-except
4. **Validate Results**: Check converted tags before using
5. **Memory Awareness**: Large HTML documents create many objects

## Common Patterns

### Adding Metadata

```python
def add_metadata_to_html(html_string, metadata):
    """Add metadata to HTML head."""
    with Html__To__Html_Tag(html_string) as tag:
        if isinstance(tag, Tag__Html):
            for name, content in metadata.items():
                meta = Tag__Base(
                    tag_name='meta',
                    attributes={'name': name, 'content': content},
                    end_tag=False
                )
                tag.head.elements.append(meta)
        
        return tag.render()
```

### Extracting Information

```python
def extract_links_from_html(html_string):
    """Extract all links from HTML."""
    links = []
    
    def extract_from_tag(tag):
        if tag.tag_name == 'a' and 'href' in tag.attributes:
            links.append({
                'href': tag.attributes['href'],
                'text': tag.inner_html,
                'attributes': tag.attributes
            })
        
        for child in getattr(tag, 'elements', []):
            if hasattr(child, 'tag_name'):
                extract_from_tag(child)
    
    with Html__To__Html_Tag(html_string) as tag:
        extract_from_tag(tag)
    
    return links
```

## Limitations

1. **Memory Usage**: Creates full object tree in memory
2. **No Streaming**: Requires complete HTML document
3. **Parse Errors**: Malformed HTML may fail to convert
4. **Performance**: Object creation adds overhead
5. **Tag Types**: Limited to available tag classes