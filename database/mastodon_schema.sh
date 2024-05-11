curl -XPUT -k 'https://127.0.0.1:9200/mastodon' \
   --user 'elastic:elastic' \
   --header 'Content-Type: application/json' \
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 10,
            "number_of_replicas": 3
        }
    },
    "mappings": {

        "properties": {
            "id": {
                "type": "text"
            },
            "content": {
                "type": "text"
            },
            "created_at": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            }
        }
    }
}'  | jq '.'
