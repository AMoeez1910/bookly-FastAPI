import redis as redis

from src.config import Config

JTI_EXPIRY = 3600  # seconds

token_blocklist = redis.from_url(Config.REDIS_URL, decode_responses=True)


async def add_jti_to_blocklist(jti: str):
    """
    Add a JWT ID (jti) to the blocklist in Redis.
    """
    token_blocklist.set(jti, "blocked", ex=JTI_EXPIRY)


async def is_jti_blocked(jti: str) -> bool:
    """
    Check if a JWT ID (jti) is in the blocklist.
    """
    return token_blocklist.get(jti) is not None


# admin
[
    "adding users",
    "change roles",
    "crud on users",
    "crud on reviews",
    "book submissions",
    "revoking access",
]

[
    "crud on their own accounts",
    "crud on their reviews",
    "crud on their own book submissions",
]
