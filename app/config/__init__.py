import os
import sys

# 로컬에서 pytest 실행 시 
# APP_ENV = test
if "pytest" in sys.modules:
    os.environ["APP_ENV"] = "test"

# 기본 APP_ENV = dev
env = os.getenv("APP_ENV", "dev")

if env == "test":
    from .test import TestConfig as Config
else:
    from .dev import DevConfig as Config