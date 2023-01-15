#!/bin/sh
until cd /app/backend
do
    echo "Waiting for server volume..."
done
# run a worker :)
celery -A coingecko_wrapper worker --beat -l info
