import os

MONGODB_SETTINGS = {
    'db': os.environ.get('DB_NAME', 'database'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 27017)),
    'username' : os.environ.get('DB_USER', 'username'),
    'password': os.environ.get('DB_PW', 'password')
}



