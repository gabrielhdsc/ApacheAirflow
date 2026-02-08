import pandas as pd
import os
from datetime import datetime

def transferir_landing_bronze():
    path_landing = "/opt/airflow/data/landingzone"
    path_bronze = "/opt/airflow/data/bronze"

    start_time = datetime.now()
    data_hoje = datetime.now().strftime("%Y-%m-%d")     #Define formato da data: 00-00-00

    #Lista todos os arquivos da landing
    arquivos = os.listdir(path_landing)

    for nome_arquivo in arquivos:

        #junta o caminho da landing + nome de cada um dos arquivos = caminho de origem -> (/opt/airflow/data/landingzone/nome_arquivo.csv)
        caminho_origem = os.path.join(path_landing, nome_arquivo)
        nome_pasta_tabela = nome_arquivo.replace("olist_","").replace("_dataset.csv","")    #Retira o nome padrão da pasta
        nome_tabela = nome_arquivo.replace(".csv","")    #Retira o .csv do nome

        #Cria a pasta para aquele arquivo e uma pasta para aquele dia
        caminho_particao = os.path.join(path_bronze, nome_pasta_tabela, data_hoje)
        os.makedirs(caminho_particao, exist_ok=True)   #

        #Le cada arquivo da landing
        df = pd.read_csv(caminho_origem)

        #Adicionar colunas de metadados
        df["Data_Ingestao"] = start_time
        df["Fonte"] = nome_arquivo

        #Salva na camada bronze
        caminho_arquivo_final = os.path.join(caminho_particao, f"{nome_tabela}.parquet")

        #Transforma em .parquet
        df.to_parquet(caminho_arquivo_final, index = False)

        print(f"Tabela {nome_tabela} Salva")

if __name__ == "__main__":
    transferir_landing_bronze()