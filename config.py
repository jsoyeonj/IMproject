import os
from pathlib import Path

# 기본 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")


class Config:
    """기본 설정 클래스"""
    # 보안 설정
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    # 기본 설정
    DEBUG = False
    TESTING = False

    # 정적 파일 및 템플릿 설정
    STATIC_FOLDER = STATIC_DIR
    TEMPLATE_FOLDER = TEMPLATE_DIR

    # CORS 설정
    CORS_HEADERS = 'Content-Type'

    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 세션 설정
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False


class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True


class TestingConfig(Config):
    """테스트 환경 설정"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """운영 환경 설정"""
    # 운영 환경에서는 환경 변수로부터 안전한 키를 가져옴
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


# 환경별 설정 매핑
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """현재 환경에 맞는 설정 반환"""
    env = os.environ.get('FLASK_ENV', 'default')
    return config[env]