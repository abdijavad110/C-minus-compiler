from stack import Stack
from symbolTable import SymbolTable

depth = 0
stack = Stack()
sym_table = SymbolTable()


def initialize_semantic_analyzer():
    global depth
    depth = 0
    stack.clear()
    sym_table.clear()


def s_type(arg):
    print(sym_table)
    stack.push(arg)


def s_add_id(arg):
    print(sym_table)
    stack.push(arg)


def s_var():
    print(sym_table)
    if sym_table.is_duplicate_free(stack.get(), depth) \
            and stack.get(1) != 'void':
        sym_table.add('int', stack.get(), depth=depth)
    stack.pop(2)


def s_fun():
    print(sym_table)
    global depth
    depth += 1
    if sym_table.is_duplicate_free(stack.get()):
        sym_table.add(stack.get(1), stack.get(), address=0)  # todo: function code address
    stack.pop(2)


def s_fun_finished():
    print(sym_table)
    sym_table.method_changed()
    global depth
    depth = 0


def s_print_sym_table():
    print(sym_table)
