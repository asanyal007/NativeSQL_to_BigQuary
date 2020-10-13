import re
import pandas as pd
from os import listdir
from os.path import isfile, join
import keyword_maps
import function_convert
import pre_process
import convert_sql
import API_Check
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)

file_path = 'C:/Workspace/SQL_To_BigQ/Objects_Complexity/Complex_SQL/'
out_file_path = r"C:\\Workspace\\SQL_To_BigQ\\Objects_Complexity\\Output_Complex\\"
diff_file_path = r"C:\\Workspace\\SQL_To_BigQ\\Objects_Complexity\\diffs\\Complex_SQL\\"
onlyfiles = [file_path+f for f in listdir(file_path) if isfile(join(file_path, f))]


main_ptrn = "[aA-zA_]+[(']+\w.*?\)+"
fallback_ptrn = "\s*([a-zA-Z_]\w*[(](\s*[a-zA-Z_]\w*[(]|[^()]+)[)])"
ptr = "[^aA-zZ][^0-9 \W]+"



for file in onlyfiles:
    #file = 'C:/Workspace/SQL_To_BigQ/Objects_Complexity/Complex_SQL/d_all_agent_metrics.sql'
    sql_file = open(file)
    sql_as_string = sql_file.read()
    dict_transaformed = pre_process.doublecolon_to_standard_cast(sql_as_string)
    df_regex_map = pre_process.regex_replace(sql_as_string, keyword_maps.regex_map)
    file_name = file.split(r"/")[-1].split('.')[0]
    all_functions = convert_sql.get_functions(sql_as_string)
    print(all_functions)
    #exit()
    ''' create list of functions conversons to be made'''
    df_converted_func = convert_sql.create_map(all_functions, dict_transaformed, file_name, fallback_ptrn)
    df_direct_conv = function_convert.map_direct(keyword_maps.direct_conversion)
    new_df = pd.concat([df_converted_func, df_direct_conv, df_regex_map ]).reset_index()
    new_df.to_csv(r"venv\\Func_Dict\\{}.csv".format(file_name))

    ''' Creating converted SQL files based on the list'''
    new_sql_as_string = convert_sql.convert(sql_as_string,file,file_name)

    '''saving the convertedfile'''
    convert_sql.save_file(new_sql_as_string,out_file_path, file_name)

    #print(API_Check.API_check(new_sql_as_string))
    '''Checking with API'''

    file_log = open("log/{}.log".format(file_name), "w+")


    result, err = API_Check.API_check(new_sql_as_string)
    if isinstance(result, list):
        errors = result[0]['message']
        if "Syntax error:" in errors:
            print(errors)
            logging.error(file +": "+ str(err))
            for er in str(err):
                file_log.writelines(er)

        else:
            print("There is no syntax errors")
            logging.info(file+ ": There is no syntax errors")
            file_log.write(file+ ": There is no syntax errors")
    file_log.close()
    ''' Creating diff'''
    convert_sql.diff(new_sql_as_string,sql_as_string,diff_file_path, file_name)









