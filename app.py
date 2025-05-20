from flask import Flask, render_template, g
from routes.routes import routes
from routes.auth import auth
from routes.api import api
from routes.playlist_guest import playlist_guest_bp
from routes.playlist_detail_member import playlist_detail_member_bp
from routes.playlist_detail_guest import playlist_detail_guest_bp
from routes.play_tab import play_tab_bp
from routes.create_controller import create_controller_bp
from routes.audio_query import audio_query_bp
from routes.generate_query import generate_query_bp
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션을 위한 시크릿 키 설정

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
app.register_blueprint(generate_query_bp)

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

@app.route('/')
def index():
    # 메인 페이지 렌더링
    return render_template('index.html', theme=json.dumps(g.theme))

@app.route('/<path:path>')
def catch_all(path):
    # React의 Outlet 역할을 하는 모든 라우트 처리
    # 클라이언트 사이드 라우팅을 위해 모든 경로에서 index.html 반환
    return render_template('index.html', theme=json.dumps(g.theme))

if __name__ == '__main__':
    app.run(debug=True)