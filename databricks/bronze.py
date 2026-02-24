from pyspark.sql.functions import current_timestamp, explode

# ==========================
# 1. CONFIGURAÇÃO STORAGE
# ==========================

spark.conf.set(
  "fs.azure.account.key.gasstation.dfs.core.windows.net",
  "SUA_STORAGE_KEY_AQUI"
)

raw_path = "abfss://raw@gasstation.dfs.core.windows.net/api_name/"

# ==========================
# 2. LER JSON COMPLETO
# ==========================

df_temp = spark.read \
    .option("multiLine", True) \
    .json(raw_path)

# ==========================
# 3. EXPLODIR ARRAY PRINCIPAL
# ==========================

df_raw = df_temp \
    .select(explode("data").alias("item")) \
    .select("item.*")

# ==========================
# 4. ADICIONAR METADADOS
# ==========================

df_bronze = df_raw.withColumn("ingestion_timestamp", current_timestamp())

# ==========================
# 5. CRIAR SCHEMA SE NÃO EXISTIR
# ==========================

spark.sql("CREATE SCHEMA IF NOT EXISTS bronze")

# ==========================
# 6. SALVAR COMO DELTA
# ==========================

df_bronze.write \
    .format("delta") \
    .mode("append") \
    .saveAsTable("bronze.gas_station_data")

print("Bronze carregado com sucesso.")