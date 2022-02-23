FLASK MIGRATE

Setup the FLASK_APP environment variable
- export FLASK_APP=task.py

cli commands after setting


`flask db init  `Sets up the migrations dir  
`flask db migrate -m "some message"  `Sets up the migration file  
`flask db upgrade  `Updates the database with the migration  
