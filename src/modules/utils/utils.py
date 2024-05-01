import os


def validate_env():
    if os.getenv(key="WEBEX_ACCESS_TOKEN") is None:
        raise Exception("WEBEX_ACCESS_TOKEN is not set in environment variables")
