import my_preprocessor
file_folder = "PreprocessorTask/"
system_folder = "PreprocessorTask/system/"


def test_factorial_cpp():
    input_file = file_folder + 'factorial.cpp'
    output_pp_file = 'factorial.pp'
    my_preprocessor.preprocessor(input_file, output_pp_file)


def test_inter_cpp():
    input_file = file_folder + 'inter.cpp'
    output_pp_file = 'inter.pp'
    my_preprocessor.preprocessor(input_file, output_pp_file)

def test_main_cpp():
    input_file = file_folder + 'main.cpp'
    output_pp_file = 'main.pp'
    my_preprocessor.preprocessor(input_file, output_pp_file)




if __name__ == '__main__':
    test_inter_cpp()
    test_factorial_cpp()
    test_main_cpp()
