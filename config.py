import os


class Config:
    api_version = "v0.1"
    jwt_secret = os.environ.get("DSAM_SECRET") or "NO SALT HERE"
    jwt_algorithm = "HS256"
    jwt_token_expires_seconds = 3600 * 24
    crypt_schemes = ["bcrypt"]
