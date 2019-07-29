# Cognnect

## Running

Mac/Linux: `export FLASK_APP=application.py`
Windows: `set FLASK_APP=application.py`

Mac/Linux: `export DATABASE_URL=postgres://vzihzhagmfngky:e520bab65138c9d74fc92b5f48330f530dd8a3e33ecb51c9ca2781ea5fd8ddd4@ec2-174-129-226-232.compute-1.amazonaws.com:5432/d6tj5q6d0li4u6`

Windows: `set DATABASE_URL=postgres://vzihzhagmfngky:e520bab65138c9d74fc92b5f48330f530dd8a3e33ecb51c9ca2781ea5fd8ddd4@ec2-174-129-226-232.compute-1.amazonaws.com:5432/d6tj5q6d0li4u6`

Alternatively, you can do `source init/init.sh` in a UNIX command line (Mac/Linux) or `call init\init.bat` in Windows for set up these environment variables automatically.

To run the flask application, enter `flask run`.

The website can now be accessed at `localhost:5000` in a browser.
