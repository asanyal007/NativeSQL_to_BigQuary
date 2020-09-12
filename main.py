import re
from os import listdir
from os.path import isfile, join
import function_convert

file_path = r"C:\Workspace\SQL_To_BigQ\Objects_Complexity\Complex_SQL\d_all_agent_metrics.sql"
out_path = r"C:\\Workspace\\SQL_To_BigQ\\Objects_Complexity\\Output_Moderate\\"
#onlyfiles = [file_path+f for f in listdir(file_path) if isfile(join(file_path, f))]
sql_file = open(file_path)
file_name = file_path.split(r"\\")[-1].split('.')[0]
sql_as_string = sql_file.read()

ptrn = "\s*([a-zA-Z_]\w*[(](\s*[a-zA-Z_]\w*|[^()]+[)]|[)])[)])"
functions_in_file = re.findall(ptrn, sql_as_string)
for matches in functions_in_file:
    print(matches)
    print( function_convert.map_function(matches[0]))

