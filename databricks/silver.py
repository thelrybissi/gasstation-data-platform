from pyspark.sql.functions import col

spark.sql("CREATE SCHEMA IF NOT EXISTS silver")

df_bronze = spark.table("bronze.gas_station_data")

df_silver = df_bronze.drop(
    "latitude",
    "longitude",
    "latitude_ANP4C",
    "longitude_ANP4C"
)

df_silver.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("silver.gas_station_data")

print("Silver carregado com sucesso.")