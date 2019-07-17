release: python ./Code/manage.py migrate
web: gunicorn --pythonpath Code Code.wsgi --log-file -
