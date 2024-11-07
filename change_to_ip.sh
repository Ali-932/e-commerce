#!/bin/bash

# Get the current IP address
CURRENT_IP=$(hostname -I | awk '{print $1}')

# Define the path to your .env file
ENV_FILE=".env"  # Change this if your file is named differently

# Check if the .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found!"
    exit 1
fi

# Update the DB_HOST value in the .env file
sed -i.bak "s/^DB_HOST=.*/DB_HOST=$CURRENT_IP/" "$ENV_FILE"

# Optional: Print the updated .env file
echo "Updated DB_HOST to $CURRENT_IP in $ENV_FILE"