include_my_file = 'include "'
hash_tag = '#'
include_line = 'include'
include_standard_library = 'include <'
ifn_def = "#ifndef"
pragma_once = "#pragma once"
define_macro = 'define'
file_folder = "PreprocessorTask/"
system_folder = "PreprocessorTask/system/"


def add_macro_to_dict(line: str, dict_macro: dict) -> dict:
    """
    get line with macro and insert it into the dict,Handle both macro variable and macro function
    :param line:line with macro -#define
    :param dict_macro: dict of all variable macro (key-macro variable,value-macro value)
    :return: dict_macro
    """
    if is_line_contain(line, '('):  # if is macro function
        line2 = line.replace("#define", "")
        name_function = line2.split('(')[0].replace(" ", "")  # name macro function
        dict_macro[name_function] = line2  # insert macro key=macro variable, value=macro value
    else:  # macro variable
        word_list = line.split()
        variable_macro = word_list[1]
        value_macro = word_list[2] if len(word_list) > 2 else ""
        dict_macro[variable_macro] = value_macro  # insert macro key=macro variable, value=macro value
    return dict_macro


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


def is_line_contain_ifndef_or_pragma_once(line: str) -> bool:
    return is_line_contain(line, ifn_def) or is_line_contain(line, pragma_once)


def is_line_contain_define_macro(line: str) -> bool:
    """
        check if the line contain variable macro ('#define' without '('-no macro function)
       :param line:  line of file that we want to check if is contain macro
       :return: True if contain macro ,else False
       """
    return is_line_contain(line, define_macro)



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


def get_name_header_file(line: str, is_standard_library: bool) -> str:
    """
    return the name of the header file-if the include is a standard_library Return also the folder name of  standard_library
    :param line: line in file that contain include
    :param is_standard_library:  if the include is to a standard library =True ,else =False
    :return: return the name of the header file
    """

    return system_folder + line.split('<')[1][:-2] + '.h' if is_standard_library else file_folder + line.split('"')[1]


def handel_line_include(line: str, copy_lines: list, header_read_list: list) -> (list, list):
    """
    check if the line include standard library of my header and call the function that copy the header file
    :param line: the line that contain include
    :param copy_lines: list of the copy line
    :return:
    """
    if is_line_contain_my_header_file(line):

        header_file_name = get_name_header_file(line, False)  # get name header file

        copy_lines, header_read_list = read_header_file(header_file_name, copy_lines, header_read_list)

    elif is_line_contain_sl_header_file(line):
        header_file_name = get_name_header_file(line, True)  # get name header file

        copy_lines, header_read_list = read_header_file(header_file_name, copy_lines, header_read_list)

    return copy_lines, header_read_list


def read_header_file(header_file: str, copy_lines: list, header_read_list: list) -> (list, list):
    """
    get a header file if not open before(#pragma once/#ifndef):copy all
    :param header_file: header file that the preprocessor read and copy
    :param copy_lines: list of line that we copy into it
    :return: copy_lines
    """

    with open(header_file) as f:
        lines = f.readlines()
        for line in lines:
            if is_line_contain_ifndef_or_pragma_once(line):

                if header_file in header_read_list:
                    return copy_lines, header_read_list
                else:

                    header_read_list.append(header_file)

            elif is_line_contain(line, include_line):

                copy_lines, temp_copy_lines = handel_line_include(line, copy_lines, header_read_list)


            else:
                # print(f"line {line}")
                copy_lines.append(line)

    return copy_lines, header_read_list


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
            if is_line_contain(line, word_macro + '('):  # if is a macro function

                macro = dict_macro[word_macro].split(')')[0]
                list_val_function = get_values_of_function(line)
                list_val_function_macro = get_values_of_function(macro)

                start_cut = line.find(word_macro)
                end_cut = line.find(')')
                cut_line = line[start_cut:end_cut]

                line = line.replace(cut_line, dict_macro[word_macro])

                for index, val in enumerate(list_val_function_macro):
                    line = line.replace(val.strip(), list_val_function[index].strip())
            else:  # if ia a macro variable
                line = line.replace(word_macro, dict_macro[word_macro])

    return line


def read_output_file(input_file: str) -> list:
    copy_lines = []  # list of all new line after copy
    dict_macro = dict()
    with open(input_file) as f:
        lines = f.readlines()
        for line in lines:

            if is_line_contain_define_macro(line):
                add_macro_to_dict(line, dict_macro)
            elif not is_line_contain(line, hash_tag):
                line = handle_macro(line, dict_macro)
                copy_lines.append(line)

    return copy_lines


def read_cpp_file(input_file: str) -> list:  #
    """
    get a cpp file and copy all line .if line contain include-open header file
    :param input_file: cpp file that the preprocessor read
    :return: list of all the new line after the work of the preprocessor
    """

    copy_lines = []  # list of all new line after copy
    header_read_list = []  # list of all header file that we read

    with open(input_file) as f:
        lines = f.readlines()
        for line in lines:
            if is_line_contain(line, include_line):
                copy_lines, header_read_list = handel_line_include(line, copy_lines, header_read_list)

            else:
                # print(f"line {line}")
                copy_lines.append(line)

    return copy_lines


def write_to_file(output_file: str, list_lines: list) -> None:
    """
    writing all the line that we copy from cpp and header file into pp file
    :param output_file:  the output file  (FILE.pp)
    :param list_lines: the list that contain all the lines we want to write into the file
    :return:None
    """

    with open(output_file, 'w') as f:
        for line in list_lines:
            f.write(line)


def preprocessor(input_file, output_pp_file):
    """
    the function is a simulator of preprocessor
    is read a cpp file :replace macro define and include:
    is open all the included files and will plant the declarations and macros in the caller source file,
     and will replace all the places in the code which use these macros with the proper literal values of them
    and create a new pp file(with the same name of cpp file) with all the line after preprocessor
    :return:None
    """

    output_lines = read_cpp_file(input_file)  # read cpp file and return list of the new line
    write_to_file(output_pp_file, output_lines)  # write the new line into pp file
    output_lines = read_output_file(output_pp_file)
    write_to_file(output_pp_file, output_lines)
