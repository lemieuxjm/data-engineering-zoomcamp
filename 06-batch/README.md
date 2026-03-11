## Module 6: Batch Processing 

Introduction to Spark and PySpark for data lake creation using NYC Taxi data

---
### Contents

There are two files in the 06-batch folder:
  - README.md
    - This file
  - Week6_HW.ipynb
    - The notebook file that contains Python, PySpark, and SQL code needed to explore and answer the homework questions

---

### Prerequisites

For this Module and Homework, I set up a local instance of Spark on a Windows 11 machine
  - [Spark setup on Windows](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-batch/setup/windows.md)
  - 📢 I ran into several issues during this configuration due to previous installations of Java, Python, and Jupyter Notebook
    - I enlisted assistance from Claude to resolve these configuration issues, but ultimately, these were the problems encountered
      - JAVA_HOME was not set to the correct java version
      - SPARK_HOME was set to a manually installed location rather than the pip-installed pyspark location in AppData
      - PYSPARK_PYTHON was not set to the correct python version
      - Variables were not holding persistently
  - Upon completion of these steps, I confirmed that Spark had been installed, so the 1st bullet point in Homework Question 1 was completed.
---

### Instructions

#### To view the contents of the notebook 📓
  - Clone or download [Week6_HW.ipynb](https://github.com/lemieuxjm/data-engineering-zoomcamp/blob/main/06-batch/Week6_HW.ipynb)
  - Open the notebook

#### To run the notebook 📓
  - Be sure you are running Jupyter Notebook or other IDE that is configured in alignment with your Spark/PySpark configuration
  - No additional installations should be needed

#### Notes:
  - Cell 1 in the notebook will run PySpark, completing the 2nd bullet point in Homework Question 2.
  - Cell 1 in the notebook will also create a local spark session
  - Execute spark.version was performed outside of the notebook
  - Answer to Homework Question 1
    - What is the output of executing spark.version?
    - 4.1.1
  - Notebook/code not needed to answer Question 5:
    - Homework Question 5 asks what local port is used to run Spark's application dashboard
    - Port 4040
---

### Notebook Steps, Explanation, and Homework

Cell 1: 
  - Prepare notebook for pyspark use by importing pyspark and SparkSession
  - Create the spark object

Cell 2:
  - Retrieve Yellow taxi data for November 2025 in parquet format from official NYC data site using wget
  - Output displays batches retrieved, percent complete, size of batches, and duration of batch retrieval
  - Indicates the data was saved to 'yellow_tripdata_2025-11.parquet'

Cell 3:
  - Create a dataframe from the Yellow 2025-11 data

Cell 4:
  - Display Yellow 2025-11 dataset to explore data
  - Output displays header and first 20 records of dataset

Cell 5:
  - Repartition the dataset into 4 partitions

Cell 6:
  - Write the reparitioned data to disk
  - (outside of notebook) Use Windows Explorer to visualize saved files, noting the size of the files
  - Answer to Homework Question 2
    - What is the avg. size of the Parquet files created by this cell?
    - 25MG

Cell 7:
  - Display schema of Yellow 2025-11 dataset

Cell 8:
  - Import SQL functions for use with SQL statements

Cell 9:
  - Identify 2 timestamp columns
  - Create 2 new columns
  - Populate the new columns with data from timestamp columns reformatted into date-only format
  - Create new expanded Yellow taxi dataset with new columns plus existing data

Cell 10:
  - Display expanded Yellow taxi dataset to explore results
  - Output displays header and first 20 records of dataset

Cell 11:
  - Create a temp table from the expanded Yellow taxi dataset

Cell 12:
  - Explore first 10 records of the temp table using SQL
```sql
      SELECT * FROM yellow_nov_data LIMIT 10;
```
  - Output displays header and first 10 records of dataset

Cell 13:
  - Runs SQL query to answer Homework Question 3
```sql
      SELECT COUNT(*)
      FROM yellow_nov_data 
      WHERE pickup_date = '2025-11-15';
```
  - Display the results of the SQL query 
  - Answer to Homework Question 3
    - How many taxi trips were started on November 15th?
    - 162604

Cell 14: 
  - Runs SQL query to answer Homework Question 4
```sql
      SELECT 
          MAX(timestampdiff(SECOND, tpep_pickup_datetime, tpep_dropoff_datetime)) / 3600 AS longest_trip_hour
      FROM yellow_nov_data;
```
  - Display the results of the SQL query 
  - Answer to Homework Question 4
    - What is the length of the longest trip (in hours) in the dataset
    - 90.65

Cell 15:
  - Retrieve zone lookup data from official NYC data site using wget
  - Output displays batch retrieved, percent complete, size of batch, and duration of batch retrieval
  - Indicates the data was saved to 'taxi_zone_lookup.csv'

Cell 16:
  - Create a dataframe from the taxi zone lookup data

Cell 17:
  - Display zone lookup dataset to explore data
  - Output displays header and first 20 records of dataset

Cell 18:
  - Create a temp view from the zone lookup data set

Cell 19: 
  - Runs SQL query to answer Homework Question 6
```sql
      SELECT 
          y.PULocationID,
          z.Zone,
          COUNT(*) AS frequency
      FROM yellow_nov_data AS y
      JOIN zones AS z ON z.LocationID = y.PULocationID
      GROUP BY y.PULocationID,z.Zone
      ORDER BY frequency ASC;
```
  - Display the results of the SQL query 
  - Answer to Homework Question 6
    - What is the name of the pickup location zone with the fewest records?
    - (there were three possible answers, 1 chosen) Arden Heights











