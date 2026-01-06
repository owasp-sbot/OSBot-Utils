# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Config - Configuration for Type_Safe Performance Optimization
# Context-aware configuration that propagates through the call stack
# ═══════════════════════════════════════════════════════════════════════════════

class Type_Safe__Config:                                                            # Configuration for Type_Safe optimization

    __slots__ = ('skip_setattr'    ,                                                # Use object.__setattr__ instead of validated
                 'skip_validation' ,                                                # Skip type validation checks
                 'skip_conversion' ,                                                # Skip type conversion (str → Safe_Id)
                 'skip_mro_walk'   ,                                                # Use cached class kwargs if available
                 'on_demand_nested',                                                # Defer nested Type_Safe creation
                 'fast_collections')                                                # Fast creation for Type_Safe__List/Dict/Set

    def __init__(self                          ,
                 skip_setattr     : bool = False,
                 skip_validation  : bool = False,
                 skip_conversion  : bool = False,
                 skip_mro_walk    : bool = False,
                 on_demand_nested : bool = False,
                 fast_collections : bool = False):
        self.skip_setattr      = skip_setattr
        self.skip_validation   = skip_validation
        self.skip_conversion   = skip_conversion
        self.skip_mro_walk     = skip_mro_walk
        self.on_demand_nested  = on_demand_nested
        self.fast_collections  = fast_collections

    def __enter__(self):                                                            # Context manager entry
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):                                  # Context manager exit
        return False

    def __repr__(self):                                                             # String representation showing enabled flags
        enabled = []
        if self.skip_setattr     : enabled.append('skip_setattr')
        if self.skip_validation  : enabled.append('skip_validation')
        if self.skip_conversion  : enabled.append('skip_conversion')
        if self.skip_mro_walk    : enabled.append('skip_mro_walk')
        if self.on_demand_nested : enabled.append('on_demand_nested')
        if self.fast_collections : enabled.append('fast_collections')

        if enabled:
            return f"Type_Safe__Config({', '.join(enabled)})"
        else:
            return "Type_Safe__Config(default)"

    def __eq__(self, other):                                                        # Equality comparison
        if not isinstance(other, Type_Safe__Config):
            return False
        return (self.skip_setattr     == other.skip_setattr     and
                self.skip_validation  == other.skip_validation  and
                self.skip_conversion  == other.skip_conversion  and
                self.skip_mro_walk    == other.skip_mro_walk    and
                self.on_demand_nested == other.on_demand_nested and
                self.fast_collections == other.fast_collections)

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods
    # ═══════════════════════════════════════════════════════════════════════════

    @classmethod
    def fast_mode(cls) -> 'Type_Safe__Config':                                      # Maximum performance - skip all validation
        return cls(skip_setattr     = True,
                   skip_validation  = True,
                   skip_conversion  = True,
                   skip_mro_walk    = True,
                   fast_collections = True)

    @classmethod
    def on_demand_mode(cls) -> 'Type_Safe__Config':                                 # On-demand nested object creation only
        return cls(on_demand_nested = True)

    @classmethod
    def bulk_load_mode(cls) -> 'Type_Safe__Config':                                 # Optimized for loading from trusted sources
        return cls(skip_setattr    = True,
                   skip_validation = True,
                   skip_conversion = True)
