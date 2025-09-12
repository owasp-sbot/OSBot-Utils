from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt

TYPE_SAFE_UINT__FILE_SIZE__MIN_VALUE = 0
TYPE_SAFE_UINT__FILE_SIZE__MAX_VALUE = 2 ** 63 - 1         # Max file size on most systems

class Safe_UInt__FileSize(Safe_UInt):                     # File size in bytes

    min_value = TYPE_SAFE_UINT__FILE_SIZE__MIN_VALUE
    max_value = TYPE_SAFE_UINT__FILE_SIZE__MAX_VALUE
    allow_bool = False

    def to_kb(self) -> float:
        return self / 1024

    def to_mb(self) -> float:
        return self / (1024 * 1024)

    def to_gb(self) -> float:
        return self / (1024 * 1024 * 1024)