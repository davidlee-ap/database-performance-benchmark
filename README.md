<h1 align="center">Database Performance Benchmark</h1><br>
<h2 align="center">CS587 Project Part 1</h1><br>
<p align="center">
<b>Chunwei Li</b><br>
<b>Ajinkya Shinde</b><br>
</p>

 ### 1. Description


The work for part 1 consists of four parts. The first part is to configure BigQuery dataset on Google Cloud; The second part is to write code to generate data; The third part is to generate sample data; The fourth part is to load sample data into database system.


In order to benchmark database system, we need set up and configure a database system. We choose Google Cloud BigQuery for our project. The work includes creating dataset named database-performance-benchmark, creating a table named TENKTUP2 and all fields described in the project document. Here is a screenshot demonstrating we set up the system.



<p align="center">
  <img src=/Screenshots/SC1.jpg>
</p>


We wrote python script to generate data according to the definition in the project document. The code includes function of calculating each field of the table, writing each tuple into a csv data file, inserting a tuple into the dataset and loading data file into the dataset.

According to the requirement for the project, we generated a data file containing 100 tuples. Then we loaded the data file into the dataset on Google Cloud BigQuery system by two means. One is to insert each tuple into the table while generating a tuple, however, this method didn’t work correctly because of permission of BigQuery of Google Cloud. The other method is to load data file into dataset directly by uploading data file to the system or run Bigquery API to load the data file into the system.


### 2. System choice

We chose Google Cloud BigQuery system to do this project. There are two reasons why we chose it. The first reason is that it is more convenient for test than a locally installed system because we can have access to it at anywhere. However, a locally installed system might not be allowed to be accessed from external networks. The second reason is that BigQuery is relatively new database system for us. We have interest in performance of a system residing in Cloud.

### 3. Loaded data to the system

We loaded csv data file into BigQuery system. Here is a screenshot demonstrating our work.

<p align="center">
  <img src=/Screenshots/SC2.jpg>
</p>



### 4.  Lessons and Issues

We learned how to setup and configure BigQuery of Google Cloud, how to use BigQuery API to access and operate on dataset of BigQuery, how to retrieve data, insert data and update data from BigQuery dataset.

We encountered two issues about BigQuery. One is that we failed to insert all tuples into table because of quota and permission issue according to response code 403 from Google Cloud which is not allowed to insert data as fast as you want. The other is that loaded tuples are garbled, so we have to sort by field unique2 when retrieving data.



