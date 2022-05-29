from src.database.settings import DatabaseSettings


def create_database_url(settings: DatabaseSettings) -> str:
    return (f'postgresql+psycopg2://'
            f'{settings.username}:{settings.password}@'
            f'{settings.host}:{settings.port}/{settings.database}')
