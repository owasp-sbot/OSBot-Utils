# Hypothesis D: skip_conversion Flag Implementation

**Date**: January 7, 2026  
**Status**: In Progress  
**Baseline**: Type_Safe with Hypothesis C (`skip_validation` in `__setattr__`)

---

## Context: Where We Are

| Hypothesis | Finding | Status |
|------------|---------|--------|
| A | Thread-local config lookup costs ~350 ns | ✅ Done |
| B | Config presence vs None adds ~0 ns | ✅ Done |
| C | `skip_validation` in `__setattr__` → 50-83% faster | ✅ Done |
| **D** | **`skip_conversion` in init → skip type coercion** | 🔄 This one |

---

## The Target

In `Type_Safe__Step__Init.init()`, user-provided kwargs go through `convert_value_to_type_safe_objects()`:

```python
def init(self, __self, __class_kwargs, **kwargs):
    
    for (key, value) in __class_kwargs.items():      # Loop 1: Defaults - NO conversion
        setattr(__self, key, value)

    for (key, value) in kwargs.items():              # Loop 2: User kwargs
        if value is not None:
            value = self.convert_value_to_type_safe_objects(...)  # ← EXPENSIVE!
            setattr(__self, key, value)
```

This method does ~70 lines of type conversion logic:
- `list` → `Type_Safe__List`
- `dict` → `Type_Safe__Dict`  
- `set` → `Type_Safe__Set`
- `"ENUM_VALUE"` → `MyEnum.ENUM_VALUE`
- `{"nested": "data"}` → `Nested_Type_Safe(...)`

---

## The Change

### Surgical Point

In `Type_Safe__Step__Init.init()`, conditionally skip conversion:

```python
def init(self, __self, __class_kwargs, **kwargs):
    config = get_active_config()
    skip_conversion = config and config.skip_conversion
    
    for (key, value) in __class_kwargs.items():
        # ... existing logic (unchanged)
        setattr(__self, key, value)

    for (key, value) in kwargs.items():
        if hasattr(__self, key):
            if value is not None:
                if not skip_conversion:                              # NEW: conditional
                    value = self.convert_value_to_type_safe_objects(__self, key, value)
                setattr(__self, key, value)
        else:
            raise ValueError(...)
```

---

## What Still Works

| Scenario | With `skip_conversion=True` |
|----------|---------------------------|
| Default nested Type_Safe | ✅ Still created (via `default_value()`) |
| Default collections | ✅ Still `Type_Safe__List/Dict/Set` |
| Kwargs with exact types | ✅ Works perfectly |
| Objects with no kwargs | ✅ Unaffected (conversion only for kwargs) |

---

## What Changes

| Scenario | With `skip_conversion=True` |
|----------|---------------------------|
| `items=['a', 'b']` kwarg | Stays `list`, not `Type_Safe__List` |
| `status='ACTIVE'` for enum | Stays `str`, not `MyEnum.ACTIVE` |
| `child={'name': 'x'}` for nested | Stays `dict`, not `Child_Type_Safe` |

---

## Why This Is Acceptable

1. **Defaults still work** - Nested Type_Safe objects still created via `default_value()`
2. **Opt-in only** - Caller explicitly requests fast mode
3. **Trusted data** - Used for bulk loading from validated sources
4. **Type match** - If you provide correct types, everything works

---

## Expected Impact

The `convert_value_to_type_safe_objects()` function is called for **every kwarg**. It involves:
- `type_safe_annotations.obj_attribute_annotation()` lookup
- `type_safe_annotations.extract_enum_from_annotation()` check
- `type_safe_annotations.get_origin()` call
- Multiple `isinstance()` checks
- Potential collection iteration and recreation

**Estimated cost**: ~200-500 ns per kwarg

For a class instantiated with 5 kwargs: ~1,000-2,500 ns savings.

---

## Test Strategy

### Baseline
```python
def run_baseline_benchmarks(timing):
    with Type_Safe__Config(skip_validation=True, skip_conversion=False):
        timing.benchmark('A_02__with_primitives', TS__With_Primitives)
```

### Hypothesis
```python
def run_hypothesis_benchmarks(timing):
    with Type_Safe__Config(skip_validation=True, skip_conversion=True):
        timing.benchmark('A_02__with_primitives', TS__With_Primitives)
```

Both have `skip_validation=True` to isolate the conversion cost.

---

## Success Criteria

1. **Performance**: Measurable improvement when providing kwargs
2. **Functional**: Default values still work correctly
3. **No regressions**: Classes with no kwargs should be unchanged

---

## Files to Create

| File | Purpose |
|------|---------|
| `HYPOTHESIS_D__brief.md` | This document |
| `Type_Safe__Hypothesis_D.py` | Class with skip_conversion support |
| `test_perf__Hypothesis_D.py` | Benchmark test |
| `hypothesis_d_report.txt` | Results (generated) |
| `HYPOTHESIS_D__debrief.md` | Post-analysis (after running) |

---

## Relationship to Production

If successful, the change to `Type_Safe__Step__Init.init()` is minimal:

```python
def init(self, __self, __class_kwargs, **kwargs):
    from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config import get_active_config
    config = get_active_config()
    skip_conversion = config and config.skip_conversion
    
    # ... rest unchanged, just wrap convert_value_to_type_safe_objects call
```

Combined with Hypothesis C (`skip_validation`), this gives users fine-grained control:
- `skip_validation=True` - Skip per-attribute type checking
- `skip_conversion=True` - Skip kwarg type coercion
- Both together - Maximum speed for trusted data