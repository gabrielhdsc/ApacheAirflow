import pandas as pd
import os
import numpy as np
from sqlalchemy import create_engine

path_silver = "/opt/airflow/data/silver"
path_gold = "/opt/airflow/data/gold"
data_base = "postgresql://airflow:airflow@postgres:5432/airflow"

engine = create_engine(data_base)

def criar_dim_date():
    df_orders = pd.read_parquet(f"{path_silver}/orders_dataset.parquet")

    #Define a base para a dimensão de data sem nulos e mantem apenas um valor(data) 
    datas = pd.to_datetime(df_orders["order_purchase_timestamp"]).dropna().unique()

    dim_date = pd.DataFrame({"data": datas}) #Cria uma tabela com uma coluna com as datas extraídas da base 

    #Cria as colunas da dim_date com base na coluna de data extraída da base
    dim_date["ano"] = dim_date["data"].dt.year
    dim_date["mes"] = dim_date["data"].dt.month
    dim_date["dia"] = dim_date["data"].dt.day
    dim_date["dia_semana"] = dim_date["data"].dt.day_name()
    dim_date["trimestre"] = dim_date["data"].dt.quarter

    dim_date = dim_date.drop_duplicates()

    dim_date.to_parquet(f"{path_gold}/dim_date.parquet", index=False)
    dim_date.to_sql("dim_date", engine, if_exists="replace", index=False)

def criar_dim_products():
    df_products = pd.read_parquet(f"{path_silver}/products_dataset.parquet")

    dim_products = df_products[["product_id", "product_category_name"]].drop_duplicates()

    dim_products.to_parquet(f"{path_gold}/dim_products.parquet", index=False)
    dim_products.to_sql("dim_products", engine, if_exists="replace", index=False)


def criar_dim_customers():
    df_customers = pd.read_parquet(f"{path_silver}/customers_dataset.parquet")

    dim_customers = df_customers[["customer_id", "customer_unique_id"]].drop_duplicates()

    dim_customers.to_parquet(f"{path_gold}/dim_customers.parquet", index=False)
    dim_customers.to_sql("dim_customers", engine, if_exists="replace", index=False)


def criar_fato_sales():
    df_orders = pd.read_parquet(f"{path_silver}/orders_dataset.parquet")
    df_order_item = pd.read_parquet(f"{path_silver}/order_items_dataset.parquet")

    #Join das tabelas
    fato_sales = pd.merge(df_order_item, df_orders, on="order_id", how="inner")
    

    #Remove pedidos sem data de entrega para não influenciar o lead time
    fato_sales = fato_sales.dropna(subset=["order_delivered_customer_date"])

   #data_pedido -> data que foi feito o pedido (remove as horas para cruzar com dim_date)
    fato_sales["data_pedido"] = fato_sales["order_purchase_timestamp"].dt.date

    #lead time -> dias entre a compra e a entrega
    fato_sales["lead_time"] = (fato_sales["order_delivered_customer_date"] - fato_sales["order_purchase_timestamp"]).dt.days

    #atraso_entrega -> valor positivo = atraso, valor negativo = adiantado/no prazo
    fato_sales["atraso_entrega"] = (fato_sales["order_delivered_customer_date"] - fato_sales["order_estimated_delivery_date"]).dt.days

    #status_entrega -> Define um status para entrega com base no "atraso_entrega"
    fato_sales["status_entrega"] = np.where(fato_sales["atraso_entrega"] > 0, "Atrasado", "No prazo")

    #Colunas finais da fato
    cols_fato = [
        "order_id", "product_id", "customer_id", "data_pedido", "price", "freight_value", "lead_time", "atraso_entrega", "status_entrega"
    ]

    fato_sales = fato_sales[cols_fato].copy()

    fato_sales.to_parquet(f"{path_gold}/fato_sales.parquet", index=False)
    fato_sales.to_sql("fato_sales", engine, if_exists="replace", index=False)


if __name__ == "__main__":
    try:
        criar_dim_date()
        criar_dim_products()
        criar_dim_customers()
        criar_fato_sales()
        print("Criação da gold concluida")

    except Exception as e:
        print(f"Erro em {e}")
