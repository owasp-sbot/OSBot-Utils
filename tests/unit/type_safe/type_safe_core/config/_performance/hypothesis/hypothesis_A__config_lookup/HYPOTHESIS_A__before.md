# Hypothesis A: Config Lookup Integration

**Date**: January 7, 2026  
**Status**: In Progress  
**Baseline**: `jan_7__before__type_safe_changes/benchmark.txt`

---

## The Change

Add `find_type_safe_config()` call to `Type_Safe.__init__` to discover optimization config from calling stack frames.

```python
# Current Type_Safe.__init__ (simplified)
def __init__(self, **kwargs):
    # ... existing initialization logic ...

# Hypothesis A: Add config lookup
def __init__(self, **kwargs):
    config = find_type_safe_config()      # ← THE CHANGE
    # For now: just lookup, don't act on flags yet
    # ... existing initialization logic ...
```

---

## Expected Outcome

| Scenario | Expected Overhead | Acceptable? |
|----------|-------------------|-------------|
| No config in stack | +200-500 ns | ✓ Yes |
| Config present, no flags | +200-500 ns | ✓ Yes |
| Config present, with flags | +200-500 ns (no action yet) | ✓ Yes |

**Key constraint**: The lookup overhead must be small enough that it doesn't negate the benefits of the optimizations it enables.

---

## Why This Matters

This is the **foundation** for all subsequent optimizations:

```
Hypothesis A (this)     → Config lookup works, overhead acceptable
    ↓
Hypothesis B            → skip_setattr flag honored
    ↓
Hypothesis C            → skip_validation flag honored
    ↓
Hypothesis D            → on_demand_nested flag honored (big win)
    ↓
Production integration  → Merge proven optimizations to Type_Safe
```

If Hypothesis A shows unacceptable overhead, we need to optimize the stack walker before proceeding.

---

## Success Criteria

1. **Performance**: Overhead < 1,000 ns when no config present
2. **Functional**: All existing Type_Safe behavior unchanged
3. **Tests**: All existing unit tests pass
4. **Measurable**: Clear before/after comparison via Perf_Benchmark

---

## Test Strategy

### Section C: Baseline (current Type_Safe)
```python
class TS__Empty(Type_Safe):
    pass
```

### Section D: Hypothesis (Type_Safe__Hypothesis_A)
```python
class TS__Empty__Hyp_A(Type_Safe__Hypothesis_A):
    pass
```

**Comparison**: Section D timings vs Section C timings = overhead of config lookup

---

## Files in This Hypothesis

| File | Purpose |
|------|---------|
| `HYPOTHESIS.md` | This document |
| `Type_Safe__Hypothesis_A.py` | Hypothesis class with config lookup |
| `test_perf__Hypothesis_A.py` | Benchmark tests |
| `benchmark.json` | Results (generated) |
| `benchmark.txt` | Human-readable results (generated) |
| `benchmark.html` | Visual dashboard (generated) |

---

## Results

*To be filled after running benchmarks*

### Overhead Measurements

| Benchmark | Baseline (C) | Hypothesis (D) | Overhead | Verdict |
|-----------|--------------|----------------|----------|---------|
| TS__Empty | ___ ns | ___ ns | ___ ns | ⏳ |
| TS__With_Primitives | ___ ns | ___ ns | ___ ns | ⏳ |
| TS__With_Nested | ___ ns | ___ ns | ___ ns | ⏳ |

### Verdict

⏳ **Pending** - Awaiting benchmark results

---

## Next Steps (if successful)

1. Document overhead numbers in Results section above
2. Mark hypothesis as ✓ Confirmed
3. Proceed to Hypothesis B: `skip_setattr` flag integration
4. Eventually merge to `Type_Safe.__init__` when full optimization chain proven