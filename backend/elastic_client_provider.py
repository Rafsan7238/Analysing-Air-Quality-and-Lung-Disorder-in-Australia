from elasticsearch8 import Elasticsearch, helpers

def get_client():
    return Elasticsearch (
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs= False,
            basic_auth=('elastic', 'elastic'),
            request_timeout=30)

def get_bulker():
    return helpers