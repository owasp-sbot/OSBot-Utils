"""
Timestamp Capture - Type_Safe Integration
==========================================

Type_Safe compatible version of the timestamp capture system,
designed for integration with the Html_MGraph pipeline.

Key Features:
- Inherits from Type_Safe for consistency with codebase
- Stack-walking to find collector (no signature changes needed)
- Minimal overhead when collector not present
- Rich timing data with aggregation

Integration Example:
    # In Html__To__Html_MGraph__Document
    @timestamp
    def convert(self, html: str) -> Html_MGraph__Document:
        ...

    @timestamp
    def _process_body(self, ...):
        ...

    # In test or profiling code
    _timestamp_collector_ = Timestamp_Collector()
    with _timestamp_collector_:
        doc = converter.convert(html)
    _timestamp_collector_.print_report()
"""