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


# recreate id sequence on melding table
psql -U $db_user $db_name -c "CREATE SEQUENCE melding_id_seq; ALTER TABLE melding ALTER COLUMN id SET DEFAULT nextval('melding_id_seq'); SELECT setval('melding_id_seq', COALESCE((SELECT MAX(id)+1 FROM melding), 1), false);"
