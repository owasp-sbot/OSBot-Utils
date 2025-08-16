# CSS_Dict__To__Css

## Overview

`CSS_Dict__To__Css` converts Python dictionaries containing CSS rules into properly formatted CSS strings. This utility enables programmatic CSS generation and manipulation through Python data structures.

## Class Definition

```python
class CSS_Dict__To__Css(Kwargs_To_Self):
    css: dict

    def add_css_entry(self, selector, data):
        self.css[selector] = data
        return self

    def convert(self, indent=''):
        css_lines = []
        for selector, properties in self.css.items():
            css_line = f"{indent}{selector} {"
            for prop, value in properties.items():
                css_line += f"\n{indent}    {prop}: {value};"
            css_line += '\n' + indent + "}"
            css_lines.append(css_line)
        return "\n".join(css_lines)
```

## Purpose

This converter enables:
1. **Programmatic CSS Generation**: Build CSS from Python data structures
2. **Dynamic Styling**: Generate CSS based on runtime conditions
3. **CSS Manipulation**: Modify CSS rules programmatically
4. **Integration**: Embed generated CSS in HTML documents

## Methods

### `add_css_entry(selector: str, data: dict) -> self`

Adds a CSS rule to the stylesheet.

```python
css_converter = CSS_Dict__To__Css()
css_converter.add_css_entry('.button', {
    'background-color': '#007bff',
    'color': 'white',
    'padding': '10px 20px'
})
```

### `convert(indent: str = '') -> str`

Converts the CSS dictionary to a formatted CSS string.

```python
css_string = css_converter.convert()
# Output:
# .button {
#     background-color: #007bff;
#     color: white;
#     padding: 10px 20px;
# }
```

## Usage Examples

### Basic CSS Generation

```python
from osbot_utils.helpers.html.transformers.CSS_Dict__To__Css import CSS_Dict__To__Css

# Create CSS converter
css_converter = CSS_Dict__To__Css()

# Add CSS rules
css_converter.add_css_entry('.container', {
    'max-width': '1200px',
    'margin': '0 auto',
    'padding': '20px'
})

css_converter.add_css_entry('.header', {
    'background-color': '#333',
    'color': '#fff',
    'padding': '1rem'
})

# Generate CSS
css_output = css_converter.convert()
print(css_output)
```

### Complex CSS Structure

```python
# Initialize with CSS data
css_data = {
    '.navbar': {
        'display': 'flex',
        'justify-content': 'space-between',
        'align-items': 'center',
        'padding': '1rem 2rem',
        'background-color': '#f8f9fa'
    },
    '.navbar-brand': {
        'font-size': '1.5rem',
        'font-weight': 'bold',
        'color': '#333',
        'text-decoration': 'none'
    },
    '.navbar-nav': {
        'display': 'flex',
        'list-style': 'none',
        'margin': '0',
        'padding': '0'
    },
    '.nav-item': {
        'margin-left': '1rem'
    },
    '.nav-link': {
        'color': '#666',
        'text-decoration': 'none',
        'transition': 'color 0.3s'
    },
    '.nav-link:hover': {
        'color': '#007bff'
    }
}

css_converter = CSS_Dict__To__Css(css=css_data)
formatted_css = css_converter.convert()
```

### With Indentation

```python
# Generate indented CSS for embedding in HTML
css_converter = CSS_Dict__To__Css()
css_converter.add_css_entry('body', {
    'font-family': 'Arial, sans-serif',
    'line-height': '1.6',
    'color': '#333'
})

# Convert with indentation
indented_css = css_converter.convert(indent='        ')
# Useful for embedding in <style> tags with proper HTML indentation
```

## Integration with Tag System

### Adding CSS to HTML Documents

```python
from osbot_utils.helpers.html.tags.Tag__Style import Tag__Style
from osbot_utils.helpers.html.transformers.CSS_Dict__To__Css import CSS_Dict__To__Css

# Create style tag
style_tag = Tag__Style()

# Add CSS rules
style_tag.add_css_entry('.alert', {
    'padding': '15px',
    'margin-bottom': '20px',
    'border': '1px solid transparent',
    'border-radius': '4px'
})

style_tag.add_css_entry('.alert-success', {
    'color': '#155724',
    'background-color': '#d4edda',
    'border-color': '#c3e6cb'
})

# The Tag__Style class uses CSS_Dict__To__Css internally
rendered_style = style_tag.render()
```

### Dynamic CSS Generation

```python
def generate_theme_css(primary_color, secondary_color, font_size='16px'):
    """Generate theme CSS based on parameters."""
    css_converter = CSS_Dict__To__Css()
    
    # Base styles
    css_converter.add_css_entry(':root', {
        '--primary-color': primary_color,
        '--secondary-color': secondary_color,
        '--font-size-base': font_size
    })
    
    # Component styles using CSS variables
    css_converter.add_css_entry('.btn-primary', {
        'background-color': 'var(--primary-color)',
        'color': 'white',
        'border': 'none',
        'padding': 'calc(var(--font-size-base) * 0.5) calc(var(--font-size-base) * 1)',
        'font-size': 'var(--font-size-base)'
    })
    
    css_converter.add_css_entry('.text-secondary', {
        'color': 'var(--secondary-color)'
    })
    
    return css_converter.convert()

# Generate theme
theme_css = generate_theme_css('#007bff', '#6c757d', '18px')
```

## Advanced Patterns

### CSS Builder Class

```python
class CssBuilder:
    def __init__(self):
        self.converter = CSS_Dict__To__Css()
    
    def add_reset_styles(self):
        """Add CSS reset styles."""
        self.converter.add_css_entry('*', {
            'margin': '0',
            'padding': '0',
            'box-sizing': 'border-box'
        })
        return self
    
    def add_typography(self, font_family='Arial, sans-serif'):
        """Add typography styles."""
        self.converter.add_css_entry('body', {
            'font-family': font_family,
            'font-size': '16px',
            'line-height': '1.5',
            'color': '#333'
        })
        
        for i in range(1, 7):
            size = 2.5 - (i * 0.3)
            self.converter.add_css_entry(f'h{i}', {
                'font-size': f'{size}rem',
                'margin-bottom': '0.5rem'
            })
        
        return self
    
    def add_utility_classes(self):
        """Add utility classes."""
        utilities = {
            '.text-center': {'text-align': 'center'},
            '.text-right': {'text-align': 'right'},
            '.mt-1': {'margin-top': '0.25rem'},
            '.mt-2': {'margin-top': '0.5rem'},
            '.mt-3': {'margin-top': '1rem'},
            '.p-1': {'padding': '0.25rem'},
            '.p-2': {'padding': '0.5rem'},
            '.p-3': {'padding': '1rem'}
        }
        
        for selector, styles in utilities.items():
            self.converter.add_css_entry(selector, styles)
        
        return self
    
    def build(self):
        """Build the final CSS."""
        return self.converter.convert()

# Usage
css = (CssBuilder()
    .add_reset_styles()
    .add_typography('Georgia, serif')
    .add_utility_classes()
    .build()
)
```

### Media Query Support

```python
def add_responsive_styles(css_converter):
    """Add responsive styles with media queries."""
    # Desktop styles
    css_converter.add_css_entry('.container', {
        'max-width': '1200px',
        'margin': '0 auto',
        'padding': '0 20px'
    })
    
    # Note: Media queries need special handling
    # This is a limitation - CSS_Dict__To__Css doesn't directly support nested rules
    # Workaround: Use selector names that include media query
    css_converter.add_css_entry('@media (max-width: 768px) { .container', {
        'padding': '0 10px'
    })
    
    # Better approach: Generate media queries separately
    mobile_css = CSS_Dict__To__Css()
    mobile_css.add_css_entry('.container', {
        'padding': '0 10px'
    })
    
    # Combine with media query wrapper
    mobile_styles = f"@media (max-width: 768px) {{\n{mobile_css.convert('    ')}\n}}"
    
    return css_converter.convert() + '\n\n' + mobile_styles
```

### CSS Preprocessing

```python
class CssPreprocessor:
    def __init__(self):
        self.variables = {}
        self.mixins = {}
    
    def define_variable(self, name, value):
        """Define a CSS variable."""
        self.variables[name] = value
    
    def process_css_dict(self, css_dict):
        """Process CSS dictionary with variable substitution."""
        processed = {}
        
        for selector, properties in css_dict.items():
            processed_props = {}
            
            for prop, value in properties.items():
                # Replace variables
                if isinstance(value, str) and value.startswith('$'):
                    var_name = value[1:]
                    if var_name in self.variables:
                        value = self.variables[var_name]
                
                processed_props[prop] = value
            
            processed[selector] = processed_props
        
        return processed

# Usage
preprocessor = CssPreprocessor()
preprocessor.define_variable('primary-color', '#007bff')
preprocessor.define_variable('spacing-unit', '8px')

raw_css = {
    '.button': {
        'background-color': '$primary-color',
        'padding': '$spacing-unit',
        'color': 'white'
    }
}

processed_css = preprocessor.process_css_dict(raw_css)
css_converter = CSS_Dict__To__Css(css=processed_css)
final_css = css_converter.convert()
```

## Performance Optimization

### Caching Generated CSS

```python
from functools import lru_cache
import hashlib
import json

class CachedCssGenerator:
    def __init__(self):
        self.cache = {}
    
    def _generate_cache_key(self, css_dict):
        """Generate cache key from CSS dictionary."""
        # Convert to sorted JSON for consistent hashing
        json_str = json.dumps(css_dict, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    def generate(self, css_dict):
        """Generate CSS with caching."""
        cache_key = self._generate_cache_key(css_dict)
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        converter = CSS_Dict__To__Css(css=css_dict)
        css_output = converter.convert()
        self.cache[cache_key] = css_output
        
        return css_output
```

## Testing Patterns

```python
def test_css_generation():
    """Test CSS generation from dictionary."""
    css_dict = {
        '.test-class': {
            'color': 'red',
            'font-size': '16px'
        }
    }
    
    converter = CSS_Dict__To__Css(css=css_dict)
    result = converter.convert()
    
    expected = """.test-class {
    color: red;
    font-size: 16px;
}"""
    
    assert result == expected

def test_css_with_indentation():
    """Test CSS generation with custom indentation."""
    converter = CSS_Dict__To__Css()
    converter.add_css_entry('.indented', {'margin': '10px'})
    
    result = converter.convert(indent='    ')
    expected = """    .indented {
        margin: 10px;
    }"""
    
    assert result == expected
```

## Best Practices

1. **Use Meaningful Selectors**: Follow CSS naming conventions
2. **Group Related Rules**: Organize CSS logically
3. **Consider Specificity**: Be aware of CSS specificity rules
4. **Validate Values**: Ensure CSS values are valid
5. **Memory Efficiency**: Reuse converters when possible

## Common Patterns

### Component-Based CSS

```python
def generate_component_css(component_name, styles):
    """Generate CSS for a component with BEM naming."""
    css_converter = CSS_Dict__To__Css()
    
    # Block styles
    css_converter.add_css_entry(f'.{component_name}', styles.get('block', {}))
    
    # Element styles
    for element, element_styles in styles.get('elements', {}).items():
        css_converter.add_css_entry(f'.{component_name}__{element}', element_styles)
    
    # Modifier styles
    for modifier, modifier_styles in styles.get('modifiers', {}).items():
        css_converter.add_css_entry(f'.{component_name}--{modifier}', modifier_styles)
    
    return css_converter.convert()

# Usage
button_styles = {
    'block': {
        'padding': '10px 20px',
        'border': 'none',
        'cursor': 'pointer'
    },
    'elements': {
        'icon': {
            'margin-right': '5px'
        }
    },
    'modifiers': {
        'primary': {
            'background-color': '#007bff',
            'color': 'white'
        },
        'large': {
            'padding': '15px 30px',
            'font-size': '18px'
        }
    }
}

button_css = generate_component_css('button', button_styles)
```

## Limitations

1. **No Nested Rules**: Doesn't support SCSS-style nesting
2. **No Media Queries**: Media queries need special handling
3. **No CSS Functions**: calc(), var() are treated as strings
4. **No Validation**: Doesn't validate CSS property/value pairs
5. **Simple Format**: Basic formatting without minification options