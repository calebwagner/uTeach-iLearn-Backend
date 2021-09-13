rm db.sqlite3

python3 ./manage.py migrate

python3 ./manage.py loaddata users
python3 ./manage.py loaddata tokens
python3 ./manage.py loaddata appusers
python3 ./manage.py loaddata categories
python3 ./manage.py loaddata posts
python3 ./manage.py loaddata connections
python3 ./manage.py loaddata comments
python3 ./manage.py loaddata messages
python3 ./manage.py loaddata meetings
python3 ./manage.py loaddata savepost

