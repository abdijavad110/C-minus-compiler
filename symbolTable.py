var_address = 500


def next_address():
    global var_address
    var_address += 4
    return var_address - 4


class TableEntry:
    def __init__(self, e_type, e_id, depth, address):
        self.e_type = e_type  # 'void' or 'int'
        self.e_id = e_id  # ID
        self.depth = depth  # (depth == None) == function
        self.address = address  # address of variable or code

    def __str__(self):
        if self.depth is None:
            return "function " + self.e_id + " of type " + self.e_type + " in: " + str(self.address) + "\n"
        return "variable " + self.e_id + " of type " + self.e_type + " and depth of " + str(self.depth) + " in: " + str(self.address) + "\n"


class SymbolTable:
    def __init__(self):
        self.array = []

    def __str__(self):
        string = ''
        for i in self.array:
            string += str(i)
        return str(string)

    def add(self, e_type, e_id, depth=None, address=None):
        if depth is None:
            self.array.append(TableEntry(e_type, e_id, depth, address))
        else:
            self.array.append(TableEntry(e_type, e_id, depth, next_address()))

    def is_duplicate_free(self, e_id, depth=None):
        for entry in self.array:
            if entry.depth == depth and entry.e_id == e_id:
                print('duplicate id')
                return False
        return True

    def method_changed(self):
        deletes = []
        for entry in self.array:
            if entry.depth not in [0, None]:
                deletes.append(entry)
        for entry in deletes:
            self.array.remove(entry)

    def clear(self):
        self.array = []

    def check_and_return_id(self, a):
        for i in range(len(self.array)-1, -1, -1):
            if self.array[i].depth is not None and self.array[i].e_id == a:
                return self.array[i].address
        return None
