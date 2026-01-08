# Hypothesis E: on_demand_nested Flag Implementation

**Date**: January 7, 2026  
**Status**: In Progress  
**Baseline**: Standard Type_Safe (creates all nested objects upfront)

---

## Context: Where We Are

| Hypothesis | Finding | Status |
|------------|---------|--------|
| A | Thread-local config lookup costs ~350 ns | ✅ Done |
| B | Config presence vs None adds ~0 ns | ✅ Done |
| C | `skip_validation` in `__setattr__` → 50-83% faster | ✅ Done |
| D | `skip_conversion` in init → 20-30% faster | ✅ Done |
| **E** | **`on_demand_nested` → defer nested creation** | 🔄 This one |

---

## The Problem

Currently, Type_Safe creates ALL nested Type_Safe objects during `__init__`:

```python
class Schema__Data(Type_Safe):
    edges : Dict[str, str]
    labels: Dict[str, str]

class Index__Edges(Type_Safe):
    data: Schema__Data                    # Created immediately during Index__Edges()

class MGraph__Index(Type_Safe):
    edges_index : Index__Edges            # Created immediately
    labels_index: Index__Labels           # Created immediately
    nodes_index : Index__Nodes            # Created immediately
```

If you create `MGraph__Index()`:
- `edges_index` is created → which creates `Schema__Data` → which creates 2 Type_Safe__Dicts
- `labels_index` is created → same cascade
- `nodes_index` is created → same cascade
- **Dozens of objects created even if never accessed!**

---

## The Solution

With `on_demand_nested=True`, nested Type_Safe objects are created **only when first accessed**:

```python
with Type_Safe__Config(on_demand_nested=True):
    index = MGraph__Index()               # Fast! No nested objects created yet
    
    # Later, when actually needed:
    index.edges_index.data.edges['a'] = 'b'   # edges_index created NOW
    
    # nodes_index and labels_index never created if never accessed!
```

---

## Existing Implementation: Type_Safe__On_Demand

This was already implemented as a separate class. Key techniques:

### 1. Intercept in `__init__`
```python
def __init__(self, **kwargs):
    object.__setattr__(self, '_on_demand__types', {})
    
    for var_name, var_type in annotations.items():
        if should_create_on_demand(var_type):
            on_demand_types[var_name] = var_type
            kwargs[var_name] = None           # Prevent Type_Safe auto-creation!
    
    super().__init__(**kwargs)
```

### 2. Create on First Access via `__getattribute__`
```python
def __getattribute__(self, name):
    if name.startswith('_'):                  # Fast path for internals
        return object.__getattribute__(self, name)
    
    on_demand_types = object.__getattribute__(self, '_on_demand__types')
    if name in on_demand_types:
        var_type = on_demand_types.pop(name)  # Remove from pending
        new_value = var_type()                # Create now!
        object.__setattr__(self, name, new_value)
        return new_value
    
    return object.__getattribute__(self, name)
```

### 3. What Gets Deferred
```python
@staticmethod
def _should_create_on_demand(var_type):
    if not issubclass(var_type, Type_Safe):
        return False                          # Only Type_Safe subclasses
    if issubclass(var_type, Type_Safe__Primitive):
        return False                          # Primitives are cheap
    if issubclass(var_type, (Type_Safe__List, Type_Safe__Dict, Type_Safe__Set)):
        return False                          # Collections are cheap
    return True
```

---

## Integration with Type_Safe__Config

The key insight: **We don't need to check config in `__getattribute__`**.

1. Check config only in `__init__` to decide whether to use on-demand mode
2. If on-demand, set up `_on_demand__types` dict
3. `__getattribute__` just checks if that dict exists and has pending items
4. When not using on-demand, `_on_demand__types` doesn't exist → normal behavior

---

## Expected Impact

From Type_Safe__On_Demand documentation:
- **20x faster** construction for complex nested hierarchies
- **98% reduction** in objects created during construction
- **~10ms savings** for Html_MGraph's 6-index initialization

For a class with 5 nested Type_Safe attributes:
- Before: 5 nested objects created × cost of each
- After: 0 nested objects created (until accessed)

---

## Test Strategy

### Baseline
```python
def run_baseline_benchmarks(timing):
    with Type_Safe__Config(on_demand_nested=False):      # Normal mode
        timing.benchmark('A_03__with_nested', TS__With_Nested)
```

### Hypothesis
```python
def run_hypothesis_benchmarks(timing):
    with Type_Safe__Config(on_demand_nested=True):       # On-demand mode
        timing.benchmark('A_03__with_nested', TS__With_Nested)
```

**Focus**: Tests with nested Type_Safe objects should show massive improvement.

---

## What Still Works

| Scenario | With `on_demand_nested=True` |
|----------|------------------------------|
| Primitives (str, int, bool) | ✅ Created normally |
| Collections (List, Dict, Set) | ✅ Created normally (cheap) |
| Type_Safe__Primitive | ✅ Created normally (cheap) |
| Explicit defaults | ✅ Used as-is |
| User-provided kwargs | ✅ Used as-is |
| JSON serialization | ✅ Works (creates pending objects) |

---

## What Changes

| Scenario | With `on_demand_nested=True` |
|----------|------------------------------|
| Nested Type_Safe without default | Created on first access |
| `repr()` shows pending count | `<MyClass (3 attrs pending)>` |

---

## Files to Create

| File | Purpose |
|------|---------|
| `HYPOTHESIS_E__brief.md` | This document |
| `Type_Safe__Hypothesis_E.py` | Class with on_demand_nested support |
| `test_perf__Hypothesis_E.py` | Benchmark test |
| `HYPOTHESIS_E__debrief.md` | Post-analysis (after running) |

---

## Success Criteria

1. **Performance**: Major improvement for nested Type_Safe classes
2. **Functional**: Objects still work correctly when accessed
3. **JSON**: Serialization still works (forces creation of pending objects)

---

## Note: Keeping It Simple

This hypothesis focuses ONLY on `on_demand_nested`. We're NOT combining with:
- `skip_validation` (Hypothesis C)
- `skip_conversion` (Hypothesis D)

This isolates the measurement to just the on-demand creation benefit.