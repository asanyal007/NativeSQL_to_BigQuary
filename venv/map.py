
dict_map = {'x1::y1' : ['CAST(x1 AS y1)', '[^ ]*::.[a-zA-Z]+\w+', '[^::]+'],
            'to_date(x1,y1)': ['CAST(x1 AS DATE)','to_date\(.+\)[^\w]','\((.*?)\)'],
            'coalesce(x1,y1)': ['COALESCE(x1,y1)','coalesce\(.+\)[^\w]','\((.*?)\)'],
            'datediff(x1,y1,z1)' : ['DATE_DIFF(y1,z1,x1)','datediff\(.+\)[^\w]','\((.*?)\)'],
            'convert_timezone(x1,y1)' : ['convert(x1,y1)','convert_timezone[a-zA-Z(/\'_,.]+\)','\((.*?)\)'],
            'dateadd(x1,y1,z1)' : ['date_add(x1,y1,z1)','dateadd\(.+\)[^\w]','\((.*?)\)'],
            #,'x::y' : ['CAST(x AS y)', '[a-zA-Z._]+\w+::.[a-zA-Z]+\w+', '[^::,]+'],
            'CS_SUPP' : ["""`enhanced-idiom-287811`""",'CS_SUPP','CS_SUPP'],
            "contains(x1,y1,z1)" : ["REGEXP_CONTAINS(x1,y1,z1)","contains\([a-zA-Z.(_,'@)+]+","\((.*)\)"],
            'UNION' : ['UNION ALL','UNION','UNION'],
            '"' : ['`','"','"'],
            }

