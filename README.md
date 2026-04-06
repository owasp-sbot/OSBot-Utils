# OSBot-Utils

![Current Release](https://img.shields.io/badge/release-v3.72.3-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Type-Safe](https://img.shields.io/badge/Type--Safe-✓-brightgreen)
![Caching](https://img.shields.io/badge/Caching-Built--In-orange)
[![codecov](https://codecov.io/gh/owasp-sbot/OSBot-Utils/graph/badge.svg?token=GNVW0COX1N)](https://codecov.io/gh/owasp-sbot/OSBot-Utils)

A comprehensive Python utility toolkit providing **Type-Safe primitives**, decorators, caching layers, HTML/AST helpers, SQLite tooling, SSH execution, LLM request pipelines, tracing, and more — all designed to accelerate building robust, maintainable automation and integration code.

---

## ✨ Key Features

* **🛡️ Type-Safe First**: Strongly typed primitives (`Safe_Str`, `Safe_Int`, `Safe_Float`, etc.) with validation and sanitization
* **⚡ Multi-layer Caching**: In-memory, per-instance, pickle-on-disk, temp-file, and request/response caches
* **🗂️ Rich Utilities**: Helpers for HTML parsing/rendering, AST inspection, SSH/SCP execution, SQLite schema management, and more
* **🧠 LLM Support**: Structured request builders, OpenAI API integration, schema enforcement, and persistent cache
* **🔍 Tracing & Debugging**: Full function call tracing with configurable depth, locals capture, and pretty output
* **🧪 Testing Utilities**: Temp SQLite DBs, mockable caches, and easy test helpers

---

## 📦 Installation

```bash
pip install osbot-utils
```

From source:

```bash
pip install git+https://github.com/owasp-sbot/OSBot-Utils.git@dev
```

---

## 🚀 Quick Start

### Using Type-Safe Primitives

```python
from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str

class Username(Safe_Str):
    max_length = 20

print(Username("alice"))  # 'alice'
print(Username("invalid username!"))  # 'invalid_username_'
```

---

### Simple In-Memory Caching

```python
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

class DataFetcher:
    @cache_on_self
    def fetch(self, x):
        print("Fetching…")
        return x * 2

fetcher = DataFetcher()
fetcher.fetch(10)  # Calls method
fetcher.fetch(10)  # Returns cached result
```

---

### HTML Parsing

```python
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict import html_to_dict

html_code = "<html><body><h1>Hello</h1></body></html>"
print(html_to_dict(html_code))
```

---

### SQLite Dynamic Table

```python
from osbot_utils.helpers.sqlite.Temp_Sqlite__Table import Temp_Sqlite__Table

with Temp_Sqlite__Table() as table:
    table.row_schema = type("Row", (), {"name": str, "age": int})
    table.create()
    table.add_row_and_commit(name="Alice", age=30)
    print(table.rows())
```

---

### LLM Request Execution

```python
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.actions.LLM_Request__Execute import LLM_Request__Execute

builder = LLM_Request__Builder__Open_AI()
builder.set__model__gpt_4o().add_message__user("Say hi in JSON")

executor = LLM_Request__Execute(request_builder=builder)
response = executor.execute(builder.llm_request())
print(response.response_data)
```

---

## 🏗️ Architecture

OSBot-Utils is organized into core **Type-Safe foundations** with layered utilities for different domains:

```
┌──────────────────────────────────────────────┐
│                 Your Code                     │
│  ┌───────────┐  ┌─────────────┐  ┌──────────┐ │
│  │ Type-Safe │  │  Decorators │  │  Helpers │ │
│  │ Primitives│  │  & Caching  │  │ (HTML,   │ │
│  │           │  │             │  │  AST,   │ │
│  │           │  │             │  │  SQLite)│ │
│  └───────────┘  └─────────────┘  └──────────┘ │
└──────────────────────────┬───────────────────┘
                           │
┌──────────────────────────▼───────────────────┐
│                OSBot-Utils                    │
│  ┌────────────────────────────────────────┐  │
│  │       Type-Safe Core Classes           │  │
│  │  Validation / Sanitization / Defaults  │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │    Caching Layers & Decorators         │  │
│  │  @cache, @cache_on_self, pickle, tmp   │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ Domain Helpers                          │ │
│  │ HTML, AST, SSH, LLMs, SQLite, Tracing   │ │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

---

## 📚 Key Modules

* **`helpers/safe_*`** — Type-Safe primitives for validated strings, ints, floats
* **`decorators/methods`** — Caching, exception capture, timing, validation
* **`helpers/html`** — HTML ↔ dict ↔ tag classes
* **`helpers/ast`** — Python AST parsing, visiting, merging
* **`helpers/sqlite`** — High-level SQLite APIs, schema generation, temp DBs
* **`helpers/ssh`** — SSH/SCP execution with caching
* **`helpers/llms`** — LLM request/response handling with caching
* **`helpers/trace`** — Function call tracing with configurable output

---

## 🎯 Benefits

### For Developers

* Strong runtime type validation with Type-Safe classes
* Consistent patterns for caching and decorators
* Rich helper library to avoid reinventing the wheel

### For Production

* Deterministic caching with persistence options
* Safe, validated data structures at integration boundaries
* Lightweight, dependency-minimal utilities

### For Teams

* Standardized approach to cross-cutting concerns (logging, tracing, caching)
* Modular helpers to fit many contexts (CLI, web apps, serverless)

---

## 🤝 Contributing

Pull requests are welcome!
Check existing patterns in `/helpers` and `/decorators` for style guidance.

---

## 📄 License

Licensed under the Apache 2.0 License.
