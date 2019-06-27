class Stack:
    def __init__(self):
        self.array = []

    def pop(self, n=1):
        for i in range(n):
            self.array.pop()

    def push(self, arg):
        self.array.append(arg)

    def get(self, depth=0):
        return self.array[len(self.array) - depth - 1]

    def clear(self):
        self.array = []

    def __str__(self):
        string = ''
        for i in self.array:
            string += str(i)
            string += " "
        return str(string)
