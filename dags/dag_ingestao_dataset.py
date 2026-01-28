from airflow import dag
from datetime import datetime
from airflow.operators.python import PythonOperator
import sys

sys.path.append("scripts")
from bronze_ingestion import transferir_landing_bronze

with DAG("pipeline_landing_to_bronze", start_date = datetime(), 
         schedule_interval = '@once', catchup = False)as dag:

    task_ingestao_bronze = PythonOperator(
        task_id = 'task_ingestao_bronze',
        python_callable = transferir_landing_bronze
    )