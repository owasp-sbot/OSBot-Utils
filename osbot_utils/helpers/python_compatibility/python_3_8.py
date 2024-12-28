import sys

if sys.version_info < (3, 9):
    class Annotated:
        def __init__(self, *args) -> None:
            pass
else:
    from typing import Annotated