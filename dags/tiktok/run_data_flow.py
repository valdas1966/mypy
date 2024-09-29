from datetime import datetime, timedelta
from airflow import models
from airflow.contrib.operators.dataflow_operator import DataflowPythonOperator
from airflow.utils.dates import days_ago

project_id = 'noteret'
gcs_temp_location = 'gs://dflow_bucket/temp'
gcs_staging_location = 'gs://dflow_bucket/staging'

# Define the DAG
dag = models.DAG(
    dag_id='run_data_flow',
    start_date=days_ago(1),
    schedule_interval='*/15 * * * *',  # A cron expression to run the DAG every 15 minutes
    catchup=False,
)

# Using DataflowPythonOperator for list Python-based Dataflow job
dataflow_python_job = DataflowPythonOperator(
    task_id='dataflow_python_job',
    py_file='gs://your_bucket/paths/to/your_dataflow_script.py',
    py_options=['-m'],
    dataflow_default_options={
        'project': project_id,
        'temp_location': gcs_temp_location,
        'staging_location': gcs_staging_location,
    },
    dag=dag,
)
