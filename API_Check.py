from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import ClientError
import subprocess
import os
import sqlvalidator

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
    query_job = client.query(
        (
            "{}".format(sql_str)
        ),
        job_config=job_config,
    )  # Make an API request.

    # A dry run query completes immediately.
    return query_job

print(get_stats("select * from `enhanced-idiom-287811.prod.INFORMATION_SCHEMA.TABLES`").total_bytes_processed)

