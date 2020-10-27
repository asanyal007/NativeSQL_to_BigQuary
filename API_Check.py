from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import ClientError
import subprocess
import os
import sqlvalidator
import keyword_maps

def API_check(str_sql):
    credentials = service_account.Credentials.from_service_account_file('enhanced-idiom-287811-7deab48e37f8.json')
    project_id = 'enhanced-idiom-287811'

    client = bigquery.Client(credentials= credentials,project=project_id)
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    try:
        query_job = client.query(str_sql, job_config=job_config, retry=None)
        results = query_job.result()  # Wait for the job to complete.
        return results
    except ClientError as err:
        error_dic = err.__dict__['_errors']
        return error_dic,err


def get_stats(sql_str):
    credentials = service_account.Credentials.from_service_account_file('enhanced-idiom-287811-7deab48e37f8.json')
    project_id = 'enhanced-idiom-287811'
    # Construct a BigQuery client object.
    client = bigquery.Client(credentials = credentials, project=project_id)

    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    # Start the query, passing in the extra configuration.
    try:
        query_job = client.query(("{}".format(sql_str)),job_config=job_config,)  # Make an API request.
        return query_job
    except:
        return False
    # A dry run query completes immediately.


def get_schema():
    sql_str = '''SELECT concat(table_schema,".",table_name) as tablename,concat("`",table_catalog,".",table_schema,".",table_name,"`") as schema   
    FROM {}.INFORMATION_SCHEMA.TABLES'''
    credentials = service_account.Credentials.from_service_account_file('enhanced-idiom-287811-7deab48e37f8.json')
    project_id = 'enhanced-idiom-287811'
    # Construct a BigQuery client object.
    client = bigquery.Client(credentials=credentials, project=project_id)
    datasets = list(client.list_datasets())
    job_config = bigquery.QueryJobConfig(dry_run=False, use_query_cache=False)

    # Start the query, passing in the extra configuration.

    dict_result = {}
    try:
        for dataset in datasets:
            sql_str_new = sql_str.format(dataset.dataset_id)
            query_job = client.query(("{}".format(sql_str_new)), job_config=job_config, )  # Make an API request.
            for a in query_job.result():
                dict_result[a[0]] = a[1]
        return dict_result
    except:
        return False


def final_check(function):
    sql_str = '''SELECT {}'''.format(functionv)
    credentials = service_account.Credentials.from_service_account_file('enhanced-idiom-287811-7deab48e37f8.json')
    project_id = 'enhanced-idiom-287811'
    # Construct a BigQuery client object.
    client = bigquery.Client(credentials=credentials, project=project_id)
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    # Start the query, passing in the extra configuration.

    dict_result = {}
    try:
        query_job = client.query(("{}".format(sql_str)), job_config=job_config, )  # Make an API request.
        for a in query_job.result():
            # print(a[0].lower(), a[1])
            dict_result[a[0].lower()] = a[1]
        return dict_result
    except:
        return False





