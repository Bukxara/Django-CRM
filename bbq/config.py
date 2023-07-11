from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

POSTGRES_URL = env.str('POSTGRES_URL')
PGNAME = env.str('PGNAME')
USER = env.str('PGUSER')
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
PGHOST = env.str('PGHOST')
PGPORT = env.int('PGPORT')
