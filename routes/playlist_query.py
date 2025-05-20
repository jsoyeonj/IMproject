from flask import Blueprint, jsonify, request, current_app, session

playlist_query_bp = Blueprint('playlist_query', __name__)


@playlist_query_bp.route('/api/playlist', methods=['GET'])
def get_playlist():
    """
    일반 플레이리스트를 가져오는 API 엔드포인트
    React의 usePlayListQuery 훅의 일부 기능을 대체
    """
    try:
        # 임시 데이터 (실제 구현에서는 데이터베이스에서 가져오기)
        playlist_data = [
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
            },
            {
                'musicId': 3,
                'title': '잔잔한 학교 음악',
                'musicUrl': '/static/audio/sumu - apart [NCS Release].mp3',
                'like': 12,
                'pressed': False
            }
        ]

        # 로그인한 사용자라면 'pressed' 값을 업데이트 (좋아요 눌렀는지 여부)
        access_token = session.get('access_token')
        if access_token:
            # 실제 구현에서는 사용자의 좋아요 정보를 데이터베이스에서 가져와 확인
            # 여기서는 임시로 1번 음악에 좋아요를 표시
            for music in playlist_data:
                if music['musicId'] == 1:
                    music['pressed'] = True

        return jsonify(playlist_data), 200

    except Exception as e:
        current_app.logger.error(f"플레이리스트 조회 오류: {str(e)}")
        return jsonify({
            'success': False,
            'message': '플레이리스트를 가져오는 중 오류가 발생했습니다.'
        }), 500


@playlist_query_bp.route('/api/playlist/popular', methods=['GET'])
def get_popular_playlist():
    """
    인기 플레이리스트를 가져오는 API 엔드포인트
    React의 usePlayListQuery 훅의 일부 기능을 대체
    """
    try:
        # 임시 데이터 (실제 구현에서는 데이터베이스에서 가져오기)
        popular_playlist_data = [
            {
                'musicId': 4,
                'title': '인기 음악 1',
                'musicUrl': '/static/audio/sumu - apart [NCS Release].mp3',
                'like': 45,
                'pressed': False
            },
            {
                'musicId': 5,
                'title': '인기 음악 2',
                'musicUrl': '/static/audio/sumu - apart [NCS Release].mp3',
                'like': 38,
                'pressed': False
            },
            {
                'musicId': 6,
                'title': '인기 음악 3',
                'musicUrl': '/static/audio/sumu - apart [NCS Release].mp3',
                'like': 32,
                'pressed': False
            }
        ]

        # 로그인한 사용자라면 'pressed' 값을 업데이트 (좋아요 눌렀는지 여부)
        access_token = session.get('access_token')
        if access_token:
            # 실제 구현에서는 사용자의 좋아요 정보를 데이터베이스에서 가져와 확인
            # 여기서는 임시로 4번 음악에 좋아요를 표시
            for music in popular_playlist_data:
                if music['musicId'] == 4:
                    music['pressed'] = True

        return jsonify(popular_playlist_data), 200

    except Exception as e:
        current_app.logger.error(f"인기 플레이리스트 조회 오류: {str(e)}")
        return jsonify({
            'success': False,
            'message': '인기 플레이리스트를 가져오는 중 오류가 발생했습니다.'
        }), 500