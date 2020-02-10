import os

JwtConfig = {
    'key' : os.environ.get('JWT_KEY', 'mysecretkey')
}
