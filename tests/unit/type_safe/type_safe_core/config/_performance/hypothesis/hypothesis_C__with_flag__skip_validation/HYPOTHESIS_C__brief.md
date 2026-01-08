# Hypothesis C: skip_validation Flag Implementation

**Date**: January 7, 2026  
**Status**: In Progress  
**Baseline**: Type_Safe with config lookup (Hypothesis A/B baseline)

---

## Context: Where We Are

| Hypothesis | Finding | Status |
|------------|---------|--------|
| A | Thread-local config lookup costs ~300-450 ns | ✅ Done |
| B | Config presence vs None adds ~0 ns | ✅ Done |
| **C** | **Actually USE skip_validation flag** | 🔄 This one |

We've established that the config infrastructure has ~350 ns overhead. Now we need to **earn that back** by actually skipping expensive operations.

---

## The Change

### Baseline (Before)
```python
class Type_Safe__Hypothesis_B(Type_Safe):
    def __init__(self, **kwargs):
        config = find_type_safe_config()
        object.__setattr__(self, "__hypothesis_config__", config)
        super().__init__(**kwargs)                                    # Full validation
```

### Hypothesis C (After)
```python
class Type_Safe__Hypothesis_C(Type_Safe):
    def __init__(self, **kwargs):
        config = find_type_safe_config()
        if config and config.skip_validation:
            self._init_without_validation(**kwargs)                   # SKIP validation!
        else:
            super().__init__(**kwargs)                                # Normal path
```

---

## What skip_validation Means

In normal `Type_Safe.__init__`, every attribute assignment goes through:

```
self.name = value
    │
    ▼
Type_Safe.__setattr__()
    │
    ├─► resolve_value()           ~200 ns
    ├─► validate_type()           ~300 ns  
    ├─► check_immutability()      ~100 ns
    └─► object.__setattr__()      ~50 ns
                                  ────────
                          Total:  ~650 ns per attribute
```

With `skip_validation=True`, we bypass all that:

```
self.name = value
    │
    ▼
object.__setattr__()              ~50 ns
                                  ────────
                          Total:  ~50 ns per attribute
```

**Potential savings: ~600 ns per attribute!**

---

## Expected Outcome

For a class with 3 attributes (`name`, `count`, `active`):

| Scenario | Time per Object | Calculation |
|----------|-----------------|-------------|
| Normal validation | ~2,000 ns | 3 attrs × 650 ns |
| Skip validation | ~500 ns | 3 attrs × 50 ns + overhead |
| **Savings** | **~1,500 ns** | **~75% faster** |

The ~350 ns config lookup overhead is **easily recovered** by skipping validation on just one attribute.

---

## Implementation Strategy

### Option 1: Override __setattr__ (Complex)

```python
class Type_Safe__Hypothesis_C(Type_Safe):
    def __setattr__(self, name, value):
        config = find_type_safe_config()
        if config and config.skip_validation:
            object.__setattr__(self, name, value)                     # Bypass
        else:
            super().__setattr__(name, value)                          # Normal
```

**Problem**: `find_type_safe_config()` called on EVERY attribute set.

### Option 2: Cache Config in __init__ (Better)

```python
class Type_Safe__Hypothesis_C(Type_Safe):
    def __init__(self, **kwargs):
        config = find_type_safe_config()
        object.__setattr__(self, '_skip_validation_', 
                           config.skip_validation if config else False)
        super().__init__(**kwargs)
    
    def __setattr__(self, name, value):
        if getattr(self, '_skip_validation_', False):
            object.__setattr__(self, name, value)
        else:
            super().__setattr__(name, value)
```

**Problem**: Still adds overhead to every __setattr__.

### Option 3: Fast Init Path (Best for Hypothesis)

```python
class Type_Safe__Hypothesis_C(Type_Safe):
    def __init__(self, **kwargs):
        config = find_type_safe_config()
        if config and config.skip_validation:
            # Direct initialization - bypass Type_Safe machinery
            for key, value in kwargs.items():
                object.__setattr__(self, key, value)
            # Also set defaults directly
            self._set_defaults_fast()
        else:
            super().__init__(**kwargs)
```

This is the cleanest for measuring the **potential** speedup.

---

## Test Structure

### Baseline: With Config Context, Normal Validation

```python
def run_baseline_benchmarks(timing):
    with Type_Safe__Config(skip_validation=False):                    # Config present, but OFF
        timing.benchmark('A_01__empty', TS__Empty)
```

### Hypothesis: With Config Context, Skip Validation

```python
def run_hypothesis_benchmarks(timing):
    with Type_Safe__Config(skip_validation=True):                     # Config present, ON
        timing.benchmark('A_01__empty', TS__Empty)
```

Same classes, same context presence, only difference is `skip_validation=True/False`.

---

## Success Criteria

1. **Performance**: Must save more than ~350 ns overhead (break-even point)
2. **Expected**: ~600+ ns savings per attribute (significant win)
3. **Functional**: Objects are still created correctly (just without validation)

---

## Why This Matters

If Hypothesis C succeeds, it proves the entire optimization strategy is viable:

```
Cost:   ~350 ns (config lookup)
Gain:   ~600 ns per attribute × N attributes
Net:    PROFIT for any class with 1+ attributes!
```

For complex classes like `MGraph__Index` with many nested Type_Safe objects, the gains compound dramatically.

---

## Files to Create

| File | Purpose |
|------|---------|
| `HYPOTHESIS_C__brief.md` | This document |
| `Type_Safe__Hypothesis_C.py` | Class implementing skip_validation |
| `test_perf__Hypothesis_C.py` | Benchmark test |
| `hypothesis_c_report.txt` | Results (generated) |
| `hypothesis_c_result.json` | Structured data (generated) |
| `HYPOTHESIS_C__debrief.md` | Post-analysis (after running) |

---

## Risks and Considerations

### 1. Type Safety Trade-off

`skip_validation=True` means:
- No type checking at construction time
- Invalid data can be assigned
- Bugs may surface later (harder to debug)

**Mitigation**: Only use for trusted data sources (e.g., loading from validated JSON/database).

### 2. Default Value Handling

Type_Safe creates default values for annotated attributes. With skip_validation, we need to ensure defaults are still set.

### 3. Nested Objects

Nested Type_Safe objects also need to respect the config. The thread-local approach handles this automatically.

---

## Relationship to Production

If Hypothesis C succeeds, the implementation path is:

1. Modify `Type_Safe.__init__` to check `find_type_safe_config()`
2. Add fast path when `skip_validation=True`
3. Ensure backward compatibility (no config = normal behavior)
4. Add similar optimizations for other flags (`skip_setattr`, `skip_conversion`, etc.)
