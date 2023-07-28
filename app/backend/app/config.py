from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str = "root"
    db_pw: str
    db_host: str = "localhost"
    db_database: str = "db"
    
    auth_secret_key: str
    auth_algorithm: str = "HS256"
    auth_access_token_expire_minutes: int = 30
    
    app_admin_pw: str

    storage_max_objects_per_dir: int = 10
    storage_quota_mb: int = 500

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()


if __name__ == "__main__":
    settings = Settings()
    print(settings)