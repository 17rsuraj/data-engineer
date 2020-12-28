#### Title: 
## Improvement of US Immigration Data with Temperature, Demographics and Airport Data


### Project Summary

The data files for this project are provided by Udacity as fulfilment of Data Engineering Nanodegree Program.

The purpose of this project is to enhance an US immigration database with the help of 4 data sets and implement dimensional modeling. This database contains 3 dimension tables and 1 fact table connected each other through Star schema. Ultimately, the US immigration data will be improved with airport codes, US demographics data and temperature data.

This database can be used for analysis of US Immigration, for example - 
1. Which type of airport immigrants usually prefer to travel ?
2. To which type of desination such as hotter or cooler, immigrants travel ?
3. What is the gender ratio of the immigrants ?

### Goals
Through this project US immigration data will be enriched and below goals will be achieved
1. Create and Define Spark session
2. Define fact and dimension tables for a star schema
3. Extract the data from different data sources, transform and load into fact and dimension tables 
4. Store the data model (fact and dimension tables) in parquet files
5. Perform data quality checks for the data stored in fact and dimension tables

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

-------------------------------------------------

### Data

1. _Immigration Data_

There are 3.08 Million rows in this immigration dataset which is to be read from <code>.sas7bdat</code> file. And hence reading the data in pandas dataframe (as shown in below cell) is time consuming. I tried it few time, but loading the data takes forever. Hence, it is commented out. As you move down in the project, this data is read in Spark data frame which is faster and efficient. The size of the Spark dataframe is understood from <code>spark_datafram.count()</code> command

2. _Temperature Data_

There are 8.6 Million rows in this temperature dataset which is to be read from <code>.csv</code> file. It is not as slow as immigration data from <code>.sas7bdat</code> file. Hence, this data is read in pandas dataframe (as shown in below cell). This step is just to explore the data. The size of the DataFrame is understood with <code>pandas.dataframe.shape<code> method.
  
3. _Airport Data_

Airport data is collected from <code>airport-codes_csv.csv</code> file which is obtained from [here](https://datahub.io/core/airport-codes#data). This is a simple table of airport codes and corresponding cities. Again, It is not as slow as immigration data from <code>.sas7bdat</code> file. Hence, this data is also read in pandas dataframe.

4. _Demographics Data_

US Demographics data is collected from <code>us-cities-demographics.csv</code> file which is obtained from [here](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/). Again, this data is also read in pandas dataframe.

------------------------------------------------------------

### Data Assessment - Quality Issues


1. Temperature Data

- Column ' dt ' contains dates, however, the data type for this column is ' object '. This should be ' datetime'  column
- The columns ' AverageTemperature ' and ' AverageTemperatureUncertainty contains 364130 missing values

2. Airport Data

- The data type for the column 'coordinates' is incorrectly set as object, it should be float
- There are missing values present in the column 'municipality' which should be eliminated to clean the dataset

3. Demographics Data

- The columns 'Male Population' and 'Female Population' has data type float. it should be int64
- There are missing values in few columns in this dataset

4. Immigration Data

- The data type for columns ' i94yr ' and ' i94mon ' is double which should be integer as year and month can not be float
- The column ' i94port ' contains invalid entries such as ' XXX '

----------------------------------------------------------------

### Data Cleaning

Looking at the quality issues, following 2 data cleaning steps will be performed.

1. **Immigration Data**:

- All data points with the destination city code i94port is not a valid value like (XXX, 99, NaN, etc) will be droped. This is described in I94_SAS_Labels_Description.SAS. 
- Hence a new file <code>i94port.txt</code> is created with only valid city codes. Also, the dictionary --> key-value pairs are created with city code and city. This dictionary can be used to clean the immigration data.

2. **Temperature Data**:

- Drop all data points where AverageTemperature is NaN and all duplicate locations
- Add the i94port of the location in each entry

3. **Airport Data**

- Drop all data points where municipality is NaN
- Add the i94port of the municipality in each entry

4. **Demographics Data**

-  Drop all data points where Male Population is NaN
-  Add the i94port of the City in each entry

---------------------------------------------------------------------

### Conceptual Data Model

#### 1. Star Schema

![image](https://github.com/17rsuraj/data-engineer/blob/master/Capstone%20Project/Schema.png)

#### 2. Dimension Tables

1. Temperature_Data

|Column Name| Description |
|-----------|------------ |
|i94port| 3 Character, i94port code of city  |
|AverageTemperature| Average temperature |
|City|  City name |
|Country| Country name |
|Latitude| Latitude |
|Longitude| Longitude |

2. Airport_Data: 

|Column Name| Description |
|-----------|------------ |
|name| Name of the Airport |
|type|  Type of the airport |
|elevation_ft| Elevation of the airport above sea level in feet |
|municipalty| Municipalty under which the airport is |
|i94port| 3 Character, i94port code of city  |


3. Demographic_Data

|Column Name| Description |
|-----------|------------ |
|City| Name of the City |
|State| Name of the State |
|AgeMedian| Median age of people in the city|
|MalePopulation| Number of Males in the city |
|FemalePopulation| Number of Females in the city |
|TotalPopulation| Total number of people in the city |
|Race| Race of the people in the city |
|i94port| i94port city code of the city |


#### 4. Fact Tables
US_Immigration_Facts:

|Column Name| Description |
|-----------|------------ |
|i94yr| 4 Digit year |
|i94mon| Numeric month |
|i94cit|  3 Digit code of origin city |
|i94port| 3 Character code of destination USA city |
|i94mode| 1 Digit travel code |
|depdate| Departure date from the USA |
|i94visa| Reason for immigration |
|gender| Gender of the immigrant |
|visatype| Type of visa the immigrant has |
|airline| Through which airline immigrant travelled |

-----------------------------------------------------------

### Data Pipelines
Finally, to create the the tables as explained above and to store them in Parquet format below steps should be performed as single ETL Pipeline. 

1. Create Dimention Table - Temperature_Data
2. Create Dimension Table - Airport_Data
3. Create Dimension Table - Demographics_Data
4. Create fact table - US_Immigration Facts
5. Immidiately after the creation, write these tables to Parquet file partitioned by valid i94port city code

The variety of data analysis can be performed by joining the fact and dimension tables on the column <code>i94port</code>

---------------------------------------------------------

### License

[Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/)



