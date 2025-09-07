from enum import Enum

class Enum__LLM__Role(str, Enum): # Extended roles for specific providers
    SYSTEM    = "system"
    USER      = "user"
    ASSISTANT = "assistant"
    TOOL      = "tool"

    def __str__(self):
        return self.value  # Override to return the value