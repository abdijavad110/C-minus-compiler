from stack import Stack
from symbolTable import SymbolTable
from ProgramBlock import ProgramBlock

depth = 0
function_args = 0
stack = Stack()
sym_table = SymbolTable()

PB = ProgramBlock()


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
    temp = sym_table.check_and_return_id(a, 1)
    stack.push(temp)
    if temp is None:
        print(a + " is not defined")
        return True
    else:
        pass  # todo: push id to semantic stack
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
    stack.pop()  # if need function name delete it


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


def c_pop():
    stack.pop()


# Rez

# varcall -> [Expression] #
def c_computeIndex():
    temp1 = sym_table.getTemp()
    PB.addInstruction("MULT", "#" + str(4), stack.get(), temp1)
    temp = sym_table.getTemp()
    PB.addInstruction("ADD", stack.get(1), temp1, temp)
    stack.pop(2)
    stack.push(temp)


# TODO
# Varcall -> (Args) #
def c_return():
    temp = sym_table.getTemp()
    # function call and store result
    stack.push(temp)


# Factor -> #pushNum num
def c_pushNum(num):
    temp = sym_table.getTemp()
    PB.addInstruction("ASSIGN", "#" + num, temp, None)
    stack.push(temp)


# F3 -> *signed factor #mult
def c_mult():
    temp = sym_table.getTemp()
    PB.addInstruction("MULT", stack.get(), stack.get(1), temp)
    stack.pop(2)
    stack.push(temp)


# signedfactor -> - factor #?
def c_negate():
    PB.addInstruction("SUB", "#" + str(0), stack.get(), stack.get())


# addop -> + #
def c_pushPlus():
    stack.push("+")


# addop -> - #
def c_pushMinus():
    stack.push("-")


# F2 -> addop term #add F2
def c_add_or_sub():
    temp = sym_table.getTemp()
    if stack.get(1) == "+":
        PB.addInstruction("ADD", stack.get(), stack.get(2), temp)
    else:
        PB.addInstruction("SUB", stack.get(), stack.get(2), temp)

    stack.pop(3)
    stack.push(temp)


# Relop -> == #
def c_pushEquality():
    stack.push("==")


# Relop -> < #
def c_pushSmallerThan():
    stack.push("<")


# E5 -> Relop AdditiveExpression #
def c_pushComparison():
    temp = sym_table.getTemp()
    if stack.get(1) == "==":
        PB.addInstruction("EQ", stack.get(), stack.get(2), temp)
    else:
        PB.addInstruction("LT", stack.get(2), stack.get(), temp)
    stack.pop(3)
    stack.push(temp)


# EZEZEZ -> = Expression #
# EXEXEX -> = Expression #
def c_assign():
    temp = stack.get()
    PB.addInstruction("ASSIGN", stack.get(), stack.get(1), None)
    stack.pop(2)
    stack.push(temp)


# While
def c_whileFirst():
    PB.addInstruction("JP", PB.line + 2, None, None)
    PB.insertDummy(2)
    stack.push(PB.line)


def c_saveLabel():
    stack.push(PB.line)
    PB.insertDummy(1)


def c_whileLast():
    PB.setInstruction("JPF", stack.get(1), PB.line + 1, None, stack.get())
    PB.setInstruction("JP", PB.line + 1, None, None, stack.get(2) - 1)
    PB.addInstruction("JP", stack.get(2), None, None)
    stack.pop(3)


# If
def c_if1():
    stack.push(PB.line)
    PB.insertDummy(1)


def c_if2():
    PB.setInstruction("JPF", stack.get(1), PB.line + 1, None, stack.get())
    stack.pop(2)
    stack.push(PB.line)
    PB.insertDummy(1)


def c_if3():
    PB.setInstruction("JP", PB.line, None, None, stack.get())
    # PB.insertDummy()
    stack.pop(1)


# continue
def c_continue():
    PB.addInstruction("JP", stack.get(2), None, None)


# break
def c_break():
    PB.addInstruction("JP", stack.get(2) - 1, None, None)
