class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test"
    OPENAI_API_KEY = "test"
    WTF_CSRF_ENABLED = False