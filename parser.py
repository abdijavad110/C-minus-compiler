from Lexer import initialize_lexer, get_next_token
from semantic import *
import sys


# first - follow - next_token
def first(non_terminal):
    return {
        'Program': ['eof', 'void', 'int'],
        'Declarationlist': ['eps', 'void', 'int'],
        'E1': [';', '['],
        'E2': ['eps', '['],
        'Compoundstmt': ['{'],
        'Statementlist': ['eps', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id', '+', '-',
                          '(', 'num'],
        'Statement': ['switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id', '+', '-', '(',
                      'num'],
        'Expressionstmt': [';', 'break', 'continue', 'id', '+', '-', '(', 'num'],
        'Selectionstmt': ['if'],
        'Iterationstmt': ['while'],
        'Returnstmt': ['return'],
        'E3': [';', 'id', '+', '-', '(', 'num'],
        'Switchstmt': ['switch'],
        'Casestmts': ['eps', 'case'],
        'Casestmt': ['case'],
        'Defaultstmt': ['eps', 'default'],
        'Expression': ['id', '+', '-', '(', 'num'],
        'EXEXEX': ['eps', '=', '[', '(', '*', '+', '-', '==', '<'],
        'EZEZEZ': ['eps', '=', '*', '+', '-', '==', '<'],
        'NewSimpleexpression': ['+', '-', '(', 'num'],
        'E5': ['eps', '==', '<'],
        'Relop': ['==', '<'],
        'Additiveexpression': ['id', '+', '-', '(', 'num'],
        'NewAdditiveexpression': ['+', '-', '(', 'num'],
        'F2': ['eps', '+', '-'],
        'Addop': ['+', '-'],
        'Term': ['id', '+', '-', '(', 'num'],
        'NewTerm': ['+', '-', '(', 'num'],
        'F3': ['eps', '*'],
        'NewSignedfactor': ['+', '-'],
        'Signedfactor': ['+', '-', 'id', '(', 'num'],
        'Args': ['eps', '+', '-', 'id', '(', 'num'],
        'Arglist': ['+', '-', 'id', '(', 'num'],
        'F4': ['eps', ','],
        'NewFactor': ['(', 'num'],
        'Factor': ['id', '(', 'num'],
        'NewVarcall': ['eps', '('],
        'Varcall': ['eps', '[', '('],
        'Typespecifier': ['void', 'int'],
        'Params': ['void', 'int'],
        'BB': ['eps', 'id'],
        'Paramlist': ['eps', '[', ','],
        'F1': ['eps', ','],
        'Declaration': ['void', 'int'],
        'AA': ['(', ';', '['],
        'Vardeclaration': [';', '['],
        'Fundeclaration': ['(']
    }[non_terminal]


def follow(non_terminal):
    return {
        'Program': [],
        'Declarationlist': ['eof', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id', '+',
                            '-', '(', 'num', '}'],
        'E1': ['void', 'int', 'eof', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id', '+',
               '-', '(', 'num', '}'],
        'E2': [')', ','],
        'Compoundstmt': ['case', 'default', 'else', 'void', 'int', 'eof', 'switch', 'return', 'while', 'if', '{', ';',
                         'break', 'continue', 'id', '+', '-', '(', 'num', '}'],
        'Statementlist': ['case', 'default', '}'],
        'Statement': ['case', 'default', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id',
                      '+', '-', '(', 'num', 'else', '}'],
        'Expressionstmt': ['case', 'default', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id',
                           '+', '-', '(', 'num', 'else', '}'],
        'Selectionstmt': ['case', 'default', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id',
                          '+', '-', '(', 'num', 'else', '}'],
        'Iterationstmt': ['case', 'default', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id',
                          '+', '-', '(', 'num', 'else', '}'],
        'Returnstmt': ['case', 'default', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id',
                       '+', '-', '(', 'num', 'else', '}'],
        'E3': ['case', 'default', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id', '+',
               '-', '(', 'num', 'else', '}'],
        'Switchstmt': ['case', 'default', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id',
                       '+', '-', '(', 'num', 'else', '}'],
        'Casestmts': ['default', '}'],
        'Casestmt': ['case', 'default', '}'],
        'Defaultstmt': ['}'],
        'Expression': [';', ',', ')', ']'],
        'EXEXEX': [';', ',', ')', ']'],
        'EZEZEZ': [';', ',', ')'],
        'NewSimpleexpression': [';', ',', ')', ']'],
        'E5': [';', ',', ')', ']'],
        'Relop': ['id', '+', '-', '(', 'num'],
        'Additiveexpression': [';', ',', ')', ']'],
        'NewAdditiveexpression': ['==', '<', ';', ',', ')', ']'],
        'F2': ['==', '<', ';', ',', ')', ']'],
        'Addop': ['id', '+', '-', '(', 'num'],
        'Term': ['==', '<', '+', '-', ';', ',', ')', ']'],
        'NewTerm': ['==', '<', '+', '-', ';', ',', ')', ']'],
        'F3': ['==', '<', '+', '-', ';', ',', ')', ']'],
        'NewSignedfactor': ['*', '==', '<', '+', '-', ';', ',', ')', ']'],
        'Signedfactor': ['*', '==', '<', '+', '-', ';', ',', ')', ']'],
        'Args': [')'],
        'Arglist': [')'],
        'F4': [')'],
        'NewFactor': ['*', '==', '<', '+', '-', ';', ',', ')', ']'],
        'Factor': ['*', '==', '<', '+', '-', ';', ',', ')', ']'],
        'Varcall': ['==', '<', '+', '-', '*', ';', ',', ')', ']'],
        'NewVarcall': ['==', '<', '+', '-', '*', ';', ',', ')', ']'],
        'Typespecifier': ['id'],
        'Params': [')'],
        'BB': [')'],
        'Paramlist': [')'],
        'F1': [')'],
        'Declaration': ['void', 'int', 'eof', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id',
                        '+', '-', '(', 'num', '}'],
        'AA': ['void', 'int', 'eof', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue', 'id', '+',
               '-', '(', 'num', '}'],
        'Vardeclaration': ['void', 'int', 'eof', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue',
                           'id', '+', '-', '(', 'num', '}'],
        'Fundeclaration': ['void', 'int', 'eof', 'switch', 'return', 'while', 'if', '{', ';', 'break', 'continue',
                           'id', '+', '-', '(', 'num', '}']
    }[non_terminal]


def next_token():
    global cur_token_vec, cur_token
    global i
    i = i + 1
    if cur_token != 'eof':
        cur_token_vec = get_next_token()
        cur_token = translate_token(cur_token_vec)


# case 1, 2, 3
def case1(terminal):
    if terminal == cur_token:
        next_token()
        global parse_tree
        parse_tree.append([depth+1, "'" + terminal + "'"])
        return True
    return False


def case2(non_terminal):
    if cur_token in first(non_terminal) or ('eps' in first(non_terminal) and cur_token in follow(non_terminal)):
        global depth, parse_tree
        depth += 1
        parse_tree.append([depth, non_terminal])
        return True
    return False


def case3(state):
    return cur_token in follow(state)


def error(type_of_error, arg):
    have_error = True
    print(cur_token_vec.line_number, type_of_error, arg)
    global error_string
    if type_of_error == 1:
        error_string.append("parser: #" + str(cur_token_vec.line_number) + " : Syntax Error! Missing " + arg)
    if type_of_error == 2:
        if cur_token != 'eof':
            error_string.append("parser: #" + str(cur_token_vec.line_number) +
                                " : Syntax Error! Unexpected " + cur_token)
            next_token()
        else:
            error_string.append("parser: #" + str(cur_token_vec.line_number) + " : Syntax Error! Malformed Input")
            sys.exit()
    if type_of_error == 3:
        error_string.append("parser: #" + str(cur_token_vec.line_number) + " : Syntax Error! Missing " + arg)
    if type_of_error == 4:
        error_string.append("parser: #" + str(cur_token_vec.line_number) + " : Syntax Error! Malformed Input")
        sys.exit()


# success - failure
def success():
    global depth
    depth -= 1
    return True


def failure():
    global depth
    depth -= 1
    return False


def program():
    if case2('Declarationlist') and declaration_list():
        if not case1('eof'):
            error(4, '')
        print(sym_table)
        have_main()
        c_file_finished()
        # print(PB.get_generated_code())
        PB.export_generated_code()
        return success()  ##### finished
    return failure()


def declaration_list():
    if case2('Declaration') and declaration():
        while not (case2('Declarationlist') and declaration_list()):
            error(2, 'Declarationlist')
            if 'eps' not in first('Declarationlist') and cur_token in follow('Declarationlist'):
                error(3, 'Declarationlist')
                return success()
        return success()
    if case3('Declarationlist'):
        return success()
    return failure()


def declaration():
    print('hi')
    if case2('Typespecifier') and type_specifier():
        s_add_id(cur_token_vec.name)
        if not case1('id'):
            error(1, 'id')
        while not (case2('AA') and AA()):
            error(2, 'AA')
            if 'eps' not in first('AA') and cur_token in follow('AA'):
                error(3, 'AA')
                break
        return success()
    return failure()


def type_specifier():
    s_type(cur_token)
    if case1('int') or case1('void'):
        return success()
    return failure()


def AA():
    if case2('Fundeclaration') and fun_declaration():
        return success()
    if case2('Vardeclaration') and var_declaration():
        # s_var()
        return success()
    return failure()


def fun_declaration():
    s_fun_start()
    if case1('('):
        while not(case2('Params') and params()):
            error(2, 'Params')
            if 'eps' not in first('Params') and cur_token in follow('Params'):
                error(3, 'Params')
                break
        if not case1(')'):
            error(1, ')')
        s_fun_parameters_finished()
        while not(case2('Compoundstmt') and compound_stmt()):
            error(2, 'Params')
            if 'eps' not in first('Params') and cur_token in follow('Params'):
                error(3, 'Params')
                break
        s_fun_finished()
        return success()
    s_fun_finished()
    return failure()


def var_declaration():
    print('hi vardec')
    if case2('E1') and E1():
        return success()
    return failure()


def E1():
    if case1(';'):
        s_var()
        return success()
    if case1('['):
        # if cur_token == 'num':
        #     stack.push(int(cur_token_vec.name))
        if not case1('num'):
            error(1, 'num')
        if not case1(']'):
            error(1, ']')
        if not case1(';'):
            error(1, ';')
        s_ptr()

        # print(sym_table)
        return success()
    return failure()


def params():
    # print('hi params')
    if case1('int'):
        s_type('int')
        s_add_id(cur_token_vec.name)
        if not case1('id'):
            error(1, 'id')
        else:
            s_var()
        while not(case2('Paramlist') and param_list()):
            error(2, 'Paramlist')
            if 'eps' not in first('Paramlist') and cur_token in follow('Paramlist'):
                error(3, 'Paramlist')
                break
        return success()
    if case1('void'):
        while not (case2('BB') and BB()):
            error(2, 'BB')
            if 'eps' not in first('BB') and cur_token in follow('BB'):
                error(3, 'BB')
                break
        return success()
    return failure()


def BB():
    tmp = cur_token_vec.name
    if case1('id'):
        print("illegal type of void")
        while not (case2('Paramlist') and param_list()):
            error(2, 'Paramlist')
            if 'eps' not in first('Paramlist') and cur_token in follow('Paramlist'):
                error(3, 'Paramlist')
                break
        return success()
    if case3('BB'):
        return success()
    return failure()


def param_list():
    if case2('E2') and E2():
        while not(case2('F1') and F1()):
            error(2, 'F1')
            if 'eps' not in first('F1') and cur_token in follow('F1'):
                error(3, 'F1')
                break
        return success()
    return failure()


def F1():
    # print('hi f1')
    if case1(','):
        while not(case2('Typespecifier') and type_specifier()):
            error(2, 'Typespecifier')
            if 'eps' not in first('Typespecifier') and cur_token in follow('Typespecifier'):
                error(3, 'Typespecifier')
                break
        s_add_id(cur_token_vec.name)
        if not case1('id'):
            error(1, 'id')
        else:
            s_var()
        while not (case2('E2') and E2()):
            error(2, 'E2')
            if 'eps' not in first('E2') and cur_token in follow('E2'):
                error(3, 'E2')
                break
        while not (case2('F1') and F1()):
            error(2, 'F1')
            if 'eps' not in first('F1') and cur_token in follow('F1'):
                error(3, 'F1')
                break
        return success()
    if case3('F1'):
        return success()
    return failure()


def E2():
    if case1('['):
        if case1(']'):
            # s_ptr()
            return success()
        else:
            error(1, ']')
    if case3('E2'):
        return success()
    return failure()


def compound_stmt():
    if case1('{'):
        while not (case2('Declarationlist') and declaration_list()):
            error(2, 'Declarationlist')
            if 'eps' not in first('Declarationlist') and cur_token in follow('Declarationlist'):
                error(3, 'Declarationlist')
                break
        while not (case2('Statementlist') and statement_list()):
            error(2, 'Statementlist')
            if 'eps' not in first('Statementlist') and cur_token in follow('Statementlist'):
                error(3, 'Statementlist')
                break
        if not case1('}'):
            error(1, '}')
        # c_return_none()
        return success()
    return failure()


def statement_list():
    if case2('Statement') and statement():
        while not (case2('Statementlist') and statement_list()):
            error(2, 'Statementlist')
            if 'eps' not in first('Statementlist') and cur_token in follow('Statementlist'):
                error(3, 'Statementlist')
                break
        return success()
    if case3('Statementlist'):
        return success()
    return failure()


def statement():
    if case2('Switchstmt') and switch_stmt():
        return success()
    if case2('Returnstmt') and return_stmt():
        return success()
    if case2('Iterationstmt') and iteration_stmt():
        return success()
    if case2('Selectionstmt') and selection_stmt():
        return success()
    if case2('Compoundstmt') and compound_stmt():
        return success()
    if case2('Expressionstmt') and expression_stmt():
        return success()
    return failure()


def expression():
    tmp = cur_token_vec.name
    if case1('id') and s_push_id(tmp):
        while not (case2('EXEXEX') and EXEXEX()):
            error(2, 'EXEXEX')
            if 'eps' not in first('EXEXEX') and cur_token in follow('EXEXEX'):
                error(3, 'EXEXEX')
                break
        return success()
    if case2('NewSimpleexpression') and new_simple_expression():
        return success()
    return failure()


def expression_stmt():
    if case1(';'):
        return success()
    if case1('break'):
        if s_break():
            c_break()
        if not case1(';'):
            error(1, ';')
        return success()
    if case1('continue'):
        s_continue()
        c_continue()
        if not case1(';'):
            error(1, ';')
        return success()
    if case2('Expression') and expression():
        if not case1(';'):
            error(1, ';')
        c_pop()
        return success()
    return failure()


def switch_stmt():
    s_switch_start(cur_token_vec.line_number)
    if case1('switch'):
        c_switch_start()
        if not case1('('):
            error(1, '(')
        while not (case2('Expression') and expression()):
            error(2, 'Expression')
            if 'eps' not in first('Expression') and cur_token in follow('Expression'):
                error(3, 'Expression')
                break
        if not case1(')'):
            error(1, ')')
        if not case1('{'):
            error(1, '{')
        while not (case2('Casestmts') and case_stmts()):
            error(2, 'Casestmts')
            if 'eps' not in first('Casestmts') and cur_token in follow('Casestmts'):
                error(3, 'Casestmts')
                break
        while not (case2('Defaultstmt') and default_stmt()):
            error(2, 'Defaultstmt')
            if 'eps' not in first('Defaultstmt') and cur_token in follow('Defaultstmt'):
                error(3, 'Defaultstmt')
                break
        if not case1('}'):
            error(1, '}')
        c_switch_finished()
        s_switch_finished()
        return success()
    return failure()


def return_stmt():
    if case1('return'):
        while not (case2('E3') and E3()):
            error(2, 'E3')
            if 'eps' not in first('E3') and cur_token in follow('E3'):
                error(3, 'E3')
        return success()
    return failure()


def iteration_stmt():
    s_while_start(cur_token_vec.line_number)
    if case1('while'):
        c_whileFirst()
        if not case1('('):
            error(1, '(')
        while not (case2('Expression') and expression()):
            error(2, 'Expression')
            if 'eps' not in first('Expression') and cur_token in follow('Expression'):
                error(3, 'Expression')
        if not case1(')'):
            error(1, ')')
        c_saveLabel()
        while not (case2('Statement') and statement()):
            error(2, 'Statement')
            if 'eps' not in first('Statement') and cur_token in follow('Statement'):
                error(3, 'Statement')
                break
        c_whileLast()
        s_while_finished()
        return success()
    return failure()


def selection_stmt():
    if case1('if'):
        if not case1('('):
            error(1, '(')
        while not (case2('Expression') and expression()):
            error(2, 'Expression')
            if 'eps' not in first('Expression') and cur_token in follow('Expression'):
                error(3, 'Expression')
                break
        if not case1(')'):
            error(1, ')')
        c_if1()
        while not (case2('Statement') and statement()):
            error(2, 'Statement')
            if 'eps' not in first('Statement') and cur_token in follow('Statement'):
                error(3, 'Statement')
                break
        c_if2()
        if not case1('else'):
            error(1, 'else')
        while not (case2('Statement') and statement()):
            error(2, 'Statement')
            if 'eps' not in first('Statement') and cur_token in follow('Statement'):
                error(3, 'Statement')
                break
        c_if3()
        return success()
    return failure()


def E3():
    if case2('Expression') and expression():
        # c_return_none()
        c_return_with_value()
        if not case1(';'):
            error(1, ';')
        return success()
    if case1(';'):
        # c_return_none()
        return success()
    return failure()


def case_stmts():
    if case2('Casestmt') and case_stmt():
        while not (case2('Casestmts') and case_stmts()):
            error(2, 'Casestmts')
            if 'eps' not in first('Casestmts') and cur_token in follow('Casestmts'):
                error(3, 'Casestmts')
                break
        return success()
    if case3('Casestmts'):
        return success()
    return failure()


def case_stmt():
    if case1('case'):
        c_switch_case_check(cur_token_vec.name)
        if not case1('num'):
            error(1, 'num')
        if not case1(':'):
            error(1, ':')
        while not (case2('Statementlist') and statement_list()):
            error(2, 'Statementlist')
            if 'eps' not in first('Statementlist') and cur_token in follow('Statementlist'):
                error(3, 'Statementlist')
                break
        c_switch_case_finished()
        return success()
    return failure()


def default_stmt():
    if case1('default'):
        c_repair_default()
        if not case1(':'):
            error(1, ':')
        while not (case2('Statementlist') and statement_list()):
            error(2, 'Statementlist')
            if 'eps' not in first('Statementlist') and cur_token in follow('Statementlist'):
                error(3, 'Statementlist')
                break
        return success()
    if case3('Defaultstmt'):
        c_repair_default()
        return success()
    return failure()


def EXEXEX():
    if case1('['):
        s_check_id(1)
        while not (case2('Expression') and expression()):
            error(2, 'Expression')
            if 'eps' not in first('Expression') and cur_token in follow('Expression'):
                error(3, 'Expression')
                break
        if not case1(']'):
            error(1, ']')
        c_computeIndex()
        while not (case2('EZEZEZ') and EZEZEZ()):
            error(2, 'EZEZEZ')
            if 'eps' not in first('EZEZEZ') and cur_token in follow('EZEZEZ'):
                error(3, 'EZEZEZ')
                break
        return success()
    if case1('='):
        s_check_id(1)
        while not (case2('Expression') and expression()):
            error(2, 'Expression')
            if 'eps' not in first('Expression') and cur_token in follow('Expression'):
                error(3, 'Expression')
                break
        c_assign()
        return success()
    if case2('NewVarcall') and new_var_call():
        while not (case2('F3') and F3()):
            error(2, 'F3')
            if 'eps' not in first('F3') and cur_token in follow('F3'):
                error(3, 'F3')
                break
        while not (case2('F2') and F2()):
            error(2, 'F2')
            if 'eps' not in first('F2') and cur_token in follow('F2'):
                error(3, 'F2')
                break
        while not (case2('E5') and E5()):
            error(2, 'E5')
            if 'eps' not in first('E5') and cur_token in follow('E5'):
                error(3, 'E5')
                break
        return success()
    return failure()


def new_simple_expression():
    if case2('NewAdditiveexpression') and new_additive_expression():
        while not (case2('E5') and E5()):
            error(2, 'E5')
            if 'eps' not in first('E5') and cur_token in follow('E5'):
                error(3, 'E5')
                break
        return success()
    return failure()


def E5():
    if case2('Relop') and relop():
        while not (case2('Additiveexpression') and additive_expression()):
            error(2, 'Additiveexpression')
            if 'eps' not in first('Additiveexpression') and cur_token in follow('Additiveexpression'):
                error(3, 'Additiveexpression')
                break
        c_pushComparison()
        return success()
    if case3('E5'):
        return success()
    return failure()


def relop():
    if case1('=='):
        c_pushEquality()
        return success()
    elif case1('<'):
        c_pushSmallerThan()
        return success()
    return failure()


def additive_expression():
    if case2('NewTerm') and new_term():
        while not (case2('F2') and F2()):
            error(2, 'F2')
            if 'eps' not in first('F2') and cur_token in follow('F2'):
                error(3, 'F2')
                break
        return success()
    tmp = cur_token_vec.name
    if case1('id') and s_push_id(tmp):
        while not (case2('Varcall') and var_call()):
            error(2, 'Varcall')
            if 'eps' not in first('Varcall') and cur_token in follow('Varcall'):
                error(3, 'Varcall')
                break
        while not (case2('F3') and F3()):
            error(2, 'F3')
            if 'eps' not in first('F3') and cur_token in follow('F3'):
                error(3, 'F3')
                break
        while not (case2('F2') and F2()):
            error(2, 'F2')
            if 'eps' not in first('F2') and cur_token in follow('F2'):
                error(3, 'F2')
                break
        return success()
    return failure()


def new_additive_expression():
    if case2('NewTerm') and new_term():
        while not (case2('F2') and F2()):
            error(2, 'F2')
            if 'eps' not in first('F2') and cur_token in follow('F2'):
                error(3, 'F2')
                break
        return success()
    return failure()


def EZEZEZ():
    if case1('='):
        while not (case2('Expression') and expression()):
            error(2, 'Expression')
            if 'eps' not in first('Expression') and cur_token in follow('Expression'):
                error(3, 'Expression')
                break
        c_assign()
        return success()
    if case2('F3') and F3():
        while not (case2('F2') and F2()):
            error(2, 'F2')
            if 'eps' not in first('F2') and cur_token in follow('F2'):
                error(3, 'F2')
                break
        while not (case2('E5') and E5()):
            error(2, 'E5')
            if 'eps' not in first('E5') and cur_token in follow('E5'):
                error(3, 'E5')
                break
        return success()
    return failure()


def new_var_call():
    if case1('('):
        s_check_id(0)
        s_fun_args_start()
        while not (case2('Args') and args()):
            error(2, 'Args')
            if 'eps' not in first('Args') and cur_token in follow('Args'):
                error(3, 'Args')
                break
        s_fun_args_finished()
        if not case1(')'):
            error(1, ')')
        c_return()
        return success()
    if case3('NewVarcall'):
        s_check_id(1)
        #s_check_id_finished()
        return success()
    return failure()


def F3():
    if case1('*'):
        while not (case2('Signedfactor') and signed_factor()):
            error(2, 'Signedfactor')
            if 'eps' not in first('Signedfactor') and cur_token in follow('Signedfactor'):
                error(3, 'Signedfactor')
                break
        c_mult()
        while not (case2('F3') and F3()):
            error(2, 'F3')
            if 'eps' not in first('F3') and cur_token in follow('F3'):
                error(3, 'F3')
                break
        return success()
    if case3('F3'):
        return success()
    return failure()


def new_term():
    if case2('NewSignedfactor') and new_signed_factor():
        while not (case2('F3') and F3()):
            error(2, 'F3')
            if 'eps' not in first('F3') and cur_token in follow('F3'):
                error(3, 'F3')
                break
        return success()
    if case2('NewFactor') and new_factor():
        while not (case2('F3') and F3()):
            error(2, 'F3')
            if 'eps' not in first('F3') and cur_token in follow('F3'):
                error(3, 'F3')
                break
        return success()
    return failure()


def F2():
    if case2('Addop') and addop():
        while not (case2('Term') and term()):
            error(2, 'Term')
            if 'eps' not in first('Term') and cur_token in follow('Term'):
                error(3, 'Term')
                break
        c_add_or_sub()
        while not (case2('F2') and F2()):
            error(2, 'F2')
            if 'eps' not in first('F2') and cur_token in follow('F2'):
                error(3, 'F2')
                break
        return success()
    if case3('F2'):
        return success()
    return failure()


def var_call():
    if case1('['):
        s_check_id(1)
        while not (case2('Expression') and expression()):
            error(2, 'Expression')
            if 'eps' not in first('Expression') and cur_token in follow('Expression'):
                error(3, 'Expression')
                break
        if not case1(']'):
            error(1, ']')
        c_computeIndex()
        #s_check_id_finished()
        return success()
    if case1('('):
        s_check_id(0)
        s_fun_args_start()
        while not (case2('Args') and args()):
            error(2, 'Args')
            if 'eps' not in first('Args') and cur_token in follow('Args'):
                error(3, 'Args')
                break
        s_fun_args_finished()
        if not case1(')'):
            error(1, ')')
        c_return()
        return success()
    if case3('NewVarcall'):
        s_check_id(1)
        return success()
    return failure()


def signed_factor():
    if case2('Factor') and factor():
        return success()
    if case1('+'):
        while not (case2('Factor') and factor()):
            error(2, 'Factor')
            if 'eps' not in first('Factor') and cur_token in follow('Factor'):
                error(3, 'Factor')
                break
        return success()
    if case1('-'):
        while not (case2('Factor') and factor()):
            error(2, 'Factor')
            if 'eps' not in first('Factor') and cur_token in follow('Factor'):
                error(3, 'Factor')
                break
        c_negate()
        return success()
    return failure()


def args():
    if case2('Arglist') and arglist():
        return success()
    if case3('Args'):
        return success()
    return failure()


def new_signed_factor():
    if case1('+'):
        while not (case2('Factor') and factor()):
            error(2, 'Factor')
            if 'eps' not in first('Factor') and cur_token in follow('Factor'):
                error(3, 'Factor')
                break
        return success()
    if case1('-'):
        while not (case2('Factor') and factor()):
            error(2, 'Factor')
            if 'eps' not in first('Factor') and cur_token in follow('Factor'):
                error(3, 'Factor')
                break
        c_negate()
        return success()
    return failure()


def new_factor():
    if case1('('):
        while not (case2('Expression') and expression()):
            error(2, 'Expression')
            if 'eps' not in first('Expression') and cur_token in follow('Expression'):
                error(3, 'Expression')
                break
        if not case1(')'):
            error(1, ')')
        return success()
    tmp = cur_token_vec.name
    if case1('num'):
        c_pushNum(tmp)
        return success()
    return failure()


def addop():
    if case1('+'):
        c_pushPlus()
        return success()
    elif case1('-'):
        c_pushMinus()
        return success()
    return failure()


def term():
    if case2('NewSignedfactor') and new_signed_factor():
        while not (case2('F3') and F3()):
            error(2, 'F3')
            if 'eps' not in first('F3') and cur_token in follow('F3'):
                error(3, 'F3')
                break
        return success()
    if case2('NewFactor') and new_factor():
        while not (case2('F3') and F3()):
            error(2, 'F3')
            if 'eps' not in first('F3') and cur_token in follow('F3'):
                error(3, 'F3')
                break
        return success()
    tmp = cur_token_vec.name
    if case1('id') and s_push_id(tmp):
        while not (case2('Varcall') and var_call()):
            error(2, 'Varcall')
            if 'eps' not in first('Varcall') and cur_token in follow('Varcall'):
                error(3, 'Varcall')
                break
        while not (case2('F3') and F3()):
            error(2, 'F3')
            if 'eps' not in first('F3') and cur_token in follow('F3'):
                error(3, 'F3')
                break
        return success()
    return failure()


def factor():
    if case1('('):
        while not (case2('Expression') and expression()):
            error(2, 'Expression')
            if 'eps' not in first('Expression') and cur_token in follow('Expression'):
                error(3, 'Expression')
                break
        if not case1(')'):
            error(1, ')')
        return success()
    tmp = cur_token_vec.name
    if case1('id') and s_push_id(tmp):
        while not (case2('Varcall') and var_call()):
            error(2, 'Varcall')
            if 'eps' not in first('Varcall') and cur_token in follow('Varcall'):
                error(3, 'Varcall')
                break
        return success()
    tmp = cur_token_vec.name
    if case1('num'):
        c_pushNum(tmp)
        return success()
    return failure()


def arglist():
    s_fun_args_increase()
    if case2('Expression') and expression():
        c_copy_argument()
        while not (case2('F4') and F4()):
            error(2, 'F4')
            if 'eps' not in first('F4') and cur_token in follow('F4'):
                error(3, 'F4')
                break
        return success()
    return failure()


def F4():
    if case1(','):
        s_fun_args_increase()
        while not (case2('Expression') and expression()):
            error(2, 'Expression')
            if 'eps' not in first('Expression') and cur_token in follow('Expression'):
                error(3, 'Expression')
                break
        c_copy_argument()
        while not (case2('F4') and F4()):
            error(2, 'F4')
            if 'eps' not in first('F4') and cur_token in follow('F4'):
                error(3, 'F4')
                break
        return success()
    if case3('F4'):
        return success()
    return failure()


def export_parse_tree():
    file = open('parse_tree.txt', 'w')
    text = ''
    global parse_tree
    for line in parse_tree:
        text += '|\t' * line[0] + line[1] + '\n'
    file.write(text)
    file.close()


def export_error_file():
    file = open('errors.txt', 'w')
    text = ''
    lex_err_file = open('Error.txt', 'r')
    lex_err = lex_err_file.read()
    global error_string
    for line in error_string:
        text += line + '\n'
    lex_err = lex_err.replace('\n', '\nscanner: ')
    lex_err = 'scanner: ' + lex_err
    text += lex_err
    file.write(text)
    file.close()
    lex_err_file.close()


def translate_token(token_vec):
    if token_vec.type in ['id', 'eof', 'num']:
        return token_vec.type
    else:
        return token_vec.name


if __name__ == '__main__':
    function_args_stack.push(0)
    initialize_lexer()
    parse_tree = [[0, 'program']]
    error_string = []
    depth = 0
    cur_token_vec = get_next_token()
    cur_token = translate_token(cur_token_vec)
    i = 0
    program()
    export_parse_tree()
    export_error_file()
    if not have_error:
        PB.export_generated_code()
    else :
        file = open('output.txt', 'w')
        file.write('')
        file.close()
