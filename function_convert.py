import keyword_maps
import re
keywords_map = keyword_maps.keywords_map
function_map = keyword_maps.function_map

def map_function(str1):
    converted = {}
    for a in range(str1.count('(')):
        func_parameters = {}
        ptrn = "\s*([a-zA-Z_]\w*[(](\s*[a-zA-Z_]\w*[(]|[^()]+[)]|[)]))"
        matches = re.findall(ptrn, str1)
        l_param = matches[0][1].replace(')', '').split(',')
        i = 0
        for val in l_param:
            i = i + 1
            func_parameters[i] = val
        str1 = str1.replace(matches[0][0], 'x')
        converted[matches[0][0].split('(')[0]] = func_parameters

    # Convert arguments
    for k, v in converted.items():
        for key, args in v.items():
            # print(key,args,keywords_map.keys())
            if args in keywords_map.keys():
                converted[k][key] = keywords_map[args]

    # Convert keys
    new_dict = {}
    for k, v in converted.items():
        if k in keywords_map.keys():
            new_dict[keywords_map[k]] = v
        else:
            new_dict[k] = v

    list_of_part = []
    for k, v in new_dict.items():
        for key, val in v.items():
            k = k.replace(str(key), val)
        list_of_part.append(k)

    final = []
    for i, e in list(enumerate(list_of_part)):
        if len(final) < 1:
            final.append(e)
        else:
            final.append(e.replace('x', final[i - 1]))
    return final[-1]

print(map_function("dateadd('month',-6,convert_timezone('America/Los_Angeles',to_date(current_timestamp)))"))