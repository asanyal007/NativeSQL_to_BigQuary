import re
import map
dict_map = map.dict_map
file_path = r"C:\\Workspace\\SQL_To_BigQ\\Objects_Complexity\\Complex_SQL\\all_agent_metrics_sf.sql"
sql_file = open(file_path)
file_name = file_path.split(r"\\")[-1].split('.')[0]
sql_as_string = sql_file.read()

for SQL_func,BigQ_func in dict_map.items():
    map_func = SQL_func.split('(')[0]

    map_args = re.findall(BigQ_func[2],str(SQL_func))
    if len(map_args) <2:
        map_args = map_args[0].split(',')

    l = []
    for f in map_args:
        if f in BigQ_func[0]:
            l.append(f)
    matches = re.findall(BigQ_func[1], sql_as_string)
    arg_dict = {}
    for m in matches:
        file_args = re.findall(BigQ_func[2],m)
        if file_args and len(file_args) < 2 :
            print("File Args: "+map_func, file_args)
            file_args = file_args[0].split(',')

        #print(map_args)
        BigQ_func1 = BigQ_func[0]
        for a in map_args:
            if file_args and a in l:
                BigQ_func1 = BigQ_func1.replace(a,file_args[map_args.index(a)])
                #print(a, file_args[map_args.index(a)])
                #print(BigQ_func1)
        arg_dict[m] = BigQ_func1
    #print(arg_dict)
    # replace functions
    for k,v in arg_dict.items():
        sql_as_string = sql_as_string.replace(str(k),str(v))

print(sql_as_string)
f = open(file_name+"_BigQ.sql", "w+")
f.write(sql_as_string)
f.truncate()
f.close()



