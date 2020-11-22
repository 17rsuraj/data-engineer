import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import TimestampType


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    - Creates a Spark session with the specified configurations
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    - Extracts the song_data from Amazon S3
    
    - Transforms the extracted data
    
    - Loads the processed data back to Amazon S3
    """
    # get filepath to song data file
    song_data = input_data + "song_data/*/*/*/*.json"
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table_columns = ["song_id", "title", "artist_id", "year", "duration"]
    songs_table = df.select(songs_table_columns).dropDulicates()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist_id").parquet(output_data + 'songs/')

    # extract columns to create artists table
    artists_table_columns = ["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]
    artists_table = df.select(artists_table_columns).dropDulicates()
    
    # write artists table to parquet files
    artists_table.write.parquet(output_data + 'artists/')


def process_log_data(spark, input_data, output_data):
    """
    - Extracts the log_data from Amazon S3
    
    - Processes the extracted data
    
    - Loads the processed data back to Amazon S3
    """
    # get filepath to log data file
    log_data = input_data + "log_data/*/*/*.json"

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == "NextSong")

    # extract columns for users table 
    users_table_columns = ["userId", "firstName", "lastName", "gender", "level"]
    users_table = df.select(users_table_columns).dropDulicates()
    
    # write users table to parquet files
    users_table.write.parquet(output_data + 'users/')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: datetime.fromtimestamp(x / 1000), TimestampType()) #column "ts" is in milliseconds, so need to divide by 1000
    df = df.withColumn("timestamp", get_timestamp(col("ts")))
        
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: to_date(x), TimestampType())
    df = df.withColumn("start_time", get_timestamp(col("ts")))
    
    # extract columns to create time table
    df = df.withColumn("hour", hour("timestamp"))
    df = df.withColumn("day", dayofmonth("timestamp"))
    df = df.withColumn("month", month("timestamp"))
    df = df.withColumn("year", year("timestamp"))
    df = df.withColumn("week", weekofyear("timestamp"))
    df = df.withColumn("weekday", dayofweek("timestamp"))
    
    time_table_columns = ["start_time", "hour", "day", "week", "month", "year", "weekday"]
    time_table = df.select(time_table_columns).dropDuplicates()
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").parquet(output_data + 'time/')

    # read in song data, artists data to use for songplays table
    song_df = spark.read.parquet(output_data + 'songs/*/*/*')
    artists_df = spark.read.parquet(output_data + 'artists/*')
    songs_log_df = df.join(songs_df, (df.song == songs_df.title))
    artists_songs_log_df = songs_log_df.join(artists_df, (songs_log_df.artist == artists_df.artist_name))
    
    songplays_df = artists_songs_log_df.join(time_table, artists_songs_log_df.ts == time_table.start_time, 'left').drop(artists_songs_logs.year)

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table_columns = ["start_time", "userId", "level", "song_id", "artist_id", "sessionId", "location", "userAgent", "year", "month"]
    songplays_table = songplays_df.select(songplays_table_columns).dropDuplicates()

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").parquet(output_data + 'songplays/')
    


def main():
    """
    - Creates Spark session with the AWS credentials
    
    - Extracts the data from Amazon S3 and trsnforms it as per requirement
    
    - Finally, loads the processed data back to the S3 bucket
    """
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://datalake-dend-project/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
