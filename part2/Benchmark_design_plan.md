<h1 align="center">Benchmarking Design</h1><br>
<h2 align="center">CS 587 Database Implementation - Project Part II</h2><br>
<p align="center">
<b>Chunwei Li</b><br>
<b>Ajinkya Shinde</b><br>
</p>



### 1. Choice of System

We choose option 2 and evaluate a single system - Postgres to do benchmark because Postgres system provides users with more options and interfaces to adjust system performance. It will better help understand what & how parameters impact on database performances. Originally we chose BigQuery in part 1, but we found BigQuery doesn’t provide enough documents about how to change system parameters to adjust system performance, so we decide to switch to Postgres in order to better focus on database performance and understand implementation of database systems.

### 2. System research on PostGreSQL parameters :

`work_mem (integer)`

It specifies the amount of memory to be used by internal sort operations and hash tables before writing to temporary disk files. The value defaults to four megabytes (4MB). Note that for a complex query, several sort or hash operations might be running in parallel; each operation will be allowed to use as much memory as this value specifies before it starts to write data into temporary files. Also, several running sessions could be doing such operations concurrently. Therefore, the total memory used could be many times the value of work_mem; it is necessary to keep this fact in mind when choosing the value. Sort operations are used for ORDER BY, DISTINCT, and merge joins. Hash tables are used in hash joins, hash-based aggregation, and hash-based processing of IN subqueries. 

`effective_cache_size`

effective_cache_size should be set to an estimate of how much memory is available for disk caching by the operating system and within the database itself, after taking into account what's used by the OS itself and other applications. This is a guideline for how much memory you expect to be available in the OS and PostgreSQL buffer caches, not an allocation! This value is used only by the PostgreSQL query planner to figure out whether plans it's considering would be expected to fit in RAM or not. If it's set too low, indexes may not be used for executing queries the way you'd expect. The setting for shared_buffers is not taken into account here--only the effective_cache_size value is, so it should include memory dedicated to the database too. Setting effective_cache_size to 1/2 of total memory would be a normal conservative setting, and 3/4 of memory is a more aggressive but still reasonable amount. You might find a better estimate by looking at your operating system's statistics. On UNIX-like systems, add the free+cached numbers from free or top to get an estimate. On Windows see the "System Cache" size in the Windows Task Manager's Performance tab. Changing this setting does not require restarting the database (HUP is enough).

`temp_buffers (integer)`

Sets the maximum number of temporary buffers used by each database session. These are session-local buffers used only for access to temporary tables. The default is eight megabytes (8MB). The setting can be changed within individual sessions, but only before the first use of temporary tables within the session; subsequent attempts to change the value will have no effect on that session.
A session will allocate temporary buffers as needed up to the limit given by temp_buffers. The cost of setting a large value in sessions that do not actually need many temporary buffers is only a buffer descriptor, or about 64 bytes, per increment in temp_buffers. However if a buffer is actually used an additional 8192 bytes will be consumed for it (or in general, BLCKSZ bytes).

`seq_page_cost (floating point)`

Sets the planner's estimate of the cost of a disk page fetch that is part of a series of sequential fetches. The default is 1.0. 

`enable_hashjoin (boolean)`

Enables or disables the query planner's use of hash-join plan types. The default is on.

### 3. Performance experiment design

#### Experiment 1: Test the 10% rule of thumb

This experiment is one of examples in project specification. We chose it because index is important feature of database system.

* Experiment specifications

1. This test explores when it is good to use an unclustered index vs. not using an index vs. using a clustered index

2. Use a 100,000 tuple relation (scaled up version of TENKTUP2)

3. Use Wisconsin Bench queries 2, 4 and 6. Run queries 2, 4, and 6 on the same dataset. Query 2 should be run without an index on unique2, Query 4 should be run with a clustered index on unique2, Query 6 requires an unclustered index on unique1.

4. No parameters changed in this test.

5. Metric is elapsed time and used memory.

6. Expect using a cluster index has the best performance, an unclustered index has second best performance, and not using an index has the worst performance.

#### Experiment 2: Aggregate performance

* Experiment specifications

1. This test explores what parameters improve aggregate performance.

2. Use a 100,000 tuple relation (scaled up version of TENKTUP2).

3. Use Wisconsin Bench queries 20 and 23. Run queries 20 and 23 on the same dataset. 

4. Run queries with different  parameters - temp_buffer size and seq_page_cost.

5. Metric is elapsed time and used memory.

6. Expect different parameters have different results. Experiment will decide what parameters give the best performance.

#### Experiment 3: Vary the hash table size for hash join 

In this experiment, we check the hash join operation performance when the hash table size is varied. 

* Experiment Specifications:

1. In this experiment, we will be changing the work_mem parameter to check the performance of hash join operation when the hash table is varied.

2. We will be using TENKTUP1 and TENKTUP2 relations as these are comparatively large datasets across which the parameter can be checked.

3. The queries to be evaluated will be specifically JOIN queries, sub-queries.

4. We will be evaluating the performance(check the work_mem parameter) based on 2 criteria’s -

     * Varying the selectivity factor(10% , 50% and 100 %) – In this , we will check if the size of the relations to be joined matter with respect to the work_mem parameter or not. 

     * Changing the joining condition based on the type of index – In this, keeping the query and selectivity factor the same, we will be selecting the joining predicates based on type of indexes(no index, clustered and non-clustered index), we will check the performance of the query overall.

5. We expect to get the best performance for query with relations hash table not spilling out i.e. the hash table does not fill out quickly and causing the number of series of batches for hash table creation to increase. 





#### Experiment 4: Effect of buffer cache size and join algorithm selection on the query plan

In this experiment, we check the query performance when the cache size PostGreSQL shared buffer cache is varied along with controlling for the join algorithm selection.

* Experiment Specifications:

1. In this experiment, we will check the query plan selected by the optimizer based on the change in cache size of shared buffer pool /cache of PostGreSQL  along with enabling/disabling the enable_hashjoin parameter.

2. We will be using TENKTUP1 and TENKTUP2 relations as these are comparatively large datasets across which the parameter can be checked.

3. The queries to be evaluated will be JOIN, INSERT queries on relations mentioned in ii.).

4. We will be evaluating the performance(change the effective_cache_size parameter) based on below criteria.

5. Varying the selectivity factor(10% , 50% and 100 %) – In this , we will check if the size of the relations to be joined matter or not. 

6. We expect to get the best performance for query with relations if the shared buffer cache can fit all the pages of the relations. However, if the shared buffer cache is too low in  size , to bring the next page in the buffer cache  a page replacement algorithm will kick in. Also, queries where we can avoid swap pagein activity is preferable viz. swapping the page out and bringing it inside into main memory.

#### 4. Lessons learned

Before implementing benchmark, even though we are proposing the experiments and their corresponding expected results, we suspect they may/may not abide to the argument stated.
For instance,if we disable the enable_hashjoin parameter, we expect the query plan to be index nested loop join but we will really have to check if this join algorithm is actually used while running the experiment or another join algorithm - Sort Merge Join is used instead.
