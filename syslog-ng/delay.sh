#!/bin/bash

# Wait for MySQL to be ready
until mysql -h db -u root -ppassword --skip-ssl -e "SELECT 1"; do
  echo "Waiting for MySQL..."
  sleep 5
done

# Run the SQL script to create the table if it doesn't exist
mysql -h db -u root -ppassword --skip-ssl logging_system < /etc/dev/create_log.sql


sleep 10
