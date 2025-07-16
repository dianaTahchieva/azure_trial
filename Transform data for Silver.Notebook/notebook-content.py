# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "b92e1a71-5b87-4d04-960d-eac926a331dc",
# META       "default_lakehouse_name": "salesLH",
# META       "default_lakehouse_workspace_id": "663ed175-8721-40bd-a204-428a0e1ab961",
# META       "known_lakehouses": [
# META         {
# META           "id": "b92e1a71-5b87-4d04-960d-eac926a331dc"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/03b-medallion-lakehouse.html#create-a-lakehouse-and-upload-data-to-bronze-layer


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pandas as pd

dfp = pd.read_csv("https://raw.githubusercontent.com/MicrosoftLearning/dp-data/main/sales.csv")
spark_df = spark.createDataFrame(dfp)
spark_df.write.format("delta") \
    .mode("overwrite") \
    .save("Tables/sales/staging_sales")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import *

orderSchema = StructType(
    [
    StructField("SalesOrderLineNumber", IntegerType()),
    StructField("OrderDate", DateType()),
    StructField("CustomerName", StringType()),
    StructField("Email", StringType()),
    StructField("Item", StringType()),
    StructField("Quantity", IntegerType()),
    StructField("UnitPrice", FloatType()),
    StructField("Tax", FloatType())
    ]
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header", "true").schema(orderSchema).load("Files/bronze/*.csv")
display(df.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import when, lit, col, current_timestamp, input_file_name

df = df.withColumn("FileName", input_file_name()) \
.withColumn("IsFlagged", when(col("OrderDate") < '2019-08-01',True).otherwise(False)) \
.withColumn("CreatedTS", current_timestamp())\
.withColumn("ModifiedTS", current_timestamp())\
.withColumn("CustomerName", when((col("CustomerName").isNull() | (col("CustomerName")=="")),lit("Unknown")).otherwise(col("CustomerName")))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import *
from delta.tables import *

DeltaTable.createIfNotExists(spark)\
    .tableName("sales.sales_silver")\
    .addColumn("SalesOrderNumber", StringType()) \
    .addColumn("SalesOrderLineNumber", IntegerType()) \
    .addColumn("OrderDate", DateType()) \
    .addColumn("CustomerName", StringType()) \
    .addColumn("Email", StringType()) \
    .addColumn("Item", StringType()) \
    .addColumn("Quantity", IntegerType()) \
    .addColumn("UnitPrice", FloatType()) \
    .addColumn("Tax", FloatType()) \
    .addColumn("FileName", StringType()) \
    .addColumn("IsFlagged", BooleanType()) \
    .addColumn("CreatedTS", DateType()) \
    .addColumn("ModifiedTS", DateType()) \
    .execute()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
