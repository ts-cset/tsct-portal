#!/bin/sh

# Create Application Database and User
# ---
# This script will use the `psql` command to run SQL commands that
# will create the needed database and user for this application.
# A running PostgreSQL server is necessary.
#
# NOTE: You only need to run this script once.
#
# Run with the following command in the project's root directory:
# $ sh bin/create-db.sh

DEV=true

if [ "$1" == "test" ]; then
  DEV=false
fi


# create user for the application
psql postgres -c 'CREATE USER portal_user;'

# create development database and grant access to application user
if [ $DEV == true ]; then
  psql postgres -c 'CREATE DATABASE portal;'
  psql postgres -c 'GRANT ALL PRIVILEGES ON DATABASE "portal" to portal_user;'
fi

# create test database and grant access to application user
psql postgres -c 'CREATE DATABASE portal_test;'
psql postgres -c 'GRANT ALL PRIVILEGES ON DATABASE "portal_test" to portal_user;'

