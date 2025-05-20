from flask import Flask, render_template, g, redirect, url_for, session
from routes.routes import routes
from routes.auth import auth
from routes.api import api
from routes.playlist_guest import playlist_guest_bp
from routes.playlist_detail_member import playlist_detail_member_bp
from routes.playlist_detail_guest import playlist_detail_guest_bp
from routes.play_tab import play_tab_bp
from routes.create_controller import create_controller_bp
from routes.audio_query import audio_query_bp
from routes.playlist_query import playlist_query_bp
from routes.create_like import create_like_bp
from routes.audio import audio_bp
import json
from config import get_config
from dotenv import load_dotenv  # 이 줄 추가
import os  # 이 줄도 추가

# .env 파일 로드
load_dotenv()

# 개발 환경에서 HTTPS 요구 사항 비활성화 (OAuth2를 위해)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def create_app(config_class=None):
    """애플리케이션 팩토리 함수"""
    app = Flask(__name__)

    # 설정 로드
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_fallback_secret_key")  # 기본값 추가
    # 블루프린트 등록
    app.register_blueprint(routes)
    app.register_blueprint(auth)
    app.register_blueprint(api)
    app.register_blueprint(playlist_guest_bp)
    app.register_blueprint(playlist_detail_member_bp)
    app.register_blueprint(playlist_detail_guest_bp)
    app.register_blueprint(play_tab_bp)
    app.register_blueprint(create_controller_bp)
    app.register_blueprint(audio_query_bp)
    app.register_blueprint(playlist_query_bp)
    app.register_blueprint(create_like_bp)
    app.register_blueprint(audio_bp)

    # 앱 설정 및 초기화
    @app.before_request
    def setup_app():
        # 테마 설정을 g 객체에 저장 (request 단위로 접근 가능한 전역 객체)
        g.theme = {
            "colors": {
                "primary": "#007bff",
                "secondary": "#6c757d",
                # theme.ts에서 가져온 다른 테마 설정들
            }
        }

    @app.route('/create/controller')
    def redirect_to_controller():
        # create_controller 블루프린트로 리다이렉트
        return redirect(url_for('create_controller.create_controller'))

    @app.route('/create-end')
    def create_end():
        # 음악 생성 완료 페이지 렌더링
        music_url = session.get('current_music_url', '')
        return render_template('create_end.html',
                               music_url=music_url,
                               theme=json.dumps(g.theme))

    @app.route('/')
    def index():
        # 메인 페이지 렌더링
        return render_template('index.html', theme=json.dumps(g.theme))

    @app.route('/<path:path>')
    def catch_all(path):
        # React의 Outlet 역할을 하는 모든 라우트 처리
        # 클라이언트 사이드 라우팅을 위해 모든 경로에서 index.html 반환
        return render_template('index.html', theme=json.dumps(g.theme))

    return app


# 기본 앱 인스턴스 생성
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)