from pydantic import BaseSettings


class Settings(BaseSettings):

    DB_USER = 'postgres'
    DB_PASSWORD = '2567'
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'lostfound'

    @property
    def database(self) -> dict[str, str | int]:
        return {
            'database': self.DB_NAME,
            'user': self.DB_USER,
            'password': self.DB_PASSWORD,
            'host': self.DB_HOST,
            'port': self.DB_PORT,
        }

    @property
    def database_url(self):
        return 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**self.database)

    ITEMS_STORAGE = '../appdata/images/items'
    USERS_STORAGE = '../appdata/images/users'


settings = Settings()
