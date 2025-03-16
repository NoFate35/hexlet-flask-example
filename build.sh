#!/data/data/com.termux/files/usr/bin/bash

pg_ctl -D $PREFIX/var/lib/postgresql start
psql -a -d $DATABASE_URL flaskdb
