from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import sys


sys.path.append("/opt/airflow/scripts")
from bronze_ingestion import transferir_landing_bronze
from silver_ingestion import transformar_products_silver, transformar_order_items_silver, transformar_orders_silver, transformar_customers_silver

with DAG("pipeline_lakehouse_layers", start_date = datetime(2026, 2, 4), 
         schedule = '@once', catchup = False) as dag:

    task_ingestao_bronze = PythonOperator(
        task_id = 'ingestao_bronze',
        python_callable = transferir_landing_bronze
    )

    task_silver_products = PythonOperator(
        task_id = 'tratamento_products',
        python_callable = transformar_products_silver
    )

    task_silver_order_items = PythonOperator(
        task_id = 'tratamento_order_items',
        python_callable = transformar_order_items_silver
    )

    task_silver_orders = PythonOperator(
        task_id = 'tratamento_orders',
        python_callable = transformar_orders_silver
    )

    task_silver_customer = PythonOperator(
        task_id = 'tratamento_customer',
        python_callable = transformar_customers_silver
    )

#Definir ordem de execução
task_ingestao_bronze >> [task_silver_products, task_silver_order_items, task_silver_orders, task_silver_customer]