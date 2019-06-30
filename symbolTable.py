print_table = False


class TableEntry:
    def __init__(self, e_type, e_id, depth, address, args=0, lv_address=None):
        self.e_type = e_type  # 'void' or 'int'
        self.e_id = e_id  # ID
        self.depth = depth  # (depth == None) == function
        self.address = address  # address of variable or code
        self.args = args
        self.lv_address = lv_address

    def __str__(self):
        if self.depth is None:
            return "function " + self.e_id + " of type " + self.e_type + " in: " + str(self.address) + " with " + str(
                self.args) + " args, and lv_address= " + str(self.lv_address) + "\n"
        return "variable " + self.e_id + " of type " + self.e_type + " and depth of " + str(self.depth) + " in: " + str(
            self.address) + "\n"


class SymbolTable:
    def __init__(self):
        self.array = []
        self.temp_address = 1000
        self.var_address = 500

    def getTemp(self):
        self.temp_address += 4
        return self.temp_address - 4

    def __str__(self):
        string = ''
        for i in self.array:
            string += str(i)
        return str(string)

    def next_address(self):
        self.var_address += 4
        return self.var_address - 4

    def add(self, e_type, e_id, depth=None, address=None, args=0, lv_address=None):
        if depth is None:
            self.array.append(TableEntry(e_type, e_id, depth, address, args=args, lv_address=self.var_address))
            self.var_address += 8
        else:
            self.array.append(TableEntry(e_type, e_id, depth, self.next_address()))
        if print_table:
            print("sth added\n" + str(self))

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

    def check_and_return_id(self, a, t):  # t=0 for fun & 1 for vars
        if t == 1:
            for i in range(len(self.array) - 1, -1, -1):
                if self.array[i].depth is not None and self.array[i].e_id == a:
                    return self.array[i].address
        elif t == 0:
            for entry in self.array:
                if entry.depth is None and entry.e_id == a:
                    return [entry.args, entry.address]
        return None

    def set_fun_args(self, n):
        self.array[len(self.array) - n - 1].args = n
        if print_table:
            print("set fun args\n" + str(self))

    def get_type_by_address(self, address):
        for i in range(len(self.array) - 1, -1, -1):
            if self.array[i].address == address:
                return self.array[i].e_type

    def get_name_by_address(self, address):
        if type(address) is type('string'):
            return address
        for i in range(len(self.array) - 1, -1, -1):
            if self.array[i].address == address:
                return self.array[i].e_id

    def get_lv_by_name(self, name):
        for i in range(len(self.array) - 1, -1, -1):
            if self.array[i].e_id == name and self.array[i].depth is None:
                return self.array[i].lv_address
