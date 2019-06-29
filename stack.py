print_stack = True


class Stack:
    def __init__(self):
        self.array = []

    def pop(self, n=1):
        for i in range(n):
            self.array.pop()
        if print_stack:
            print("......pop :" + str(self))

    def push(self, arg):
        self.array.append(arg)
        if print_stack:
            print("......push :" + str(self))

    def get(self, depth=0):
        return self.array[len(self.array) - depth - 1]

    def clear(self):
        self.array = []

    def check_and_return_control_statement(self, is_break):
        for i in range(len(self.array) - 1, -1, -1):
            entry = self.array[i]
            if type(entry) == type(self.array) and (entry[0] == 'while' or (is_break and entry[0] == 'switch')):
                return entry[i][1]
        return None

    def __str__(self):
        string = ''
        for i in self.array:
            string += str(i)
            string += " "
        return str(string)
