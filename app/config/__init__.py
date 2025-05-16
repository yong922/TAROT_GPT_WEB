import os
import sys

if "pytest" in sys.modules:
    os.environ["APP_ENV"] = "test"

env = os.getenv("APP_ENV", "dev")
print(f"[CONFIG INIT] APP_ENV = {env}")

if env == "test":
    from .test import TestConfig as Config
else:
    from .dev import DevConfig as Config

print("[CONFIG INIT] APP_ENV =", os.getenv("APP_ENV"))