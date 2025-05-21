from flask import Blueprint, redirect, url_for, session, request, jsonify
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 개발 환경에서 HTTPS 요구 사항 비활성화
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# 구글 OAuth 설정
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# useMember.ts의 설정 값
TS_CLIENT_ID = '343811570389-v2c7b274ap2drc630gut75l80ivm889t.apps.googleusercontent.com'

# GOOGLE_CLIENT_ID가 없을 경우 TS_CLIENT_ID 사용
if not GOOGLE_CLIENT_ID:
    GOOGLE_CLIENT_ID = TS_CLIENT_ID

auth = Blueprint('auth', __name__)
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# 환경 변수가 제대로 로드되었는지 확인하는 디버그 코드 추가
@auth.route('/auth/debug')
def debug_auth():
    """OAuth 설정 디버그용 라우트"""
    return jsonify({
        'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID[:10] + '...' if GOOGLE_CLIENT_ID else None,
        'GOOGLE_CLIENT_SECRET': '설정됨' if GOOGLE_CLIENT_SECRET else None
    })


@auth.route("/auth/google")
def google_login():
    """Google OAuth 로그인 시작"""
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
    """직접 Google 로그인 페이지로 리다이렉트"""
    # 현재 호스트 URL 동적으로 가져오기
    FRONT_URL = request.host_url.rstrip('/')

    # 로깅 추가 (디버깅용)
    print(f"Front URL: {FRONT_URL}")
    print(f"Client ID: {GOOGLE_CLIENT_ID}")

    # Google OAuth URL 생성
    REQUEST_URI = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={FRONT_URL}/auth/google/callback&response_type=code&scope=profile email openid"

    return redirect(REQUEST_URI)


@auth.route("/auth/google/callback")
def callback():
    """Google OAuth 콜백 처리"""
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
            session['user_email'] = users_email  # 이메일도 저장
            session['user_name'] = users_name  # 이름도 저장
            session['is_member'] = True
            session['access_token'] = token_response.json().get("access_token")

            # 세션 갱신
            session.modified = True

            # 로그 출력 추가 (디버깅용)
            print(f"User logged in: {users_name} ({users_email})")

            # 클라이언트 로컬 스토리지 설정 및 리다이렉트
            return f"""
            <script>
                localStorage.setItem('accessToken', '{session['access_token']}');
                localStorage.setItem('userName', '{users_name}');
                localStorage.setItem('userEmail', '{users_email}');
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
    """사용자 로그인 상태 확인 API"""
    # 세션에서 사용자 정보 확인
    is_member = 'user_id' in session and session.get('is_member', False)

    # 응답 데이터
    response_data = {
        "is_member": is_member,
        "user_id": session.get('user_id') if is_member else None
    }

    # 로그인 상태인 경우 추가 정보 제공
    if is_member:
        response_data.update({
            "user_email": session.get('user_email'),
            "user_name": session.get('user_name')
        })

    return jsonify(response_data)


def get_google_provider_cfg():
    """Google OAuth 설정 정보 요청 함수"""
    try:
        return requests.get(GOOGLE_DISCOVERY_URL).json()
    except Exception as e:
        print(f"Error getting Google provider config: {e}")
        return {}


@auth.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    """사용자 로그아웃 처리"""
    # 세션에서 사용자 정보 제거
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('user_name', None)
    session.pop('is_member', None)
    session.pop('access_token', None)

    # 세션 갱신
    session.modified = True

    # 로그아웃 메시지 출력 (디버깅용)
    print("User logged out")

    # 클라이언트 측 로컬 스토리지 토큰 제거
    if request.method == 'GET':
        return """
        <script>
            localStorage.removeItem('accessToken');
            localStorage.removeItem('userName');
            localStorage.removeItem('userEmail');
            alert('로그아웃 되었습니다.');
            window.location.href = '/';
        </script>
        """
    else:
        return jsonify({'success': True, 'message': '로그아웃 되었습니다.'})