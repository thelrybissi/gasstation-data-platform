from pyspark.sql.functions import current_timestamp, explode

# ==========================
# 1. CONFIGURAÇÃO STORAGE
# ==========================

storage_key = "YOU_STORAGE_KEY".strip()

spark.conf.set(
  "fs.azure.account.key.gasstations.dfs.core.windows.net",
  storage_key
)

raw_path = "abfss://raw@gasstations.dfs.core.windows.net/api_name/"

# ==========================
# 2. LER JSON COMPLETO
# ==========================

df_temp = spark.read \
    .option("multiLine", True) \
    .option("recursiveFileLookup", "true") \
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
# 6. SALVAR COMO DELTA
# ==========================

df_bronze.write \
    .format("delta") \
    .mode("append") \
    .save("abfss://raw@gasstations.dfs.core.windows.net/bronze/gas_station_data")

print("Bronze carregado com sucesso.")