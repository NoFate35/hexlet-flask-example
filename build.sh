:'
#!/bin/bash
sudo service postgresql start
psql -a -d $DATABASE_URL flaskdb
psql flaskdb < init.sql

:'
#!/data/data/com.termux/files/usr/bin/bash
pg_ctl -D $PREFIX/var/lib/postgresql start
psql flaskdb < init.sql
'