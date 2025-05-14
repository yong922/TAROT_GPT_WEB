import os

env = os.getenv("APP_ENV", "dev")

if env == "test":
    from .test import TestConfig as Config
else:
    from .dev import DevConfig as Config