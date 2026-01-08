# Hypothesis F: Schema-Based Fast Create Implementation

**Date**: January 7, 2026  
**Status**: In Progress  
**Baseline**: Standard Type_Safe (full __init__ process)

---

## Context: Where We Are

| Hypothesis | Finding | Status |
|------------|---------|--------|
| A | Thread-local config lookup costs ~350 ns | ✅ Done |
| B | Config presence vs None adds ~0 ns | ✅ Done |
| C | `skip_validation` in `__setattr__` → 50-83% faster | ✅ Done |
| D | `skip_conversion` in init → 20-30% faster | ✅ Done |
| E | `on_demand_nested` → 52-84% faster | ✅ Done |
| **F** | **Schema-based fast_create** | 🔄 This one |

---

## The Problem

Type_Safe's `__init__` does a lot of work every single time:

```python
def __init__(self, **kwargs):
    class_kwargs = self.__cls_kwargs__(provided_kwargs=kwargs)  # Walk MRO, compute defaults
    type_safe_step_init.init(self, class_kwargs, **kwargs)       # Loop fields, validate each
```

Even with Hypothesis C/D/E optimizations, we still:
- Walk the MRO to find annotations
- Compute default values
- Loop through fields
- Apply kwargs

**But the class structure never changes at runtime!**

---

## The Solution: Pre-Computed Schema

### Key Insight

For each Type_Safe class, pre-compute a "creation schema" that describes:
- Which fields exist
- What their default values are
- Which values can be shared (immutable) vs need fresh copies (mutable)

Then use `object.__new__()` + direct `__dict__` assignment to bypass `__init__` entirely.

### Field Classification

| Field Type | Mode | Action |
|------------|------|--------|
| `str = ''` | **static** | Share reference (immutable) |
| `int = 0` | **static** | Share reference (immutable) |
| `bool = False` | **static** | Share reference (immutable) |
| `node_id: Obj_Id` | **factory** | Call `Obj_Id()` each time |
| `items: List[str]` | **factory** | Call `Type_Safe__List()` each time |
| `data: Dict[str, int]` | **factory** | Call `Type_Safe__Dict()` each time |
| `child: Child_Type_Safe` | **nested** | Recursive fast_create |
| `child: Child_Type_Safe` | **on_demand** | Set to `None`, create on access |

---

## Schema Structure

```python
class Field__Schema(Type_Safe):
    name           : str                           # Field name
    mode           : str                           # 'static' | 'factory' | 'nested' | 'on_demand'
    static_value   : Any           = None          # For 'static' mode
    factory_type   : type          = None          # For 'factory' mode
    nested_schema  : type          = None          # For 'nested'/'on_demand' mode (target class)

class Class__Creation__Schema(Type_Safe):
    target_class   : type                          # The Type_Safe class this schema is for
    fields         : List[Field__Schema]           # All fields
    static_dict    : Dict[str, Any]                # Pre-built dict of static values
```

---

## Fast Create Flow

```python
# Cache schemas per class
_schema_cache: Dict[type, Class__Creation__Schema] = {}

def fast_create(cls, **kwargs):
    schema = get_or_create_schema(cls)
    
    # 1. Create empty shell
    obj = object.__new__(cls)
    
    # 2. Start with static values (single dict.copy)
    new_dict = schema.static_dict.copy()
    
    # 3. Add factory-created values
    for field in schema.fields:
        if field.name in kwargs:
            continue  # User provided
        
        if field.mode == 'factory':
            new_dict[field.name] = field.factory_type()
        
        elif field.mode == 'nested':
            new_dict[field.name] = fast_create(field.nested_schema)
        
        elif field.mode == 'on_demand':
            new_dict[field.name] = None
    
    # 4. Apply user kwargs
    new_dict.update(kwargs)
    
    # 5. Set dict directly (bypasses __init__ entirely!)
    object.__setattr__(obj, '__dict__', new_dict)
    
    return obj
```

---

## Cost Comparison

### Normal Type_Safe.__init__

```
__cls_kwargs__()              # Walk MRO, build defaults      ~2,000 ns
type_safe_step_init.init()    # Loop through fields           
  └─► hasattr() check         # Per field                     ~200 ns
  └─► __setattr__()           # Validate                      ~1,500 ns
      └─► convert_value()     # Type conversion               ~500 ns
                              
Total (5 fields): ~15,000 ns
Total (10 fields): ~30,000 ns
```

### Schema-Based fast_create

```
schema.static_dict.copy()     # Single dict copy              ~100-200 ns
factory_type()                # Per factory field             ~200-500 ns each
new_dict.update(kwargs)       # Apply overrides               ~50-100 ns
object.__setattr__(__dict__)  # Single assignment             ~50 ns

Total (5 fields, 2 factory): ~500-800 ns
Total (10 fields, 3 factory): ~700-1,200 ns
```

### Expected Speedup

| Scenario | Normal | Fast Create | Speedup |
|----------|--------|-------------|---------|
| Simple (5 fields) | ~15,000 ns | ~600 ns | **25x** |
| Complex (10 fields) | ~30,000 ns | ~900 ns | **33x** |
| With nested | ~50,000 ns | ~1,200 ns | **40x** |

---

## Schema Generation

```python
def generate_schema(cls: type) -> Class__Creation__Schema:
    """Generate creation schema for a Type_Safe class (called once per class)"""
    
    # Create one instance normally to get defaults
    template = cls()
    template_dict = template.__dict__.copy()
    
    fields = []
    static_dict = {}
    
    for name, value in template_dict.items():
        if name.startswith('_'):
            continue
        
        field = Field__Schema(name=name)
        
        if is_immutable(value):
            field.mode = 'static'
            field.static_value = value
            static_dict[name] = value
        
        elif is_type_safe_subclass(type(value)):
            field.mode = 'nested'  # or 'on_demand' based on config
            field.nested_schema = type(value)
        
        else:  # Mutable (list, dict, etc.)
            field.mode = 'factory'
            field.factory_type = type(value)
        
        fields.append(field)
    
    return Class__Creation__Schema(
        target_class = cls,
        fields       = fields,
        static_dict  = static_dict
    )
```

---

## Integration with Type_Safe__Config

```python
with Type_Safe__Config(fast_create=True):
    node = Schema__MGraph__Node(node_id=id)  # Uses fast path

with Type_Safe__Config(fast_create=True, on_demand_nested=True):
    node = Schema__MGraph__Node()            # Fast + deferred nested
```

---

## What Still Works

After fast_create, the object is fully functional:

| Capability | Works? |
|------------|--------|
| `isinstance(obj, Type_Safe)` | ✅ Yes |
| `isinstance(obj, Schema__MGraph__Node)` | ✅ Yes |
| `obj.json()` | ✅ Yes |
| `obj.from_json(data)` | ✅ Yes |
| `obj.__setattr__()` validation | ✅ Yes (on subsequent sets) |
| All inherited methods | ✅ Yes |

**We only bypass the initial construction, not runtime safety!**

---

## Files to Create

| File | Purpose |
|------|---------|
| `HYPOTHESIS_F__brief.md` | This document |
| `Type_Safe__Fast_Create__Schema.py` | Schema classes |
| `Type_Safe__Hypothesis_F.py` | fast_create implementation |
| `test_perf__Hypothesis_F.py` | Benchmark tests |
| `HYPOTHESIS_F__debrief.md` | Post-analysis (after running) |

---

## Success Criteria

1. **Performance**: 25-50x faster than normal Type_Safe for complex classes
2. **Functional**: Created objects work identically to normal Type_Safe objects
3. **Compatibility**: Can be enabled via Type_Safe__Config

---

## Potential Issues to Watch

1. **Schema generation cost**: First instantiation per class is expensive (but amortized)
2. **Inheritance**: Need to handle class hierarchies correctly
3. **Edge cases**: Optional fields, Union types, custom defaults
4. **Thread safety**: Schema cache access from multiple threads
