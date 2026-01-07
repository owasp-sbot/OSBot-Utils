# ═══════════════════════════════════════════════════════════════════════════════
# Enum__Hypothesis__Status - Outcome status for hypothesis evaluation
# Indicates whether a performance hypothesis was confirmed
# ═══════════════════════════════════════════════════════════════════════════════

from enum import Enum


class Enum__Hypothesis__Status(Enum):                                            # Hypothesis outcome
    SUCCESS      = 'success'                                                     # Met or exceeded target
    FAILURE      = 'failure'                                                     # Did not meet target
    INCONCLUSIVE = 'inconclusive'                                                # Mixed or unclear results
    REGRESSION   = 'regression'                                                  # Performance got worse
