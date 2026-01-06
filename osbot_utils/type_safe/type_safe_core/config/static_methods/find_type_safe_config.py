# ═══════════════════════════════════════════════════════════════════════════════
# Stack Discovery Functions
# ═══════════════════════════════════════════════════════════════════════════════
import sys
from typing                                                                                  import Optional
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                           import Type_Safe__Config

# ═══════════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════════

TYPE_SAFE__CONFIG__VAR_NAME    = '_type_safe_config_'                               # Variable name to search for in stack
TYPE_SAFE__CONFIG__CHECKED_VAR = '_type_safe_config__checked_'                      # Marker for "already searched this path"
TYPE_SAFE__CONFIG__MAX_DEPTH   = 15                                                 # Maximum frames to walk

_getframe = sys._getframe                                                           # Fast frame access


# ═══════════════════════════════════════════════════════════════════════════════
# find_type_safe_config
# ═══════════════════════════════════════════════════════════════════════════════

def find_type_safe_config(max_depth: int = TYPE_SAFE__CONFIG__MAX_DEPTH) -> Optional[Type_Safe__Config]:

    try:
        frame = _getframe(1)                                                        # Start from caller's frame
    except ValueError:
        return None

    previous_frames = []

    try:
        for _ in range(max_depth):
            if frame is None:
                break

            frame_locals = frame.f_locals
            value        = frame_locals.get(TYPE_SAFE__CONFIG__VAR_NAME)

            if value.__class__ is Type_Safe__Config:                                # Found config - inject into walked frames
                for prev_frame in previous_frames:
                    prev_frame.f_locals[TYPE_SAFE__CONFIG__VAR_NAME] = value
                return value

            if frame_locals.get(TYPE_SAFE__CONFIG__CHECKED_VAR):                    # Already searched this path
                return None

            previous_frames.append(frame)
            frame = frame.f_back

        for prev_frame in previous_frames:                                          # Not found - mark frames as checked
            prev_frame.f_locals[TYPE_SAFE__CONFIG__CHECKED_VAR] = True

        return None

    finally:
        del frame                                                                   # Clean up frame references
        del previous_frames