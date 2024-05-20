import requests
import pandas as pd

fission_url = 'http://localhost:9090'
def get_from_url_extension(url_extension, is_data=True):
    url = f'{fission_url}{url_extension}'
    print(f"Fetching from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        # Parse JSON response
        res_json = response.json()
        return res_json['data'] if is_data else res_json
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        return None

def dataframe_from_query(query):
    url = f'{fission_url}/sql/query'
    print(f"Fetching from {url}")
    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
        # Parse JSON response
        res_json = response.json()['result']
        return pd.DataFrame(res_json['rows'], columns=res_json['columns'])
    else:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}. Content: {response.content}")
    
def dataframe_from_url_ext(ext):
    url = f'{fission_url}{ext}'
    print(f"Fetching from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        # Parse JSON response
        res_json = response.json()['result']
        return pd.DataFrame(res_json['rows'], columns=res_json['columns'])
    else:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}. Content: {response.content}")