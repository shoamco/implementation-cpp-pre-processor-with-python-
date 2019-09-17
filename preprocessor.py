include_my_file = 'include "'
include_standard_library = 'include <'
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


def is_line_contain_my_header_file(line: str) -> bool:
    """
     check if the line include my header file('#include " "')
    :param line:  line of file that we want to check if is contain include
    :return: True if contain include ,else False
    """
    return line.find(include_my_file) != -1


def is_line_contain_sl_header_file(
        line: str) -> bool:
    """
     check if the line include standard library header file('#include <>')
    :param line: line of file that we want to check if is contain include of standard library
    :return:True if contain include of standard library,else False
    """
    return line.find(include_standard_library) != -1


def copy_header_file(header_file: str) -> list:
    """
    copy all lines from header file,if the line contain include -handel this
    :param header_file: the header file that we want to copy
    :return: list of all copy lines
    """
    output = []
    with open(header_file) as f:
        lines = f.readlines()
        for line in lines:
            if is_line_contain_my_header_file(line):
                lines = handle_include_header_file(line, lines, False)  # todo:recorsivi
            elif not is_line_contain(line, "#"):
                output.append(line)

    return output


def handle_include_header_file(line: str, output_lines: list, is_standard_library: bool) -> list:
    """
    copy the header file  in the  include (in the line)
    :param line: line in file that contain include
    :param output_lines: the list of all output line after preprocessor
    :param is_standard_library: if the include is to a standard library =True ,else =False
    :return: the new list of output line after preprocessor copy the header file
    """
    header_file = get_name_header_file(line, is_standard_library)  # get name hader file
    output_lines += (copy_header_file(header_file))
    return output_lines


def get_name_header_file(line: str, is_standard_library: bool) -> str:
    """
    return the name of the header file-if the include is a standard_library Return also the folder name of  standard_library
    :param line: line in file that contain include
    :param is_standard_library:  if the include is to a standard library =True ,else =False
    :return: return the name of the header file
    """
    return system_folder + line.split('<')[1][:-2] + '.h' if is_standard_library else file_folder + line.split('"')[1]


def write_to_pp_file(output_file: str, list_lines: list):
    """
    writing all the line of the cpp file and the line the preprocessor copy from header files
    :param output_file: the file output (FILE.pp)
    :param list_lines: the list that contain all the lines we want to write into the file
    :return:None
    """
    with open(output_file, 'w') as f:
        for line in list_lines:
            if is_line_contain_my_header_file(line):  # if the line contain include to my file (#include "")
                output_lines = handle_include_header_file(line, output_lines, False)
            elif is_line_contain_sl_header_file(line):
                output_lines = handle_include_header_file(line, output_lines, True)
            else:
                f.write(line)


def read_cpp_file(input_file: str) -> list:  # read cpp file and return a list of all new line after preprocessor
    """
    get a cpp file and do preprocessor on it,and return the list of all new line
    :param input_file: cpp file that the preprocessor read
    :return: list of all the new line after the work of the preprocessor
    """

    output_lines = []

    with open(input_file) as f:
        lines = f.readlines()

        for line in lines:
            if is_line_contain_my_header_file(line):  # if the line contain include to my file (#include "")
                output_lines = handle_include_header_file(line, output_lines, False)
            elif is_line_contain_sl_header_file(line):
                output_lines = handle_include_header_file(line, output_lines, True)

            else:
                output_lines.append(line)

    return output_lines


def preprocessor():
    """
    the function is a simulator of preprocessor
    is read a cpp file :replace macro define and include
    and create a new pp file(with the same name of cpp file) with all the line after preprocessor
    :return:None
    """
    input_file = file_folder + 'factorial.cpp'
    output_pp_file = 'factorial.pp'
    output_lines = read_cpp_file(input_file)  # read cpp file and return list of the new line
    write_to_pp_file(output_pp_file, output_lines)  # write the new line into pp file
