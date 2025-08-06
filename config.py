from environs import env

env.read_env()

POSTGRES_NAME = env('POSTGRES_NAME')
POSTGRES_USER = env('POSTGRES_USER')
POSTGRES_PASS = env('POSTGRES_PASS')
POSTGRES_HOST = env('POSTGRES_HOST', default='127.0.0.1')
POSTGRES_PORT = env('POSTGRES_PORT', default='5432')

DB_URL = (
    f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASS}@'
    f'{POSTGRES_HOST}:{POSTGRES_PORT}/'
    f'{POSTGRES_NAME}'
)
