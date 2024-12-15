from pydantic import AmqpDsn, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rabbit_mq_dsn: AmqpDsn = "amqp://guest:guest@rabbitmq:5672/"


settings = Settings()
