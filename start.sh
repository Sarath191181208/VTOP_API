# run mypy on the src folder 
mypy src

# run pytest on the tests folder
pytest tests

# start the server
gunicorn --bind 0.0.0.0:5050 wsgi:app --reload

# psrecord --plot memory.png "python main.py" 