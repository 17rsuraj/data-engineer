# Data Lake

_Data Engineering project with real and simulated data_

### The Goals:

Implementing data lake in AWS to build an ETL pipeline for a data stored in Amazon S3, below mentioned goals are achieved.
1. Creating AWS EMR Cluster for Distributed Computing
2. Create and Define Spark session
3. Extract data from Amazon S3 to Spark DataFrame
4. Transform and load the data into fact and dimension tables. Writing ETL pipeline for it.

### Project Background:

An Imaginary startup called as Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. 
The analytics team is particularly interested in understanding what songs users are listening to. 
Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app

Being a Data Engineer, I built an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

------------------------------------------------------

### Datasets:

Two separate datasets song_data and log_data are used in this project.

**1. song_data :**

This is a subset of real data from the [Million Song Dataset](http://millionsongdataset.com/) . Each file is in JSON format and contains metadata about a song and the artist of that song.

This is the example of single song file in this dataset,

>{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

**2. log_data :**

The second dataset consists of log files in JSON format generated by this [Event Simulator](https://github.com/Interana/eventsim) based on the songs in song_data above. These simulate activity logs from a music streaming app based on specified configurations.

### Data Tables:

ETL Pipeline is created to extract and load the data in the fact and dimension tables

1. Fact Table:

One fact table called as songplays is created by extracting below mentioned data from other song_data and log_data datasets

columns: [songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent]


2. Dimension Tables:

Four dimension tables are created with the columns as shown below and loaded with the data .

1. songs: [song_id, title, artist_id, year, duration]
2. users: [user_id, first_name, last_name, gender, level]
3. artists: [artist_id, name, location, latitude, longitude]
4. time: [start_time, hour, day, week, month, year, weekday]

--------------------------------------------------

### Files and Usage:

Create these files in the given order

1. dl.cfg : Configuration file where user need to add the Cluster credentials. (_Never share your cluster credentials with anyone_)

2. etl.py : To read and process files from song_data and log_data and loads them into your tables. 

-----------------------------------------------------

### Implementation:

Create S3 bucket to store the output data. I created S3 bucket named <code>datalake-dend-project</code>


Run / Edit these files in given order

1. Edit **dl.cfg** file with your AWS credentials
2. Run **etl.py**


------------------------------------------------------

#### License

[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/)
