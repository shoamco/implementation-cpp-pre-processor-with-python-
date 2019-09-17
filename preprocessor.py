include_my_file = 'include "'
include = 'include'
include_standard_library = 'include <'
define_macro = 'define'
file_folder = "PreprocessorTask/"
system_folder = "PreprocessorTask/system/"


def is_line_contain(line: str, words: str) -> bool:
    """
    get line and string and check if the line contain the list
    :param line: line of file that we want to check if is contain a specific word
    :param words:the string we look for
    :return:True if we find the string else return False
    """

    return line.find(words) != -1


def get_values_of_function(line: str) -> list:
    """
    get line and return all value between brackets
    for example:
    input: MAX(5,3)
    output:  [3,5]
    :param line:
    :return:
    """
    return line.split('(')[-1].split(')')[0].split(',')


def handle_macro(line: str, dict_macro: dict) -> str:
    """
    get line and replace the macro variable\function with the value macro
    :param line:  line in file that contain define
    :param dict_macro: dict of all variable macro (key-macro variable,value-macro value)
    :return:the new line after replace the macro
    """

    if not is_line_contain_define_macro(line):
        word_macro = find_variable_macro(line, dict_macro)
        if word_macro:

            print(f"word_macro {word_macro}")

            if is_line_contain(line, word_macro + '('):  # if is a macro function
                macro = dict_macro[word_macro].split(')')[0]

                list_val_function = get_values_of_function(line)
                list_val_function_macro = get_values_of_function(macro)

                start_cut = line.find(word_macro)
                end_cut = line.find(')')
                cut_line = line[start_cut:end_cut]


                # print(f"list_val_function{list_val_function}")
                # print(f"list_val_function_macro{list_val_function_macro}")


                line = line.replace(cut_line, dict_macro[word_macro])
                # print(f"----line {line}")
                # print(f"\n\nlist_val_function_macro[0] {list_val_function_macro[0]},list_val_function[1]:{list_val_function[0]} ")
                # print(f"list_val_function_macro[0]{list_val_function_macro[1].split()[0]},list_val_function[1]:{list_val_function[1].split()[0]} ")

                # len_val=len(list_val_function_macro)
                for index, val in enumerate(list_val_function_macro):
                    # print(f"index {index}, val  {val}, list_val_function[index]  {list_val_function[index]}")
                    # print(f"befor line : {line}")
                    line = line.replace(val, list_val_function[index])
                    # print(f"after line : {line}")


            else:  # if ia a macro variable
                line = line.replace(word_macro, dict_macro[word_macro])

    return line


def find_variable_macro(line: str, dict_macro: dict) -> str:
    """
    the function get line and return macro word if find in dict macro ,else None
    :param line: line of file that we look for the word macro
    :param dict_macro:dict of all variable macro (key-macro variable,value-macro value)
    :return: the word macro if find else return None
    """

    list_word = line.replace('(', " ").split()  # for

    for word in list_word:

        if word in dict_macro:
            return word

    return None


def is_line_contain_define_macro(line: str) -> bool:
    """
        check if the line contain variable macro ('#define' without '('-no macro function)
       :param line:  line of file that we want to check if is contain macro
       :return: True if contain macro ,else False
       """
    return is_line_contain(line, define_macro)
    # return is_line_contain(line, define_macro) and not is_line_contain(line, '(')  # macro variable not macro function


def is_line_contain_my_header_file(line: str) -> bool:
    """
     check if the line include my header file('#include " "')
    :param line:  line of file that we want to check if is contain include
    :return: True if contain include ,else False
    """
    return is_line_contain(line, include_my_file)


def is_line_contain_sl_header_file(
        line: str) -> bool:
    """
     check if the line include standard library header file('#include <>')
    :param line: line of file that we want to check if is contain include of standard library
    :return:True if contain include of standard library,else False
    """
    return is_line_contain(line, include_standard_library)


def handle_include(line: str, output_lines: list, dict_macro: dict) -> (list, dict):
    if is_line_contain_my_header_file(line):  # if the line contain include to my file (#include "")
        return handle_include_header_file(line, output_lines, dict_macro, False)
    elif is_line_contain_sl_header_file(line):
        return handle_include_header_file(line, output_lines, dict_macro, True)


def copy_header_file(header_file: str, dict_macro: dict) -> (list, dict):
    """
    copy all lines from header file,if the line contain include -handel this
    :param header_file: the header file that we want to copy
    :parameter dict_macro:dict of all variable macro (key-macro variable,value-macro value)
    :return: list of all copy lines
    """
    output = []
    with open(header_file) as f:
        lines = f.readlines()
        for line in lines:
            if is_line_contain_my_header_file(line):
                lines, dict_macro = handle_include_header_file(line, lines, dict_macro, False)  # todo:Recursive

            elif is_line_contain_define_macro(line):
                add_macro_to_dict(line, dict_macro)

    return output, dict_macro



def handle_include_header_file(line: str, output_lines: list, dict_macro: dict, is_standard_library: bool) -> (
        list, dict):
    """
    copy the header file  in the  include (in the line)
    :param line: line in file that contain include
    :param output_lines: the list of all output line after preprocessor
     :param dict_macro: dict of all variable macro (key-macro variable,value-macro value)
    :param is_standard_library: if the include is to a standard library =True ,else =False
    :return: the new list of output line after preprocessor copy the header file,and the list of macro variables
    """
    header_file = get_name_header_file(line, is_standard_library)  # get name hader file
    output_lines, dict_macro = copy_header_file(header_file, dict_macro)
    output_lines += output_lines
    return output_lines, dict_macro


def get_name_header_file(line: str, is_standard_library: bool) -> str:
    """
    return the name of the header file-if the include is a standard_library Return also the folder name of  standard_library
    :param line: line in file that contain include
    :param is_standard_library:  if the include is to a standard library =True ,else =False
    :return: return the name of the header file
    """
    return system_folder + line.split('<')[1][:-2] + '.h' if is_standard_library else file_folder + line.split('"')[1]


def write_to_pp_file(output_file: str, list_lines: list, dict_macro: dict) -> None:
    """
    writing all the line of the cpp file and the line the preprocessor copy from header files
    :param output_file: the file output (FILE.pp)
    :param dict_macro:dict of all variable macro (key-macro variable,value-macro value)
    :param list_lines: the list that contain all the lines we want to write into the file
    :return:None
    """

    with open(output_file, 'w') as f:
        for line in list_lines:
            if is_line_contain(line, include):
                output_lines, dict_macro = handle_include(line, output_lines, dict_macro)
            elif is_line_contain_define_macro(line):
                add_macro_to_dict(line, dict_macro)
            else:
                print(f"line {line}")
                line = handle_macro(line, dict_macro)
                f.write(line)


def add_macro_to_dict(line: str, dict_macro: dict) -> dict:
    if is_line_contain(line, '('):  # if is macro function
        line2 = line.replace("#define", "")
        name_function = line2.split('(')[0].replace(" ", "")
        dict_macro[name_function] = line2  # insert macro key=macro variable, value=macro value
    else:
        word_list = line.split()
        variable_macro = word_list[1]
        value_macro = word_list[2] if len(word_list) > 2 else ""
        dict_macro[variable_macro] = value_macro  # insert macro key=macro variable, value=macro value
    return dict_macro


def read_cpp_file(input_file: str) -> (
        list, dict):  # read cpp file and return a list of all new line after preprocessor
    """
    get a cpp file and do preprocessor on it,and return the list of all new line
    :param input_file: cpp file that the preprocessor read
    :return: list of all the new line after the work of the preprocessor
    """

    output_lines = []  # list of all new line after preprocessor
    dict_macro = dict()  # list of all variable macro

    with open(input_file) as f:
        lines = f.readlines()
        for line in lines:
            if is_line_contain(line, include):
                output_lines, dict_macro = handle_include(line, output_lines, dict_macro)
            elif is_line_contain_define_macro(line):
                add_macro_to_dict(line, dict_macro)
            else:
                # print(f"line {line}")
                output_lines.append(line)


    return output_lines, dict_macro


def preprocessor(input_file,output_pp_file):
    """
    the function is a simulator of preprocessor
    is read a cpp file :replace macro define and include:
    is open all the included files and will plant the declarations and macros in the caller source file,
     and will replace all the places in the code which use these macros with the proper literal values of them
    and create a new pp file(with the same name of cpp file) with all the line after preprocessor
    :return:None
    """

    output_lines, dict_macro = read_cpp_file(input_file)  # read cpp file and return list of the new line
    write_to_pp_file(output_pp_file, output_lines, dict_macro)  # write the new line into pp file
