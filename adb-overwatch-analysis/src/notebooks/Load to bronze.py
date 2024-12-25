# Databricks notebook source
result_df = spark.sql("DESCRIBE EXTERNAL LOCATION `landing`")
landing_url = result_df.select("url").collect()[0][0]

# COMMAND ----------

schemaLoc = landing_url + "checkpoints"

# COMMAND ----------

display(schemaLoc)

# COMMAND ----------

# MAGIC %md
# MAGIC **creating a read_Traffic_Data() Function**

# COMMAND ----------

def read_Traffic_Data():
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
    from pyspark.sql.functions import current_timestamp
    print(" Reading Traffic Data: ", end='')
    schema = StructType([
        StructField("Record_ID", IntegerType()),
        StructField("Count_point_id", IntegerType()),
        StructField("Direction_of_travel", StringType()),
        StructField("Year", IntegerType()),
        StructField("Count_date", StringType()),
        StructField("hour", IntegerType()),
        StructField("Region_id", IntegerType()),
        StructField("Region_name", StringType()),
        StructField("Local_authority_name", StringType()),
        StructField("Road_name", StringType()),
        StructField("Road_Category_ID", IntegerType()),
        StructField("Start_junction_road_name", StringType()),
        StructField("End_junction_road_name", StringType()),
        StructField("Latitude", DoubleType()),
        StructField("Longitude", DoubleType()),
        StructField("Link_length_km", DoubleType()),
        StructField("Pedal_cycles", IntegerType()),
        StructField("Two_wheeled_motor_vehicles", IntegerType()),
        StructField("Cars_and_taxis", IntegerType()),
        StructField("Buses_and_coaches", IntegerType()),
        StructField("LGV_Type", IntegerType()),
        StructField("HGV_Type", IntegerType()),
        StructField("EV_Car", IntegerType()),
        StructField("EV_Bike", IntegerType())
    ])

    rawTraffic_stream = (spark.readStream
                         .format("cloudFiles")
                         .option("cloudFiles.format", "csv")
                         .option("cloudFiles.schemaLocation", f'{schemaLoc}/rawTrafficLoad/schemaInfer')
                         .option('header', 'true')
                         .schema(schema)
                         .load(landing_url + '/sourcefiles/raw_traffic')
                         .withColumn("Extract_Time", current_timestamp()))

    print('Reading Sucess !!')
    return rawTraffic_stream

# COMMAND ----------

read_df = read_Traffic_Data()

# COMMAND ----------

def write_Traffic_Data(StreamingDF):
    write_Data = (StreamingDF.writeStream
                    .format('delta')
                    .option("checkpointLocation", landing_url + '/rawTrafficLoad/Checkpt')
                    .outputMode('append')
                    .queryName('rawRoadsWriteStream')
                    .trigger(availableNow=True)
                    .toTable("`main`.`bronze`.`raw_traffic`"))
    
    write_Data.awaitTermination()
    print('Write Success')
    print("****************************")    


# COMMAND ----------

# MAGIC %md
# MAGIC Calling read and WriteFunctions

# COMMAND ----------

read_df = read_Traffic_Data()
write_Traffic_Data(read_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Creating read_Road_Data() Function
# MAGIC
# MAGIC # COMMAND ----------

# COMMAND ----------


def read_Road_Data():
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
    from pyspark.sql.functions import current_timestamp
    print("Reading the Raw Roads Data :  ", end='')
    schema = StructType([
        StructField('Road_ID',IntegerType()),
        StructField('Road_Category_Id',IntegerType()),
        StructField('Road_Category',StringType()),
        StructField('Region_ID',IntegerType()),
        StructField('Region_Name',StringType()),
        StructField('Total_Link_Length_Km',DoubleType()),
        StructField('Total_Link_Length_Miles',DoubleType()),
        StructField('All_Motor_Vehicles',DoubleType())
        
        ])
    rawRoads_stream = (spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format","csv")
        .option('cloudFiles.schemaLocation', f'{schemaLoc}/rawRoadsLoad/schemaInfer')
        .option('header','true')
        .schema(schema)
        .load(landing_url+'sourcefiles/raw_roads')
        )
    
    print('Reading Succcess !!')
    print('*******************')

    return rawRoads_stream

# COMMAND ----------

# MAGIC %md
# MAGIC ## Creating write_Traffic_Data(StreamingDF,environment) Function
# MAGIC # COMMAND ----------

# COMMAND ----------

def write_Road_Data(StreamingDF):
    writerw_Data = (StreamingDF.writeStream
                    .format('delta')
                    .option("checkpointLocation", landing_url + 'checkpoints/rawRoadsLoad/Checkpt')
                    .trigger(availableNow=True)
                    .toTable("`main`.`bronze`.`raw_roads`"))
    writerw_Data.awaitTermination()

# COMMAND ----------

read_roads = read_Road_Data()
## Writing the raw_roads's data from landing to Bronze
write_Road_Data(read_roads)


# COMMAND ----------

# MAGIC %sql
# MAGIC select * from main.bronze.raw_roads
