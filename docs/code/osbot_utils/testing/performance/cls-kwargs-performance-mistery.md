# The cls_kwargs Performance Mystery: A Technical Analysis

- Part 1 is Claude 3.5's analysis of the mystery
- Part 2 is ChatGPT o1's analysis of Part 1
- Part 3 is ChatGPT o1's analysis of the dis (disassembly) diff

------ 

# Part 1 - Claude 3.5's analysis of the mystery 

## The Problem

During a refactoring exercise of the Type_Safe class, we encountered an unexpected performance improvement when moving the `__cls_kwargs__` method into a separate cache class. What makes this particularly interesting is that the improvement occurred without adding any actual caching logic - we simply moved the exact same code into a different location.

## Performance Testing Framework

This mystery was discovered thanks to the `Performance_Measure__Session` testing framework, which provides nanosecond-precision timing measurements and statistical analysis. Here's the key test that revealed the difference:

```python
def test_measure(self):
    class An_Class_1():
        pass

    class An_Class_2(Type_Safe):
        pass

    class An_Class_3(Type_Safe):
        an_int : int

    class An_Class_4(Type_Safe):
        an_int : int = 42

    class An_Class_5(Type_Safe):
        an_str: str

    class An_Class_6(Type_Safe):
        an_str: str = '42'

    Performance_Measure__Session().measure(str        ).assert_time(time_100_ns)
    Performance_Measure__Session().measure(Random_Guid).assert_time(time_6_kns)
    Performance_Measure__Session().measure(An_Class_1 ).assert_time(time_100_ns)
    Performance_Measure__Session().measure(An_Class_2 ).assert_time(time_5_kns, time_6_kns)
    Performance_Measure__Session().measure(An_Class_3 ).assert_time(time_20_kns)
    Performance_Measure__Session().measure(An_Class_4 ).assert_time(time_10_kns, time_20_kns)
    Performance_Measure__Session().measure(An_Class_5 ).assert_time(time_20_kns)
    Performance_Measure__Session().measure(An_Class_6 ).assert_time(time_10_kns, time_20_kns)
```

This test is particularly effective because it:
1. Tests a range of scenarios from simple to complex
2. Uses consistent baseline measurements (str, Random_Guid)
3. Provides nanosecond-level precision
4. Includes multiple runs to ensure statistical significance
5. Tests both with and without type annotations
6. Tests both with and without default values

## Performance Results

### Original Implementation (in Type_Safe class):
```
str          | score:     100 ns  | raw:      79 ns
Random_Guid  | score:   6,000 ns  | raw:   5,552 ns
An_Class_1   | score:     100 ns  | raw:     128 ns
An_Class_2   | score:   6,000 ns  | raw:   5,581 ns
An_Class_3   | score:  20,000 ns  | raw:  16,267 ns
An_Class_4   | score:  20,000 ns  | raw:  15,422 ns
An_Class_5   | score:  20,000 ns  | raw:  16,294 ns
An_Class_6   | score:  20,000 ns  | raw:  15,466 ns
```

### Refactored Implementation (with Cache__Class_Kwargs):
```
str          | score:     100 ns  | raw:      79 ns
Random_Guid  | score:   6,000 ns  | raw:   5,594 ns
An_Class_1   | score:     100 ns  | raw:     131 ns
An_Class_2   | score:   5,000 ns  | raw:   5,168 ns
An_Class_3   | score:  20,000 ns  | raw:  15,914 ns
An_Class_4   | score:  10,000 ns  | raw:  14,885 ns
An_Class_5   | score:  20,000 ns  | raw:  15,955 ns
An_Class_6   | score:  10,000 ns  | raw:  14,997 ns
```

Key differences:
- An_Class_2: Improved from 6,000ns to 5,000ns
- An_Class_4: Improved from 20,000ns to 10,000ns
- An_Class_6: Improved from 20,000ns to 10,000ns

## Code Comparison

### Original Version (Inside Type_Safe)

```python
class Type_Safe:
    # [468 lines of other code...]
    
    @classmethod
    def __cls_kwargs__(cls, include_base_classes=True):
        kwargs = {}
        for base_cls in inspect.getmro(cls):
            if base_cls is object:
                continue
            for k, v in vars(base_cls).items():
                if not k.startswith('__') and not isinstance(v, types.FunctionType):
                    if isinstance(v, classmethod):
                        continue
                    if type(v) is functools._lru_cache_wrapper:
                        continue
                    if isinstance(v, property):
                        continue
                    if (k in kwargs) is False:
                        kwargs[k] = v
            
            if hasattr(base_cls,'__annotations__'):
                for var_name, var_type in base_cls.__annotations__.items():
                    # [type checking and validation logic...]
                    
            if include_base_classes is False:
                break
        return kwargs
```

### Refactored Version

```python
# In Cache__Class_Kwargs.py
class Cache__Class_Kwargs:
    def get_cls_kwargs(self, cls: Type, include_base_classes: bool = True) -> Dict[str, Any]:
        # [Exact same code as above]
        return kwargs

cache__class_kwargs = Cache__Class_Kwargs()

# In Type_Safe.py
class Type_Safe:
    @classmethod
    def __cls_kwargs__(cls, include_base_classes=True):
        return cache__class_kwargs.get_cls_kwargs(cls, include_base_classes)
```

## Hypotheses

1. **Scope and Variable Resolution**
   - The original version needs to resolve variables in the context of a large class
   - In the refactored version, all variables are in a tighter, more focused scope
   - Could lead to faster variable lookups and resolution

2. **Method Dispatch Overhead**
   - The original @classmethod needs to go through Python's method resolution order
   - The standalone cache class has a simpler method dispatch path
   - Might reduce lookup time for method calls

3. **Memory Locality**
   - The original version is part of a large class (478 lines)
   - The refactored version is in its own small module
   - Could lead to better memory locality and cache performance

4. **Context Switching**
   - The original version switches context between class and instance methods
   - The refactored version maintains a consistent execution context
   - Might reduce context switching overhead

5. **Class Dictionary Access**
   - The original version interacts with a larger class dictionary
   - The refactored version has a smaller, more focused scope
   - Could improve dictionary lookup times

## Next Steps

To validate these hypotheses, we could:
1. Add fine-grained timing around variable lookups
2. Profile memory access patterns
3. Measure method dispatch times
4. Test with different class sizes
5. Analyze Python bytecode differences

## The Power of Performance Testing

This case study demonstrates why having comprehensive performance tests is crucial:

1. **Detection**: The performance difference was only noticed because we had precise timing tests
2. **Validation**: The tests provided confidence that the refactoring was beneficial
3. **Regression Prevention**: The tests will catch any future performance degradation
4. **Measurement**: The nanosecond-level precision helped identify subtle improvements
5. **Comparison**: The consistent baseline measurements (str, Random_Guid) provided context

The `Performance_Measure__Session` class played a key role by:
- Providing statistical analysis of measurements
- Using Fibonacci sequences for measurement loops (1,2,3,5,8,13,21...)
- Handling outlier detection
- Normalizing scores for consistent results
- Supporting both raw and normalized timing comparisons

This level of testing precision was essential for spotting this unexpected performance improvement, which might have gone unnoticed with less rigorous testing.



-----

# Part 2: ChatGPT o1's analysis of Part 1

It's one of those pleasant mysteries in dynamic languages where “the same code” can run faster (or slower) just by living in a different location. Since the Python runtime is always juggling multiple layers of lookups (class dicts, instance dicts, method resolution order, etc.), even minor changes to scoping or where the code physically resides can shift performance in small but measurable ways. Below are likely contributors:

---

## 1. Python’s Method Lookup & Class Scope

- **Method Resolution Overhead**  
  A `@classmethod` inside a class must pass through Python’s method resolution pipeline, which checks each class in `mro()`, ensures the method is indeed a classmethod, then finally calls it.  
  - In the refactored version, `get_cls_kwargs` is just a plain old instance method on a separate helper object. That means you sidestep some of the overhead that Python’s built-in descriptor protocol can add, especially once you combine `@classmethod` with a large base class.

- **Class Dictionary Size**  
  When a method lives in a massive class like `Type_Safe` (hundreds of lines, plus inheritance from who-knows-what), Python’s internal dictionary of attributes is larger. That dictionary is consulted to find attributes, which can be microscopically slower than a smaller dictionary. Moving the same logic to `Cache__Class_Kwargs` means a new, smaller dictionary for attribute lookups.

---

## 2. Code Object & Memory Locality

- **Code Object Split**  
  Each function or method in Python is compiled into a `code` object with certain metadata. A huge class can accumulate multiple `code` objects, docstrings, decorators, etc.  Tools like CPython’s instruction cache or the CPU’s L1/L2 caches might better handle the smaller code object in a dedicated file (`Cache__Class_Kwargs.py`) than that same code nested deep within `Type_Safe`.

- **Better Instruction / Data Caching**  
  Modern CPU caches can sometimes see a difference between code that’s near other “hot” or frequently-used code vs. code that’s in a large class with many definitions. Although Python isn’t generally JIT-compiled in CPython, there’s still some interplay with how the CPU fetches and caches instructions. If your refactored code is in a smaller module, there’s a chance the CPU or Python’s memory layout hits some sweet spot.

---

## 3. Variable Lookups and Closure Context

- **Simpler Variable Resolution**  
  Inside a huge class, references like `vars(base_cls)` or `base_cls.__annotations__` may be resolved through slightly more complicated scoping rules. A dedicated helper class may have fewer local variables, fewer closures, or fewer references in scope.  
  - Even something as small as an additional local variable name in the `Type_Safe` scope can add overhead. Python’s symbol table, closure references, and the internal `_PyEval_EvalFrame` function all have incremental overhead as they handle more named references.

- **Class vs. Instance Execution Context**  
  When `__cls_kwargs__` is called as `Type_Safe.__cls_kwargs__`, Python sets up the call in a way that includes the class as the first argument (`cls`). With the separate helper, it’s a normal method call on the `cache__class_kwargs` object. The difference is small, but everything from the descriptor call to how the “self” or “cls” is bound can show up in nanosecond-level tests.

---

## 4. Subtle Artifacts in Your Testing Framework

- **Performance Measurement Structure**  
  Sometimes, test harness structure alone can create slight differences in how Python executes or JIT-optimizes built-ins (in PyPy, for instance). Although you mention the code and logic is identical, the function references, import lines, or the order of how the classes are loaded may cause the runtime to warm up differently.  
  - If the `Cache__Class_Kwargs` file is imported earlier (or differently) in your tests, it might get better CPU cache locality or skip some overhead. If it’s imported lazily, the overhead might appear in a different place, ironically making the measured part look faster.

---

## 5. Confirmation via Bytecode Inspection

If you’re curious, you can do:

```python
import dis
dis.dis(Type_Safe.__cls_kwargs__)
dis.dis(cache__class_kwargs.get_cls_kwargs)
```

While they might look extremely similar, you could see differences in:
- **LOAD_GLOBAL vs. LOAD_FAST**  
- Extra steps in `classmethod` dispatch  
- Additional name lookups (like `inspect.getmro`)  
- How references to `cls` or `self` are loaded

Even small differences in the order or frequency of LOAD/STORE opcodes can alter performance at the nanosecond scale.

---

## Conclusion

At the end of the day, you’re seeing a classic Python micro-optimization scenario: code that is “logically the same” but runs faster simply due to changes in how Python looks up and executes that code. The big takeaways:

1. **Method resolution & scope** matter a lot in Python.  
2. **Moving code to a dedicated helper** can reduce overhead in surprising ways.  
3. **Performance tests at the nanosecond level** will reveal these subtle differences.  

It’s great you have a test harness like `Performance_Measure__Session()` to catch these anomalies—this is exactly how unexpected performance gains (or losses) are often discovered in dynamic environments like Python.

-----

# Part 3 - ChatGPT o1's analysis of the dis (disassembly) diff

A close look at the disassembly shows that in **Type_Safe.__cls_kwargs__** you are effectively doing extra work at function‐call time (building tuples, importing modules into local scope, etc.) whereas in **cache__class_kwargs.get_cls_kwargs** those same references are loaded from the global/module scope rather than being reconstructed on every call.

---

## 1. Building `IMMUTABLE_TYPES` Each Time

In `Type_Safe.__cls_kwargs__`, you see instructions like:

```none
130          42 LOAD_GLOBAL             12 (bool)
             ...
             144 BUILD_TUPLE             11
             146 STORE_FAST               6 (IMMUTABLE_TYPES)
```

That means every time `__cls_kwargs__` is called, it’s building an 11‐element tuple in the function itself and storing it in a local variable. By contrast, the second disassembly (from `cache__class_kwargs.get_cls_kwargs`) just does:

```none
...
60     >>  926 LOAD_FAST  8 (var_type)
            LOAD_GLOBAL 46 (IMMUTABLE_TYPES)
            CONTAINS_OP 1
...
```

There is **no BUILD_TUPLE** in the second version. `IMMUTABLE_TYPES` is presumably defined once at the module or class level and referenced as a global rather than reconstructed every time the method runs.

Even though building a small tuple is “fast” in Python, it can still cost a few hundred nanoseconds or more in a tight loop. In a microbenchmark, that’s enough overhead to register as a difference.

---

## 2. Re-importing and Storing Modules in Locals

You’ll see lines like:

```none
125           2 LOAD_CONST 1 (0)
              4 LOAD_CONST 0 (None)
              6 IMPORT_NAME 0 (functools)
              8 STORE_FAST 2 (functools)
...
```

This appears in the **Type_Safe.__cls_kwargs__** disassembly but not in `cache__class_kwargs`. It indicates that your “original” method code is using local imports or assigning modules to local variables inside the function. That is overhead each time the function is invoked (or each time the code object is executed). In the refactored version, you simply do:

```none
LOAD_GLOBAL X (functools)
```

at call time, which is typically faster than the pattern “import the module + store it in a local variable” on each invocation.

---

## 3. Net Effect: Fewer Instructions & Fewer Name Lookups

If you skim the second disassembly, you’ll notice:

1. Fewer `BUILD_TUPLE` or `IMPORT_NAME` instructions  
2. More direct `LOAD_GLOBAL` references to already imported objects  
3. A shorter sequence of opcodes overall  

All of that can easily trim a few microseconds or nanoseconds from your function. It’s a classic Python micro-optimization scenario: the same high-level “logic” is present, but small differences in how modules/constants are declared or accessed translate into measureable changes in raw speed.

---

## Bottom Line

Even though the **logic** is the same, the **implementation details** in the original `Type_Safe` method cause it to do extra work during each call—building tuples, local imports, etc. The refactored “cache” version avoids that and just does **fewer opcodes** on each invocation. That’s almost certainly the main source of your unexpected but welcome performance boost.