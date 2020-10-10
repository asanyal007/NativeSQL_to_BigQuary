keywords_map = {'dateadd' : 'DATE_ADD(x,INTERVAL 2 1)',
                'current_timestamp' : 'CURRENT_TIMESTAMP()',
                "'month'" : 'MONTH',
                'convert_timezone' : 'DATE(2,1)',
                'to_date' : 'to_date(1)',
                "'hour'" : 'HOUR',
                "hour" : 'HOUR',
                'date_part': "EXTRACT(1 FROM 2)",
                'dow ': 'DAYOFWEEK',
                'extract(1 from 2)' : 'EXTRACT(1 FROM 2)',
                'lower' : 'LOWER(1)',
                'sum' : 'SUM(1)',
                'date_trunc' :'TIMESTAMP_TRUNC(2, 1)',
                'timestamp_ltz' : 'TIMESTAMP',
                'timestamp_ntz' : 'TIMESTAMP',
                'abc' : 'ABC',
                'hello(1,2)' : 'hi(2((2(1))))',
                'xyz(1)' : 'XYZ(1)',
                'rrt(1)' : 'RRT(1)',
                'max(1)' : 'MAX(XYZ(1))'
                # below list of func dont need conver:

                }
