from stack import Stack
from symbolTable import SymbolTable

depth = 0
function_args = 0
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
    global function_args
    if stack.get(1) != 'void':
        if sym_table.is_duplicate_free(stack.get(), depth):
            sym_table.add('int', stack.get(), depth=depth)
            function_args += 1
    else:
        print('illegal type of void')
    stack.pop(2)
    return True


def s_fun_start():
    global depth, function_args
    depth += 1
    function_args = 0
    if sym_table.is_duplicate_free(stack.get()):
        sym_table.add(stack.get(1), stack.get(), address=0)  # todo: function code address
    stack.pop(2)
    return True


def s_fun_finished():
    sym_table.method_changed()
    global depth
    depth = 0
    return True


def s_fun_parameters_finished():
    global function_args
    sym_table.set_fun_args(function_args)
    function_args = 0


def s_print_sym_table():
    print(sym_table)


def s_check_id(a):
    stack.push(a)
    temp = sym_table.check_and_return_id(a, 1)
    if temp is None:
        print(a + " is not defined")
        return True
    else:
        pass        # todo: push id to semantic stack
        return True


def s_check_id_finished():
    stack.pop()


def s_fun_args_start():
    global function_args
    function_args = 0


def s_fun_args_finished():
    args = sym_table.check_and_return_id(stack.get(), 0)
    if args is None:
        print(stack.get() + " is not defined")
    elif args != function_args:
        print("Mismatch in numbers of arguments of " + stack.get())
        pass
    stack.pop()     # if need function name delete it


def s_fun_args_increase():
    global function_args
    function_args += 1


def s_switch_start(lno):
    stack.push(['switch', lno])


def s_while_start(lno):
    stack.push(['while', lno])


def s_break():
    dest = stack.check_and_return_control_statement(True)
    if dest is None:
        print("No ’while’ or ’switch’ found for ’break’.")
    # todo: generate break code


def s_continue():
    dest = stack.check_and_return_control_statement(False)
    if dest is None:
        print("No ’while’ found for ’continue’.")
    # todo: generate continue code


def s_while_finished():
    stack.pop()


def s_switch_finished():
    stack.pop()
