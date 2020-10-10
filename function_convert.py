import keyword_maps
import re
keywords_map = keyword_maps.keywords_map

def map_function(str1):
    converted = {}
    list_param = {}
    for a in range(str1.count('(')):
        func_parameters = {}
        ptrn = "\s*([a-zA-Z_]\w*[(](\s*[a-zA-Z_]\w*[(]|[^()]+)[)])"
        matches = re.findall(ptrn, str1)
        #print(str1, matches)

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
                func_parameters[i] = val
            str1 = str1.replace(matches[0][0], 'x')
            converted[matches[0][0].split('(')[0]] = func_parameters

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
            #else:
                #new_dict[k] = v
    #print(new_dict)
    list_of_part = []
    for k, v in new_dict.items():
        for key, val in v.items():
            k = k.replace(str(key), val)
        list_of_part.append(k)
    #print(list_of_part)
    final = []
    for i, e in list(enumerate(list_of_part)):
        if len(final) < 1:
            final.append(e)
        else:
            final.append(e.replace('x', final[i - 1]))
#    print(final)
    if final:
        return final[-1]
    else:
        return "Not Available"
