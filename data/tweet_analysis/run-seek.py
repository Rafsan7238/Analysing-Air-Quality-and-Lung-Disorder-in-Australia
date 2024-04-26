#!/usr/bin/env python


'''
    FOR COMP90024 ASSIGNMENT 2
    BY TEAM 45: 
        William Chen 1400081
        Petr Andreev 1375858
        Rafsan Al Mamun 1407776
        Xinran Li 1549584
        Ojaswi Dheer 1447227

    Repurposed from Assignment 1
    Instead of finding max tweet counts and sentiments, 
    find total sentiments and tweet counts per date and save as csv.
    Do not default sentiments, only consider tweets with valid sentiment values.
'''

from mpi4py import MPI
import sys
from datetime import datetime
import time
import json

start_time = time.time()

#region enum support

def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    copied from example files
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# Define MPI message tags
tags = enum('READY', 'CONSUME', 'DONE')
#endregion

#region Initializations and preliminaries

comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.size        # total number of processes
rank = comm.rank        # rank of this process
status = MPI.Status()   # get MPI status object

target_file = sys.argv[1]
environment_description = sys.argv[2]
chunk_size = 200

failed_sentiment_loads = 0
failed_datetime_loads = 0
daily_dict = dict()
curr_tweet_index = 0
#endregion

#region Task Consumption 

def try_get_sentiment(string):
    try:
        return float(string)
    except:
        return None
    
def try_get_created_at(string):
    try:
        return datetime.strptime(string ,"%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        return None

def add_tweet_to_sums(tweet):
    '''Takes in a tweet of form {date, sentiment} and adds to the process's summations'''
    global daily_dict
    
    curr_sentiment, curr_count = daily_dict.get(tweet['date'], (0, 0))
    daily_dict[tweet['date']] = (curr_sentiment + tweet['sentiment'], curr_count + 1)


def next_tweet_from_file(data_file):
    '''
    Takes in a data file. Assumes that the file reader has been 
    navigated to the next line to read.
    
    Throws if datetime fails to parse.
    Returns None if the next line does not have a valid sentiment value.
    Otherwise, returns an object with the line's date and sentiment value.
    '''
    line = next(data_file)
    line = line.strip()[:-1] # Remove trailing comma

    json_object = json.loads(line)

    created_at = None
    sentiment = None
    global failed_sentiment_loads
    data = json_object['doc']['data']
    try:
        created_at =  datetime.strptime(data['created_at'] ,"%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        # This should never occur.
        raise Exception(f'Process {rank} failed to load tweet datetime')

    try:
        sentiment = float(data['sentiment'])
    except: 
        # Unlike assignment 1, we don't want to default sentiments to 0 since we will likely want to work with averages
        failed_sentiment_loads += 1
        return None
    
    date = created_at.date()

    return {'date': date, 'sentiment': sentiment}

def consume_task(chunk_offset, data_file):
    '''
    Takes in a task, IE a chunk byte offset, and a file read instance of the target file.
    Points the reader to the byte offset such that the reader is pointing to the start of the intended chunk.
    Processes a chunk's worth of lines then finishes.
    '''
    data_file.seek(chunk_offset)

    for _ in range(chunk_size):
        try:
            tweet = next_tweet_from_file(data_file)
            if tweet is None:
                # Something went wrong but was handled already to return None
                print('Failed to load tweet', flush=True)
                continue

            add_tweet_to_sums(tweet)
        except StopIteration as e:
            print(f'Process {rank} hit file end', flush = True)
            break
        except json.JSONDecodeError as e:
            # Expected for first and last rows in the original document.
            # First row is preamble junk.
            # Last row is an empty tweet for some reason.
            print(f'Process {rank} failed to parse line.', flush=True)
            continue

#endregion

class offset_chunker():
    '''
    Opens its own reader instance.
    curr_offset represents the current byte access point of the reader instance.
    move_forward progresses this pointer to the start of the next chunk.
    '''
    def __init__(self) -> None:
        self.chunker_data_file = open(target_file, "rb")
        self.done = False
        self.curr_offset = 0

    def move_forward(self):
        if not self.done:
            for _ in range(chunk_size):
                line = next(self.chunker_data_file, None)
                if line is None:
                    self.done = True
                    self.chunker_data_file.close()
                    break
                self.curr_offset += len(line)

def do_master_actions():
    '''
    Generatess the byte offsets corresponding to the starts of each data chunk.
    Sends these offsets to workers when found (and processes some itself).
    Collects results from all workers when done.
    '''
    print('Master starting.', flush=True)
    workers = list(range(1, size))

    print(f'Master beginning chunking', flush=True)
    chunker = offset_chunker()
    
    while not chunker.done:
        for _ in range(len(workers)): # start with workers, end with master
            comm.recv(source=MPI.ANY_SOURCE, tag=tags.READY, status=status)
            source = status.Get_source()
            
            comm.send(chunker.curr_offset, dest=source, tag=tags.CONSUME) # This blocks until the worker is ready to receive
            chunker.move_forward()
            if chunker.done:
                break

        with open(target_file, "rb") as master_processing_data_file: # obtain separate file pointer for processing
            consume_task(chunker.curr_offset, master_processing_data_file)

        chunker.move_forward()
        if chunker.done:
            break

    print(f'All chunks sent')

    print('Master done chunking.', flush=True)

    for worker in workers:
        comm.recv(source=worker, tag=tags.READY)
        comm.send(None, dest=worker, tag=tags.DONE)
            
    # All chunks have been sent and master itself is done
    print('Collecting Summations', flush=True)
    global daily_dict
    global failed_sentiment_loads
    global failed_datetime_loads
    for worker in workers:
        # Collect results, add to master summation
        worker_daily_summation, worker_sentiment_fails = comm.recv(source=worker, tag=tags.DONE)
        print(f'Received from worker {worker}.')
        failed_sentiment_loads += worker_sentiment_fails

        for date, sums in worker_daily_summation.items():
            add_sentiment, add_count = sums
            curr_sentiment, curr_count = daily_dict.get(date, (0, 0))
            daily_dict[date] = (curr_sentiment + add_sentiment, curr_count + add_count)

        print(f'Collected from worker {worker}', flush=True)
    print('Processing complete.', flush=True)

def do_worker_actions(): 
    '''
        Continually requests next task from master.
        Processes each task when received. 
        If master says it is done, send the worker's summation back to master for collection.
    '''
    print(f'Worker No.{rank} starting', flush=True)   
    with open(target_file, 'rb') as data_file:
        while True:
            comm.send(None, dest=0, tag=tags.READY)

            chunk_offest = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()
            
            if tag == tags.CONSUME:
                # Do the work here
                consume_task(chunk_offest, data_file)     
            elif tag == tags.DONE:
                print(f'Worker No.{rank} sending to master.', flush=True)   
                comm.send((daily_dict, failed_sentiment_loads), dest=0, tag=tags.DONE)
                break

    end_time = time.time()
    print(f'Worker No.{rank} done after {end_time - start_time} seconds.')

if rank == 0:
    do_master_actions()
else:
    do_worker_actions()

if(rank == 0):
    '''
        Master prints diagnostic lines.
        Saves the final collected dictionary to a json file output.
        This json file can be read by a fission function and ingested into elastic.
    '''
    # Let the master print and save the output
    print(f'###  ENV: {environment_description} ###', flush=True) # Node and Core description

    dict_as_json = {
    "name": "historic_tweet_sentiments",
    "entries": [{
        "year": key.year,
        "month": key.month,
        "day": key.day,
        "total_sentiment": value[0],
        "total_tweets": value[1]
        } for key, value in daily_dict.items()]
    }

    with open('historic_tweet_sentiments.json', 'w') as out_file:
        json.dump(dict_as_json, out_file, sort_keys = True )

    print(f'{failed_sentiment_loads} tweets had non-float or unexpected sentiment formats', flush=True)
    print(f'{failed_datetime_loads} tweets had unexpected datetime formats', flush=True)

    end_time = time.time()
    print(f'Processing for {target_file} ran in {end_time - start_time} seconds', flush=True) # Time required
    print(f'######', flush=True)
