import re

dict_map = {'to_date(x,y)': 'CAST(x,y AS DATE)'}

sql_file = open("C:\Workspace\SQL_To_BigQ\Objects_Complexity\Moderate_SQL\d_all_refunds.sql")
sql_as_string = sql_file.read()

map_func = list(dict_map.keys())[0].split('(')[0]
map_args = list(dict_map.keys())[0].split('(')[1][:-1].split(',')
BigQ_func = list(dict_map.values())[0]
l = []
for f in map_args:
    if f in BigQ_func:
        l.append(f)
matches = re.findall(map_func +".+.\)", sql_as_string)

arg_dict = {}
for m in matches:
    file_args = m.split('(')[1][:-1].split(',')
    BigQ_func1 = BigQ_func
    for a in map_args:
        if a in l:

            BigQ_func1 = BigQ_func1.replace(a,file_args[map_args.index(a)])
    arg_dict[m] =BigQ_func1

# replace functions
for k,v in arg_dict.items():
    print(k)
    sql_as_string = sql_as_string.replace(str(k),str(v))


print(sql_as_string)



