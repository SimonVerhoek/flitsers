#!/bin/sh
set -e

db_host=`printenv DB_HOST`
db_user=`printenv POSTGRES_USER`
db_name=`printenv POSTGRES_DB`

tables=$(psql -U $db_user -h $db_host $db_name -A -t -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
for table in $tables; do
    echo $table
    psql -U $db_user -h $db_host $db_name -c "\copy (SELECT * FROM $table) TO STDOUT" | \
    psql -U $db_user $db_name -c "\copy $table FROM STDIN"
done

materialized_views=$(psql -U $db_user -h $db_host $db_name -A -t -c "SELECT matviewname FROM pg_matviews WHERE schemaname = 'public';")
for matview in $materialized_views; do
    echo $matview
    psql -U $db_user $db_name -c "REFRESH MATERIALIZED VIEW $matview;"
done
