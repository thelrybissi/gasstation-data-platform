📘 README – Gas Stations Data Platform (Azure + Databricks)
🚀 Objetivo do Projeto

Este projeto implementa uma Data Platform moderna em arquitetura Lakehouse, consumindo dados públicos via API, armazenando no Azure Data Lake e processando com Databricks utilizando o modelo Bronze → Silver → Gold.

O objetivo é demonstrar:

Ingestão automatizada de dados via API

Armazenamento em Data Lake (ADLS Gen2)

Processamento distribuído com Spark

Modelagem em camadas (Medallion Architecture)

Versionamento com Git

Deploy automatizado com GitHub Actions

🏗️ Arquitetura
API Pública (ANP)
        ↓
Azure Data Factory
        ↓
Azure Data Lake (raw)
        ↓
Databricks (Bronze → Silver → Gold)
        ↓
Delta Lake Tables

CI/CD:

GitHub
   ↓
GitHub Actions
   ↓
Databricks Workspace
🧱 Camadas da Arquitetura (Medallion)
🥉 Bronze

Leitura de JSON bruto da API

Explode de arrays aninhados

Inclusão de metadata (ingestion_timestamp)

Persistência em Delta Lake

Objetivo: preservar dados quase brutos para auditoria e reprocessamento.

🥈 Silver

Limpeza de campos desnecessários

Remoção de colunas inválidas (latitude, longitude etc.)

Normalização de estrutura

Objetivo: dados confiáveis e estruturados.

🥇 Gold

Aplicação de regra de negócio:

distribuidora == "BANDEIRA BRANCA"

Dados prontos para consumo analítico

Objetivo: camada final orientada a negócio.

⚙️ Componentes Utilizados
Azure

Resource Group

Storage Account (ADLS Gen2)

Container: raw

Azure Data Factory (pipeline REST → Blob)

Databricks

Spark SQL

Delta Lake

Hive Metastore (spark_catalog)

Cluster compute

DevOps

GitHub Repository

GitHub Actions

Databricks CLI v2

🔄 Fluxo de Dados

ADF consome API REST

JSON salvo em:

abfss://raw@storage/api_name/yyyy/mm/dd/

Databricks lê recursivamente

Processa Bronze

Cria Delta Table

CI/CD versiona código

🔐 Segurança

Autenticação via Storage Key (MVP)

Recomenda-se uso de Secret Scope ou Managed Identity em produção

📌 Principais Aprendizados Técnicos

Diferença entre DBFS e ADLS

Limitações do Hive Metastore com DBFS desabilitado

Uso correto de .option("path") para tabelas externas

Deploy automatizado via CLI

Arquitetura Lakehouse moderna
