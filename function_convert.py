import keyword_maps
import re
import pandas as pd
keywords_map = keyword_maps.keywords_map

def map_function(str1):
    converted = {}
    list_param = {}
    for a in range(str1.count('(')):
        func_parameters = {}
        ptrn = "\s*([a-zA-Z_]\w*[(](\s*[a-zA-Z_]\w*[(]|[^()]+)[)])"
        matches = re.findall(ptrn, str1)
        #print("backhod match ", str1, matches)

        if matches:
            if 'from' in matches[0][1]:
                list_param[matches[0][0]] = matches[0][1].replace(')','').split('from')
            else:
                list_param[matches[0][0]] = matches[0][1].replace(')', '').split(',')

            #print(list_param)

           #print(list_param)
            i = 0
            for val in list_param[matches[0][0]]:
                i = i + 1
                func_parameters[str(i)+"_"] = val
            str1 = str1.replace(matches[0][0], 'x')
            converted[matches[0][0].split('(')[0]] = func_parameters
            #print("func_par", func_parameters)

    #print(converted)
    # Convert arguments
    for k, v in converted.items():
        for key, args in v.items():
            # print(key,args,keywords_map.keys())
            if args in keywords_map.keys():
                converted[k][key] = keywords_map[args]

    # Convert keys
    new_dict = {}
    for k, v in converted.items():
        for key in keywords_map.keys():
            if k in key.split('(')[0]:
                new_dict[keywords_map[key]] = v

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
    if final:
        return final[-1]
    else:
        return "Not Available"

def map_direct(direct_map):
    df_direct_map = pd.DataFrame(list(direct_map.items()), columns=['SQL_Functions', 'Converted_Functions']).reset_index()
    return df_direct_map
