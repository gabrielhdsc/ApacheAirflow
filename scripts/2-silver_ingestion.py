import pandas as pd
import os
from datetime import datetime

def transferir_bronze_silver():
    path_bronze = "data/bronze/olist_orders_dataset.parquet"
    path_silver = "/opt/airflow/data/silver"


    df = pd.read_parquet(path_bronze)

    cols = ["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_delivered_carrier_date", 
        "order_delivered_customer_date", "order_estimated_delivery_date"]
    
    df = df[cols]

    colunas_data = df.filter(like="date").columns or df.filter(like = "timestamp").columns
    df[colunas_data] = df[colunas_data].apply(pd.to_datetime, errors = "coerce")


    nome_tabela = "orders_dataset.parquet"
    caminho_final = os.path.join(path_silver, f"{nome_tabela}")

    df.to_parquet(caminho_final, index = False)


    print(f"Tabela {nome_tabela} Salva")


if __name__ == "__main__":
    transferir_bronze_silver()