# run mypy on the src folder 
mypy src

# install the vtop_handler package 
python -m pip install -e .

# run pytest on the tests folder
pytest tests

# uninstall the vtop_handler package 
python -m pip uninstall vtop_handler -y

# start the server
# gunicorn --bind 0.0.0.0:5050 wsgi:app --reload
waitress-serve --listen=127.0.0.1:5000 wsgi:app
# recording the usage statistics
# psrecord --plot memory.png "python main.py" 
