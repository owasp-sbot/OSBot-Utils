class Cache_Metrics:                                                                # Track cache performance metrics

    def __init__(self):
        self.hits                    = 0
        self.misses                  = 0
        self.reloads                 = 0
        self.key_generation_time     = 0.0
        self.cache_lookup_time       = 0.0
        self.function_execution_time = 0.0

    @property
    def hit_rate(self) -> float:                                                    # Calculate cache hit rate
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def record_hit(self) -> None:                                                   # Record cache hit
        self.hits += 1

    def record_miss(self) -> None:                                                  # Record cache miss
        self.misses += 1

    def record_reload(self) -> None:                                                # Record cache reload
        self.reloads += 1

    def reset(self) -> None:                                                        # Reset all metrics
        self.hits                    = 0
        self.misses                  = 0
        self.reloads                 = 0
        self.key_generation_time     = 0.0
        self.cache_lookup_time       = 0.0
        self.function_execution_time = 0.0