import re
import pprint
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import ClientError
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Function, Parenthesis, Comparison, Where
from sqlparse.tokens import Keyword, DML
pp = pprint.PrettyPrinter(indent=4)

def run_script(sql_str):
    credentials = service_account.Credentials.from_service_account_file('enhanced-idiom-287811-7deab48e37f8.json')
    project_id = 'enhanced-idiom-287811'
    client = bigquery.Client(credentials = credentials, project=project_id)
    job_config = bigquery.QueryJobConfig(dry_run=False, use_query_cache=False, autodetect=True)
    query_job = client.query(("{}".format(sql_str)),job_config=job_config)  # Make an API request.
    return query_job

def extract_table_identifiers(token_stream,list_of_columns, name):
    for item in token_stream:
        #print("recurse", isinstance(item, Identifier ) and 'SELECT' in item.value.upper(), item)
        if isinstance(item, Identifier) or isinstance(item, Parenthesis) and 'SELECT' in item.value.upper() :
            print("recurse")
            #_extract_table_identifiers(item.tokens)
            return list_of_columns
        elif isinstance(item, Where):
             extract_table_identifiers(item.tokens)
        elif isinstance(item, IdentifierList):
            for ident in item.get_identifiers():
                try:
                    alias = ident.get_alias()
                    real_name = str(ident).split(' as ')[0]
                    #print("real name: {} alias: {}".format(real_name,alias))
                    list_of_columns.append([real_name,alias])
                except AttributeError:
                    continue
def process_union(sql_as_string):
    parsed = sqlparse.parse(sql_as_string)[0]

    for tok in parsed.tokens:
        if isinstance(tok,Identifier ) and 'select' in tok.value.lower():
            sub_select_with_union = tok

    b = ""
    closing_br = 0
    open_br = 0
    for a in sub_select_with_union.tokens:
        open_br = open_br + a.value.count("(")
        closing_br = closing_br + a.value.count(")")

        b = b + a.value

        if open_br == closing_br and (open_br > 0 and closing_br > 0):
            #print(b)
            break

    new_union_str = b[1:len(b)-1]

    list_of_unions = new_union_str.split("UNION ALL")

    # create temp table
    sql = '''CREATE or REPLACE VIEW `enhanced-idiom-287811.temp.new`
    OPTIONS(
        expiration_timestamp=TIMESTAMP_ADD(
            CURRENT_TIMESTAMP(), INTERVAL 48 HOUR),
        friendly_name="new_view",
        description="a view that expires in 2 days",
        labels=[("org_unit", "development")]
    )
    AS {} LIMIT 1'''

    get_view_sql = '''SELECT column_name,data_type FROM temp.INFORMATION_SCHEMA.COLUMNS
                        where table_name = 'new' ;'''
    i = 0

    dict_rows = []
    for un in list_of_unions:
        list_of_columns = []

        if i == 0:
            pass
        else:
            pp.pprint("---------------------- {} ----------------------------".format(i))
            job = run_script(sql.format(un))
            job.result()
            jb = run_script(get_view_sql)

            cols = extract_table_identifiers(sqlparse.parse(un)[0].tokens, list_of_columns, i)
            g = 0
            f = 0
            for a in jb.result():
                cols[g].append(list(a)[1])
                print(cols[g], g)

                g = g + 1
            dict_rows.append(cols)
        i = i + 1

    df_columns = pd.DataFrame(dict_rows)
    null_list = []
    not_null_list = []
    list_of_unions = sub_select_with_union.value.split("UNION ALL")
    for i in range(df_columns.shape[1]):
        #print(i)
        null_list = []
        not_null_list = []
        for s in df_columns[i]:
            if re.search(r'\bnull\b', s[0]) and 'INT64' in s[2]:
                null_list.append(s)
            elif not re.search(r'\bnull\b', s[0]) and 'INT64' not in s[2]:
                not_null_list.append(s[2])
        if null_list and not_null_list:
            for n in null_list:
                g = 0
                for a in list_of_unions:
                    source = "{}\s+as\s+{}".format(n[0], n[1])
                    target = "CAST({} AS {}) as {}".format(n[0], list(set(not_null_list))[0], n[1])
                    #print(source)
                    list_of_unions[g] = re.sub(source, target, a)
                    #print(list_of_unions[g])
                    g = g + 1
    SQL_STRING = ""
    for tok in parsed.tokens:
        if isinstance(tok, Identifier) and 'select' in tok.value.lower():
            #print(' UNION ALL '.join(list_of_unions))
            SQL_STRING = SQL_STRING + ' UNION ALL '.join(list_of_unions)
        else:
            #print(tok)
            SQL_STRING = SQL_STRING + tok.value

    return SQL_STRING



