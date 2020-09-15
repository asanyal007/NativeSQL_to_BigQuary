import re
import pandas as pd
from os import listdir
from os.path import isfile, join
import function_convert
import pre_process
import convert_sql

file_path = 'C:/Workspace/SQL_To_BigQ/Objects_Complexity/Complex_SQL/'
out_file_path = r"C:\\Workspace\\SQL_To_BigQ\\Objects_Complexity\\Output_Complex\\"
diff_file_path = r"C:\\Workspace\\SQL_To_BigQ\\Objects_Complexity\\diffs\\Complex_SQL\\"
onlyfiles = [file_path+f for f in listdir(file_path) if isfile(join(file_path, f))]


main_ptrn = "[aA-zA_]+[(']+\w.*?\)+"
fallback_ptrn = "\s*([a-zA-Z_]\w*[(](\s*[a-zA-Z_]\w*[(]|[^()]+[)]|[)]))"
ptr = "[^aA-zZ][^0-9 \W]+"


#file = 'C:/Workspace/SQL_To_BigQ/Objects_Complexity/Complex_SQL/complex_text_sql.sql'
for file in onlyfiles:
    sql_file = open(file)
    sql_as_string = sql_file.read()
    dict_transaformed = pre_process.doublecolon_to_standard_cast(sql_as_string)
    file_name = file.split(r"/")[-1].split('.')[0]
    all_functions = convert_sql.get_functions(sql_as_string)
    #print(matches_main)
    ''' create list of functions conversons to be made'''
    df_converted_func = convert_sql.create_map(all_functions, dict_transaformed, file_name)
    df_converted_func.to_csv(r"venv\\Func_Dict\\{}.csv".format(file_name))

    ''' Creating converted SQL files based on the list'''
    new_sql_as_string = convert_sql.convert(sql_as_string,file,file_name)

    '''saving the convertedfile'''
    convert_sql.save_file(sql_as_string,out_file_path, file_name)

    ''' Creating diff'''
    convert_sql.diff(new_sql_as_string,sql_as_string,diff_file_path, file_name)









