from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")

SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
JOIN_NO_MEDIA_TIME = env.int("JOIN_NO_MEDIA_TIME", 10)
ADMINS_ID = env.list("ADMINS_ID")

REDIS_HOST = env("REDIS_HOST", "127.0.0.1")
REDIS_PORT = env("REDIS_PORT", 6379)

aiogram_redis = {
    'host': REDIS_HOST,
}

redis = {
    'address': (REDIS_HOST, REDIS_PORT),
    'encoding': 'utf8'
}
