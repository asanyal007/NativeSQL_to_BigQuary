import re
import keyword_maps
import function_convert
def doublecolon_to_standard_cast(sql_as_string):
    keywords_map = keyword_maps.keywords_map
    new_ptr = ['\s*([a-zA-Z_]\w*[(](\s*[a-zA-Z_]\w*[(]|[^()]+[)]|[)])::[a-z_]+)' , '[a-zA-Z_.][^ (\n)]*::.[a-zA-Z]+\w+']
    new_match=[]
    for pat in new_ptr:
        new_match.extend(re.findall(pat, sql_as_string))
    all_list = []
    for n in new_match:
        if len(n)==2:
            all_list.append(n[0])
        else:
            all_list.append(n)
    final = {}
    for each in all_list:
        if '(' in each:
            x = function_convert.map_function(re.findall('[^::]+',each)[0])
        else:
            x = re.findall('[^::]+',each)[0]
        if re.findall('[^::]+',each)[1] in keywords_map.keys():
            y = keywords_map[re.findall('[^::]+',each)[1]]
        else:
            y = re.findall('[^::]+',each)[1]
        final[each] = "CAST({} AS {})".format(x,y)
    return final