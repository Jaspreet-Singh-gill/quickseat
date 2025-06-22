#!/bin/bash


#only use this script to the working of entire application
#or if you can't run the Ai model then this can generate data for the web application
URL_IN="[your ip adress ]/dashboard/in"
URL_INO="[your ip adress]/dashboard/get"

for i in {195..205}
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

    sleep $(( RANDOM % 50 + 1 ))
done

echo "Done!"
