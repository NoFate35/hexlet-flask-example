#!/bin/bash
sudo service postgresql start
psql flaskdb < init.sql
:'
pg_ctl -D $PREFIX/var/lib/postgresql start
psql -a -d $DATABASE_URL flaskdb
psql flaskdb < init.sql
'