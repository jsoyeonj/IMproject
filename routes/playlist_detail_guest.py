from flask import Blueprint, render_template, jsonify
import requests  # API 요청을 위한 라이브러리

playlist_detail_guest_bp = Blueprint('playlist_detail_guest', __name__)


@playlist_detail_guest_bp.route('/playlist/guest/detail')
def playlist_detail_guest():
    try:
        # API에서 공개 음악 목록 가져오기 (백엔드 API가 있다고 가정)
        # 백엔드한테 주소 받고 여기 주소를 실제 API URL로 변경
        response = requests.get('http://127.0.0.1:5000')

        if response.status_code == 200:
            music_list = response.json()
            return render_template('components/play_list_detail_guest.html', music_list=music_list)
        else:
            return render_template('components/play_list_detail_guest.html', music_list=[],
                                   error="음악 목록을 불러오는 데 실패했습니다")

    except Exception as e:
        print(f"Error: {e}")
        return render_template('components/play_list_detail_guest.html', music_list=[], error="서버 오류가 발생했습니다")