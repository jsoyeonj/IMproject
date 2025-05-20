from flask import Blueprint, redirect, url_for, session, request
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
import os
from flask import jsonify
from dotenv import load_dotenv

# from models.auth import create_google_login_response, create_login_error_response
# .env 파일 로드
load_dotenv()

# 개발 환경에서 HTTPS 요구 사항 비활성화
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # 이 줄 추가

# 개발 환경에서 HTTPS 요구 사항 비활성화
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# 구글 OAuth 설정
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# useMember.ts의 설정 값
TS_CLIENT_ID = '343811570389-v2c7b274ap2drc630gut75l80ivm889t.apps.googleusercontent.com'
# FRONT_URL = 'https://croffle-fe.vercel.app'  # 이미 환경 변수로 설정된 경우 사용

# GOOGLE_CLIENT_ID가 없을 경우 TS_CLIENT_ID 사용
if not GOOGLE_CLIENT_ID:
    GOOGLE_CLIENT_ID = TS_CLIENT_ID

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


@auth.route('/login/direct-google')
def direct_google_login():
    """useMember.ts 스타일의 직접 Google 로그인 페이지로 리다이렉트"""
    FRONT_URL = request.host_url.rstrip('/')
    REQUEST_URI = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={FRONT_URL}/auth/google/callback&response_type=code&scope=profile email openid"
    return redirect(REQUEST_URI)


@auth.route("/auth/google/callback")
def callback():
    # Google로부터 인증 코드 받기
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Authorization code not found"}), 400

    try:
        # Google OAuth 서버에서 구성 정보 얻기
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        # 액세스 토큰 요청 준비
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )

        # 액세스 토큰 요청
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )

        # 토큰 파싱
        client.parse_request_body_response(json.dumps(token_response.json()))

        # 사용자 정보 요청
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        # 사용자 정보 확인
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json().get("picture")
            users_name = userinfo_response.json().get("given_name")

            # 세션에 사용자 정보 저장
            session['user_id'] = unique_id
            session['is_member'] = True
            session['access_token'] = token_response.json().get("access_token")

            # 클라이언트 로컬 스토리지 설정 및 리다이렉트
            return f"""
            <script>
                localStorage.setItem('accessToken', '{session['access_token']}');
                window.location.href = '/';
            </script>
            """
        else:
            return jsonify({"error": "User email not verified by Google."}), 400

    except Exception as e:
        print(f"Error during OAuth authentication: {e}")
        return jsonify({"error": str(e)}), 500


@auth.route("/api/check-member", methods=['GET'])
def check_member():
    # 세션에서 사용자 정보 확인
    is_member = 'user_id' in session and session.get('is_member', False)

    # 로컬 스토리지 체크 로직을 클라이언트에 제공
    return jsonify({
        "is_member": is_member,
        "user_id": session.get('user_id') if is_member else None
    })


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@auth.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    # 세션에서 사용자 정보 제거
    session.pop('user_id', None)
    session.pop('is_member', None)
    session.pop('access_token', None)

    # 클라이언트 측 로컬 스토리지 토큰 제거
    if request.method == 'GET':
        return """
        <script>
            localStorage.removeItem('accessToken');
            window.location.href = '/';
        </script>
        """
    else:
        return jsonify({'success': True})


@auth.route("/api/auth/google/callback", methods=["POST"])
def google_callback_api():
    try:
        # 구글 로그인 처리 로직
        # ...

        # 성공적으로 처리된 경우
        access_token = "generated_access_token"  # 실제로는 OAuth 프로세스에서 생성

        # 응답 생성
        response = create_google_login_response(access_token)
        return jsonify(response)

    except Exception as e:
        # 오류 처리
        response = create_login_error_response(str(e))
        return jsonify(response), 400