import pandas as pd
import os
from sqlalchemy import create_engine

path_silver = "/opt/airflow/data/silver"
path_gold = "/opt/airflow/data/gold"

data_base = "postgresql://airflow:airflow@postgres:5432/airflow"

def criar_dim_products():
    engine = create_engine(data_base)
    df_products = pd.read_parquet(f"{path_silver}/products_dataset.parquet")
    dim_products = df_products[["product_id", "product_category_name"]].drop_duplicates()
    dim_products.to_parquet(f"{path_gold}/dim_products.parquet", index=False)
    dim_products.to_sql("dim_products", engine, if_exists="replace", index=False)


def criar_dim_customers():
    engine = create_engine(data_base)
    df_customers = pd.read_parquet(f"{path_silver}/customers_dataset.parquet")
    dim_customers = df_customers[["customer_id", "customer_unique_id"]].drop_duplicates()
    dim_customers.to_parquet(f"{path_gold}/dim_customers.parquet", index=False)
    dim_customers.to_sql("dim_customers", engine, if_exists="replace", index=False)


def criar_fato_sales():
    engine = create_engine(data_base)
    df_orders = pd.read_parquet(f"{path_silver}/orders_dataset.parquet")
    df_order_item = pd.read_parquet(f"{path_silver}/order_items_dataset.parquet")

    #Join das tabelas
    fato_sales = pd.merge(df_order_item, df_orders, on="order_id", how="inner")
    
    fato_sales = fato_sales.dropna(subset=["order_delivered_customer_date"])

    fato_sales["lead_time"] = (fato_sales["order_delivered_customer_date"] - fato_sales["order_purchase_timestamp"]).dt.days
    fato_sales["atraso_entrega"] = (fato_sales["order_delivered_customer_date"] - fato_sales["order_estimated_delivery_date"]).dt.days


    cols_fato = [
        "order_id", "product_id", "customer_id", "price", "lead_time", "atraso_entrega"
    ]

    fato_sales = fato_sales[cols_fato].copy()

    fato_sales.to_parquet(f"{path_gold}/fato_sales.parquet", index=False)
    fato_sales.to_sql("fato_sales", engine, if_exists="replace", index=False)


if __name__ == "__main__":
    criar_dim_products()
    criar_dim_customers()
    criar_fato_sales()
