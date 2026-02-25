# ============================================
# 1️⃣ CONFIGURAÇÃO JDBC
# ============================================

jdbc_url = (
    "jdbc:sqlserver://YOU_Server:1433;"
    "database=YOU_DB_NAME;"
    "encrypt=true;"
    "trustServerCertificate=false;"
    "hostNameInCertificate=*.database.windows.net;"
    "loginTimeout=30;"
)

connection_properties = {
    "user": "YOU_DB_USER".strip(),
    "password": "YOU_DB_PASSWORD".strip(),
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# ============================================
# 2️⃣ CONFIGURAÇÃO STORAGE
# ============================================

storage_key = "YOU_STORAGE_KEY".strip()

spark.conf.set(
    "fs.azure.account.key.gasstations.dfs.core.windows.net",
    storage_key
)

# ============================================
# 3️⃣ LEITURA DO GOLD (DELTA)
# ============================================

gold_path = "abfss://raw@gasstations.dfs.core.windows.net/gold/bandeira_branca_postos"

df_gold = spark.read.format("delta").load(gold_path)

# ============================================
# 4️⃣ TRATAR COLUNAS COMPLEXAS (ARRAY / STRUCT)
# ============================================

from pyspark.sql.functions import col, concat_ws, to_json

df_gold_fixed = df_gold \
    .withColumn("inadimplenciaPMQC", concat_ws(",", col("inadimplenciaPMQC"))) \
    .withColumn("produtos", to_json(col("produtos")))

# ============================================
# 5️⃣ ENVIAR PARA AZURE SQL
# ============================================

df_gold_fixed.write \
    .mode("append") \
    .jdbc(jdbc_url, "dbo.bandeira_branca_postos", properties=connection_properties)

print("✅ Dados enviados para Azure SQL com sucesso!")