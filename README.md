Descrição do DERSO

Este repositório apresenta um pipeline completo de engenharia de dados utilizando Apache Airflow em ambiente on-premise (Databricks local), com o objetivo de orquestrar a ingestão, transformação, modelagem e disponibilização de dados em múltiplas camadas.

O projeto utiliza 3 ou mais tabelas relacionadas ao mesmo domínio temático (ex.: datasets do Kaggle, dados gerados pelo GPT, etc.), demonstrando o processo de ponta a ponta de um fluxo moderno de dados. Todo o desenvolvimento é controlado por versionamento via GitHub, utilizando commits estruturados e documentação adequada.

Principais Componentes
Orquestração

Execução via Apache Airflow

DAGs criadas para controlar dependências entre etapas

Monitoramento e reprocessamento de tarefas

Processamento de Dados

Execução local com Databricks (on-premise)

Camadas definidas em arquitetura estilo medallion:

Landing

Bronze

Silver

Gold

Modelagem Dimensional

Estrutura em Fato e Dimensão

Aplicação de boas práticas de Data Warehouse

Ajustes para consultas analíticas

Dataset

Conjunto de tabelas do mesmo assunto/tema (econômico, esportivo, mídia, etc.)

Possibilidade de expansão (mais tabelas/dominios)

Governança e Versionamento

Controle via Git + GitHub

Commits granulares e descritivos

Issue tracking e milestones

Documentação

README com explicação do cenário

Stack utilizada

Como executar o projeto

Fluxo das etapas e exemplos

Objetivos de Aprendizado

Este projeto busca demonstrar competências em:

✔ Orquestração de pipelines batch
✔ ETL/ELT completo do zero
✔ Boas práticas de engenharia de dados
✔ Modelagem Dimensional
✔ Organização e controle de versionamento
✔ Documentação e padronização de repositório

Timeline Estimada

🗓 Duração total: 20 dias
📅 Prazo planejado: até 09/02
