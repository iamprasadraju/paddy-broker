rm -rf farmers/migrations
rm -rf db.sqlite3


python3 manage.py makemigrations farmers

python3 manage.py migrate


python3 manage.py createsuperuser


bash run.sh
