import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.conf import SparkConf
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from pyspark.sql.functions import col, avg

args = getResolvedOptions(sys.argv, [])
job_name = args['JOB_NAME'] if 'JOB_NAME' in args else 'test'

spark_conf = SparkConf().setAppName("AppName")
spark_conf.set("spark.hadoop.fs.s3a.endpoint", "http://172.22.0.2:9000")

sc = SparkContext(conf=spark_conf)
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(job_name, args)

table = "data"
source = "s3a://input/data.csv"
parquet_path = "s3a://output/"

df = spark.read \
    .option("delimiter", ",") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(source)

S3bucket_node1 = DynamicFrame.fromDF(dataframe=df, glue_ctx=glueContext, name=table)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.getSink(
    path=parquet_path,
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    # compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="S3bucket_node3",
)
S3bucket_node3.setCatalogInfo(catalogDatabase="rlv", catalogTableName=table)
S3bucket_node3.setFormat("csv")
S3bucket_node3.writeFrame(S3bucket_node1)

job.commit()
