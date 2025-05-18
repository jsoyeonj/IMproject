from flask import Blueprint, redirect, url_for, session, request
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
import os

# 구글 OAuth 설정..
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

auth = Blueprint('auth', __name__)
client = WebApplicationClient(GOOGLE_CLIENT_ID)


@auth.route("/auth/google")
def google_login():
    # Google OAuth 서버에서 구성 정보 얻기
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Google에 요청 생성
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth.route("/auth/google/callback")
def callback():
    # Google로부터 인증 코드 받기
    code = request.args.get("code")

    # 인증 코드를 액세스 토큰으로 교환하는 로직
    # 이 부분은 실제 구현시 더 복잡합니다

    # 사용자 정보 검색 로직
    # ...

    # 로그인 성공시 홈페이지로 리디렉트
    return redirect(url_for("routes.home"))

@auth.route("/check_member")
def check_member():
    # 세션에서 사용자 정보 확인
    if 'user_id' in session:
        # 사용자가 로그인되어 있음
        return {"is_member": True}
    else:
        # 사용자가 로그인되어 있지 않음
        return {"is_member": False}

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@auth.route('/auth/logout', methods=['POST'])
def logout():
    # 세션에서 사용자 정보 제거
    session.pop('user_id', None)
    session.pop('is_member', None)

    return jsonify({'success': True})