from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.getenv('SECRET_KEY')

    # CSRF 보호 비활성화 (Postman 테스트용)
    WTF_CSRF_ENABLED = False

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # 테스트용 더미 키

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 메모리 DB를 사용하여 테스트 환경에서 데이터베이스 초기화
    TESTING = True  # Flask의 테스트 모드 활성화
