from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import sys


sys.path.append("/opt/airflow/scripts")
from bronze_ingestion import transferir_landing_bronze
from silver_ingestion import transformar_products_silver, transformar_order_items_silver, transformar_orders_silver, transformar_customers_silver, transformar_geolocation_silver, transformar_order_payments_silver, transformar_order_reviews_silver, transformar_sellers_silver
from gold_ingestion import  criar_dim_products, criar_dim_customers, criar_fato_sales, criar_dim_date

with DAG("pipeline_medallion_architecture", start_date = datetime(2026, 2, 8), 
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

    task_silver_geolocation = PythonOperator(
        task_id = 'tratamento_geolocation',
        python_callable = transformar_geolocation_silver
    )

    task_silver_order_payments = PythonOperator(
        task_id = 'tratamento_order_payments',
        python_callable = transformar_order_payments_silver
    )

    task_silver_order_reviews = PythonOperator(
        task_id = 'tratamento_order_reviews',
        python_callable = transformar_order_reviews_silver
    )

    task_silver_sellers = PythonOperator(
        task_id = 'tratamento_sellers',
        python_callable = transformar_sellers_silver
    )

    task_gold_products = PythonOperator(
        task_id = 'criação_dim_products',
        python_callable = criar_dim_products
    )

    task_gold_customers = PythonOperator(
        task_id = 'criação_dim_customer',
        python_callable = criar_dim_customers
    )

    task_gold_date = PythonOperator(
        task_id = 'criação_dim_date',
        python_callable = criar_dim_date
    )

    task_gold_fato = PythonOperator(
        task_id = 'criação_fato_sales',
        python_callable = criar_fato_sales
    )
    
#Definir ordem de execução
task_ingestao_bronze >> [task_silver_products, task_silver_order_items, task_silver_orders, task_silver_customer, task_silver_geolocation, task_silver_order_payments, task_silver_order_reviews, task_silver_sellers]

#Dependência Dims
task_silver_products >> task_gold_products
task_silver_customer >> task_gold_customers
task_silver_orders >> task_gold_date

#Depedência Fato
[task_silver_orders, task_silver_order_items,] >> task_gold_fato