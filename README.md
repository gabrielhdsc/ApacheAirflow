# Data Lakehouse Pipeline with Apache Airflow (Medallion Architecture)

## 📌 Descrição do Projeto

Este projeto implementa um pipeline de engenharia de dados utilizando Apache Airflow para orquestração e a arquitetura Medallion (Bronze → Silver → Gold) para organização e refinamento de dados.

O pipeline realiza a ingestão de múltiplos datasets de um domínio de e-commerce, persistindo os dados brutos, aplicando padronizações e validações, e disponibilizando ao final um modelo analítico dimensional (Star Schema) pronto para consultas analíticas.

O resultado final é uma camada Gold estruturada em Fato e Dimensões, pronta para análises de vendas, produtos, clientes e desempenho logístico. Os dados de geolocalização, pagamentos, avaliações e vendedores também são tratados na Silver e podem alimentar expansões futuras da camada analítica.

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

* `Data_Ingestao` - timestamp de quando o arquivo foi ingerido
* `Fonte` - nome do arquivo original

### Silver Layer

Camada de tratamento e padronização dos dados:

* tipagem correta de colunas
* remoção de inconsistências
* deduplicação quando aplicável à chave de negócio de cada dataset
* preparação para modelagem

Representa a versão **confiável e limpa** dos dados operacionais.

### Gold Layer

Camada analítica com **modelagem dimensional (Star Schema)**:

* Tabelas dimensão (Dim)
* Tabela fato (Fato)

Projetada para consultas analíticas e métricas de negócio.

---

## 🧰 Tecnologias Utilizadas

* **Python 3.12.7** - Linguagem de programação
* **Apache Airflow 3.1.6** - Orquestração de workflows
* **Pandas** - Manipulação e transformação de dados
* **PostgreSQL 16** - Banco de dados relacional
* **Redis** - Broker de mensagens para Celery
* **SQLAlchemy** - ORM para conexão com banco de dados
* **Docker & Docker Compose** - Containerização e orquestração de infraestrutura
* **NumPy** - Cálculo de métricas e classificação do status de entrega
* **PyArrow / Parquet** - Formato e suporte para armazenamento colunar de dados

---

## 📊 Fonte dos Dados

Foi utilizado um dataset público de e-commerce contendo informações de pedidos, clientes, produtos e entregas.

O domínio foi escolhido por sua clara estruturação e por permitir análises de vendas e logísticas reais.

---

## 🧱 Modelagem de Dados

A camada final é otimizada para consultas análisticas, seguindo um modelo **Star Schema**.

### Tabela Fato

`fato_sales`

Contém colunas de relacionamento com pedidos, produtos, clientes e data, além de métricas quantitativas. As relações são lógicas: o pipeline não cria restrições de chave estrangeira no PostgreSQL.

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

O pipeline é orquestrado por uma **DAG do Apache Airflow** utilizando **CeleryExecutor** (com Redis e PostgreSQL) para processamento distribuído:

### Fluxo de Execução

1. **Ingestão (Bronze Layer)**
   - `ingestao_bronze`: Lê todos os CSVs da Landing e cria partições por data em Parquet

2. **Transformação (Silver Layer)** - 8 tarefas liberadas após a Bronze
   - `tratamento_products`, `tratamento_orders`, `tratamento_customers`
   - `tratamento_order_items`, `tratamento_geolocation`, `tratamento_order_payments`
   - `tratamento_order_reviews`, `tratamento_sellers`
   - Cada tarefa seleciona colunas, padroniza tipos e aplica as regras específicas do dataset. `order_items` preserva múltiplos itens por pedido e `geolocation` não é deduplicada.

3. **Modelagem Dimensional (Gold Layer)**
   - `criação_dim_products`, `criação_dim_customers`, `criação_dim_date`
   - `criação_fato_sales`: depende de `orders` e `order_items`; realiza joins e calcula métricas (`lead_time`, `atraso_entrega`, `status_entrega`)
   - **Persistência dupla**: Parquet (`/data/gold/`) + PostgreSQL (tabelas prontas para BI)

A execução respeita dependências entre datasets para garantir consistência entre as camadas.

---

## ▶️ Como Executar

Pré-Requisitos
* Docker Desktop com Docker Compose
* Pelo menos 4 GB de memória disponíveis para o Docker
* Os arquivos CSV do dataset de e-commerce, mantidos apenas localmente

1. Clonar o repositório

```
git clone https://github.com/gabrielhdsc/ApacheAirflow
```

2. Preparar os dados locais

Crie as pastas abaixo e coloque os CSVs de origem em `data/landingzone/`. Os dados são ignorados pelo Git intencionalmente e não são enviados ao repositório.

```powershell
New-Item -ItemType Directory -Force data/landingzone, data/silver, data/gold
```

Os nomes dos arquivos devem seguir o padrão esperado pela ingestão, como `olist_orders_dataset.csv`, `olist_products_dataset.csv` e `olist_customers_dataset.csv`. A tarefa Bronze cria automaticamente as partições em `data/bronze/<tabela>/<data-de-ingestao>/`.

3. Dependências Python locais (opcional)
```
pip install -r requirements.txt
```

Este comando prepara apenas o ambiente Python local; ele não instala dependências dentro dos contêineres. Para executar a DAG com Docker, a imagem do Airflow precisa conter Pandas, NumPy, PyArrow, SQLAlchemy e `psycopg2`. O Compose atual permite informar dependências adicionais pela variável `_PIP_ADDITIONAL_REQUIREMENTS`, mas para uso recorrente é preferível criar uma imagem customizada.

4. Subir o ambiente

```
docker-compose up -d
```

5. Acessar o Airflow

```
http://localhost:8080

Usuário: airflow
Senha: airflow
```

6. Ativar e executar a DAG:

```
pipeline_medallion_architecture
```

---

## 📁 Estrutura do Repositório

```
projeto-ApacheAirflow/
├── dags/
│   └── dag_ingestao_dataset.py          # Orquestração do fluxo completo (Airflow DAG)
├── scripts/
│   ├── __init__.py                      # Módulo Python
│   ├── bronze_ingestion.py              # Carga bruta: Landing → Bronze (metadados, particionamento)
│   ├── silver_ingestion.py              # Transformação: Bronze → Silver (limpeza, tipagem, dedup)
│   └── gold_ingestion.py                # Modelagem: Silver → Gold (Star Schema, métricas, joins)
├── config/
│   └── airflow.cfg                      # Configuração do Airflow
├── data/                          
│   ├── landingzone/                     # Arquivos .csv originais (não versionado)
│   ├── bronze/                          # Dados particionados por data de ingestão (não versionado)
│   │   ├── orders/
│   │   │   └── 2026-02-13/
│   │   │       └── orders_dataset.parquet
│   │   ├── products/
│   │   ├── customers/
│   │   └── ...
│   ├── silver/                          # Tabelas limpas, padronizadas (não versionado)
│   │   ├── orders_dataset.parquet
│   │   ├── products_dataset.parquet
│   │   └── ...
│   ├── gold/                            # Tabelas Fato + Dimensões (não versionado)
│   │   ├── fato_sales.parquet
│   │   ├── dim_customers.parquet
│   │   ├── dim_products.parquet
│   │   └── dim_date.parquet
│   └── .gitkeep                         # Placeholder para manter pasta no git
├── logs/                                # Logs de execução do Airflow (não versionado)
├── docker-compose.yaml                  # Configuração da infraestrutura
├── requirements.txt                     # Dependências Python
├── .gitignore                           # Arquivos a ignorar no git
└── README.md
```
                    
---

## ⚙️ Decisões Técnicas

**Pandas em vez de Spark**
Volume de dados compatível com processamento local e objetivo educacional focado em arquitetura e modelagem.

**Particionamento por data de ingestão**
Permite rastrear cargas, reprocessar dados e manter histórico. Uma nova execução para a mesma tabela e data substitui o arquivo Parquet daquela partição.

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
