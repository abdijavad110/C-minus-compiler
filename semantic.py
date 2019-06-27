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
    return True


def s_type(arg):
    stack.push(arg)
    return True


def s_add_id(arg):
    stack.push(arg)
    return True


def s_var():
    if sym_table.is_duplicate_free(stack.get(), depth):
        if stack.get(1) != 'void':
            sym_table.add('int', stack.get(), depth=depth)
        else:
            print('illegal type of void')
    stack.pop(2)
    return True


def s_fun():
    global depth
    depth += 1
    if sym_table.is_duplicate_free(stack.get()):
        sym_table.add(stack.get(1), stack.get(), address=0)  # todo: function code address
    stack.pop(2)
    return True


def s_fun_finished():
    sym_table.method_changed()
    global depth
    depth = 0
    return True


def s_print_sym_table():
    print(sym_table)


def s_check_id(a):
    temp = sym_table.check_and_return_id(a)
    if temp is None:
        print(a + " is not defined")
        return True
    else:
        pass        # todo: push id to semantic stack
        return True

