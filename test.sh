#!/bin/bash

read -p "Enter the port your server is running on (e.g. 8080): " PORT

PORT=${PORT:-8080}
HOST="http://127.0.0.1:$PORT"

echo -e "\nRunning tests against $HOST...\n"

echo "=== 1. Testing GET / ==="
curl -i "$HOST/"
echo -e "\n----------------------------------------\n"

echo "=== 2. Testing GET /api/status with Query Params ==="
curl -i "$HOST/api/status?user=fedi&role=admin"
echo -e "\n----------------------------------------\n"

echo "=== 3. Testing POST /api/echo with Valid JSON ==="
curl -i -X POST "$HOST/api/echo" \
	-H "Content-Type: application/json" \
	-d '{"app": "AsyncServer", "language": "Python"}'
echo -e "\n----------------------------------------\n"

echo "=== 4. Testing 404 Not Found ==="
curl -i "$HOST/unknown-endpoint"
echo -e "\n----------------------------------------\n"

echo "=== 5. Testing 400 Bad Request (Malformed JSON) ==="
curl -i -X POST "$HOST/api/echo" \
	-H "Content-Type: application/json" \
	-d '{"bad": broken_json}'
echo -e "\n"
