class Tag__Text:
    def __init__(self, data=""):
        self.type = "text"
        self.data = data

    def render(self):
        return self.data