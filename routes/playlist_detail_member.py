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
        # 실제 프로젝트에 맞게 API URL 수정
        api_url = 'http://your-api-url/api/myplaylist'

        # 임시 데이터 (API가 아직 없는 경우 테스트용)
        test_data = [
            {
                'musicId': 1,
                'title': '편안한 카페 음악',
                'musicUrl': '/static/audio/sumu - apart [NCS Release].mp3',
                'like': 15,
                'pressed': False
            },
            {
                'musicId': 2,
                'title': '신나는 산책 음악',
                'musicUrl': '/static/audio/sumu - apart [NCS Release].mp3',
                'like': 8,
                'pressed': False
            }
        ]

        # API 사용 여부 결정 (테스트할 때는 False로 설정)
        use_real_api = False

        if use_real_api:
            # 실제 API 호출
            response = requests.get(
                api_url,
                headers={'Authorization': f'Bearer {access_token}'}
            )

            if response.status_code == 200:
                music_list = response.json()
            else:
                return render_template('components/play_list_detail_member.html',
                                       music_list=[],
                                       error="음악 목록을 불러오는 데 실패했습니다")
        else:
            # 테스트 데이터 사용
            music_list = test_data

        # 로그에 데이터 출력 (디버깅용)
        print(f"음악 목록: {music_list}")

        return render_template('components/play_list_detail_member.html',
                               music_list=music_list,
                               current_music_id=session.get('current_music_id', 0))

    except Exception as e:
        print(f"Error: {e}")
        return render_template('components/play_list_detail_member.html',
                               music_list=[],
                               error="서버 오류가 발생했습니다")