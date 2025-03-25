#!/bin/bash

URL_IN="http://127.0.0.1:8000/dashboard/in"

for i in {1..20}
do
    STATUS=$(shuf -e true false -n 1)
    JSON_DATA="{\"in_out\": $STATUS}"
    
    echo "Calling Dashboard IN API with: $JSON_DATA"
    
    curl -X POST "$URL_IN" \
        -H "Content-Type: application/json" \
        -d "$JSON_DATA"
    
    sleep 1
done

echo "Done!"