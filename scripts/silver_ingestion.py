import pandas as pd
import os
from datetime import datetime

path_bronze = "/opt/airflow/data/bronze"
path_silver = "/opt/airflow/data/silver"

def ler_bronze(tabela):
    path_base = os.path.join(path_bronze, tabela)  #Pasta onde estão as partições diárias da tabela

    if not os.path.exists(path_base):
        raise FileNotFoundError(f"Tabela {tabela} não encontrada") #Verifica se a tabela digitada existe
    
    dfs = []  #lista de dataframes das versões que serão unificados

    for particao in os.listdir(path_base):
        path_particao = os.path.join(path_base, particao)  #percorre cada partição de dia

        for arquivo in os.listdir(path_particao):
            path_arquivo = os.path.join(path_particao, arquivo)  #percorre cada arquivo dentro de cada partição
            print(f"Lendo: {particao}/{arquivo}") 

            df_temporario = pd.read_parquet(path_arquivo)  #lê o arquivo

            dfs.append(df_temporario)  #Adiciona na lista de data_frames

    if len(dfs) == 0:  #verificação de existência de arquivos
        print(f"Nenhum arquivo encontrado na tabela {tabela}")  

    df_unificado = pd.concat(dfs, ignore_index=True)   #unifica os data_frames salvos em um só

    return df_unificado


def salvar_silver(df, nome_arquivo):
    path_local = os.path.join(path_silver, nome_arquivo)
    df.to_parquet(path_local, index = False)   #Salva o arquivo no caminho da prata e .parquet

    print(f"Arquivo {nome_arquivo} salvo em {path_local}")


def transformar_orders_silver():
    df = ler_bronze("orders")       #le os dfs da tabela orders

    #Define as colunas da tabela na prata (mesmas que ja existiam, nesse caso)
    cols = ["order_id", "customer_id", "order_status", "order_purchase_timestamp", 
            "order_approved_at", "order_delivered_carrier_date", 
        "order_delivered_customer_date", "order_estimated_delivery_date"]       
    
    df = df[cols].copy()

    #Lista as colunas de data para serem transfomadas
    colunas_data = ["order_purchase_timestamp", 
                    "order_approved_at",
                    "order_delivered_carrier_date",
                    "order_delivered_customer_date",
                    "order_estimated_delivery_date"]
    
    #Transforma todas as colunas de data para datetime de uma vez
    df[colunas_data] = df[colunas_data].apply(pd.to_datetime, errors="coerce")

    #Deduplicação, mantém o id mais recente se ele for duplicado na coluna order_id
    df = df.drop_duplicates(subset=["order_id"])

    salvar_silver(df, "orders_dataset.parquet")  #Salva o arquivo na prata


def transformar_products_silver():
    df = ler_bronze("products")       #le os dfs da tabela products

    cols = ["product_id", "product_category_name", "product_name_lenght",
            "product_description_lenght", "product_photos_qty", "product_weight_g",
            "product_lenght_cm", "product_height_cm", "product_width_cm"]
    
    df = df[cols].copy()

    #preenche o campo caso seja nulo
    df["product_category_name"] = df["product_category_name"].fillna(value="não informado")
    
    cols_numbers = ["product_name_lenght", "product_description_lenght", "product_photos_qty",
        "product_weight_g", "product_lenght_cm", "product_height_cm", "product_width_cm"]
    
    #Transforma todas as colunas de numero de uma vez
    df[cols_numbers] = df[cols_numbers].apply(pd.to_numeric, errors = "coerce")

    df = df.drop_duplicates(subset=["product_id"])

    salvar_silver(df,"products_dataset.parquet")


def transformar_order_items_silver():
    df = ler_bronze("order_items")       #le os dfs da tabela order_items

    cols = ["order_id", "order_item_id", "product_id", "seller_id", "shipping_limit_date", "price", "freight_value"]
    df = df[cols].copy()

    #Transformações e prenchumento de colunas de números e datas
    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)
    df["freight_value"] = pd.to_numeric(df["freight_value"], errors="coerce").fillna(0.0)

    #Sem deduplicação. 1 pedido (order_id) tem vários itens atrelados

    salvar_silver(df,"order_items_dataset.parquet")


def transformar_customers_silver():
    df = ler_bronze("customers")       #le os dfs da tabela customers

    cols = ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"]
    df = df[cols].copy()

    df["customer_zip_code_prefix"] = pd.to_numeric(df["customer_zip_code_prefix"], errors="coerce")

    #Deixa apenas um registro (uma linha) para cada cliente
    df = df.drop_duplicates(subset=["customer_unique_id"])

    salvar_silver(df, "customers_dataset.parquet")


def transformar_geolocation_silver():
    df = ler_bronze("geolocation")       #le os dfs da tabela geolocation

    cols = ["geolocation_zipcode_prefix", "geolocation_lat", "geolocation_lng", "geolocation_city", "geolocation_state"]
    df = df[cols].copy()

    cols_num = ["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"]
    df[cols_num] = df[cols_num].apply(pd.to_numeric, errors="coerce")

    salvar_silver(df, "geolocation_dataset.parquet")


def transformar_order_payments_silver():
    df = ler_bronze("order_payments")       #le os dfs da tabela order_payments

    cols = ["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"]
    df = df[cols].copy()

    df["payment_sequential"] = pd.to_numeric(df["payment_sequential"], errors="coerce")
    df["payment_installments"] = pd.to_numeric(df["payment_installments"], errors="coerce")
    df["payment_value"] = pd.to_numeric(df["payment_value"], errors="coerce")

    df = df.drop_duplicates(subset=["order_id"])
    
    salvar_silver(df, "order_payment_dataset.parquet")


def transformar_order_reviews_silver():
    df = ler_bronze("order_reviews")       #le os dfs da tabela order_reviews

    cols = ["review_id", "order_id", "review_score", "review_comment_title",
            "review_comment_message", "review_creation_date", "review_answer_timestamp"]
    
    df = df[cols].copy()

    df["review_score"] = pd.to_numeric(df["review_score"], errors="coerce")
    df["review_creation_date"] = pd.to_datetime(df["review_creation_date"], errors="coerce")
    df["review_answer_timestamp"] = pd.to_datetime(df["review_answer_timestamp"], errors="coerce")

    df = df.drop_duplicates(subset=["review_id"])
    
    salvar_silver(df, "order_reviews_dataset.parquet")


def transformar_sellers_silver():
    df = ler_bronze("sellers")       #le os dfs da tabela sellers

    cols = ["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"]
    df = df[cols].copy()

    df["seller_zip_code_prefix"] = pd.to_numeric(df["seller_zip_code_prefix"], errors="coerce")

    df = df.drop_duplicates(subset=["seller_id"])
    
    salvar_silver(df, "sellers_dataset.parquet")


if __name__ == "__main__":
    try:
        transformar_products_silver()
        transformar_order_items_silver()
        transformar_orders_silver()
        transformar_customers_silver()
        transformar_geolocation_silver()
        transformar_order_payments_silver()
        transformar_order_reviews_silver()
        transformar_sellers_silver()
        print("Tratamento da Silver concluido")

    except Exception as e:
        print(f"Erro em: {e}")
