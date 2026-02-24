from pyspark.sql.functions import current_timestamp

raw_path = "abfss://raw@gasstation.dfs.core.windows.net/api_name/"

df_raw = spark.read.option("multiLine", True).json(raw_path)

df_bronze = df_raw.withColumn("ingestion_timestamp", current_timestamp())

df_bronze.write.format("delta") \
    .mode("append") \
    .saveAsTable("bronze.gas_station_data")