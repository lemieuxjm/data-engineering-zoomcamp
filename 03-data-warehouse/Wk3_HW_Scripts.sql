--Create an external table using the Yellow Taxi Trip Records

CREATE OR REPLACE EXTERNAL TABLE `de-camp-01.de_hw_03_dataset.yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://de-camp-03-dw/yellow_tripdata_2024-*.parquet']
);


-- Create a (regular/materialized) table in GQ using the Yellow Taxi Trip Records (not paritiioned/not clustered)

CREATE OR REPLACE TABLE `de-camp-01.de_hw_03_dataset.yellow_tripdata_nonpartitioned`
AS SELECT * FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata`;


-- Question 1. Counting Records
-- What is the count of records for the 2024 Yellow Taxi Data?

SELECT COUNT(*) FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata`;

-- Answer is: 20332093


-- Question 2. Data read estimation
-- Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
-- What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

-- Answer is: 0MB for the External Table and 0MB for the Materialized Table

SELECT DISTINCT COUNT(*) FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata`;

SELECT DISTINCT COUNT(*) FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata_nonpartitioned`;

-- Question 3. Understanding columnar storage
-- Write a query to retrieve the PULocationID from the table (not external) in BQ. Now write a query to retrieve the PULocationID
-- and DOLocationId on the same table
-- Why are byte estimate numbers different?

SELECT PULocationID FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata` ORDER BY PULocationID LIMIT 1000;

SELECT PULocationID, DOLocationID FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata` ORDER BY PULocationID  LIMIT 1000;

-- Answer is: My estimates were the same (both zero) but the 1st answer is accurate



-- Question 4. Counting zero fair trips
-- How many records have a fare_amount of 0?

SELECT * FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata` LIMIT 100; 
SELECT COUNT(fare_amount) FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata` WHERE fare_amount = 0;   --8333

-- Answer is: 8333


-- Question 5. Partitioning and Clustering
-- What is the best strategy to make an optimized table in Big Query if your query will always filter based on 
-- tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

CREATE OR REPLACE TABLE `de-camp-01.de_hw_03_dataset.yellow_tripdata_partitioned`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS (
  SELECT * FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata`
);


-- Answer is: Partition by tpep_dropoff_datetime and Partition by VendorID

-- Question 6: Partition benefits

-- Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)
-- Use the materialized table you created earlier in your from clause and note the estimated bytes. 

SELECT DISTINCT VendorID FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata_nonpartitioned` WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata_partitioned` WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. 
-- What are these values?
-- Choose the answer which most closely matches.

-- Answer is: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table


-- Question 7: External table storage
-- Where is the data stored in the External Table you created?

-- Answer is: It is stored in the GCP Buckete


-- Question 8: Clustering best practices
-- It is best practice in BigQuery to always cluster your data

-- Answer is: False


-- Question 9: Understanding table scans
-- No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

-- SELECT DISTINCT COUNT(*) FROM `de-camp-01.de_hw_03_dataset.yellow_tripdata_nonpartitioned`;
-- Answer is: zero. Great question - cached? Although I could reset the cache, so not sure
