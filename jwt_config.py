import os

"""
JWT configuration for Flask app.

Environment variable required:
 - JWT_KEY: The secret signing key for JWT tokens. (Never check this into version control.)
"""

JWT_CONFIG = {
    'key': os.environ.get('JWT_KEY', 'mysecretkey')
}
