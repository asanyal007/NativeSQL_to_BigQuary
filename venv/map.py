
dict_map = {'x1::y1' : ['CAST(x1 AS y1)', '[^ (\n]*::.[a-zA-Z]+\w+', '[^::]+'],
            'to_date(x1,y1)': ['CAST(x1 AS DATE)','to_date\(.+\)[^\w]','\((.*?)\)'],
            'datediff(x1,y1,z1)' : ['DATE_DIFF(y1,z1,x1)','datediff\(.+\)[^\w]','\((.*?)\)'],
            'convert_timezone(x1,y1)' : ['convert(x1,y1)','convert_timezone[a-zA-Z(/\'_,.]+\)','\((.*?)\)'],
            'CS_SUPP' : ["""`enhanced-idiom-287811`""",'CS_SUPP','CS_SUPP'],
            "contains(x1,y1,z1)" : ["REGEXP_CONTAINS(x1,y1,z1)","contains\([a-zA-Z.(_,'@)+]+","\((.*)\)"],
            'UNION' : ['UNION ALL','UNION','UNION'],
            '"' : ['`','"','"'],
            }

