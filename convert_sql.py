import pandas as pd
import re
import difflib
import function_convert
from keyword_maps import keywords_map, datatype
def get_functions(sql_as_string):
    open_br = 0
    closed_br = 0
    list_of_function = []
    list_of_fun_name_new = []
    i = 0
    ptr = "[aA-zZ]+\("
    ptr2 = "[aA-zA_]+[(']+\w.*?\)+"
    ptr3 = "{}+[(']+\w.*?\)+"
    for ptr in datatype:
        patrn = ptr3.format(ptr)
        for a in re.findall(patrn, sql_as_string, re.IGNORECASE):
            list_of_fun_name_new.append(a)
    keys = [k.split('(')[0] for k in keywords_map.keys()]
    list_of_fun_name = [a.split("(")[0] for a in re.findall(ptr, sql_as_string) if a.split("(")[0] in keys]
    list_of_fun_column_names = re.findall(ptr2, sql_as_string)

    list_of_fun_name.append("contains")
    for s in list_of_fun_name:
        start = sql_as_string.find(s + "(")
        sub_str = sql_as_string[start:len(sql_as_string)]
        for a in sub_str:
            i = i + 1
            if "(" in a:
                open_br = open_br + 1
            elif ")" in a:
                closed_br = closed_br + 1
            if (open_br + closed_br) > 0 and (open_br == closed_br):
                list_of_function.append(sub_str[0:i])
                open_br = 0
                closed_br = 0
                i = 0
                break
                # sub_str = ""
    return list(set(list_of_function+list_of_fun_name_new+list_of_fun_column_names))

def create_map(all_functions, dict_transaformed, file_name, ptrn):
    for matches in all_functions:
        '''balnces the opening and closing brackets'''
        open_br = matches.count("(")
        closing_br = matches.count(")")
        diff_count = closing_br - open_br
        if diff_count>0:
            for i in range(diff_count):
                matches = matches.replace(")","")
        elif diff_count<0:
            for i in range(diff_count):
                matches = matches.replace("(","")


        try:
            dict_transaformed[matches] = function_convert.map_function(matches)
            #print(dict_transaformed)
        except:
            dict_transaformed["-"] = function_convert.map_function(matches)

    df_converted_func = pd.DataFrame.from_dict(dict_transaformed, orient='index').reset_index()
    print(dict_transaformed)
    df_converted_func = df_converted_func.rename(columns={'index': 'SQL_Functions', 0: 'Converted_Functions'},
                                                 inplace=False)

    return df_converted_func



def convert(sql_as_string,file_path,out_path):

    sql_file = sql_as_string
    file_name = file_path.split(r"/")[-1].split('.')[0]
    map = pd.read_csv(r"venv\\Func_Dict\\{}.csv".format(file_name))
    sql_as_string = sql_file
    for s in map['SQL_Functions']:
        replace_str = map[map['SQL_Functions'] == s]['Converted_Functions'].iloc[0]

        if replace_str != "Not Available":
            print("replace value", s, replace_str)
            #sql_as_string = sql_as_string.replace(s,replace_str)
            redata = re.compile(re.escape(s), re.IGNORECASE)
            sql_as_string = redata.sub(replace_str, sql_as_string)
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

def convert_tables(sql_as_string, map):
    for key, val in map.items():
        #redata = re.compile(r'\bstg_sfdc_task\b', re.IGNORECASE)
        sql_as_string = sql_as_string.replace("cs_supp.","")
        sql_as_string = re.sub(r'\b{}\b'.format(key.lower()),val, sql_as_string)
    #print(sql_as_string)
    #exit()
    return sql_as_string
