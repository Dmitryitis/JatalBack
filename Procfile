release: python3 src/manage.py migrate
web: gunicorn NewsPortal.wsgi --chdir src --preload --log-file -