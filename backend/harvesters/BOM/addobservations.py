import requests
from flask import current_app
import concurrent.futures 
from elasticsearch8 import Elasticsearch

def call_bom(station_name, url):
    print("URL", url)
    res = requests.get(url)
    if res.status_code == 200:
        return station_name, res.json()

    return station_name, None

def parse_json(data_entry):
    insert = {}

    aif_time = data_entry['aifstime_utc']
    year = aif_time[2:4]
    month = aif_time[4:6]
    day = aif_time[6:8]

    insert['date'] = f'{day}/{month}/{year}'
    insert['aifstime_utc'] = data_entry['aifstime_utc']
    insert['air_temp'] = data_entry['air_temp']
    insert['name'] = data_entry['name']
    insert['rain_trace'] = data_entry['rain_trace']

    return insert

def insert_as_document(es, data_entry):
    try:
        observation = parse_json(data_entry)
        #ping_results.append(observation)
        current_app.logger.info(f'Got observation: {observation}')
        id = f"{observation['aifstime_utc']}-{observation['name']}"
        current_app.logger.info(f'Pushin to elastic with id {id}')
        res = es.index(
            index='bom_observations',
            id=id,
            body=observation

        )
        current_app.logger.info(f'Indexed observation {id}')
        print(f'Indexed observation {id}')
    except Exception as e:
        print('data entry %r generated an exception: %s' % (data_entry, e))

def ingest(most_recent_only = True):

    print('Function invoked')
    elastic_client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        basic_auth=('elastic', 'elastic'),
        request_timeout=30
    )

    print('getting stations')
    # Initialize the scroll
    page = elastic_client.search(
    index='stations',

    scroll='1m',  # Length of time to keep the scroll window open    
    body={
        "size": 1000,
        "query": {"match_all": {}}}
    )

    url_list = page['hits']['hits']

    print(url_list)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:


        # depending on testing function specified in metadata file, run the specfied function for the correspondning test 
        future_to_result = {executor.submit(call_bom, val['_source']['station_name'], val['_source']['url']): val for val in url_list}

        for future in concurrent.futures.as_completed(future_to_result):
            result = future_to_result[future]
            try:

                # get the data back from the test
                data = future.result()[1]
                if data is None:
                    raise Exception('Error fetching data')
                else:
                    data = data['observations']['data']
                current_app.logger.info(f'Parsing observation')  
             
                if most_recent_only:
                    most_recent_entry = data[0]
                    insert_as_document(elastic_client, most_recent_entry)
                else:
                    for data_entry in data:
                        insert_as_document(elastic_client, data_entry)

                print(f'Indexing done.')
            except Exception as e:
                print('%r generated an exception: %s' % (result, e))

    return 'ok'

def catch_up_history():
    return ingest(most_recent_only = False)

def main():
    return ingest()


if __name__ == '__main__':
    main()