# Hypothesis H: Debrief on Type_Safe Fast Create Integration

**Date**: January 2026  
**Status**: ✅ Complete  
**Related Hypotheses**: Hypothesis C (Proof of Concept), Hypothesis G (Production Implementation)

---

## Executive Summary

This document details the integration of the `fast_create` performance optimization into the production `Type_Safe` class. The optimization provides **50-85% performance improvement** for object creation by bypassing validation when working with trusted data sources.

### Key Changes

| Location | Lines Added | Purpose |
|----------|-------------|---------|
| `Type_Safe.__init__` | ~5 lines | Check config, delegate to fast_create |
| `Type_Safe.__setattr__` | ~4 lines | Check config, bypass validation |

### Test Coverage Added

| Test File | Tests | Purpose |
|-----------|-------|---------|
| `test_Type_Safe__Fast_Create__created_with_no_side_effects.py` | 45 | Correctness verification |
| `test_Type_Safe__Fast_Create__created_and_cached.py` | 20 | `__init__` wiring verification |
| `test_Type_Safe__Fast_Create__skip_validation_wired.py` | 14 | `__setattr__` wiring verification |
| `test_Type_Safe__Fast_Create__fast_create_side_effects.py` | ~22 | Document fast_create trade-offs |
| `test_Type_Safe__Fast_Create__skip_validation_side_effects.py` | ~16 | Document skip_validation trade-offs |

---

## Background: The Performance Problem

Type_Safe provides runtime type safety through validation in `__init__` and `__setattr__`. This validation is valuable for catching bugs early, but creates performance overhead:

```python
# Every object creation triggers:
# 1. __cls_kwargs__() - Collect class annotations
# 2. type_safe_step_init.init() - Validate and convert each field
# 3. __setattr__() called for each field - Type checking

obj = MyTypeSafeClass()  # Hundreds of microseconds for complex classes
```

For bulk operations with trusted data (database loads, JSON deserialization, API responses), this validation is redundant - the data has already been validated at the source.

---

## Evolution: Hypothesis C → Hypothesis G → Hypothesis H

### Hypothesis C: Proof of Concept

**Goal**: Prove that schema-based creation could work

**Approach**: Created standalone prototype classes:
- `Type_Safe__Fast_Create__Schema.py` - Schema generation
- `Type_Safe__Hypothesis_C.py` - Test subclass with fast_create logic

**Key Insight**: By analyzing class structure once and caching a "schema", we can:
1. Pre-compute which fields are static (immutable defaults)
2. Pre-compute which fields need factories (collections)
3. Pre-compute which fields are nested Type_Safe objects
4. Use `object.__new__()` + direct `__dict__` assignment instead of `__init__`

**Result**: Proved 50-85% improvement was achievable.

### Hypothesis G: Production-Ready Implementation

**Goal**: Refactor prototype into production-quality modules

**Deliverables**:

```
osbot_utils/type_safe/type_safe_core/fast_create/
├── Type_Safe__Fast_Create.py           # Main create() function
├── Type_Safe__Fast_Create__Cache.py    # Schema caching singleton
└── schemas/
    ├── Schema__Type_Safe__Fast_Create__Class.py   # Class schema
    └── Schema__Type_Safe__Fast_Create__Field.py   # Field descriptor
```

**Key Classes**:

1. **`Type_Safe__Fast_Create__Cache`** (singleton: `type_safe_fast_create_cache`)
   - `schema_cache: dict` - Maps class → schema
   - `generating: set` - Recursion guard for nested classes
   - `get_schema(cls)` - Get or create schema
   - `warm_cache(cls)` - Pre-warm for performance
   - `is_generating(cls)` - Check recursion guard

2. **`Type_Safe__Fast_Create`** (singleton: `type_safe_fast_create`)
   - `create(instance, **kwargs)` - Main fast creation method

3. **`Schema__Type_Safe__Fast_Create__Class`**
   - `target_class` - The class this schema describes
   - `fields` - List of field descriptors
   - `static_dict` - Pre-computed immutable defaults
   - `factory_fields` - Fields needing fresh instances
   - `nested_fields` - Fields that are Type_Safe objects

4. **`Schema__Type_Safe__Fast_Create__Field`**
   - `name` - Field name
   - `mode` - 'static' | 'factory' | 'nested'
   - `static_value` - For static fields
   - `factory_func` - For factory fields (creates fresh instance)
   - `nested_class` - For nested fields (the Type_Safe class)

### Hypothesis H: Integration & Benchmarking

**Goal**: Wire fast_create into production Type_Safe and benchmark

**This Document**: Details the wiring process and test coverage.

---

## The Wiring: What Changed in Type_Safe

### 1. Type_Safe.__init__ Changes

**Before**:
```python
class Type_Safe:
    def __init__(self, **kwargs):
        class_kwargs = self.__cls_kwargs__(provided_kwargs=kwargs)
        type_safe_step_init.init(self, class_kwargs, **kwargs)
```

**After**:
```python
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config import get_active_config
from osbot_utils.type_safe.type_safe_core.fast_create.Type_Safe__Fast_Create import type_safe_fast_create
from osbot_utils.type_safe.type_safe_core.fast_create.Type_Safe__Fast_Create__Cache import type_safe_fast_create_cache

class Type_Safe:
    def __init__(self, **kwargs):
        config = get_active_config()
        if config and config.fast_create:
            if not type_safe_fast_create_cache.is_generating(type(self)):
                type_safe_fast_create.create(self, **kwargs)
                return
        
        class_kwargs = self.__cls_kwargs__(provided_kwargs=kwargs)
        type_safe_step_init.init(self, class_kwargs, **kwargs)
```

**Explanation**:
1. `get_active_config()` - Returns current `Type_Safe__Config` from context stack (or None)
2. `config.fast_create` - Check if fast_create mode is enabled
3. `is_generating()` - Recursion guard: during schema generation, we create instances to inspect defaults. These MUST use normal path to avoid infinite recursion.
4. `type_safe_fast_create.create()` - Bypasses normal init, uses schema-based direct __dict__ assignment
5. `return` - Exit early, skip normal validation

### 2. Type_Safe.__setattr__ Changes

**Before**:
```python
def __setattr__(self, name, value):
    type_safe_step_set_attr.setattr(super(), self, name, value)
```

**After**:
```python
def __setattr__(self, name, value):
    config = get_active_config()
    if config and config.skip_validation:
        object.__setattr__(self, name, value)
        return
    
    type_safe_step_set_attr.setattr(super(), self, name, value)
```

**Explanation**:
1. `config.skip_validation` - Check if validation should be skipped
2. `object.__setattr__()` - Direct assignment, bypasses all Type_Safe validation
3. `return` - Exit early, skip normal validation path

---

## The Config System: Type_Safe__Config

The configuration uses a context manager pattern with thread-local storage:

```python
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config import Type_Safe__Config

# Usage
with Type_Safe__Config(fast_create=True, skip_validation=True):
    # All Type_Safe operations in this block use fast path
    obj = MyClass()           # Uses fast_create
    obj.field = value         # Uses skip_validation
```

**Config Options**:
| Option | Default | Effect |
|--------|---------|--------|
| `fast_create` | `False` | Bypass `__init__` validation, use schema-based creation |
| `skip_validation` | `False` | Bypass `__setattr__` validation |

**Key Implementation Details**:
- Uses `contextvars.ContextVar` for thread-safe context stack
- Contexts can be nested (inner context takes precedence)
- Context automatically cleans up on exit (including exceptions)

---

## Test Files: Detailed Breakdown

### 1. `test_Type_Safe__Fast_Create__created_with_no_side_effects.py`

**Purpose**: Verify that objects created with fast_create are **correct** (have right values, types, behavior)

**Key Property**: These tests **pass regardless of whether wiring is in place**. If fast_create isn't wired, the normal path produces the same results.

**Test Categories**:
- Normal mode baseline (3 tests)
- Fast create mode: basic, kwargs, collections, nested, deep nesting (18 tests)
- Object usability: isinstance, type, attributes, json (7 tests)
- Skip validation in setattr (3 tests)
- Config context behavior (3 tests)
- Equivalence: normal vs fast_create produce identical results (6 tests)
- Batch operations (3 tests)

**Example Test**:
```python
def test__fast_create__basic_creation(self):
    with Type_Safe__Config(fast_create=True):
        obj = TS__Simple()
    
    assert type(obj)   is TS__Simple
    assert obj.name    == ''
    assert obj.count   == 0
    assert obj.active  is False
```

### 2. `test_Type_Safe__Fast_Create__created_and_cached.py`

**Purpose**: Verify that the fast_create **mechanism** is actually being invoked (cache is populated)

**Key Property**: These tests **fail without wiring** because the cache is never populated when fast_create path isn't taken.

**Test Categories**:
- Basic cache population (3 tests)
- Recursive cache population for nested classes (2 tests)
- Cache NOT populated without fast_create=True (2 tests)
- Multiple creations use same cached schema (2 tests)
- Schema content verification (5 tests)
- Cache persistence after context exit (2 tests)
- Mixed usage patterns (2 tests)

**Example Test**:
```python
def test__fast_create__populates_cache_for_simple_class(self):
    with Type_Safe__Config(fast_create=True):
        obj = TS__Simple()
    
    schema = type_safe_fast_create_cache.schema_cache.get(TS__Simple)
    assert schema is not None                    # FAILS without wiring!
    assert schema.target_class is TS__Simple
```

### 3. `test_Type_Safe__Fast_Create__skip_validation_wired.py`

**Purpose**: Verify that skip_validation **mechanism** is actually being invoked

**Key Property**: These tests try to set **invalid values** which would normally raise errors. They **fail without wiring** because validation still runs.

**Test Categories**:
- Invalid value assignment (8 tests) - string to int, int to str, etc.
- Multiple invalid assignments (1 test)
- Validation still works without skip_validation (2 tests)
- Skip validation only active in context (1 test)
- Valid values still work (1 test)

**Example Test**:
```python
def test__skip_validation__allows_wrong_type_str_to_int(self):
    with Type_Safe__Config(fast_create=True, skip_validation=True):
        obj = TS__Typed_Fields()
        obj.int_field = 'not_an_int'           # Would normally raise TypeError!
    
    assert obj.int_field == 'not_an_int'       # FAILS without wiring!
```

### 4. `test_Type_Safe__Fast_Create__fast_create_side_effects.py`

**Purpose**: Document the **intentional trade-offs** of using fast_create=True

**Key Property**: All tests **pass** - they document expected behavior, not bugs.

**Documented Side Effects**:
- kwargs with wrong types are accepted
- kwargs are not auto-converted
- List/Dict kwargs with wrong element types accepted
- Nested kwarg can be dict instead of Type_Safe object
- Unknown kwargs are accepted (added to __dict__)
- Post-creation setattr still validates (unless skip_validation also set)
- json() serializes whatever is there

**Safe Patterns Documented**:
- Loading from trusted data sources
- JSON roundtrip (deserializing your own data)

### 5. `test_Type_Safe__Fast_Create__skip_validation_side_effects.py`

**Purpose**: Document the **intentional trade-offs** of using skip_validation=True

**Key Property**: All tests **pass** - they document expected behavior, not bugs.

**Documented Side Effects**:
- Type hints become documentation only
- json() serializes whatever is there (handles non-serializable gracefully → None)
- Collections can hold wrong types
- Collections can be replaced entirely (list field = string)
- Nested objects can be replaced with anything
- Invalid state persists after context exits
- Operations on wrong types may fail (e.g., `int.upper()`)

---

## Performance Benchmark Files

### `test_perf__Hypothesis_H__fast_create.py`

**Comparison**: Default Type_Safe vs `fast_create=True`

**Benchmarks**:
- A_01-A_08: Single object creation (empty → MGraph-like)
- B_01-B_04: Batch creation (x10 objects)

### `test_perf__Hypothesis_H__skip_validation.py`

**Comparison**: Default `__setattr__` vs `skip_validation=True`

**Benchmarks**:
- C_01-C_04: Attribute assignment patterns (x100 objects, x400 assignments)

### `test_perf__Hypothesis_H__fast_create_skip_validation.py`

**Comparison**: Default Type_Safe vs Maximum Speed Mode (both optimizations)

**Benchmarks**:
- A_01-A_08: Single object creation
- B_01-B_04: Batch creation (x10 objects)
- D_01-D_04: Create + modify patterns (real-world usage)

---

## When to Use Each Mode

| Mode | Use Case | Trade-off |
|------|----------|-----------|
| **Default** | User input, untrusted data | Full validation, slower |
| **fast_create=True** | Bulk creation from DB/cache | No __init__ validation |
| **skip_validation=True** | Bulk updates from trusted source | No __setattr__ validation |
| **Both** | Maximum speed bulk loading | No validation at all |

### Safe Usage Pattern

```python
# Loading from database (data already validated by DB schema)
with Type_Safe__Config(fast_create=True, skip_validation=True):
    records = []
    for row in database_cursor:
        record = MyRecord()
        record.id   = row['id']
        record.name = row['name']
        record.data = row['data']
        records.append(record)

# Outside context: validation active again
# Any new assignments are validated
records[0].name = user_input  # This IS validated
```

---

## Recursion Guard: Why is_generating() Matters

During schema generation, we create a temporary instance to inspect default values:

```python
# In Type_Safe__Fast_Create__Cache.generate_schema()
temp_instance = target_class()  # Need defaults from a real instance
```

If fast_create is enabled and we're generating the schema for `MyClass`, this would cause infinite recursion:

1. `MyClass()` called
2. fast_create sees config, calls `type_safe_fast_create.create()`
3. `create()` needs schema, calls `get_schema(MyClass)`
4. `get_schema()` generates schema, calls `MyClass()` for defaults
5. GOTO 1 (infinite loop!)

**Solution**: The `generating` set tracks which classes are mid-generation:

```python
def generate_schema(self, target_class):
    self.generating.add(target_class)      # Mark as generating
    try:
        temp_instance = target_class()     # Uses normal path (is_generating=True)
        # ... build schema ...
    finally:
        self.generating.discard(target_class)  # Cleanup
```

And in `Type_Safe.__init__`:
```python
if not type_safe_fast_create_cache.is_generating(type(self)):
    # Only use fast path if NOT generating schema
    type_safe_fast_create.create(self, **kwargs)
```

---

## Summary: Complete File List

### Production Code (in osbot_utils)

```
osbot_utils/type_safe/
├── Type_Safe.py                          # Modified: +9 lines for wiring
└── type_safe_core/
    ├── config/
    │   └── Type_Safe__Config.py          # Context manager for config
    └── fast_create/
        ├── Type_Safe__Fast_Create.py     # Main create() function
        ├── Type_Safe__Fast_Create__Cache.py  # Schema caching
        └── schemas/
            ├── Schema__Type_Safe__Fast_Create__Class.py
            └── Schema__Type_Safe__Fast_Create__Field.py
```

### Test Files

```
tests/unit/type_safe/type_safe_core/fast_create/
├── test_Type_Safe__Fast_Create.py                              # create() method tests
├── test_Type_Safe__Fast_Create__Cache.py                       # Cache/schema tests
├── test_Type_Safe__Fast_Create__created_with_no_side_effects.py # Correctness tests
├── test_Type_Safe__Fast_Create__created_and_cached.py          # __init__ wiring tests
├── test_Type_Safe__Fast_Create__skip_validation_wired.py       # __setattr__ wiring tests
├── test_Type_Safe__Fast_Create__fast_create_side_effects.py    # fast_create trade-offs
├── test_Type_Safe__Fast_Create__skip_validation_side_effects.py # skip_validation trade-offs
├── test_perf__Hypothesis_H__fast_create.py                     # Benchmark: fast_create
├── test_perf__Hypothesis_H__skip_validation.py                 # Benchmark: skip_validation
└── test_perf__Hypothesis_H__fast_create_skip_validation.py     # Benchmark: maximum speed
```

---

## Conclusion

The fast_create optimization is now fully integrated into production Type_Safe with:

1. **Minimal code changes** (~9 lines in Type_Safe.py)
2. **Comprehensive test coverage** (~130+ tests)
3. **Documented trade-offs** (side effects tests)
4. **Performance benchmarks** (3 comparison files)
5. **Safe usage patterns** (context manager scoping)

The optimization is **opt-in** via `Type_Safe__Config`, maintaining full backward compatibility while providing significant performance improvements for bulk operations with trusted data.
