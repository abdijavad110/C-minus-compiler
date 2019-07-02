from stack import Stack
from symbolTable import SymbolTable
from ProgramBlock import ProgramBlock

depth = 0
function_args_stack = Stack()
function_args = 0
stack = Stack()
sym_table = SymbolTable()
have_error = False

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
            temp = function_args_stack.get()
            temp += 1
            function_args_stack.pop(1)
            function_args_stack.push(temp)
            # function_args += 1
    else:
        print('illegal type of void')
    stack.pop(2)
    return True

# def s_addArraySize():
#     sym_table.var_address += 4 * stack.get()
#     stack.pop(1)

def s_ptr():
    global function_args
    if stack.get(1) != 'void':
        if sym_table.is_duplicate_free(stack.get(), depth):
            # s_addArraySize()
            # stack.pop(1)
            sym_table.add('int*', stack.get(0), depth=depth)
            # sym_table.var_address += 4 * (stack.get() - 1)
            function_args += 1
    else:
        print('illegal type of void')
    stack.pop(2)
    return True


def s_fun_start():
    global depth, function_args
    depth += 1
    function_args_stack.push(0)
    # function_args = 0
    if sym_table.is_duplicate_free(stack.get()):
        sym_table.add(stack.get(1), stack.get(), address=PB.line)
    # stack.pop(2)
    return True


def s_fun_finished():
    sym_table.method_changed()
    global depth
    depth = 0
    stack.pop(2)
    function_args_stack.pop(1)
    return True


def s_fun_parameters_finished():
    global function_args
    sym_table.set_fun_args(function_args_stack.get())
    # function_args_stack.pop(1)


def s_print_sym_table():
    print(sym_table)


def s_push_id(a):
    stack.push(a)
    return True


def s_check_id(fun_0):
    a = stack.get()
    stack.pop()
    temp = sym_table.check_and_return_id(a, fun_0)
    # print(temp)

    if temp is None:
        print(a + " is not defined")
        return True
    else:
        if fun_0 == 0:
            stack.push(temp[1])
        elif fun_0 == 1:
            stack.push(temp)
        pass  # todo: push id to semantic stack
        return True



def s_check_id_finished():
    stack.pop()


def s_fun_args_start():
    global function_args
    function_args_stack.push(0)
    # function_args = 0


def s_fun_args_finished():
    tt = sym_table.check_and_return_id(sym_table.get_name_by_address(stack.get(function_args_stack.get())), 0)
    print('****', tt)
    # function_args_stack.pop(1)
    # stack.push(addr)
    if tt is None:
        print(sym_table.get_name_by_address(stack.get()) + " is not defined")
    elif tt[0] != function_args_stack.get():
        args = tt[0]
        addr = tt[1]
        print("Mismatch in number of arguments of " + sym_table.get_name_by_address(stack.get(function_args_stack.get())))
        pass
    stack.pop(function_args_stack.get())
    function_args_stack.pop(1)


def s_fun_args_increase():
    global function_args
    temp = function_args_stack.get()
    temp += 1
    function_args_stack.pop(1)
    function_args_stack.push(temp)
    # function_args += 1


def s_switch_start(lno):
    stack.push(['switch', lno])


def s_while_start(lno):
    stack.push(['while', lno])


def s_break():
    dest = stack.check_and_return_control_statement(True)
    if dest is None:
        print("No ’while’ or ’switch’ found for ’break’.")
        return False
    return True
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


def c_file_finished():
    args = sym_table.check_and_return_id('main', 0)
    if args is not None:
        PB.setInstruction('JP', args[1], None, None, 0)


def c_pop():
    stack.pop()


def c_return_with_value():
    if stack.get() == 'main':
        return True
    lv_address = sym_table.get_lv_by_name(stack.get(1))
    if lv_address == None:
        return
    PB.addInstruction('ASSIGN', stack.get(), lv_address, None)
    PB.addInstruction('JP', '@'+str(lv_address + 4), None, None)
    stack.pop()


def c_copy_argument():
    fun_name = sym_table.get_name_by_address(stack.get(function_args_stack.get()))
    lv_address = sym_table.get_lv_by_name(fun_name)
    print('***************', lv_address, fun_name)
    if fun_name == 'output':
        PB.addInstruction('ASSIGN', stack.get(), lv_address, None)
        return True
    if sym_table.get_type_by_address(stack.get()) == 'int':
        PB.addInstruction('ASSIGN', stack.get(), lv_address+4+4*function_args_stack.get(), None)
    else:
        PB.addInstruction('ASSIGN', str(stack.get()), lv_address+4+4*function_args_stack.get(), None)
    # stack.pop()


def c_return_none():
    if stack.get() == 'main':
        return True
    lv_address = sym_table.get_lv_by_name(stack.get())
    PB.addInstruction('JP', '@'+str(lv_address + 4), None, None)


# Rez

# varcall -> [Expression] #
def c_computeIndex():
    # temp1 = sym_table.getTemp()
    # PB.addInstruction("ASSIGN", "#" + stack.get(), temp1, None)
    # stack.pop(1)
    temp2 = sym_table.getTemp()
    PB.addInstruction('ASSIGN', '#' + str(4), temp2, None)
    temp3 = sym_table.getTemp()
    PB.addInstruction('MULT', stack.get(), temp2, temp3)
    stack.pop(1)
    temp4 = sym_table.getTemp()
    PB.addInstruction('ADD', stack.get(), temp3, temp4)
    stack.pop(1)
    stack.push('@' + str(temp4))

    # temp1 = sym_table.getTemp()
    #
    # PB.addInstruction("MULT", "#" + str(4), stack.get(), temp1)
    # temp = sym_table.getTemp()
    # PB.addInstruction("ADD", stack.get(1), temp1, temp)
    # stack.pop(2)
    # stack.push(temp)


# Varcall -> (Args) #
def c_return():
    fun_name = sym_table.get_name_by_address(stack.get())
    lv_address = sym_table.get_lv_by_name(fun_name)
    if fun_name == 'output':
        PB.addInstruction('PRINT', lv_address, None, None)
        return True
    address = sym_table.check_and_return_id(fun_name, 0)[1]
    PB.addInstruction('ASSIGN', PB.line+2, lv_address+4, None)
    PB.addInstruction('JP', str(address), None, None)
    tmp = stack.get()
    stack.pop()
    if sym_table.get_type_by_address(tmp):
        t = sym_table.getTemp()
        PB.addInstruction('ASSIGN', lv_address, t, None)    # todo: dorost assign kardam ?
        stack.push(t)


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
    PB.insertDummy(1)
    stack.push(PB.line)
    stack.push(PB.line)


def c_saveLabel():
    stack.push(PB.line)
    PB.insertDummy(1)


def c_whileLast():
    PB.setInstruction("JPF", stack.get(1), PB.line + 1, None, stack.get())
    PB.addInstruction("JP", stack.get(2), None, None)
    PB.setInstruction("JP", PB.line, None, None, stack.get(3) - 1)
    stack.pop(4)


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


# switch
def c_switch_start():
    PB.addInstruction("JP", PB.line+2, None, None)
    PB.insertDummy(1)
    stack.push(PB.line)


def c_switch_finished():
    PB.setInstruction("JP", PB.line, None, None, stack.get(1)-1)
    stack.pop(2)


def c_switch_case_check(num):
    temp = sym_table.getTemp()
    PB.addInstruction("EQ", '#'+str(num), stack.get(), temp)
    stack.push(PB.line)
    PB.insertDummy(1)
    stack.push(temp)


def c_switch_case_finished():
    PB.addInstruction("JP", PB.line+3, None, None)
    PB.setInstruction("JPF", stack.get(), PB.line, None, stack.get(1))
    stack.pop(2)


# continue
def c_continue():
    PB.addInstruction("JP", stack.get(2), None, None)


# break
def c_break():
    PB.addInstruction("JP", stack.get(3) - 1, None, None)

def have_main():
    for entry in sym_table.array:
        if entry.e_id == 'main' and entry.e_type == 'void':
            return True
    print('main function not found!')
