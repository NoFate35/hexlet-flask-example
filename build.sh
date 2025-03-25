:'
#!/bin/bash
sudo service postgresql start
psql -a -d $DATABASE_URL flaskdb
export DATABASE_URL="postgresql://u0_a441:@localhost/flaskdb"
psql flaskdb < init.sql
'

#!/data/data/com.termux/files/usr/bin/bash
pg_ctl -D $PREFIX/var/lib/postgresql start
export DATABASE_URL="postgresql://u0_a441:@localhost/flaskdb"
psql flaskdb < init.sql

