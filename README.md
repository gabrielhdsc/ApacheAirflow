# Data Lakehouse Pipeline with Apache Airflow (Medallion Architecture)

## 📌 Descrição do Projeto

Este projeto implementa um pipeline de engenharia de dados utilizando Apache Airflow para orquestração e a arquitetura Medallion (Bronze → Silver → Gold) para organização e refinamento de dados.

O pipeline realiza a ingestão de múltiplos datasets de um domínio de e-commerce, persistindo os dados brutos, aplicando padronizações e validações, e disponibilizando ao final um modelo analítico dimensional (Star Schema) pronto para consultas analíticas.

O resultado final é uma camada Gold estruturada em Fato e Dimensões, permitindo análises de custos, distribuição geográfica, desempenho logístico e de satisfação, performance de vendas, clientes e vendedores.

---

## 🎯 Objetivo

O objetivo do projeto é simular um ambiente real de engenharia de dados, demonstrando a construção de um pipeline ponta-a-ponta que contempla:

* Ingestão de dados
* Estruturação de data lakehouse
* ETL
* Persistência em múltiplas camadas
* Tratamento e padronização de dados
* Modelagem dimensional
* Orquestração automatizada
* Disponibilização para consumo analítico

A solução foi desenvolvida com foco em boas práticas de Data Engineering, organização de código e rastreabilidade de processamento.

---

## 🏗 Arquitetura

O pipeline segue o padrão **Medallion Architecture**, separando responsabilidades por camadas:

### Landing Zone

Local responsável por armazenar os arquivos originais (CSV) exatamente como recebidos da fonte, sem qualquer modificação.

### Bronze Layer

Camada de persistência histórica (append-only).
Os arquivos são ingeridos e armazenados em formato Parquet particionado por data de ingestão, mantendo:

* rastreabilidade
* reprocessamento
* auditoria

Metadados adicionados:

* `data_ingestao`
* `fonte_original`

### Silver Layer

Camada de tratamento e padronização dos dados:

* tipagem correta de colunas
* remoção de inconsistências
* Deduplicação de dados
* preparação para modelagem

Representa a versão **confiável e limpa** dos dados operacionais.

### Gold Layer

Camada analítica com **modelagem dimensional (Star Schema)**:

* Tabelas dimensão (Dim)
* Tabela fato (Fato)

Projetada para consultas analíticas e métricas de negócio.

---

## 🧰 Tecnologias Utilizadas

* Python (Pandas)
* Apache Airflow
* Pandas
* PostgreSQL
* Docker
* Git & GitHub

---

## 📊 Fonte dos Dados

Foi utilizado um dataset público de e-commerce contendo informações de pedidos, clientes, produtos e entregas.

O domínio foi escolhido por sua clara estruturação e por permitir análises de vendas e logísticas reais.

---

## 🧱 Modelagem de Dados

A camada final é otimizada para consultas análisticas, seguindo um modelo **Star Schema**.

### Tabela Fato

`fato_sales`

Chave estrangeiras e métricas quantitativas.

Métricas:

* preço
* valor do frete
* lead time de entrega
* atraso de entrega

### Dimensões

Disponibilizam atributos descritivo e idenficação únicas de clientes e produtos

* `dim_customers`
* `dim_products`
* `dim_date`

A dimensão de data permite análises temporais como:

* sazonalidade
* tendências mensais
* desempenho por dia da semana

---

## ⏱ Orquestração

O pipeline é orquestrado por uma DAG do **Apache Airflow**, responsável por:

1. Ingestão da Landing → Bronze
2. Transformações Bronze → Silver
3. Construção das Dimensões
4. Construção da Tabela Fato

A execução respeita dependências entre datasets para garantir consistência entre as camadas.

---

## ▶️ Como Executar

Pré-Requisitos
* Docker
* Docker compose 

1. Clonar o repositório

```
git clone <https://github.com/gabrielhdsc/ApacheAirflow>
```

2. Instalar bibliotecas
```
pip install -r requirements.txt
```

3. Subir o ambiente

```
docker-compose up -d
```

4. Acessar o Airflow

```
http://localhost:8080

Usuário: Airflow
Senha: Airfolw
```

5. Executar a DAG:

```
pipeline_medallion_architecture
```

---

## 📁 Estrutura do Repositório

```
projeto-ApacheAirflow/
├── dags/
│   └── dag_ingestão_dataset.py      # Orquestração do fluxo completo no Airflow
├── scripts/
│   ├── landing_to_bronze.py       # Carga bruta, metadados e particionamento
│   ├── bronze_to_silver.py        # Limpeza, tipagem, deduplicação e Full Load
│   └── silver_to_gold.py          # Modelagem Star Schema, Joins e métricas de negócio
├── data/                          
│   ├── landingzone/               # Arquivos .csv originais
│   ├── bronze/                    # Dados particionados por data de ingestão
│   │   └── orders/
│   │       └── 2026-02-09/
│   │           └── orders.parquet
│   ├── silver/                    # Tabelas limpas, padronizadas e consolidadas
│   └── gold/                      # Tabelas Fato e Dimensões prontas para consumo
├── docker-compose.yaml            # Configuração da infraestrutura (Airflow, Postgres)
├── requirements.txt               
├── .gitignore                     
└── README.md  

```
                    
---

## ⚙️ Decisões Técnicas

**Pandas em vez de Spark**
Volume de dados compatível com processamento local e objetivo educacional focado em arquitetura e modelagem.

**Particionamento por data de ingestão**
Permite rastrear cargas, reprocessar dados e manter histórico.

**Full Load Silver/Gold**
Simplifica consistência do modelo dimensional durante a fase inicial do projeto.


---

## 🔮 Melhorias Futuras

* Implementação de carga incremental (CDC)
* Substituir o Full Load pela ingestão incremental usando Upsert e SCD Type 2
* Integração com ferramenta de BI e visualização de dados

---

## 📌 Conclusão

O projeto demonstra a construção de um pipeline de dados seguindo conceitos modernos de Data Lakehouse, boas práticas de engenharia de dados e modelagem dimensional, buscando simular um fluxo de processamento semelhante ao encontrado em ambientes corporativos.
