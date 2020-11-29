# Data Pipeline

_Data Engineering project with real and simulated data_

### The Goals:

Setting up a Data Pipeline using Apache Airflow below mentioned goals are achieved.
1. Build 4 operators to stage the data, transform the data, and run checks on data quality
2. Configure Airflow DAG
3. Create connections for AWS Redshift and AWS credentials
4. Configure the task dependencies to Transform and load the data into fact and dimension tables.

### Project Background:

An Imaginary startup called as Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. 
The analytics team is particularly interested in understanding what songs users are listening to. 
Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app

Being a Data Engineer, I built high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills for their analytics team to continue finding insights in what songs their users are listening to.

------------------------------------------------------

### Datasets:

Two separate datasets song_data and log_data are used in this project.

**1. song_data :**

This is a subset of real data from the [Million Song Dataset](http://millionsongdataset.com/) . Each file is in JSON format and contains metadata about a song and the artist of that song.

This is the example of single song file in this dataset,

>{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

**2. log_data :**

The second dataset consists of log files in JSON format generated by this [Event Simulator](https://github.com/Interana/eventsim) based on the songs in song_data above. These simulate activity logs from a music streaming app based on specified configurations.

### Operators:

1. Stage Operator : To load any JSON formatted files from S3 to Amazon Redshift
2. Fact Operators : To run data transformations with the help of provided SQL helper class
3. Dimension Operators : To run data transformations with the help of provided SQL helper class. Dimension loads are often done with the truncate-insert pattern where the target table is emptied before the load
4. Data Quality Operator : To run checks on the data itself

### DAG Configurations

1. The DAG does not have dependencies on past runs
2. On failure, the task are retried 3 times
3. Retries happen every 5 minutes
4. Catchup is turned off
5. Do not email on retry

### Task Dependencies

![](https://github.com/17rsuraj/data-engineer/blob/master/Data%20Pipeline%20with%20Apache%20Airflow/Task%20dependencies.JPG)



--------------------------------------------------

### Files and Usage:

Below are the project files for this Data Pipeline

1. README: The one you are reading now, includes project documentation
2. dags/udag_example_dag.py: Directed Acyclic Graph definition with imports, tasks and task dependencies
3. plugins/helpers/sql_queries.py: Contains Insert SQL statements
4. plugins/operators/stage_redshift.py: Operator that copies data from S3 buckets into redshift staging tables
5. plugins/operators/load_dimension.py: Operator that loads data from redshift staging tables into dimensional tables
6. plugins/operators/load_fact.py: Operator that loads data from redshift staging tables into fact table
7. plugins/operators/data_quality.py: Operator that validates data quality in redshift tables


-----------------------------------------------------

### Implementation:

Run the **udag_example_dag.py** file to host the Airflow web server. Once it is ready to use, go on Airflow web server UI and trigger the DAG to execute the pipeline.


------------------------------------------------------

#### License

[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/)