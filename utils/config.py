from datetime import timedelta
from dotenv import load_dotenv
import os
import redis

load_dotenv()


class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    #SESSION_REDIS = redis.from_url("redis://172.16.238.4:6379")
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME ='eyachaari@ieee.org'
    MAIL_PASSWORD ='eya12345'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    JWT_SECRET_KEY = os.environ["SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)