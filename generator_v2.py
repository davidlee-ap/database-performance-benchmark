'''
Author: Ajinkya Shinde
        Chunwei Li
'''
import random
import csv
import os
from google.cloud import bigquery


global generator,prime

def convert_uniq_to_str_uniq(unique):

	print('inside convert_uniq_to_str_uniq')
	print(unique)
	result = ""

	for i in range(7):
		result+='A'

	
	tmp = ""
	while unique > 0:
		rem = unique % 26
		tmp+=chr(ord('A') + rem)
		unique = unique // 26


	t1 = tmp*len(tmp)+result[len(tmp)+1:]+'x'*45
	print('result is',t1)

	return t1



def generate_dataset(rows,fname):

	os.makedirs(os.path.dirname(fname), exist_ok=True)
	with open(fname,'w',newline='') as f:
		writer = csv.writer(f)
		writer.writerow(["unique1","unique2","two","four","ten","twenty","onePercent","tenPercent","twentyPercent","fiftyPercent","unique3","evenOnePercent","oddOnePercent","stringu1","stringu2","string4"])
		for row in rows:
			writer.writerow(row)


def insert_data_bigquery(fname):

	client = bigquery.Client(project = 'cs587db')


	# Code for creating dataset
	# dataset_id = '{}.wisconsinbenchmk'.format(client.project)
	# print(dataset_id)


	# # # Construct a full Dataset object to send to the API.
	# dataset = bigquery.Dataset(dataset_id)


	# # # TODO(developer): Specify the geographic location where the dataset should reside.
	# dataset.location = "US"

	# print(dataset.dataset_id)


	# # # Send the dataset to the API for creation.
	# # # Raises google.api_core.exceptions.Conflict if the Dataset already
	# # # exists within the project.
	# dataset = client.create_dataset(dataset)  # API request
	# print("Created dataset {}.{}".format(client.project, dataset.dataset_id))




	dataset_id = 'wisconsinbenchmk'
	table_id = 'TENKTUP'

	dataset_ref = client.dataset(dataset_id)
	table_ref = dataset_ref.table(table_id)
	job_config = bigquery.LoadJobConfig()
	job_config.source_format = bigquery.SourceFormat.CSV
	job_config.skip_leading_rows = 1
	job_config.autodetect = True

	with open(fname, "rb") as source_file:
	    job = client.load_table_from_file(
	        source_file,
	        table_ref,
	        location="US",  # Must match the destination dataset location.
	        job_config=job_config,
	    )  # API request

	job.result()  # Waits for table load to complete.

	print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))














def randValue(seed,limit):
	# Deprecated function

	print('inside randValue function')
	global generator
	global prime

	while seed > limit:
		seed = (generator * seed) % prime
	
	print('the value of seed is', seed)
	return seed



def generate_relation(tupCount):
	print('inside generate relation function')
	global generator

	seed = generator

		
	unique1 = random.sample(range(tupCount), tupCount)
	unique2 = [i for i in range(tupCount)]
	two = [each%2 for each in unique1]
	four = [each%4 for each in unique1]
	ten = [each%10 for each in unique1]
	twenty = [each%20 for each in unique1]
	onePercent = [each%100 for each in unique1]
	tenPercent = [each%10for each in unique1]
	twentyPercent = [each%5 for each in unique1]
	fiftyPercent = [each%2 for each in unique1]
	unique3 = unique1
	evenOnePercent = [(each*2) for each in onePercent] 
	oddOnePercent = [(each*2)+ 1 for each in onePercent]

	# stringu1 and stringu2 generation
	stringu1 = [convert_uniq_to_str_uniq(each) for each in unique1] 
	stringu2 = [convert_uniq_to_str_uniq(each) for each in unique2] 

	# string4 generation
	rnd_str4_len = tupCount //  4
	str4_seq = ['A'*4+'x'*45,'H'*4+'x'*45,'O'*4+'x'*45,'V'*4+'x'*45]
	rnd_str4_1 = [each for i in range(rnd_str4_len)  for each in str4_seq]
	rnd_str4_2 = rnd_str4_1[:tupCount-len(rnd_str4_1)]
	string4 = rnd_str4_1 + rnd_str4_2 

	print('unique1',unique1)
	print('unique2',unique2)
	print('two',two)
	print('four',four)
	print('ten',ten)
	print('twenty',twenty)
	print('onePercent',onePercent)
	print('onePercent',onePercent)
	print('onePercent',onePercent)
	print('onePercent',onePercent)
	print('unique3',unique3)
	print('stringu1',stringu1)
	print('stringu2',stringu2)
	print('string4',string4)

	rows = zip(unique1,unique2,two,four,ten,twenty,onePercent,tenPercent,twentyPercent,fiftyPercent,unique3,evenOnePercent,oddOnePercent,stringu1,stringu2,string4)	
	
	filename = './data/TENKTUP1.csv'

	generate_dataset(rows,filename)	
	insert_data_bigquery(filename)


def initialize():

	global generator, prime
	while (True):
		try:
			tupCount = input("Enter the required table size\n")
			tupCount = int(tupCount)
			# print('tupCount entered', tupCount)
			if tupCount <= 1000:
				generator = 279
				prime = 1009
				break
			elif (tupCount <= 10000):
				generator = 2969
				prime = 1007
				break
			elif (tupCount <= 100000):
				generator = 21395
				prime = 100003
				break
			elif (tupCount <= 1000000):
				generator = 2107
				prime = 10000
				break
			elif (tupCount <= 10000000):
				generator = 211
				prime = 10000
				break
			elif (tupCount <= 100000000):
				generator = 21
				prime = 100000
				break
			else:
				print('too many rows requested \n')
				continue	
		except ValueError:
			print('Value for table size is not entered as int')
			exit()

	print('Calling generate_relation') 
	generate_relation(tupCount)


initialize()

