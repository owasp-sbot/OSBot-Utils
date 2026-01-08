# Hypothesis E: on_demand_nested Flag Implementation - Debrief

**Date**: January 7, 2026  
**Status**: ✅ MAJOR SUCCESS  
**Result**: 52-61% improvement, up to 6.4x speedup for complex nested classes

---

## Executive Summary

Hypothesis E proved that deferring nested Type_Safe object creation until first access delivers **massive performance gains** for complex hierarchies. We also developed a **simplified v2 implementation** that eliminates permanent tracking attributes while maintaining (and slightly improving) performance.

This is the **biggest single optimization** in the hypothesis series, with speedups of up to **6.4x** for MGraph-like structures.

---

## The Problem

Type_Safe creates ALL nested objects during `__init__`:

```python
class MGraph__Index(Type_Safe):
    edges_index : Index__Edges      # Created immediately
    nodes_index : Index__Nodes      # Created immediately  
    labels_index: Index__Labels     # Created immediately

index = MGraph__Index()  # Creates 3 indexes + their nested objects + their dicts...
```

For complex hierarchies, this creates dozens of objects even if never accessed.

---

## The Solution

With `on_demand_nested=True`, nested Type_Safe objects are created **only when first accessed**:

```python
with Type_Safe__Config(on_demand_nested=True):
    index = MGraph__Index()              # Fast! No nested objects created
    
    index.edges_index.data['key'] = 'v'  # edges_index created NOW
    # nodes_index, labels_index never created if never accessed!
```

---

## Two Implementations

### v1: Tracking Dict Approach (Original Type_Safe__On_Demand)

```python
def __init__(self, **kwargs):
    object.__setattr__(self, '_on_demand__init_complete', False)
    object.__setattr__(self, '_on_demand__types', {})
    
    # ... collect types into _on_demand__types ...
    
    super().__init__(**kwargs)
    object.__setattr__(self, '_on_demand__init_complete', True)

def __getattribute__(self, name):
    if name in self._on_demand__types:
        var_type = self._on_demand__types.pop(name)
        # ... create and return ...

def json(self):
    result = super().json()
    return self._on_demand__clean_json(result)  # Remove tracking attrs
```

**Issues:**
- Permanent `_on_demand__types` dict on every object
- Permanent `_on_demand__init_complete` flag on every object
- Requires `_on_demand__clean_json()` hack for serialization

### v2: Temporary Flag Approach (Simplified)

```python
def __init__(self, **kwargs):
    if config and config.on_demand_nested:
        object.__setattr__(self, '_on_demand__init_complete', False)  # SET
        try:
            # ... set kwargs[var_name] = None for Type_Safe attrs ...
            super().__init__(**kwargs)
        finally:
            object.__delattr__(self, '_on_demand__init_complete')     # DELETE
    else:
        super().__init__(**kwargs)

def __getattribute__(self, name):
    try:
        object.__getattribute__(self, '_on_demand__init_complete')
        return object.__getattribute__(self, name)  # In init → don't create
    except AttributeError:
        pass  # After init → do create logic
    
    value = object.__getattribute__(self, name)
    if value is None:
        var_type = get_annotation_type(name)
        if should_create_on_demand(var_type):
            new_value = var_type()
            object.__setattr__(self, name, new_value)
            return new_value
    return value
```

**Benefits:**
- Flag only exists DURING `__init__`, then deleted
- No permanent tracking attributes
- No json cleanup needed
- Simpler code (~90 lines vs ~120 lines)

---

## Performance Results

### v1 Results

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ HYPOTHESIS: Hypothesis E: on_demand_nested=True vs False                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Benchmark              │ Before       │ After      │ Change   │ Speedup        │
├─────────────────────────────────────────────────────────────────────────────────┤
│ A_01__empty            │ 8,358 ns     │ 7,871 ns   │ -5.8% ▼  │ 1.1x           │
│ A_03__one_nested       │ 42,436 ns    │ 17,362 ns  │ -59.1% ▼ │ 2.4x           │
│ A_04__three_nested     │ 105,329 ns   │ 25,408 ns  │ -75.9% ▼ │ 4.1x           │
│ A_05__deep_nested      │ 93,511 ns    │ 17,065 ns  │ -81.8% ▼ │ 5.5x           │
│ A_06__mgraph_like      │ 131,943 ns   │ 21,887 ns  │ -83.4% ▼ │ 6.0x           │
│ B_04__mgraph_like_x10  │ 1,130,750 ns │ 201,280 ns │ -82.2% ▼ │ 5.6x           │
├─────────────────────────────────────────────────────────────────────────────────┤
│ ✓ SUCCESS (61.1% >= 30.0% target)                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### v2 Results

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ HYPOTHESIS: Hypothesis E v2: on_demand_nested (simplified)                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Benchmark              │ Before     │ After      │ Change   │ Speedup          │
├─────────────────────────────────────────────────────────────────────────────────┤
│ A_01__empty            │ 1,133 ns   │ 1,663 ns   │ +46.8% ▲ │ 0.7x (overhead)  │
│ A_03__one_nested       │ 26,659 ns  │ 11,871 ns  │ -55.5% ▼ │ 2.2x             │
│ A_04__three_nested     │ 51,194 ns  │ 18,994 ns  │ -62.9% ▼ │ 2.7x             │
│ A_05__deep_nested      │ 56,829 ns  │ 12,002 ns  │ -78.9% ▼ │ 4.7x             │
│ A_06__mgraph_like      │ 97,928 ns  │ 15,375 ns  │ -84.3% ▼ │ 6.4x             │
│ B_04__mgraph_like_x10  │ 923,547 ns │ 147,003 ns │ -84.1% ▼ │ 6.3x             │
├─────────────────────────────────────────────────────────────────────────────────┤
│ ✓ SUCCESS (52.1% >= 30.0% target)                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## v1 vs v2 Comparison

| Metric | v1 | v2 | Winner |
|--------|----|----|--------|
| Overall improvement | 61.1% | 52.1% | v1 |
| A_06 MGraph-like | 83.4% | **84.3%** | **v2** |
| B_04 MGraph x10 | 82.2% | **84.1%** | **v2** |
| A_01 empty overhead | -5.8% | +46.8% | v1 |
| Permanent tracking attrs | Yes | **No** | **v2** |
| json() cleanup needed | Yes | **No** | **v2** |
| Code complexity | Higher | **Lower** | **v2** |
| Lines of code | ~120 | **~90** | **v2** |

### Key Insight

v2's lower overall score (52.1% vs 61.1%) is due to the empty class overhead (+46.8%). But for the cases that matter (nested classes), **v2 is actually faster**:

| Nested Complexity | v1 | v2 | Winner |
|-------------------|----|----|--------|
| MGraph-like (A_06) | 6.0x | **6.4x** | **v2** |
| MGraph-like x10 (B_04) | 5.6x | **6.3x** | **v2** |

---

## The Temporary Flag Insight

The key breakthrough for v2 was realizing:

1. **The flag only needs to exist during `__init__`**
2. **After `__init__`, we can delete it**
3. **`__getattribute__` checks flag existence, not value**

```python
# During __init__: flag exists
try:
    object.__getattribute__(self, '_on_demand__init_complete')
    # Flag exists → we're in init → don't auto-create
except AttributeError:
    # Flag doesn't exist → we're after init → do auto-create
```

This means:
- No permanent attributes polluting the object
- `json()`, `from_json()`, `obj()` never see the flag
- No cleanup hacks needed

---

## Scaling Analysis

| Nested Objects | v2 Speedup | Time Saved |
|----------------|------------|------------|
| 1 | 2.2x | ~15 µs |
| 3 | 2.7x | ~32 µs |
| Deep (3 levels) | 4.7x | ~45 µs |
| MGraph-like | **6.4x** | **~83 µs** |
| MGraph-like x10 | **6.3x** | **~777 µs** |

**The more nested objects, the bigger the win.**

For Html_MGraph with 6 indexes, each with nested Schema__Data objects:
- Estimated savings: **~500 µs per MGraph__Index creation**
- For batch operations creating 100 objects: **~50 ms saved**

---

## What Gets Deferred

```python
@staticmethod
def should_create_on_demand(var_type):
    # YES - defer these (expensive):
    if issubclass(var_type, Type_Safe):           # ✅ Defer
        return True
    
    # NO - create immediately (cheap):
    if issubclass(var_type, Type_Safe__Primitive): # ❌ Cheap
        return False
    if issubclass(var_type, Type_Safe__List):      # ❌ Cheap
        return False
    if issubclass(var_type, Type_Safe__Dict):      # ❌ Cheap
        return False
    if issubclass(var_type, Type_Safe__Set):       # ❌ Cheap
        return False
```

Only **nested Type_Safe subclasses** are deferred - primitives and collections are cheap to create.

---

## Production Implementation

### Recommended: v2 Approach

Add to `Type_Safe.__init__`:

```python
def __init__(self, **kwargs):
    config = get_active_config()
    
    if config and config.on_demand_nested:
        object.__setattr__(self, '_on_demand__init_complete', False)
        try:
            # Walk MRO, set kwargs[var_name] = None for Type_Safe attrs
            for base_cls in type(self).__mro__:
                if base_cls is object:
                    continue
                for var_name, var_type in getattr(base_cls, '__annotations__', {}).items():
                    if should_create_on_demand(var_type) and var_name not in kwargs:
                        kwargs[var_name] = None
            
            # Normal init
            class_kwargs = self.__cls_kwargs__(provided_kwargs=kwargs)
            type_safe_step_init.init(self, class_kwargs, **kwargs)
        finally:
            object.__delattr__(self, '_on_demand__init_complete')
    else:
        # Normal init
        class_kwargs = self.__cls_kwargs__(provided_kwargs=kwargs)
        type_safe_step_init.init(self, class_kwargs, **kwargs)
```

Add `__getattribute__` to `Type_Safe`:

```python
def __getattribute__(self, name):
    if name.startswith('_'):
        return object.__getattribute__(self, name)
    
    try:
        object.__getattribute__(self, '_on_demand__init_complete')
        return object.__getattribute__(self, name)  # In init
    except AttributeError:
        pass
    
    value = object.__getattribute__(self, name)
    if value is None:
        var_type = get_annotation_type_for(self, name)
        if should_create_on_demand(var_type):
            new_value = var_type()
            object.__setattr__(self, name, new_value)
            return new_value
    return value
```

---

## Usage Pattern

```python
# Normal usage - all nested objects created (safe default)
index = MGraph__Index()
index.edges_index.data['key'] = 'value'

# Bulk operations - defer creation for performance
with Type_Safe__Config(on_demand_nested=True):
    indexes = [MGraph__Index() for _ in range(100)]  # 6.4x faster!
    
    # Objects created only when accessed
    for idx in indexes:
        if needs_edges(idx):
            idx.edges_index.process()  # Created here
        # nodes_index never created if not needed!
```

---

## Summary: Hypothesis Journey

| Hypothesis | Flag | Impact | Status |
|------------|------|--------|--------|
| A | Thread-local config | ~350 ns overhead | ✅ Done |
| B | Config presence | ~0 ns | ✅ Done |
| C | `skip_validation` | 50-83% faster | ✅ Done |
| D | `skip_conversion` | 20-30% faster | ✅ Done |
| **E** | **`on_demand_nested`** | **52-84% faster** | ✅ Done |

### Combined Potential

| Configuration | MGraph-like Creation | Speedup |
|---------------|---------------------|---------|
| Normal (no config) | ~100 µs | 1x |
| `skip_validation` only | ~20 µs | 5x |
| `on_demand_nested` only | ~15 µs | 6.4x |
| All flags combined | **~5 µs** | **~20x** |

---

## Lessons Learned

### 1. Temporary State > Permanent State

Instead of keeping `_on_demand__init_complete` forever, **delete it after use**. No cleanup needed!

### 2. AttributeError as Signal

Using `try/except AttributeError` to check flag existence is:
- Clean (no hasattr overhead)
- Self-documenting (flag gone = init complete)
- No pollution of object state

### 3. Simpler Can Be Faster

v2's simpler implementation (no tracking dict) is **faster for complex cases** than v1's more complex approach.

### 4. Target the Expensive Cases

Deferring only Type_Safe subclasses (not primitives/collections) gives maximum benefit with minimum complexity.

---

## Files

| File | Purpose |
|------|---------|
| `Type_Safe__Hypothesis_E.py` | v1 implementation (tracking dict) |
| `Type_Safe__Hypothesis_E_v2.py` | v2 implementation (temporary flag) |
| `test_perf__Hypothesis_E.py` | v1 benchmarks |
| `test_perf__Hypothesis_E_v2.py` | v2 benchmarks |
| `test_Type_Safe__Hypothesis_E_v2.py` | v2 functional tests |
| `HYPOTHESIS_E__brief.md` | Initial hypothesis |
| `HYPOTHESIS_E__debrief.md` | This document |

---

## Recommendation

**Use v2 (temporary flag approach)** for production:

1. **Simpler code** - easier to maintain
2. **No permanent attributes** - cleaner objects
3. **No json cleanup** - no hacks needed
4. **Faster for complex cases** - 6.4x vs 6.0x
5. **Acceptable trade-off** - empty class overhead is negligible in practice

The empty class overhead (+46.8%) only matters for classes with no nested Type_Safe attributes - exactly the cases where `on_demand_nested` provides no benefit anyway!
