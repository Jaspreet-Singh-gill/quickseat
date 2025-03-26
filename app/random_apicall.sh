#!/bin/bash

URL_IN="http://127.0.0.1:8000/dashboard/in"
URL_INO="http://127.0.0.1:8000/dashboard/get"

for i in {21..100}
do
    JSON_DATA="{\"user_id\": $i, \"in_out\": true}"
    curl -X POST "$URL_IN" \
        -H "Content-Type: application/json" \
        -d "$JSON_DATA"

    echo "Calling Dashboard IN API with: $JSON_DATA"

    k=$(( RANDOM % i + 1 ))
    STATUS=$(shuf -e true false -n 1)


    response=$(curl -s -X POST "$URL_INO" \
        -H "Content-Type: application/json" \
        -d "{\"user_id\": $k,\"in_out\": $STATUS}")


    if [[ $(echo "$response" | jq '.status') != "$STATUS" ]]; then
        JSON_DATA="{\"user_id\": $k, \"in_out\": $STATUS}"
        curl -X POST "$URL_IN" \
            -H "Content-Type: application/json" \
            -d "$JSON_DATA"

        echo "Updated user $k status to $STATUS"
    fi

    sleep $(( RANDOM % 100 + 1 ))
done

echo "Done!"
