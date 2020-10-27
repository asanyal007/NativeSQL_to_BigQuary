keywords_map = {'dateadd(1_, 2_, 3_)' : 'DATE_ADD(3_,INTERVAL 2_ 1_)',
                'current_timestamp' : 'CURRENT_TIMESTAMP()',
                "'month'" : 'MONTH',
                'convert_timezone' : 'DATE(2_,1_)',
                'to_date(1_)' : 'to_date(1_)',
                "'hour'" : 'HOUR',
                "'year'" : 'YEAR',
                'contains(1_,2_)' : 'REGEXP_CONTAINS(1_,2_)',
                'replace(1_,2_)' : 'REPLACE(1_,2_,"''")',
                'date_trunc(1_,2_)' :'TIMESTAMP_TRUNC(2_, 1_)',
                'timestamp_ltz' : 'TIMESTAMP',
                'timestamp_ntz' : 'TIMESTAMP',
                ' ' : 'TIMESTAMP',
                'varchar()' : 'String',
                'VARCHAR()' : 'String',
                'TIMESTAMP_TZ' : 'TIMESTAMP', # Not sure
                'TIMESTAMP_NTZ' : 'TIMESTAMP', # Not sure
                'nvl(1_,2_)' : 'ifnull(1_,2_)',
                'TO_NUMBER(1_,2_,3_)' : 'CAST(1_ AS NUMERIC)',
                'dow' : 'DAYOFWEEK',
                'NUMBER()' : 'NUMERIC',
                'extract(1_,2_)' :'EXTRACT(1_,2_)'

                # below list of func dont need conver:

                }
direct_conversion = {
                        'integer':'INT64',
                        'double' : 'FLOAT64',
                        'USE ' : '--USE ',
                        'GRANT ': '--GRANT ',
                        'union all' : 'UNION',
                        'UNION' : 'UNION ALL',
                        'contains(' : 'REGEXP_CONTAINS(',
                        'CONTAINS(' : 'REGEXP_CONTAINS(',
                        'cs_supp.' : ' ',
                        "'TRUE'" : 'TRUE'
}

datatype = {'VARCHAR' : 'String',
            'NUMBER' : 'NUMERIC',
            'TIMESTAMP_TZ' : 'TIMESTAMP',
            'TIMESTAMP_NTZ' : 'TIMESTAMP'




}

regex_map = {
    'AS "[aA-zZ_].*' : ['"',''],
    "[aA-zZ]\'\'" : ["''", r"\'"]
}