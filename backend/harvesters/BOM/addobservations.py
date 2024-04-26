import logging, json, requests, socket
from flask import current_app
import concurrent.futures 
from elasticsearch8 import Elasticsearch
import os

def call_bom(station_name, url):


    print("URL", url)
    res = requests.get(url)
    if res.status_code == 200:
        return station_name, res.json()

    return station_name, None

def parse_json(returned_json):
    data = returned_json['observations']['data'][0]
    return data


def main():


    elastic_client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        basic_auth=('elastic', 'elastic')
    )

    
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
        future_to_result = {executor.submit(call_bom, val['_source']['station_name'], val['_source'][' url']): val for val in url_list}

        for future in concurrent.futures.as_completed(future_to_result):
            result = future_to_result[future]
            try:

                # get the data back from the test
                data = future.result()
                current_app.logger.info(f'Parsing observation: {data[1]}')               
                observation = parse_json(data[1])
                #ping_results.append(observation)
                current_app.logger.info(f'Got observation')
                current_app.logger.info(f'Pushin to elastic')
                res = elastic_client.index(
                    index='observations',
                    id=f"{observation['wmo']}-{observation['local_date_time']}",
                    body=observation

                )
                current_app.logger.info(f'Indexed observation {observation["stationid"]}-{observation["timestamp"]}')

            except Exception as e:
                print('%r generated an exception: %s' % (result, e))

    return 'ok'

if __name__ == '__main__':
    main()