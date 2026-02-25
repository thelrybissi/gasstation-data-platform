from pyspark.sql.functions import col

storage_key = "YOU_STORAGE_KEY".strip()

# ==========================
# 1. CONFIGURAÇÃO STORAGE
# ==========================

spark.conf.set(
  "fs.azure.account.key.gasstations.dfs.core.windows.net",
  storage_key
)

# ==========================
# 1. LER SILVER (DELTA NO ADLS)
# ==========================

silver_path = "abfss://raw@gasstations.dfs.core.windows.net/silver/gas_station_data"

df_silver = spark.read.format("delta").load(silver_path)

# ==========================
# 2. REGRA DE NEGÓCIO
# ==========================

df_gold = df_silver.filter(
    col("distribuidora") == "BANDEIRA BRANCA"
)

# ==========================
# 3. SALVAR GOLD COMO DELTA
# ==========================

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .save("abfss://raw@gasstations.dfs.core.windows.net/gold/bandeira_branca_postos")

print("Gold carregado com sucesso!")