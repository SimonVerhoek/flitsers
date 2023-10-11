from environs import Env
from sqlalchemy import create_engine


env = Env()
env.read_env()


DB_TYPE = "postgresql"
DB_HOST = env.str("DB_HOST")
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_PORT = 5432

engine = create_engine(f"{DB_TYPE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
