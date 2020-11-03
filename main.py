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
import post_process
logging.basicConfig(filename='app.log', level=logging.INFO)

file_path = 'C:/Workspace/SQL_To_BigQ/Objects_Complexity/Complex_SQL/'
out_file_path = r"C:\\Workspace\\SQL_To_BigQ\\Objects_Complexity\\Output_Complex\\"
diff_file_path = r"C:\\Workspace\\SQL_To_BigQ\\Objects_Complexity\\diffs\\Complex_SQL\\"
onlyfiles = [file_path+f for f in listdir(file_path) if isfile(join(file_path, f))]


main_ptrn = "[aA-zA_]+[(']+\w.*?\)+"
fallback_ptrn = "\s*([a-zA-Z_]\w*[(](\s*[a-zA-Z_]\w*[(]|[^()]+)[)])"
ptr = "[^aA-zZ][^0-9 \W]+"



#for file in onlyfiles:
file = 'C:/Workspace/SQL_To_BigQ/Objects_Complexity/Complex_SQL/all_agent_metrics_sf.sql'
print("Reading {}".format(file))
sql_file = open(file)
sql_as_string = sql_file.read()
'''replace double colon'''
sql_as_string, dict_transaformed = pre_process.doublecolon_to_standard_cast(sql_as_string)
df_regex_map = pre_process.regex_replace(sql_as_string, keyword_maps.regex_map)
file_name = file.split(r"/")[-1].split('.')[0]
''' generaing list of functions in SQL'''
all_functions = convert_sql.get_func(sql_as_string)
''' create list of functions conversons to be made'''
df_converted_func = convert_sql.create_map(all_functions, dict_transaformed, file_name, main_ptrn)

''' Covert tables'''
sql_as_string= convert_sql.convert_tables(sql_as_string, API_Check.get_schema())
''' Direct conversions'''
df_direct_conv = function_convert.map_direct(keyword_maps.direct_conversion)
new_df = pd.concat([df_converted_func, df_direct_conv, df_regex_map ]).reset_index()
new_df.to_csv(r"venv\\Func_Dict\\{}.csv".format(file_name))



''' Creating converted SQL files based on the list'''
new_sql_as_string = convert_sql.convert(sql_as_string,file,file_name)



''' convert ref'''
#new_sql_as_string = convert_sql.convert_reference(new_sql_as_string)

'''saving the convertedfile'''
convert_sql.save_file(new_sql_as_string,out_file_path, file_name)

#print(API_Check.API_check(new_sql_as_string))
'''Checking with API'''

file_log = open("log/run_log/{}.log".format(file_name), "w+")

# get error report
result, err = API_Check.API_check(new_sql_as_string)
if isinstance(result, list):
    errors = result[0]['message']
    if "argument types:" in errors:
        print(file_name +": "+ str(errors))
        logging.error(file +": "+ str(errors))
        for er in str(err):
            file_log.writelines(er)

    else:
        print(file_name +": "+"There is no syntax errors")
        logging.info(file+ ": There is no syntax errors")
        # get stats
        job_detail = API_Check.get_stats(new_sql_as_string)
        if job_detail:
            val = job_detail.total_bytes_processed
        else:
            val = 0
        logging.info(file+ ": Total bytes processed {}".format(val))
        file_log.write(file+ ": There is no syntax errors")
file_log.close()
''' Creating diff'''
convert_sql.diff(new_sql_as_string,sql_as_string,diff_file_path, file_name)

final_function_list = convert_sql.get_func(new_sql_as_string)


function_log = open("log/function_log/success/function_{}.log".format(file_name), "w+")
function_err_log = open("log/function_log/error/function_error_{}.log".format(file_name), "w+")

for f in list(set(final_function_list)):
    result, err = API_Check.API_check("select {} ".format(f))
    if isinstance(result, list):
        errors = result[0]['message']

        if "Function not found:" in errors:
            print(f + ": " + str(errors))
            function_err_log.write(f + ": " + str(errors)+"\n")
            new_sql_as_string = convert_sql.re_try(sql_as_string, f, file_name)
        else:
            print(f + ": " + "There is no syntax errors")
            function_log.write(f + ": " + "There is no syntax errors\n")
function_log.close()
function_err_log.close()

# Post_process

new_sql_as_string = post_process.process_union(new_sql_as_string)

convert_sql.save_file(new_sql_as_string,out_file_path, file_name)








