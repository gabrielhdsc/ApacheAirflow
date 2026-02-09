# Data Lakehouse Pipeline with Apache Airflow (Medallion Architecture)

## 📌 Descrição do Projeto

Este projeto implementa um pipeline completo de engenharia de dados utilizando **Apache Airflow** para orquestração e a arquitetura **Medallion (Landing → Bronze → Silver → Gold)** para organização e processamento dos dados.

O pipeline realiza a ingestão de múltiplos datasets de um domínio de e-commerce, persistindo os dados brutos, aplicando padronizações e validações, e disponibilizando ao final um modelo analítico dimensional (Star Schema) pronto para consultas analíticas.

O resultado final é uma **camada Gold estruturada em Fato e Dimensões**, permitindo análises de desempenho logístico, como **lead time de entrega** e **atraso de pedidos**.

---

## 🎯 Objetivo

O objetivo do projeto é simular um ambiente real de engenharia de dados corporativa, demonstrando a construção de um pipeline ponta-a-ponta que contempla:

* Ingestão de dados
* Persistência em múltiplas camadas
* Tratamento e padronização
* Modelagem dimensional
* Orquestração automatizada
* Disponibilização para consumo analítico

A solução foi desenvolvida com foco em **boas práticas de Data Engineering**, organização de código e rastreabilidade de processamento.

---

## 🏗 Arquitetura

O pipeline segue o padrão **Medallion Architecture**, separando responsabilidades por camadas:

### Landing Zone

Área de aterrissagem responsável por armazenar os arquivos originais (CSV) exatamente como recebidos da fonte, sem qualquer modificação.

### Bronze Layer

Camada de persistência histórica (append-only).
Os arquivos são ingeridos e armazenados em **formato Parquet particionado por data de ingestão**, mantendo:

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
* seleção de campos relevantes
* preparação para modelagem

Representa a versão **confiável e limpa** dos dados operacionais.

### Gold Layer

Camada analítica com **modelagem dimensional (Star Schema)**:

* Tabelas dimensão (Dim)
* Tabela fato (Fato)

Projetada para consultas analíticas e métricas de negócio.

---

## 🧰 Tecnologias Utilizadas

* Python
* Apache Airflow
* Pandas
* PostgreSQL
* Parquet
* SQLAlchemy
* Git & GitHub

---

## 📊 Fonte dos Dados

Foi utilizado um dataset público de e-commerce contendo informações de pedidos, clientes, produtos e entregas.

O domínio foi escolhido por permitir análises logísticas reais, especialmente:

* tempo de entrega
* performance operacional
* atrasos de pedidos

---

## 🧱 Modelagem de Dados

A camada Gold segue um modelo **Star Schema**.

### Tabela Fato

`fato_sales`

Métricas:

* preço
* valor do frete
* lead time de entrega
* atraso de entrega

### Dimensões

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

1. Clonar o repositório

```
git clone <repo>
```

2. Subir o ambiente

```
docker-compose up -d
```

3. Acessar o Airflow

```
http://localhost:8080
```

4. Ativar a DAG:

```
pipeline_lakehouse_layers
```

---

## 📁 Estrutura do Repositório

```
dags/                -> DAGs de orquestração
scripts/             -> Scripts das camadas Bronze, Silver e Gold
data/landingzone/    -> Arquivos originais
data/bronze/         -> Dados brutos particionados
data/silver/         -> Dados tratados
data/gold/           -> Modelo dimensional
```

---

## ⚙️ Decisões Técnicas

**Parquet**
Escolhido por ser um formato colunar, comprimido e otimizado para leitura analítica.

**Particionamento por data de ingestão**
Permite rastrear cargas, reprocessar dados e manter histórico.

**Append-Only na Bronze**
Garante auditoria e reprodutibilidade do pipeline.

**Full Load Silver/Gold**
Simplifica consistência do modelo dimensional durante a fase inicial do projeto.

**Pandas em vez de Spark**
Volume de dados compatível com processamento local e objetivo educacional focado em arquitetura e modelagem.

---

## 🔮 Melhorias Futuras

* Implementação de carga incremental (CDC)
* Uso de Delta Lake
* Criação de SCD Type 2 em dimensões
* Deploy em ambiente cloud
* Integração com ferramenta de BI
* Monitoramento de qualidade de dados

---

## 📌 Conclusão

O projeto demonstra a construção de um pipeline completo de dados seguindo conceitos modernos de Data Lakehouse, boas práticas de engenharia de dados e modelagem dimensional, simulando um fluxo de processamento semelhante ao encontrado em ambientes corporativos.
