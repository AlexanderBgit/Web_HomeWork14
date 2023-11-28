from pydantic_settings import BaseSettings
# from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "contacts"

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: int
    postgres_domain: str
    sqlalchemy_database_url: str = "postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}"
    secret_key: str 
    algorithm: str 
    mail_username: str 
    mail_password: str 
    mail_from: str 
    mail_port: int 
    mail_server: str 
    
    mail_from_name: str
    mail_starttls: bool
    mail_ssl_tls: bool
    use_credentials: bool
    validate_certs: bool
    
    redis_host: str 
    redis_port: int

    cloudinary_name: str = 'name'
    cloudinary_api_key: int = 247459982199157
    cloudinary_api_secret: str = 'secret'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
