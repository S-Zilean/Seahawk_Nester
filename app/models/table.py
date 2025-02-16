class Table:
    def __init__(self, value):
        self.data = { value : value}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        return self.data[key]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)
