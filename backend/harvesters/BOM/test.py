import logging, json, requests, socket
import concurrent.futures
import pandas as pd

def call_bom(station_name, url):
    #url ='http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json'
    print("URL", url)
    res = requests.get(url)
    if res.status_code == 200:
        return station_name, res.json()

    return station_name, None

def parse_json(returned_json):
    data = returned_json['observations']['data'][0]
    return data

def main():
    #current_app.logger.info(f'Harvested one weather observation')
    with open("/root/backend/harvesters/BOM/mapper.txt", "r") as file:

        lines = file.readlines()
    
    url_list = []

    for line in lines[1:]:
        val = line.strip("\n").split(", ")
        station_name = val[0]
        url = val[1]

        url_list.append((station_name, url))
        #break
    ping_results = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:


        # depending on testing function specified in metadata file, run the specfied function for the correspondning test 
        future_to_result = {executor.submit(call_bom, val[0], val[1]): val for val in url_list}

        for future in concurrent.futures.as_completed(future_to_result):
            result = future_to_result[future]
            try:
                # get the data back from the test
                data = future.result()
               
                parsed_result = parse_json(data[1])
                ping_results.append(parsed_result)
                
            except Exception as e:
                print('%r generated an exception: %s' % (result, e))

    df = pd.DataFrame(ping_results)
    df.to_csv("test.csv")
    print(df)

    
    #return json.dumps(requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json').json())



#
#http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_display_type=dailyZippedDataFile&p_stn_num=029085&p_c=-169205910&p_nccObsCode=136&p_startYear=1976




if __name__ == '__main__':
    main()