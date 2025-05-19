from flask import Blueprint, render_template, jsonify, request, session
import requests  # API 요청을 위한 라이브러리

playlist_detail_member_bp = Blueprint('playlist_detail_member', __name__)


@playlist_detail_member_bp.route('/playlist/member')
def playlist_detail_member():
    # 세션에서 사용자 토큰 가져오기
    access_token = session.get('access_token')

    # 로그인 확인
    if not access_token:
        return render_template('login.html', error="로그인이 필요합니다")

    try:
        # API에서 회원의 음악 목록 가져오기 (백엔드 API가 있다고 가정)
        # 실제 API URL로 변경해야 합니다
        response = requests.get(
            'http://your-api-url/api/myplaylist',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        if response.status_code == 200:
            music_list = response.json()
            return render_template('components/play_list_detail_member.html', music_list=music_list)
        else:
            return render_template('components/play_list_detail_member.html', music_list=[],
                                   error="음악 목록을 불러오는 데 실패했습니다")

    except Exception as e:
        print(f"Error: {e}")
        return render_template('components/play_list_detail_member.html', music_list=[], error="서버 오류가 발생했습니다")