include_my_file = 'include "'
include_line = 'include'
include_standard_library = 'include <'
ifndef = "#ifndef"
pragma_once = "#pragma once"
define_macro = 'define'
file_folder = "PreprocessorTask/"
system_folder = "PreprocessorTask/system/"


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
    return is_line_contain(line, ifndef) or is_line_contain(line, pragma_once)


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
    print(f"line: {line}")
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
        print(f"header_file_name {header_file_name}")
        temp_copy_line, temp_header_list = read_header_file(header_file_name, copy_lines, header_read_list)
        copy_lines += temp_copy_line
        header_read_list += temp_header_list
    elif is_line_contain_sl_header_file(line):
        header_file_name = get_name_header_file(line, True)  # get name header file
        print(f"header_file_name {header_file_name}")
        temp_copy_line, temp_header_list = read_header_file(header_file_name, copy_lines, header_read_list)
        copy_lines += temp_copy_line
        header_read_list += temp_header_list
    return copy_lines, header_read_list


# def handle_include_header_file(line: str, output_lines: list, dict_macro: dict, is_standard_library: bool) -> (
#         list, dict):
#     """
#     copy the header file  in the  include (in the line)
#     :param line: line in file that contain include
#     :param output_lines: the list of all output line after preprocessor
#      :param dict_macro: dict of all variable macro (key-macro variable,value-macro value)
#     :param is_standard_library: if the include is to a standard library =True ,else =False
#     :return: the new list of output line after preprocessor copy the header file,and the list of macro variables
#     """
#     header_file = get_name_header_file(line, is_standard_library)  # get name hader file
#     output_lines, dict_macro = copy_header_file(header_file, dict_macro)
#     output_lines += output_lines
#     return output_lines, dict_macro
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
                    break
                else:

                    header_read_list.append(header_file)

            elif is_line_contain(line, include_line):


                temp_copy_lines, temp_header_read_list = handel_line_include(line, copy_lines, header_read_list)
                copy_lines += temp_copy_lines
                header_read_list += temp_header_read_list

            else:
                # print(f"line {line}")
                copy_lines.append(line)

    return copy_lines, header_read_list


def read_cpp_file(input_file: str) -> list:  # read cpp file and return a list of all new line after preprocessor
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
                temp_copy_lines, temp_header_read_list = handel_line_include(line, copy_lines, header_read_list)
                copy_lines += temp_copy_lines
                header_read_list += temp_header_read_list




            else:
                # print(f"line {line}")
                copy_lines.append(line)

    return copy_lines


def write_to_file_step1(output_file: str, list_lines: list) -> None:
    """
    writing all the line that we copy from cpp and header file into pp file
    :param output_file: the file output (FILE.pp)
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
    write_to_file_step1(output_pp_file, output_lines)  # write the new line into pp file
