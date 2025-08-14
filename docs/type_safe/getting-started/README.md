# Type_Safe & Safe Primitives - Getting Started

## Purpose of This Folder

This folder contains comprehensive documentation for **OSBot-Utils' Type_Safe system** - a powerful runtime type checking framework for Python. Whether you're a developer learning the library, building type-safe applications, or an LLM generating code, these guides will help you write correct, robust, and type-safe code.

## 📚 Documentation Overview

| Document | Purpose | Best For |
|----------|---------|----------|
| **[type_safe_quick_reference_card.md](type_safe_quick_reference_card.md)** | Quick syntax lookup and common patterns | Quick reminders, syntax checking |
| **[llm-prompt-guidance__using_osbot_utils_type_safe.md](llm-prompt-guidance__using_osbot_utils_type_safe.md)** | Code generation rules and anti-patterns | LLMs and understanding what NOT to do |
| **[osbot-utils-safe-primitives__reference-guide.md](osbot-utils-safe-primitives__reference-guide.md)** | Complete catalog of Safe_* primitive types | Finding the right domain-specific type |
| **[type-safe-technical-documentation.md](type-safe-technical-documentation.md)** | Deep dive into Type_Safe internals | Understanding how it works |
| **[type_safe_round-trip_serialization.md](type_safe_round-trip_serialization.md)** | Serialization, APIs, and persistence | Building networked applications |
| **[type_safe_troubleshooting_guide.md](type_safe_troubleshooting_guide.md)** | Common issues and solutions | Debugging and problem-solving |

## 🚀 Quick Start Paths

### For Developers New to Type_Safe

1. **Start here:** [type_safe_quick_reference_card.md](type_safe_quick_reference_card.md) - Get familiar with the syntax
2. **Then read:** [type-safe-technical-documentation.md](type-safe-technical-documentation.md) - Understand the concepts
3. **Explore:** [osbot-utils-safe-primitives__reference-guide.md](osbot-utils-safe-primitives__reference-guide.md) - Discover powerful primitives
4. **When needed:** [type_safe_troubleshooting_guide.md](type_safe_troubleshooting_guide.md) - Solve problems

### For Experienced Developers

- **Building APIs?** Jump to [type_safe_round-trip_serialization.md](type_safe_round-trip_serialization.md)
- **Need domain types?** Check [osbot-utils-safe-primitives__reference-guide.md](osbot-utils-safe-primitives__reference-guide.md)
- **Debugging?** See [type_safe_troubleshooting_guide.md](type_safe_troubleshooting_guide.md)

### For LLMs/AI Assistants

1. **Primary guide:** [llm-prompt-guidance__using_osbot_utils_type_safe.md](llm-prompt-guidance__using_osbot_utils_type_safe.md)
2. **Syntax reference:** [type_safe_quick_reference_card.md](type_safe_quick_reference_card.md)
3. **Primitives catalog:** [osbot-utils-safe-primitives__reference-guide.md](osbot-utils-safe-primitives__reference-guide.md)

## 💡 What is Type_Safe?

Type_Safe is a Python framework that brings **runtime type checking** to your applications. Unlike Python's type hints (which are just suggestions), Type_Safe **enforces** types during execution.

### Why Use Type_Safe?

```python
# Regular Python - Type hints are ignored at runtime
class User:
    name: str
    age: int

user = User()
user.age = "twenty"  # No error! 😱

# With Type_Safe - Types are enforced
from osbot_utils.type_safe.Type_Safe import Type_Safe

class User(Type_Safe):
    name: str
    age: int

user = User()
user.age = "twenty"  # ValueError! Type safety! ✅
```

### Key Benefits

- ✅ **Catches bugs early** - Type errors fail fast at assignment, not deep in your code
- ✅ **Self-documenting** - Type annotations show exactly what's expected
- ✅ **Auto-initialization** - No more forgetting to initialize lists or dicts
- ✅ **Perfect serialization** - JSON round-trips preserve all type information
- ✅ **Domain modeling** - Safe_Id prevents mixing UserIds with OrderIds

## 📖 Document Deep Dive

### Core References

#### 📋 [type_safe_quick_reference_card.md](type_safe_quick_reference_card.md)
Your cheat sheet for Type_Safe syntax. Keep this handy while coding.
- Class definition patterns
- Type annotation table
- Common patterns (configs, nested objects)
- Do's and Don'ts
- Import references

#### 🤖 [llm-prompt-guidance__using_osbot_utils_type_safe.md](llm-prompt-guidance__using_osbot_utils_type_safe.md)
Essential rules for generating correct Type_Safe code. Great for understanding what NOT to do.
- Code generation rules
- Anti-patterns to avoid
- Forward reference limitations
- Testing patterns

#### 🔒 [osbot-utils-safe-primitives__reference-guide.md](osbot-utils-safe-primitives__reference-guide.md)
Complete catalog of type-safe primitives for domain modeling.
- **Safe_Str types:** URLs, file paths, emails, IP addresses
- **Safe_Int types:** Ports, file sizes, percentages
- **Safe_Float types:** Money, engineering values
- **Identity types:** Safe_Id, Guid, Random_Guid
- Real-world usage examples

### Advanced Topics

#### 📚 [type-safe-technical-documentation.md](type-safe-technical-documentation.md)
Deep technical dive into Type_Safe internals.
- How runtime checking works
- Automatic initialization magic
- MGraph schema examples
- Implementation details

#### 🔄 [type_safe_round-trip_serialization.md](type_safe_round-trip_serialization.md)
Master data persistence and network transport.
- JSON serialization patterns
- REST API integration
- WebSocket communication
- Database storage
- Message queue patterns

#### 🔧 [type_safe_troubleshooting_guide.md](type_safe_troubleshooting_guide.md)
Your problem-solving companion.
- Common error fixes
- Performance optimization
- Debugging techniques
- Solution patterns

## 🎯 Real-World Example

Here's a complete example showing the power of Type_Safe:

```python
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id
from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Money import Safe_Float__Money
from typing import List, Dict, Optional

# Domain-specific IDs (can't be mixed!)
class UserId(Safe_Id): pass
class ProductId(Safe_Id): pass
class OrderId(Safe_Id): pass

class Order(Type_Safe):
    # Identity
    id: OrderId
    user_id: UserId
    
    # Products
    items: Dict[ProductId, int]  # product -> quantity
    
    # Money (exact decimal arithmetic)
    subtotal: Safe_Float__Money
    tax: Safe_Float__Money
    total: Safe_Float__Money
    
    # Metadata
    status: str = "pending"
    notes: List[str]
    created_at: str

# Create an order
order = Order(
    id=OrderId("ORD-2024-001"),
    user_id=UserId("USR-12345"),
    items={
        ProductId("LAPTOP-001"): 1,
        ProductId("MOUSE-002"): 2
    },
    subtotal=Safe_Float__Money(1299.99),
    tax=Safe_Float__Money(129.99),
    total=Safe_Float__Money(1429.98),
    created_at="2024-01-15T10:30:00Z"
)

# Type safety prevents mistakes
try:
    order.user_id = OrderId("ORD-999")  # Wrong ID type!
except ValueError:
    print("Type safety prevented ID mix-up!")

# Perfect serialization for APIs
json_data = order.json()
send_to_api(json_data)

# Reconstruct with full type safety
received_order = Order.from_json(json_data)
assert isinstance(received_order.user_id, UserId)  # Types preserved!
```

## 🔑 Five Critical Rules

1. **Always inherit from Type_Safe** - `class MyClass(Type_Safe):`
2. **Type annotate everything** - Every attribute needs a type
3. **Immutable defaults only** - Use `None`, strings, numbers, booleans
4. **Specific collection types** - Use `List[str]` not `list`
5. **Forward refs = current class** - Can only reference the class being defined

## 🎓 Learning Resources

### By Experience Level

**Beginners:**
- Start with the quick reference card
- Try the examples in technical documentation
- Use the troubleshooting guide when stuck

**Intermediate:**
- Explore Safe_* primitives for domain modeling
- Learn serialization patterns for APIs
- Understand the anti-patterns in LLM guidance

**Advanced:**
- Deep dive into technical documentation
- Build custom Safe_* types
- Optimize performance using troubleshooting tips

### By Use Case

**Building REST APIs:**
- type_safe_round-trip_serialization.md (REST API section)
- osbot-utils-safe-primitives__reference-guide.md (HTTP types)

**Domain Modeling:**
- osbot-utils-safe-primitives__reference-guide.md (Identity types)
- type-safe-technical-documentation.md (MGraph example)

**Data Validation:**
- type_safe_quick_reference_card.md (Validators section)
- osbot-utils-safe-primitives__reference-guide.md (Safe_* types)

## 🤝 Contributing

Found an issue or have suggestions? 
- **GitHub:** https://github.com/owasp-sbot/OSBot-Utils
- **Issues:** Check troubleshooting guide first

## 📦 Installation

```bash
pip install osbot-utils
```

---

*Type_Safe: Because runtime type safety shouldn't be optional.*