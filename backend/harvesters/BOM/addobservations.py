import logging, json, requests, socket
from flask import current_app
import concurrent.futures 
from elasticsearch8 import Elasticsearch
import os




def main():


    elastic_client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        basic_auth=('elastic', 'elastic')
    )


    current_app.logger.info(f'Connected To elastic')
    current_app.logger.info(os.listdir())
    print("DIR", os.listdir())
    with open("./mapper.txt", "r") as file:

        lines = file.readlines()
    
    url_list = []
    current_app.logger.info(f'Read files: {len(lines)}')

    for line in lines[1:]:
        val = line.strip("\n").split(", ")
        station_name = val[0]
        url = val[1]

        url_list.append((station_name, url))
        #break
    #ping_results = []
    current_app.logger.info(f'Starting Threading')

    
    with concurrent.futures.ThreadPoolExecutor() as executor:


        # depending on testing function specified in metadata file, run the specfied function for the correspondning test 
        future_to_result = {executor.submit(call_bom, val[0], val[1]): val for val in url_list}

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