#!/usr/bin/python3
#Project: database performance benchmark
#
#Author: Chunwei Li
         Ajinkya Shinde
    
#Date  : 4-14-2019
#
from google.cloud import bigquery
import os
import sys
import random

def insertuple(tuples):
    """insert tuples into table on google cloud BigQuery dataset
    """
    client = bigquery.Client()
    query = """INSERT INTO `database-performance-benchmark.wisconsinbenchmark.TENKTUP2`  
                                (unique1, unique2, two, four, ten, twenty, onePercent, tenPercent, 
                                 twentyPercent, fiftyPercent, unique3, evenOnePercent, oddOnePercent,
                                 stringu1, stringu2, string4) 
                                VALUES
                                (@unique1, @unique2, @two, @four, @ten, @twenty, @onePercent, @tenPercent, 
                                 @twentyPercent, @fiftyPercent, @unique3, @evenOnePercent, @oddOnePercent,
                                 @stringu1, @stringu2, @string4) 
                             """
    for tup in tuples:
        query_params = [
            bigquery.ScalarQueryParameter("unique1", "INTEGER", tup[0]),
            bigquery.ScalarQueryParameter("unique2", "INTEGER", tup[1]),
            bigquery.ScalarQueryParameter("two", "INTEGER", tup[2]),
            bigquery.ScalarQueryParameter("four", "INTEGER", tup[3]),
            bigquery.ScalarQueryParameter("ten", "INTEGER", tup[4]),
            bigquery.ScalarQueryParameter("twenty", "INTEGER", tup[5]),
            bigquery.ScalarQueryParameter("onePercent", "INTEGER", tup[6]),
            bigquery.ScalarQueryParameter("tenPercent", "INTEGER", tup[7]),
            bigquery.ScalarQueryParameter("twentyPercent", "INTEGER", tup[8]),
            bigquery.ScalarQueryParameter("fiftyPercent", "INTEGER", tup[9]),
            bigquery.ScalarQueryParameter("unique3", "INTEGER", tup[10]),
            bigquery.ScalarQueryParameter("evenOnePercent", "INTEGER", tup[11]),
            bigquery.ScalarQueryParameter("oddOnePercent", "INTEGER", tup[12]),
            bigquery.ScalarQueryParameter("stringu1", "STRING", tup[13]),
            bigquery.ScalarQueryParameter("stringu2", "STRING", tup[14]),
            bigquery.ScalarQueryParameter("string4", "STRING", tup[15]),
        ]
        job_config = bigquery.QueryJobConfig()
        job_config.query_parameters = query_params
        query_job = client.query( query, location="US", job_config=job_config,)
        try:
            results = query_job.result()
            print(results)
        except:
            print("Exception")

def retrievetuples():
    """Retrieve data from table on Google Cloud BigQuery dataset
    """
    client = bigquery.Client()
    query_job = client.query("""SELECT * FROM `database-performance-benchmark.wisconsinbenchmark.TENKTUP2`""")
    results = query_job.result()
    for row in results:
        print("{} : {} ".format(row.unique1, row.unique2))

def generatetuple(numOfTuple):
    """Generate tuples according to wisconsin benchmark
    """
    unique1       = random.sample(range(numOfTuple), numOfTuple)
    unique2       = range(numOfTuple)
    two           = [ x % 2 for x in unique1 ]
    four          = [ x % 4 for x in unique1 ]
    ten           = [ x % 10 for x in unique1 ]
    twenty        = [ x % 20 for x in unique1 ]
    onePercent    = [ x % 100 for x in unique1 ]
    tenPercent    = [ x % 10 for x in unique1 ]
    twentyPercent = [ x % 5 for x in unique1 ]
    fiftyPercent  = [ x % 2 for x in unique1 ]
    unique3       = unique1
    evenOnePercent = [ x * 2 for x in onePercent ]
    oddOnePercent  = [ x + 1 for x in evenOnePercent ]
    stringu1 = [ convertstring(x) for x in unique1 ]
    stringu2 = [ convertstring(x) for x in unique2 ]
    string4 = generatestring4(numOfTuple)
    
    tuples = zip(unique1, unique2, two, four, ten, twenty,  \
                 onePercent, tenPercent, twentyPercent, \
                 fiftyPercent, unique3, evenOnePercent, \
                 oddOnePercent, stringu1, stringu2, string4)
    
    generatedatafile(tuples, 'data/TENKTUP2.csv')
    #insertuple(tuples)

def generatedatafile(tuples, fname):
    """Generate data file according to wisconsin benchmark
    """
    with open(fname, '+w') as f:
        f.write("unique1,unique2,two,four,ten,twenty,onePercent,tenPercent," + 
                "twentyPercent,fiftyPercent,unique3,evenOnePercent,oddOnePercent," +
                "stringu1,stringu2,string4\n")
        for tup in tuples: 
            data = ''
            for elm in tup:
                data += str(elm) + ','
            f.write(data[:-1] + '\n')

def convertstring(unique):
    """generate stringu1 and stringu2
    """
    tmp    = ''
    while unique > 0:
        rem = unique % 26
        tmp += chr(ord('A') + rem)
        unique = unique // 26
    result = tmp + 'A'*(7 - len(tmp)) + 'x'*45
    return result

def generatestring4(numOfTuple):
    """generate string4
    """
    component = ['AAAA'+'x'*48, 'HHHH'+'x'*48, 'OOOO'+'x'*48, 'VVVV'+'x'*48] 
    string41 = component * (numOfTuple // 4)
    string42 = component[:(numOfTuple % 4)]
    return string41 + string42 

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 generator.py ['r'|'g' [[number of tuples]]")
        print("       r - retrieve data")
        print("       g - generate data")
        exit()

    if sys.argv[1] == 'r' and len(sys.argv) == 2:
        retrievetuples()

    if sys.argv[1] == 'g' and len(sys.argv) == 3:
        try:
            numOfTuple = int(sys.argv[2])
        except:
            print('Wrong number')

        generatetuple(numOfTuple)
