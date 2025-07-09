# Html__To__Html_Document

## Overview

`Html__To__Html_Document` provides a direct conversion path from HTML strings to `Schema__Html_Document` objects. It combines the parsing and schema conversion steps into a single, convenient interface.

## Class Definition

```python
class Html__To__Html_Document(Type_Safe):
    html          : str
    html__dict    : dict
    html__document: Schema__Html_Document
```

## Purpose

This class simplifies the two-step process of:
1. Parsing HTML to dictionary (`Html__To__Html_Dict`)
2. Converting dictionary to schema (`Html_Dict__To__Html_Document`)

Into a single operation, making it easier to work with HTML content.

## Methods

### `convert() -> Schema__Html_Document`

Main method that performs the complete conversion from HTML to document schema.

```python
converter = Html__To__Html_Document(html="<div>Hello</div>")
document = converter.convert()
```

The method:
1. Parses HTML using `Html__To__Html_Dict`
2. Converts the resulting dictionary using `Html_Dict__To__Html_Document`
3. Returns the schema document or `None` on failure

## Usage Examples

### Basic Conversion

```python
from osbot_utils.helpers.html.Html__To__Html_Document import Html__To__Html_Document

html = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>My Page</title>
    </head>
    <body>
        <h1>Welcome</h1>
    </body>
</html>
"""

converter = Html__To__Html_Document(html=html)
document = converter.convert()

# Access the document structure
print(document.root_node.tag)  # 'html'
print(document.root_node.attrs['lang'])  # 'en'
print(document.timestamp)  # Current timestamp
```

### Error Handling

```python
def safe_parse_html(html_string):
    """Safely parse HTML with error handling."""
    if not html_string:
        return None
    
    try:
        converter = Html__To__Html_Document(html=html_string)
        return converter.convert()
    except Exception as e:
        print(f"Failed to parse HTML: {e}")
        return None
```

### With Context Manager

```python
# Using with statement for cleaner code
with Html__To__Html_Document(html=html_content) as converter:
    document = converter.convert()
    if document:
        process_document(document)
```

## Integration Patterns

### Direct to Serialization

```python
def html_to_json(html_string):
    """Convert HTML directly to JSON."""
    converter = Html__To__Html_Document(html=html_string)
    document = converter.convert()
    
    if document:
        return document.json()
    return None
```

### Batch Processing

```python
def process_html_files(file_paths):
    """Process multiple HTML files."""
    documents = []
    
    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        converter = Html__To__Html_Document(html=html)
        document = converter.convert()
        
        if document:
            documents.append({
                'path': path,
                'document': document,
                'timestamp': document.timestamp
            })
    
    return documents
```

### Validation Pipeline

```python
def validate_and_convert(html_string):
    """Validate HTML during conversion."""
    converter = Html__To__Html_Document(html=html_string)
    document = converter.convert()
    
    if not document:
        return None, ["Failed to parse HTML"]
    
    errors = []
    
    # Check for required elements
    if document.root_node.tag != 'html':
        errors.append("Missing <html> root element")
    
    # Check for head and body
    head_found = False
    body_found = False
    
    for child in document.root_node.child_nodes:
        if child.tag == 'head':
            head_found = True
        elif child.tag == 'body':
            body_found = True
    
    if not head_found:
        errors.append("Missing <head> element")
    if not body_found:
        errors.append("Missing <body> element")
    
    return document, errors
```

## Advanced Usage

### Custom Processing

```python
class HtmlProcessor:
    def __init__(self):
        self.processed_count = 0
    
    def process_html(self, html):
        """Process HTML with tracking."""
        converter = Html__To__Html_Document(html=html)
        document = converter.convert()
        
        if document:
            self.processed_count += 1
            # Perform custom processing
            self._add_metadata(document)
            self._validate_structure(document)
        
        return document
    
    def _add_metadata(self, document):
        """Add processing metadata."""
        document.root_node.attrs['data-processed'] = 'true'
        document.root_node.attrs['data-processor-version'] = '1.0'
    
    def _validate_structure(self, document):
        """Validate document structure."""
        # Custom validation logic
        pass
```

## Performance Considerations

### Memory Usage

```python
def estimate_memory_usage(html):
    """Estimate memory usage for conversion."""
    import sys
    
    # Parse and convert
    converter = Html__To__Html_Document(html=html)
    document = converter.convert()
    
    if document:
        # Estimate sizes
        html_size = sys.getsizeof(html)
        dict_size = sys.getsizeof(converter.html__dict)
        doc_size = sys.getsizeof(document)
        
        return {
            'html_size': html_size,
            'dict_size': dict_size,
            'document_size': doc_size,
            'overhead': doc_size - html_size
        }
```

### Streaming Large Files

```python
def process_large_html_file(file_path, chunk_size=1024*1024):
    """Process large HTML files in chunks."""
    # Note: This is conceptual - full HTML parsing requires complete document
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # For very large files, consider:
    # 1. Using a streaming HTML parser
    # 2. Processing sections independently
    # 3. Using memory-mapped files
    
    converter = Html__To__Html_Document(html=html_content)
    return converter.convert()
```

## Error Handling Patterns

### Graceful Degradation

```python
def convert_with_fallback(html, fallback_html="<html><body></body></html>"):
    """Convert with fallback on error."""
    try:
        converter = Html__To__Html_Document(html=html)
        document = converter.convert()
        
        if document:
            return document
    except Exception as e:
        print(f"Primary conversion failed: {e}")
    
    # Try fallback
    try:
        converter = Html__To__Html_Document(html=fallback_html)
        return converter.convert()
    except Exception as e:
        print(f"Fallback conversion failed: {e}")
        return None
```

### Detailed Error Reporting

```python
def convert_with_diagnostics(html):
    """Convert with detailed diagnostics."""
    diagnostics = {
        'success': False,
        'errors': [],
        'warnings': [],
        'document': None
    }
    
    try:
        converter = Html__To__Html_Document(html=html)
        
        # Check intermediate steps
        if not converter.html:
            diagnostics['errors'].append("Empty HTML input")
            return diagnostics
        
        document = converter.convert()
        
        if document:
            diagnostics['success'] = True
            diagnostics['document'] = document
            
            # Add warnings for common issues
            if not document.root_node.attrs.get('lang'):
                diagnostics['warnings'].append("Missing lang attribute on <html>")
        else:
            diagnostics['errors'].append("Conversion returned None")
    
    except Exception as e:
        diagnostics['errors'].append(f"Exception: {str(e)}")
    
    return diagnostics
```

## Testing Utilities

```python
def create_test_document(title="Test", body_content="Test content"):
    """Create a test document quickly."""
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>{title}</title>
        </head>
        <body>
            <p>{body_content}</p>
        </body>
    </html>
    """
    
    converter = Html__To__Html_Document(html=html)
    return converter.convert()

def assert_valid_document(html):
    """Assert that HTML produces valid document."""
    converter = Html__To__Html_Document(html=html)
    document = converter.convert()
    
    assert document is not None, "Failed to create document"
    assert document.root_node is not None, "Missing root node"
    assert document.timestamp is not None, "Missing timestamp"
    
    return document
```

## Best Practices

1. **Always Check Return**: The method returns `None` on failure
2. **Handle Malformed HTML**: Be prepared for parsing failures
3. **Validate Results**: Check document structure after conversion
4. **Use Type Hints**: Leverage type safety in your code
5. **Consider Memory**: Large HTML documents consume significant memory

## Common Issues

1. **Malformed HTML**: Parser may fail or produce unexpected structure
2. **Memory Limits**: Very large documents may cause memory issues
3. **Character Encoding**: Ensure proper encoding when reading files
4. **Missing Elements**: Parser doesn't add missing required elements
5. **Performance**: Conversion has overhead compared to raw parsing