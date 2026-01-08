# Hypothesis G: Production-Ready Fast Object Creation

**Date**: January 8, 2026  
**Status**: 🔬 TESTING  
**Target**: ≥85% performance improvement (matching Hypothesis F)

---

## Objective

Integrate Hypothesis F's schema-based fast creation into a production-ready structure that can be merged into the main `Type_Safe` codebase with minimal changes.

---

## Architecture

### File Structure

```
hypothesis_G__production_fast_create/
├── schemas/
│   ├── __init__.py
│   ├── Field__Schema.py           # Single field description
│   └── Class__Schema.py           # Full class description
│
├── Type_Safe__Config.py           # Simplified config (2 flags)
├── Type_Safe__Fast_Create__Cache.py   # Schema generation + caching
├── Type_Safe__Step__Fast_Create.py    # Fast creation step
├── Type_Safe__Hypothesis_G.py     # Type_Safe subclass
│
├── test_Fast_Create__Cache.py     # Schema/cache tests
├── test_Type_Safe__Hypothesis_G.py    # Functional tests
├── test_perf__Hypothesis_G.py     # Performance benchmarks
│
└── HYPOTHESIS_G__brief.md         # This file
```

### Key Design Decisions

1. **Simplified Config** - Only 2 flags:
   - `fast_create` - Use schema-based creation
   - `skip_validation` - Bypass `__setattr__` validation

2. **Regular dict for cache** - Classes never get GC'd at runtime, so WeakKeyDictionary is unnecessary overhead

3. **No `__new__` override** - Everything done in `__init__`, matching existing Type_Safe pattern

4. **Separate Schema Classes** - `Field__Schema` and `Class__Schema` in dedicated files for clarity

5. **Module Singletons** - `type_safe_fast_create_cache` and `type_safe_step_fast_create` follow existing patterns

---

## Changes Required to Type_Safe

Only **~10 lines** needed in `Type_Safe`:

```python
def __init__(self, **kwargs):
    config = get_active_config()
    if config and config.fast_create:
        if not type_safe_fast_create_cache.is_generating(type(self)):
            type_safe_step_fast_create.create(self, **kwargs)
            return
    # ... existing code ...

def __setattr__(self, name, value):
    config = get_active_config()
    if config and config.skip_validation:
        object.__setattr__(self, name, value)
    else:
        # ... existing code ...
```

---

## Expected Performance

Based on Hypothesis F results:

| Benchmark | Expected Improvement |
|-----------|---------------------|
| Empty class | ~25% |
| Primitives only | ~85% |
| With collections | ~91% |
| Many fields | ~92% |
| Nested objects | ~90-94% |
| MGraph-like complex | ~94% |

---

## Usage

```python
from hypothesis_G__production_fast_create import Type_Safe__Config, Type_Safe__Hypothesis_G

class MyClass(Type_Safe__Hypothesis_G):
    name  : str = ''
    count : int = 0

# Normal creation (full validation)
obj = MyClass(name='test')

# Fast creation (~10-20x faster)
with Type_Safe__Config(fast_create=True):
    obj = MyClass(name='test')

# Fast everything (bulk loading)
with Type_Safe__Config(fast_create=True, skip_validation=True):
    for row in database_rows:
        obj = MyClass(**row)
```

---

## Future Flags (Not Implemented)

Noted in `Type_Safe__Config` for future implementation:

- `immutable` - Prevent attribute addition after `__init__` completes