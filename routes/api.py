from flask import Blueprint, request, jsonify, session

api = Blueprint('api', __name__)


@api.route('/api/like-music', methods=['POST'])
def like_music():
    # 로그인 확인
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'login_required'})

    data = request.json
    music_id = data.get('music_id')

    # 여기에 실제 데이터베이스에 좋아요 정보를 저장하는 코드 구현
    # 예: update_like_in_database(session['user_id'], music_id)

    return jsonify({'success': True})