from pyspark.sql.functions import col

spark.sql("CREATE SCHEMA IF NOT EXISTS gold")

df_silver = spark.table("silver.gas_station_data")

df_gold = df_silver.filter(
    col("distribuidora") == "BANDEIRA BRANCA"
)

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold.bandeira_branca_postos")

print("Gold carregado com sucesso.")