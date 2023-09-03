# Glue Spark Job Runner with Docker Compose

## Introduction
This project allows you to run and test Glue Spark jobs locally using Docker images. It mimics Amazon S3 using the Minio service for storing input and output files, and it uses the official AWS Docker image for Glue to execute the jobs. Docker Compose is used to orchestrate these services.

## Prerequisites
Before getting started, ensure you have the following prerequisites installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Installation
1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/trupropel/local-glue-runner.git
   cd local-glue-runner
   ```

2. Build the Docker containers:

   ```bash
   docker-compose build
   ```

3. Start the services:

   ```bash
   docker-compose up -d
   ```

## Customizing S3 Endpoint Configuration

By default, this project is configured to use Minio as the S3 endpoint for local testing, with the endpoint URL set to `http://s3:9000`. If you need to use a different S3 endpoint for your Glue job initialization, you can do so by modifying the Spark configuration in your Glue job script.

In your Glue job script (`/home/glue_user/workspace/src/my-job.py`), you can customize the S3 endpoint using the `spark.hadoop.fs.s3a.endpoint` configuration option. Here's an example of how to set a different S3 endpoint:

```python
from pyspark.context import SparkContext
from pyspark.conf import SparkConf
from awsglue.context import GlueContext
from awsglue.job import Job

# Initialize Spark configuration
spark_conf = SparkConf().setAppName("MyAppName")

# Customize the S3 endpoint (replace with your desired endpoint URL)
spark_conf.set("spark.hadoop.fs.s3a.endpoint", "http://s3:9000")

# Initialize SparkContext
sc = SparkContext(conf=spark_conf)

# Initialize GlueContext and SparkSession
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
```

After this setup you can load your files using the `s3a` protocol name like this

```python
df = spark.read \
    .schema(schema) \
    .csv("s3a://out/my_data_file.csv")
```

## Usage
1. Mimic S3 locally using Minio:
   - Access the Minio console at [http://localhost:9000](http://localhost:9000) (credentials: `local` / `locallocal`).

2. Upload your input files to Minio, creating a bucket if necessary.

3. Edit your Glue Spark job script located at `./src/my-job.py`.

4. Execute the Glue job using the following command:

   ```bash
   docker-compose exec glue spark-submit /home/glue_user/workspace/src/my-job.py
   ```

   Replace `/home/glue_user/workspace/src/my-job.py` with the correct path to your Glue Spark job script if needed.

## Troubleshooting
- If you encounter any issues or errors, please refer to the following troubleshooting steps:
  - Ensure that Docker and Docker Compose are correctly installed and running.
  - Check your Glue job script for errors.
  - Verify that Minio is running and accessible at [http://localhost:9000](http://localhost:9000).
  - Double-check your AWS credentials and configuration in the `docker-compose.yml` file.
  - Inspect the logs of the Glue and Minio containers for error messages.

## Contributing
Feel free to contribute to this project by opening issues or creating pull requests.

## License
This project is licensed under the [MIT License](LICENSE).
