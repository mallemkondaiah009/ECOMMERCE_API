#!/bin/bash
# Exit on error
set -o errexit

# Step 1: Install Dependencies
pip install -r requirements.txt

# Step 2: Collect Static Files
python manage.py collectstatic --no-input

# Step 3: Apply Database Migrations
python manage.py migrate

# Step 4: Start the Server (Optional)

exec gunicorn ecom_api.asgi:application \
    --name ecom_api \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-4} \
    --worker-class uvicorn.workers.UvicornWorker \
    --log-level=${GUNICORN_LOG_LEVEL:-info} \
    --access-logfile - \
    --error-logfile - \
    --max-requests 10000 \
    --max-requests-jitter 500 \
    --timeout 120 \
    --keep-alive 5