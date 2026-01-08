# Hypothesis B: NOP Type_Safe__Config in Context

**Date**: January 7, 2026  
**Status**: In Progress  
**Baseline**: `hypothesis_A__config_lookup` (Type_Safe with thread-local config lookup)

---

## Context: Where We Are

Hypothesis A established that:
1. Thread-local config lookup costs ~75 ns (down from ~2,200 ns with stack walking)
2. Total overhead for config lookup in `Type_Safe.__init__` is ~300-450 ns per object
3. The infrastructure is viable

**Now we need to answer**: What happens when a `Type_Safe__Config` is **actually present** in the context?

---

## The Change

### Baseline (Hypothesis A)
```python
# No config context - find_type_safe_config() returns None
obj = Type_Safe__Hypothesis_A()
```

### Hypothesis B
```python
# Config IS in context - find_type_safe_config() returns the config
with Type_Safe__Config(skip_validation=True):
    obj = Type_Safe__Hypothesis_B()
```

**Key point**: Hypothesis B does NOT act on the config flags yet. It just:
1. Finds the config (which now returns an actual object, not None)
2. Stores it (optional, for debugging)
3. Continues with normal Type_Safe initialization

This is a **NOP (No Operation)** test - measuring the overhead of having config present without using it.

---

## What We're Measuring

| Scenario | Config Lookup Returns | Expected Overhead |
|----------|----------------------|-------------------|
| Hypothesis A (baseline) | `None` | ~300-450 ns |
| Hypothesis B (with context) | `Type_Safe__Config` object | ~??? ns |

### Questions to Answer

1. **Is there additional overhead when config is found vs not found?**
   - `getattr(_thread_local, 'config', None)` returns `None` → fast path?
   - `getattr(_thread_local, 'config', None)` returns object → same speed?

2. **Does storing the config reference add overhead?**
   - If we do `object.__setattr__(self, '_config_', config)` only when config exists

3. **What's the baseline before we start skipping operations?**
   - This becomes the "before" for Hypothesis C (where we actually use the flags)

---

## Expected Outcome

Thread-local `getattr()` should be **the same speed** whether it returns `None` or an object. Therefore:

| Metric | Expected |
|--------|----------|
| Overhead vs Hypothesis A | ~0 ns (no significant difference) |
| Status | ✅ SUCCESS if overhead < 100 ns |

If there IS significant overhead, we need to investigate why.

---

## Test Structure

### Baseline: Type_Safe__Hypothesis_A (from Hypothesis A)
```python
class Type_Safe__Hypothesis_A(Type_Safe):
    def __init__(self, **kwargs):
        config = find_type_safe_config()                    # Returns None (no context)
        object.__setattr__(self, "__hypothesis_config__", config)
        super().__init__(**kwargs)
```

### Hypothesis B: Type_Safe__Hypothesis_B
```python
class Type_Safe__Hypothesis_B(Type_Safe):
    def __init__(self, **kwargs):
        config = find_type_safe_config()                    # Returns Type_Safe__Config!
        object.__setattr__(self, "__hypothesis_config__", config)
        super().__init__(**kwargs)

# Test runs INSIDE context:
with Type_Safe__Config(skip_validation=True):
    obj = Type_Safe__Hypothesis_B()
```

The code is **identical** - only the context differs.

---

## Benchmark Design

```python
def run_baseline_benchmarks(timing):
    """Hypothesis A: No config context"""
    timing.benchmark('A_01__empty', TS__Empty__Hyp_A)
    timing.benchmark('A_02__with_primitives', TS__With_Primitives__Hyp_A)
    # ...

def run_hypothesis_benchmarks(timing):
    """Hypothesis B: With config context (but NOP)"""
    with Type_Safe__Config(skip_validation=True):           # Config IS present
        timing.benchmark('A_01__empty', TS__Empty__Hyp_B)
        timing.benchmark('A_02__with_primitives', TS__With_Primitives__Hyp_B)
        # ...
```

---

## Success Criteria

1. **Performance**: Overhead vs Hypothesis A < 100 ns per object
2. **Functional**: Config is correctly found inside context
3. **Verification**: `obj.__hypothesis_config__` is not None inside context

---

## Why This Matters

This establishes the **true baseline** for optimization:

```
┌─────────────────────────────────────────────────────────────────────┐
│ Hypothesis A: Config lookup (no context)     → ~350 ns overhead     │
├─────────────────────────────────────────────────────────────────────┤
│ Hypothesis B: Config lookup (with context)   → ~??? ns overhead     │
│               (NOP - don't use flags yet)                           │
├─────────────────────────────────────────────────────────────────────┤
│ Hypothesis C: Actually USE skip_validation   → SPEEDUP expected!    │
│               (This is where we gain back the overhead)             │
└─────────────────────────────────────────────────────────────────────┘
```

If Hypothesis B shows ~350 ns overhead (same as A), then Hypothesis C just needs to save >350 ns by skipping validation to break even - and we expect it to save **much more** than that.

---

## Files to Create

| File                         | Purpose |
|------------------------------|---------|
| `HYPOTHESIS_B__brief.md`     | This document |
| `Type_Safe__Hypothesis_B.py` | Same as Hypothesis_A (or inherits from it) |
| `test_perf__Hypothesis_B.py` | Benchmark with config context active |
| `hypothesis_b_report.txt`    | Results (generated) |
| `hypothesis_b_result.json`   | Structured data (generated) |
| `HYPOTHESIS_B__debrief.md`   | Post-analysis (after running) |

---

## Relationship to Other Hypotheses

```
Hypothesis A (DONE)
    │
    │  "Config lookup works, ~350ns overhead"
    │
    ▼
Hypothesis B (THIS ONE)
    │
    │  "Config present in context, still ~350ns?" (NOP)
    │
    ▼
Hypothesis C (NEXT)
    │
    │  "Use skip_validation → SPEEDUP!"
    │
    ▼
Hypothesis D, E, F...
    │
    │  "Use other flags (skip_setattr, skip_conversion, etc.)"
    │
    ▼
Production Integration
```

---

## Notes

- The Hypothesis B class can be **identical** to Hypothesis A class
- The only difference is the **test harness** wrapping benchmarks in `with Type_Safe__Config():`
- This isolates the variable: "Does having config present (vs None) add overhead?"