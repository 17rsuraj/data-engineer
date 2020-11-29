# Data Pipeline

_Data Engineering project with US Immigration Data Obtained from [US National Tourism and Trade Office](https://travel.trade.gov/research/reports/i94/historical/2016.html)_

### The Goals:

While achieving enrichment of US Immigration Data, below mentioned goals are achieved.
1. Create and Define Spark session
2. Define fact and dimension tables for a star schema
3. Extract the data from different data sources, transform and load into fact and dimension tables.
4. Perform data quality checks

### Project Background:

The purpose of this project is to create a US immigration database optimized for query performance and further analysis of US immigration data . 
This database will contain the US immigration data enriched with additional data such as temperature data for destination cities.


Being a Data Engineer, I built an ETL pipeline that extracts data from two different data sources, assess, clean, transform it and final load it in fact and dimension tables. 
At the end, I also perform data quality checks to ensure the data is correctly loaded into the database.

### Project Execution:

Project follows this simplified structure in 5 steps which are mentioned in the <code>Capstone Project Template.ipynb</code> file

- Step 1: Scope the Project and Gather Data
- Step 2: Explore and Assess the Data
- Step 3: Define the Data Model
- Step 4: Run ETL to Model the Data
- Step 5: Complete Project Write Up

------------------------------------------------------

### Datasets:

1. Immigration Data

This data comes from the [US National Tourism and Trade Office](https://travel.trade.gov/research/reports/i94/historical/2016.html). A data dictionary is included in project notebook. 
There's a sample file so you can take a look at the data in csv format before reading it all in. 
I selected only April 2016 data to accomplish the goal of this project. It contains nearly 3 Million rows and 7 columns

2. Temperature Data
This data is collected from [Kaggle](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data) dataset. This contains nearly 8 Million rows

### Data Tables:

**Dimension Tables**

1. I94_Immigration

|Column Name| Description |
|-----------|------------ |
|i94yr| 4 Digit year |
|i94mon| Numeric month |
|i94cit|  3 Digit code of origin city |
|i94port| 3 Character code of destination USA city |
|arrdate| Arrival date in the USA |
|i94mode| 1 Digit travel code |
|depdate| Departure date from the USA |
|i94visa| Reason for immigration |

2. Temperature_Data

|Column Name| Description |
|-----------|------------ |
|i94port| 3 Character code of destination city  |
|AverageTemperature| Average temperature |
|City|  City name |
|Country| Country name |
|Latitude| Latitude |
|Longitude| Longitude |

**Fact Table** 

US_Immigration_Facts:

|Column Name| Description |
|-----------|------------ |
|i94yr| 4 Digit year |
|i94mon| Numeric month |
|i94cit|  3 Digit code of origin city |
|i94port| 3 Character code of destination USA city |
|arrdate| Arrival date in the USA |
|i94mode| 1 Digit travel code |
|depdate| Departure date from the USA |
|i94visa| Reason for immigration |
|AverageTemperature| Average temperature of destination city |

--------------------------------------------------

### Files and Usage:

1. <code>Capstone Project Template.ipynb</code> 
This file contains all the 5 steps in which this project is executed.

2. <code>i94port.txt</code> 
This file contains valid city codes which are required in the further steps in data pipeline. 

These both files should be in the same directory to execute the data pipeline successfully.
-----------------------------------------------------

### Rationale for the choice of tools and technologies for the project

- **Technologies used**: Spark DataFrame, Pandas DataFrame, Spark SQL

- **Reasons**:
>> 
        - Spark can handle different file formats such as .SAS7BDAT and .csv which contain large amount of data. 
        - I initially tried to load the data into Pandas DataFrame for the file with nearly 3 Million rows but the time taken for this operation was very large. Hence, I decided to use the Spark DataFrame. 
        - Spark SQL was used to process the input files into dataframes and manipulated via standard SQL join operations to create the tables

-----------------------------------------------------
### How to approach the problem differently under below scenarios:

1. The data was increased by 100x
 - **Approach_1**: Use Amazon Redshift which is optimized for aggregation and read-heavy workloads
 - **Approach_2**: Use Spark in distributed way with the help of Elastic Map Reduce (EMR)
 
2. The data populates a dashboard that must be updated on a daily basis by 7am every day
 - **Approach**: Use Airflow and create a DAG that trigegrs daily for the designed pipeline
 
3. The database needed to be accessed by 100+ people
 - **Approach**: Again Amazon Redshift can be used. Redshift has auto-scaling capabilities and good read performance. Hence, the data can be accessed by 100+ people easily



------------------------------------------------------

#### License

[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/)
