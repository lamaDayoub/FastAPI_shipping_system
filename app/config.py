from pydantic_settings import BaseSettings,SettingsConfigDict

class DataBaseSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    model_config = SettingsConfigDict(
        env_file='.\.env',
        env_ignore_empty=True,
        extra='ignore'
    )
    @property
    def POSTGRES_URL(self) -> str:
        # Format: postgresql+asyncpg://user:password@server:port/db
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    
settings = DataBaseSettings()