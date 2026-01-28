import pandas as pd
import os
import glob
from datetime import datetime

def transferir_landing_bronze():
    path_landing = "data/landingzone"
    path_bronze = "data/bronze"

    #lista todos os caminhos de arquivos .csv
    path_padrao = os.path.join(path_landing, "*.csv")

    #Lista o caminho completo dos arquivos com caminhos padrao definidos da pasta landing (data/landing/arquivoTal.csv)
    arquivos = glob.glob(path_padrao)

    for caminho_arquivo in arquivos:
        #Le cada arquivo da landing
        df = pd.read_csv(caminho_arquivo)

        #Adiciona colunas de metadados
        df["Data_Ingestao"] = datetime.now()
        df["Fonte"] = caminho_arquivo

        #Pega apenas o nome do arquivo do caminho completo
        nome_arquivo = os.path.basename(caminho_arquivo)

        #Salva na camada bronze
        nome_tabela = nome_arquivo.replace(".csv", "")
        caminho_final = os.path.join(path_bronze, f"{nome_tabela}.parquet")

        #Transforma em .parquet
        df.to_parquet(caminho_final, index = False)

        print(f"Tabela {nome_tabela} Salva")

if __name__ == "__main__":
    transferir_landing_bronze()