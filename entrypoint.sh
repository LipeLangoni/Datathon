#!/bin/bash

echo "Training Model..."
python3 /app/src/train.py

echo "Starting Uvicorn..."
uvicorn main:app --host 0.0.0.0 --port 80