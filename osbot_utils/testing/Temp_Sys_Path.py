import sys


class Temp_Sys_Path:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.append(self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.path.remove(self.path)