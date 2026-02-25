from pyspark.sql.functions import col

storage_key = "YOU_STORAGE_KEY".strip()

# ==========================
# 1. CONFIGURAÇÃO STORAGE
# ==========================

spark.conf.set(
  "fs.azure.account.key.gasstations.dfs.core.windows.net",
  storage_key
)

bronze_path = "abfss://raw@gasstations.dfs.core.windows.net/bronze/gas_station_data"

df_bronze = spark.read.format("delta").load(bronze_path)

df_silver = df_bronze.drop(
    "latitude",
    "longitude",
    "latitude_ANP4C",
    "longitude_ANP4C"
)

df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .save("abfss://raw@gasstations.dfs.core.windows.net/silver/gas_station_data")

print("Silver carregado com sucesso.")