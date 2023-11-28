from environs import Env


class PSQLConfig:
    def __init__(self, path):
        env = Env()
        env.read_env(path)
        self.db_netloc = env("DB_NETLOC")
        self.db_user = env("DB_USER")
        self.db_name = env("DB_NAME")
        self.db_pass = env("DB_PASS")
        self.db_port = env("DB_PORT")

    def load_driver_url(self, *, dbs: str = "postgresql", driver: str = "asyncpg") -> str:
        url = f'{dbs}{"+" + driver if driver else ""}://{self.db_user}:{self.db_pass}@' \
              f'{self.db_netloc}:{self.db_port}/{self.db_name}'
        return url


settings = PSQLConfig('.env')

# print(settings.load_driver_url(driver='psycopg'))
