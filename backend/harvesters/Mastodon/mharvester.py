from flask import current_app, request
#from 
from mastodon import Mastodon
import json, time
from elasticsearch8 import Elasticsearch
from elasticsearch8 import helpers

def parse_json(msgs):
    new_msgs = []
    keys = ['content', 'created_at', 'id']

    for msg in msgs:
        new_msg = {}
        for key in keys:
            if key == "created_at":
                raw_date = msg.get(key)
                if raw_date:
                    date = raw_date[0:19]
                    new_msg[key] = date
                else:
                    new_msg[key] = None
            else:
                new_msg[key] = msg.get(key)

        new_msgs.append(new_msg)
    return new_msgs


def generate_docs(msgs):
    for msg in msgs:
        msg['_index'] = 'mastodon'
        yield msg

def main():
    
    elastic_client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        basic_auth=('elastic', 'elastic')
    )

    m = Mastodon(
        api_base_url=f'https://mastodon.au'
    )


    # get latest ID
    page = elastic_client.search(
    index='mastodon',
    scroll='1m',  # Length of time to keep the scroll window open    
    body={
        "query" : {
        "match_all" : { }
        },
        "sort": [
        {
            "created_at": {
            "order": "desc"
            }
        }
        ],
        "size": 1
        }
    )
    
    doc = page['hits']['hits']
    # 
    current_app.logger.info(f' Returned Query: {doc}')               

    if len(doc)>0:
        val = doc[0]
        current_app.logger.info(f'getting ID from {val["_id"]}')
        lastid = val['_id']
    else:
        current_app.logger.info(f'pinging latest record for id')
        # Get the ID of the lastid status main the public timeline
        lastid= m.timeline(timeline='public', since_id=None, limit=1, remote=True)[0]['id']
        time.sleep(5)



   


    msg = json.loads(json.dumps(m.timeline(timeline='public', since_id=lastid, limit=100, remote=True), default=str))
    parsed_msgs = parse_json(msg)

    current_app.logger.info(f'Got {len(parsed_msgs)} messages')



    for msg in parsed_msgs:
        # helpers.bulk(elastic_client, generate_docs(parsed_msgs))
        res = elastic_client.index(
                        index='mastodon',
                        id=f"{msg['id']}",
                        body=msg
                    )
                


if __name__ == '__main__':
    main()