# start the server
gunicorn --bind 0.0.0.0:5050 wsgi:app --reload