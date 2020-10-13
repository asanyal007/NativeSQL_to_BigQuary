keywords_map = {'dateadd(1_, 2_, 3_)' : 'DATE_ADD(3_,INTERVAL 2_ 1_)',
                'current_timestamp' : 'CURRENT_TIMESTAMP()',
                "'month'" : 'MONTH',
                'convert_timezone' : 'DATE(2_,1_)',
                'to_date' : 'to_date(1)',
                "'hour'" : 'HOUR',
                "'year'" : 'YEAR',
                'contains(1_,2_)' : 'REGEXP_CONTAINS(1_,2_)',
                'date_trunc(1_,2_)' :'TIMESTAMP_TRUNC(2_, 1_)',
                'timestamp_ltz' : 'TIMESTAMP',
                'timestamp_ntz' : 'TIMESTAMP',
                'varchar()' : 'String',

                # below list of func dont need conver:

                }
direct_conversion = {
                        'integer':'INT64',
                        'double' : 'FLOAT64',
                        'USE ' : '--USE ',
                        'GRANT ': '--GRANT ',
                        'UNION' : 'UNION ALL',
                        '"' : ' '



}