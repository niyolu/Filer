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
    
    app_force_create_admin: bool = False
    app_admin_name: str = "root"
    app_admin_pw: str
    app_admin_quota_mb: int
    app_admin_max_objects_per_dir: int

    storage_max_objects_per_dir: int = 10
    storage_quota_mb: int = 500

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()


if __name__ == "__main__":
    settings = Settings()
    print(settings)