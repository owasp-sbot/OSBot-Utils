"""
Timestamp Collector - Core Recording
=====================================

Collects timestamps from @timestamp decorated methods.
Found via stack-walking - no need to pass through call chain.

Usage:
    _timestamp_collector_ = Timestamp_Collector(name="my_workflow")
    with _timestamp_collector_:
        result = do_work()
"""

import time
import threading
from typing                                                                import List, Dict, Any
from osbot_utils.helpers.timestamp_capture.schemas.Schema__Timestamp_Entry import Schema__Timestamp_Entry
from osbot_utils.type_safe.Type_Safe                                       import Type_Safe


class Timestamp_Collector(Type_Safe):

    name            : str                              = 'default'
    entries         : List[Schema__Timestamp_Entry]    = None
    start_time_ns   : int                              = 0
    end_time_ns     : int                              = 0
    thread_id       : int                              = 0
    _depth          : int                              = 0
    _active         : bool                             = False
    _call_stack     : List[Schema__Timestamp_Entry]    = None          # For self-time calculation

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entries     = []
        self._call_stack = []
        self.thread_id   = threading.get_ident()

    # ═══════════════════════════════════════════════════════════════════════════
    # Context Manager
    # ═══════════════════════════════════════════════════════════════════════════

    def __enter__(self):
        self.start_time_ns = time.perf_counter_ns()
        self._active       = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time_ns = time.perf_counter_ns()
        self._active     = False
        return False                                                            # Don't suppress exceptions

    # ═══════════════════════════════════════════════════════════════════════════
    # Recording API
    # ═══════════════════════════════════════════════════════════════════════════

    def record(self, name: str, event: str, extra: Dict[str, Any] = None) -> Schema__Timestamp_Entry:
        if not self._active:                                                    # Record a timestamp entry (low-level API)
            return None

        entry = Schema__Timestamp_Entry(name         = name                   ,
                                        event        = event                  ,
                                        timestamp_ns = time.perf_counter_ns() ,
                                        clock_ns     = time.time_ns()         ,
                                        thread_id    = threading.get_ident()  ,
                                        depth        = self._depth            ,
                                        extra        = extra                  )
        self.entries.append(entry)
        return entry

    def enter(self, name: str, extra: Dict[str, Any] = None):                   # Record method entry
        entry = self.record(name, 'enter', extra)
        if entry:
            self._call_stack.append(entry)
        self._depth += 1

    def exit(self, name: str, extra: Dict[str, Any] = None):                    # Record method exit
        self._depth = max(0, self._depth - 1)
        self.record(name, 'exit', extra)
        if self._call_stack:
            self._call_stack.pop()

    # ═══════════════════════════════════════════════════════════════════════════
    # Basic Accessors
    # ═══════════════════════════════════════════════════════════════════════════

    def total_duration_ns(self) -> int:
        return self.end_time_ns - self.start_time_ns

    def total_duration_ms(self) -> float:
        return self.total_duration_ns() / 1_000_000

    def entry_count(self) -> int:
        return len(self.entries)

    def method_count(self) -> int:
        return len(set(e.name for e in self.entries))

    def is_active(self) -> bool:
        return self._active