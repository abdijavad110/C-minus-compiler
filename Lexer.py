class Token:
    def __init__(self, type, name, line_number):
        self.type = type
        self.name = name
        self.line_number = line_number


class Invalid_token:
    def __init__(self, name, line):
        self.name = name
        self.line = line


tokens = []
token_number = 0
invalid_tokens = []


def get_next_token():
    global token_number
    global tokens
    if token_number < len(tokens):
        token_number += 1
        # print(tokens[token_number - 1].type, tokens[token_number - 1].name)
        return tokens[token_number - 1]


# ises
def is_keyword(buffer):
    keywords = ["if", "else", "void", "int", "while", "break",
                "continue", "switch", "default", "case", "return"]
    for str in keywords:
        if str == buffer:
            return True
    return False


def is_symbol(buffer):
    symbols = [";", ":", ",", "[", "]", "(", ")", "{",
               "}", "+", "-", "*", "=", "<"]
    for str in symbols:
        if str == buffer:
            return True
    return False


def is_whitespace(buffer):
    whitespaces = [" ", "\n", "\r", "\t", "\v", "\f"]
    for str in whitespaces:
        if str == buffer:
            return True
    return False


def is_id(buffer):
    if not buffer[0].isalpha():
        return False
    for single_char in buffer[1:]:
        if not (single_char.isalpha() or single_char.isdigit()):
            return False
    return True


def is_num(buffer):
    return buffer.isdigit()


line_number = 1
line_to_write = "1. "


def handle_buffer(buffer):
    global line_to_write
    global line_number
    if is_keyword(buffer):
        tkn = Token("keyword", buffer, line_number)
        tokens.append(tkn)
        line_to_write += ("(" + tkn.type + ", " + tkn.name + ") ")
    elif is_id(buffer):
        tkn = Token("id", buffer, line_number)
        tokens.append(tkn)
        line_to_write += ("(" + tkn.type + ", " + tkn.name + ") ")
    elif is_num(buffer):
        tkn = Token("num", buffer, line_number)
        tokens.append(tkn)
        line_to_write += ("(" + tkn.type + ", " + tkn.name + ") ")
    elif buffer[0].isdigit():
        i = 1
        while i < len(buffer):
            if buffer[i].isalpha():
                break
            i += 1
        handle_buffer(buffer[:i])
        handle_buffer(buffer[i:])
    else:
        itoken = Invalid_token(buffer, line_number)
        invalid_tokens.append(itoken)


# text = "void main(void){\n  int a = 0;\n    // comment\n" \
#        "a = 2+ +2;\n    a = a + -3;\n   cde = a;\n  " \
#        "if (b /* comment2 */ == 3) {\n      a = 3;\n\t\t" \
#        "cd!e = -7;\n\t\t}\n\t\telse\n\t\t{\n\t\t\t" \
#        "b = a < cde;\n\t\t\t{cde = @2;\n\t\t}}\n\t\t" \
#        "return;\n}"
file = open("input.txt", "r")
output_file = open("lexer_output.txt", "w")
error_file = open("Error.txt", "w")
text = file.read()
text_size = len(text)
buffer = ""
i = 0


def initialize_lexer():
    global i, buffer, line_number, line_to_write, invalid_tokens
    while i < text_size:
        single_char = text[i]
        if is_symbol(single_char):
            if buffer != "":
                handle_buffer(buffer)
                buffer = ""
            tkn = None
            if single_char == "=":
                if i + 1 < text_size and text[i + 1] == "=":
                    tkn = Token("symbol", "==", line_number)
                    i += 1
                else:
                    tkn = Token("symbol", single_char, line_number)
            else:
                tkn = Token("symbol", single_char, line_number)
            tokens.append(tkn)
            line_to_write += ("(" + tkn.type + ", " + tkn.name + ") ")

        elif single_char == "/":
            if text[i + 1] == "*":
                i += 2
                while (i < text_size - 1) and (text[i:i + 2] != "*/"):
                    i += 1
                if i >= text_size - 1:
                    break
                i += 1
            elif text[i + 1] == "/":
                i += 2
                while i < text_size and text[i] != "\n":
                    i += 1
                if i >= text_size:
                    break
                i -= 1
            else:
                buffer += single_char
                itoken = Invalid_token(buffer, line_number)
                invalid_tokens.append(itoken)
                buffer = ""

        elif is_whitespace(single_char):
            if buffer != "":
                handle_buffer(buffer)
                buffer = ""
            if single_char == "\n":
                output_file.write(line_to_write)
                output_file.write("\n")
                line_number += 1
                line_to_write = str(line_number) + ". "

        elif single_char.isalpha() or single_char.isdigit():
            buffer += single_char

        else:
            buffer += single_char
            itoken = Invalid_token(buffer, line_number)
            invalid_tokens.append(itoken)
            buffer = ""
        i += 1

    # Reached end of text
    if i >= text_size:
        if buffer != "":
            handle_buffer(buffer)
        output_file.write(line_to_write)
        tokens.append(Token("eof", "eof", line_number))

        if len(invalid_tokens) != 0:
            current_line = invalid_tokens[0].line
            error_write_line = str(invalid_tokens[0].line) + ". "
            for token in invalid_tokens:
                if current_line == token.line:
                    error_write_line += ("(" + token.name + ", invalid input) ")
                else:
                    error_file.write(error_write_line)
                    error_file.write("\n")
                    current_line = token.line
                    error_write_line = str(current_line) + ". (" + token.name + ", invalid input) "
            error_file.write(error_write_line)
            error_file.close()
            file.close()

# while 1:
#     next_token = get_next_token()
#     print(next_token.type, next_token.name, next_token.line_number)
#     if(next_token.type == "EOF"):
#         break
