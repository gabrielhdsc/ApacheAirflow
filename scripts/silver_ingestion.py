import pandas as pd
import os
from datetime import datetime

path_silver = "/opt/airflow/data/silver"

def salvar_silver(df, nome_arquivo):
    path_local = os.path.join(path_silver, nome_arquivo)
    df.to_parquet(path_local, index = False)

    print(f"Arquivo {nome_arquivo} salvo em {path_local}")

def transformar_orders_silver():
    path_arquivo = "/opt/airflow/data/bronze/olist_orders_dataset.parquet"

    df = pd.read_parquet(path_arquivo)

    cols = ["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_delivered_carrier_date", 
        "order_delivered_customer_date", "order_estimated_delivery_date"]
    
    df = df[cols].copy()

    colunas_data = ["order_purchase_timestamp", 
                    "order_delivered_carrier_date",
                    "order_delivered_customer_date",
                    "order_estimated_delivery_date"]
    
    df[colunas_data] = df[colunas_data].apply(pd.to_datetime, errors="coerce")

    df = df.drop_duplicates(["order_id"])

    salvar_silver(df, "orders_dataset.parquet")


def transformar_products_silver():
    path_arquivo = "/opt/airflow/data/bronze/olist_products_dataset.parquet"

    df = pd.read_parquet(path_arquivo)

    cols = ["product_id", "product_category_name"]
    df = df[cols].copy()

    df["product_category_name"] = df["product_category_name"].fillna(value="não informado")

    df = df.drop_duplicates(["product_id"])

    salvar_silver(df,"products_dataset.parquet")


def transformar_order_items_silver():
    path_arquivo = "/opt/airflow/data/bronze/olist_order_items_dataset.parquet"

    df = pd.read_parquet(path_arquivo)

    cols = ["order_id", "order_item_id", "product_id", "shipping_limit_date", "price"]
    df = df[cols].copy()

    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)


    salvar_silver(df,"order_items_dataset.parquet")


def transformar_customers_silver():
    path_arquivo = "/opt/airflow/data/bronze/olist_customers_dataset.parquet"

    df = pd.read_parquet(path_arquivo)

    cols = ["customer_id", "customer_unique_id"]
    df = df[cols].copy()

    df = df.dropna()
    df = df.drop_duplicates(subset=["customer_id"])

    salvar_silver(df, "customers_dataset.parquet")


if __name__ == "__main__":
    try:
        transformar_products_silver()
        transformar_order_items_silver()
        transformar_orders_silver()
        transformar_customers_silver()
        print("Tratamento da Silver concluido")

    except Exception as e:
        print(f"Erro em: {e}")
