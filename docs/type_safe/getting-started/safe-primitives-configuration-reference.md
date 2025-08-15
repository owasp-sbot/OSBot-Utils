# Safe Primitives Configuration Reference

## Introduction

The OSBot-Utils Safe Primitives library provides a comprehensive set of type-safe wrappers around Python's built-in types (`str`, `int`, `float`). Each primitive class is designed with specific validation rules, sanitization patterns, and domain constraints that make them suitable for particular use cases in production applications.

This reference guide provides a complete overview of all configuration options and validation rules for each Safe Primitive class, extracted directly from the source code. Understanding these properties is essential for:

- **Choosing the right primitive** for your specific use case
- **Understanding validation behavior** and what values will be accepted or rejected  
- **Debugging issues** when values are transformed or validation fails
- **Extending the library** with your own domain-specific primitives

### How to Read These Tables

Each primitive type has specific configuration properties that control its behavior:

- **Max Length**: Maximum allowed length for string values (where applicable)
- **Regex**: Regular expression pattern used for validation or sanitization
- **Regex Mode**: How the regex is applied - `REPLACE` (sanitize) or `MATCH` (validate)
- **Allow Empty/None**: Whether empty strings or None values are permitted
- **Strict Validation**: Whether invalid input raises an error (strict) or gets sanitized (non-strict)
- **Min/Max Value**: Numeric range constraints for integer and float types
- **Decimal Places**: Precision control for floating-point operations
- **Use Decimal**: Whether to use Python's `Decimal` class for exact arithmetic (vs binary float)

### Key Patterns to Note

1. **Sanitization vs Validation**: Most string primitives use `REPLACE` mode to sanitize input, while cryptographic types use `MATCH` mode with strict validation
2. **Domain-Specific Constraints**: Each primitive encodes domain knowledge (e.g., `Safe_UInt__Port` enforces 0-65535 range)
3. **Security by Default**: Dangerous characters are automatically removed or rejected based on the context
4. **Performance vs Precision Trade-offs**: Financial types use `Decimal` for exactness, while engineering types use binary floats for performance

The tables below provide the complete configuration for every Safe Primitive class in the library, organized by category.

### 1) Safe\_Str-based primitives
| Class                           | Max Length | Regex                                  | Regex Mode                     | Allow Empty | Strict Validation | Notes                                                        |                                                                                         |
| ------------------------------- | ---------: | -------------------------------------- | ------------------------------ | :---------: | :---------------: | ------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| Safe_Str                      |        512 | [^a-zA-Z0-9]                         | REPLACE                        |      ✅      |         ❌         | Base defaults                                                |                                                                                         |
| Safe_Str__File__Name          |        512 | [^a-zA-Z0-9_\-. ]                    | REPLACE                        |      ❌      |         ❌         | Filename-safe chars                                          |                                                                                         |
| Safe_Str__File__Path          |       1024 | [^a-zA-Z0-9_\-./\\ ]                 | REPLACE                        |      ✅      |         ❌         | Allows / and \                                           |                                                                                         |
| Safe_Str__Url                 |       2048 | \^(?!https?://).\*                    | \[^a-zA-Z0-9:/-.\_\~&=?#+%@]\ |   REPLACE   |         ✅         | ❌                                                            | Pattern blocks raw text starting without http(s):// segment and filters invalid chars |
| Safe_Str__IP_Address          |          — | —                                      | —                              |      ✅      |         —         | Validated via ipaddress.ip_address() (IPv4/IPv6)           |                                                                                         |
| Safe_Str__Http__Content_Type  |        256 | [^a-zA-Z0-9/\-+.;= ]                 | REPLACE                        |      ❌      |         ❌         | MIME-like tokens                                             |                                                                                         |
| Safe_Str__Http__ETag          |        128 | [^a-zA-Z0-9"\/\-_.:]                 | REPLACE                        |      ✅      |         ❌         | Allows quoted, weak ETags                                    |                                                                                         |
| Safe_Str__Http__Last_Modified |         64 | [^a-zA-Z0-9:, -]                     | REPLACE                        |      ✅      |         ❌         | Date-ish header text                                         |                                                                                         |
| Safe_Str__Http__Text          |    1048576 | [\x00\x01-\x08\x0B\x0C\x0E-\x1F\x7F] | REPLACE                        |      ✅      |         ❌         | Removes control chars; normalizes newlines                   |                                                                                         |
| Safe_Str__Html                |    1048576 | [\x00\x01-\x08\x0B\x0C\x0E-\x1F]     | REPLACE                        |      ✅      |         ❌         | Minimal filtering for HTML                                   |                                                                                         |
| Safe_Str__Hash                |         10 | [^a-fA-F0-9]                         | REPLACE                        |      ❌      |         ✅         | Exactly 10 hex chars (via exact_length=True)               |                                                                                         |
| Safe_Str__SHA1                |         40 | ^[a-fA-F0-9]{40}$                    | MATCH                          |      ❌      |         ✅         | Full SHA-1                                                   |                                                                                         |
| Safe_Str__SHA1__Short         |          7 | ^[a-fA-F0-9]{7}$                     | MATCH                          |      ❌      |         ✅         | Short SHA                                                    |                                                                                         |
| Safe_Str__NaCl__Private_Key   |         64 | ^[a-fA-F0-9]{64}$                    | MATCH                          |      ❌      |         ✅         | 32-byte key as 64 hex                                        |                                                                                         |
| Safe_Str__NaCl__Public_Key    |         64 | ^[a-fA-F0-9]{64}$                    | MATCH                          |      ❌      |         ✅         | 32-byte key as 64 hex                                        |                                                                                         |
| Safe_Str__Git__Ref_Base       |        255 | [\x00-\x1f\x7f ~^:?*\[\]\\]          | REPLACE                        |      ❌      |         ❌         | Also enforces git ref rules (no .., @{}, etc.)           |                                                                                         |
| Safe_Str__Git__Branch         |        255 | [\x00-\x1f\x7f ~^:?*\[\]\\]          | REPLACE                        |      ❌      |         ❌         | Plus: cannot start with -                                  |                                                                                         |
| Safe_Str__Git__Tag            |        255 | [\x00-\x1f\x7f ~^:?*\[\]\\]          | REPLACE                        |      ❌      |         ❌         | Tag = same ref rules                                         |                                                                                         |
| Safe_Str__Git__Ref            |        255 | —                                      | —                              |      ❌      |         —         | Accepts if any of: SHA1, short SHA, valid branch, or tag |                                                                                         |
| Safe_Str__Version             |         12 | ^v(\d{1,3})\.(\d{1,3})\.(\d{1,3})$   | MATCH                          |      ❌      |         ✅         | Versions like v1.2.3                                       |                                                                                         |
| Safe_Str__GitHub__Repo        |        140 | [^a-zA-Z0-9\-_./]                    | REPLACE                        |      ❌      |         ❌         | Must be owner/repo; each part further validated            |                                                                                         |
| Safe_Str__GitHub__Repo_Name   |        100 | [^a-zA-Z0-9\-_.]                     | REPLACE                        |      ❌      |         ❌         | Extra guards against ./.. names                          |                                                                                         |
| Safe_Str__GitHub__Repo_Owner  |         39 | [^a-zA-Z0-9\-]                       | REPLACE                        |      ❌      |         ❌         | No leading/trailing or double hyphens                        |                                                                                         |
---
### 2) Safe\_Int / Safe\_UInt primitives
| Class                   | Min Value | Max Value | Allow None | Allow Bool | Allow Str | Strict Type | Notes                                   |
| ----------------------- | --------: | --------: | :--------: | :--------: | :-------: | :---------: | --------------------------------------- |
| Safe_Int              |         — |         — |      ✅     |      ❌     |     ✅     |      ❌      | Converts str → int; range checks if set |
| Safe_UInt             |         0 |         — |      ✅     |      ❌     |     ✅     |      ❌      | Unsigned base                           |
| Safe_UInt__Byte       |         0 |       255 |      ✅     |      ❌     |     ✅     |      ❌      | 1-byte range                            |
| Safe_UInt__Port       |         0 |     65535 |      ❌     |      ❌     |     ✅     |      ❌      | Disallows None; standard port range   |
| Safe_UInt__FileSize   |         0 |    2^63−1 |      ✅     |      ❌     |     ✅     |      ❌      | Has .to_kb()/.to_mb()/.to_gb()        |
| Safe_UInt__Percentage |         0 |       100 |      ✅     |      ❌     |     ✅     |      ❌      | Percent 0–100                           |
---
### 3) Safe\_Float primitives
| Class                          | Min Value | Max Value | Decimal Places | Use Decimal | Epsilon | Round Output | Clamp To Range | Allow None | Allow Str | Allow Int | Allow Bool | Notes                                        |
| ------------------------------ | --------: | --------: | -------------: | :---------: | ------: | :----------: | :------------: | :--------: | :-------: | :-------: | :--------: | -------------------------------------------- |
| Safe_Float                   |         — |         — |              — |      ❌      |    1e-9 |       ✅      |        ❌       |      ✅     |     ✅     |     ✅     |      ❌     | Core float with range/precision options      |
| Safe_Float__Money            |       0.0 |         — |              2 |      ✅      |    1e-9 |       ✅      |        ❌       |      ✅     |     ✅     |     ✅     |      ❌     | Exact cents via Decimal                    |
| Safe_Float__Percentage_Exact |       0.0 |     100.0 |              2 |      ✅      |    1e-9 |       ✅      |        ❌       |      ✅     |     ✅     |     ✅     |      ❌     | Exact percentage domain                      |
| Safe_Float__Engineering      |         — |         — |              — |      ❌      |    1e-6 |       ✅      |        ❌       |      ✅     |     ✅     |     ✅     |      ❌     | Perf-focused (binary float), tighter epsilon |
---
### 4) Identifiers / Misc
| Class               | Max Length | Validation / Behavior                             | Notes                                   |
| ------------------- | ---------: | ------------------------------------------------- | --------------------------------------- |
| Safe_Id           |        512 | Sanitized via safe_id() ([^a-zA-Z0-9_-])      | Auto-generates safe ID if none provided |
| Guid              |          — | If string is GUID → keep; else UUID5 in namespace | Deterministic for same input            |
| Random_Guid       |          — | Requires valid GUID; generates if none            | Uses random_guid()                    |
| Random_Guid_Short |          — | Short ID generator                                | Uses random_guid_short()              |
| Timestamp_Now     |          — | Current Unix timestamp if none                    | Inherits int                          |
---