Module 6: Batch Processing

Goal: Introduction to Spark and PySpark for data lake creation using NYC Taxi data

- Prerequisites

- For this Module and Homework, I set up a local instance of Spark on a Windows 11 machine
  - [Spark setup on Windows](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-batch/setup/windows.md)
  - I ran into several issues during this configuration due to previous installations of Java, Python, and Jupyter Notebook
    - I enlisted assistance from Claude to resolve these configuration issues, but ultimately, these were the problems encountered
      - JAVA_HOME was not set to the correct java version
      - SPARK_HOME was set to a manually installed location rather than the pip-installed pyspark location in AppData
      - PYSPARK_PYTHON was not set to the correct python version
      - Variables were not holding persistently

- To view the contents of the notebook
  - Clone or download [Week6_HW.ipynb](https://github.com/lemieuxjm/data-engineering-zoomcamp/blob/main/06-batch/Week6_HW.ipynb)
  - Open the notebook

   
- To run the notebook
  - Be sure you are running Jupyter Notebook or other IDE that is configured in alignment with your Spark/PySpark configuration
  - No additional installations should be needed


