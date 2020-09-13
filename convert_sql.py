import pandas as pd
import re
import difflib
import function_convert

def create_map(matches_main, matches_fallback, dict_transaformed, file_name):
    list_of_functions = []
    for a in matches_main:
        if re.findall('\((.*?)\)', a[0]):
            list_of_functions.append(a[0])

    for b in matches_fallback:
        if re.findall('\((.*?)\)', b[0]) and b not in list_of_functions:
            list_of_functions.append(b[0])
    for matches in list_of_functions:
        dict_transaformed[matches] = function_convert.map_function(matches)

    df_converted_func = pd.DataFrame.from_dict(dict_transaformed, orient='index').reset_index()
    df_converted_func = df_converted_func.rename(columns={'index': 'SQL_Functions', 0: 'Converted_Functions'},
                                                 inplace=False)

    return df_converted_func



def convert(sql_as_string,file_path,out_path):

    sql_file = open(file_path)
    file_name = file_path.split(r"/")[-1].split('.')[0]
    map = pd.read_csv(r"venv\\Func_Dict\\{}.csv".format(file_name))
    sql_as_string = sql_file.read()
    for s in map['SQL_Functions']:
        replace_str = map[map['SQL_Functions'] == s]['Converted_Functions'].iloc[0]
        if "(" in replace_str:
            sql_as_string = sql_as_string.replace(s,replace_str)
    return sql_as_string

def diff(new_sql_as_string,old_sql_as_string,diff_file_path,file_name):
    f = open(diff_file_path +file_name + "_diff.sql", "w+")
    for line in difflib.unified_diff(old_sql_as_string.strip().splitlines(), new_sql_as_string.strip().splitlines(),
                                     fromfile='old_file', tofile='sql_as_string', lineterm=''):
        f.write("\n"+line)
        f.truncate()
    f.close()
def save_file(sql_as_string,out_file_path,file_name):
    f = open(out_file_path+file_name+"_BigQ.sql", "w+")
    f.write(sql_as_string)
    f.truncate()
    f.close()
