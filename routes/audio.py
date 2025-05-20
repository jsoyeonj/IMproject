from flask import Blueprint, jsonify, request, session, current_app

audio_bp = Blueprint('audio', __name__)


@audio_bp.route('/api/audio/state', methods=['GET'])
def get_audio_state():
    """
    현재 오디오 재생 상태를 가져오는 API 엔드포인트
    """
    try:
        # 세션에서 음악 재생 상태 정보 가져오기
        audio_state = {
            'currentMusicId': session.get('current_music_id', 0),
            'isPlaying': session.get('is_playing', False),
            'musicUrl': session.get('current_music_url', ''),
            'progress': session.get('current_progress', 0)
        }

        return jsonify({
            'success': True,
            'response': audio_state
        }), 200

    except Exception as e:
        current_app.logger.error(f"오디오 상태 조회 오류: {str(e)}")
        return jsonify({
            'success': False,
            'message': '오디오 상태를 가져오는 중 오류가 발생했습니다.'
        }), 500


@audio_bp.route('/api/audio/play', methods=['POST'])
def play_audio():
    """
    음악 재생 상태를 저장하는 API 엔드포인트
    """
    try:
        # 요청 데이터 확인
        data = request.json
        if not data or 'musicId' not in data or 'musicUrl' not in data:
            return jsonify({
                'success': False,
                'message': '유효하지 않은 요청입니다.'
            }), 400

        # 세션에 음악 재생 정보 저장
        session['current_music_id'] = data['musicId']
        session['current_music_url'] = data['musicUrl']
        session['is_playing'] = True
        session['current_progress'] = 0  # 초기 진행 상태는 0

        return jsonify({
            'success': True,
            'message': '음악 재생 정보가 저장되었습니다.'
        }), 200

    except Exception as e:
        current_app.logger.error(f"음악 재생 처리 오류: {str(e)}")
        return jsonify({
            'success': False,
            'message': '음악 재생 처리 중 오류가 발생했습니다.'
        }), 500


@audio_bp.route('/api/audio/stop', methods=['POST'])
def stop_audio():
    """
    음악 재생 중지 상태를 저장하는 API 엔드포인트
    """
    try:
        # 세션에서 재생 중지 상태 저장
        session['is_playing'] = False

        return jsonify({
            'success': True,
            'message': '음악 재생이 중지되었습니다.'
        }), 200

    except Exception as e:
        current_app.logger.error(f"음악 중지 처리 오류: {str(e)}")
        return jsonify({
            'success': False,
            'message': '음악 중지 처리 중 오류가 발생했습니다.'
        }), 500


@audio_bp.route('/api/audio/remove', methods=['POST'])
def remove_audio():
    """
    음악 재생 상태를 제거하는 API 엔드포인트
    """
    try:
        # 세션에서 음악 정보 제거
        session.pop('current_music_id', None)
        session.pop('current_music_url', None)
        session.pop('is_playing', None)
        session.pop('current_progress', None)

        return jsonify({
            'success': True,
            'message': '음악 정보가 제거되었습니다.'
        }), 200

    except Exception as e:
        current_app.logger.error(f"음악 제거 처리 오류: {str(e)}")
        return jsonify({
            'success': False,
            'message': '음악 제거 처리 중 오류가 발생했습니다.'
        }), 500


@audio_bp.route('/api/audio/progress', methods=['POST'])
def update_progress():
    """
    음악 재생 진행 상태를 업데이트하는 API 엔드포인트
    """
    try:
        # 요청 데이터 확인
        data = request.json
        if not data or 'progress' not in data:
            return jsonify({
                'success': False,
                'message': '유효하지 않은 요청입니다.'
            }), 400

        # 세션에 진행 상태 저장
        session['current_progress'] = data['progress']

        return jsonify({
            'success': True,
            'message': '재생 진행 상태가 업데이트되었습니다.'
        }), 200

    except Exception as e:
        current_app.logger.error(f"진행 상태 업데이트 오류: {str(e)}")
        return jsonify({
            'success': False,
            'message': '진행 상태 업데이트 중 오류가 발생했습니다.'
        }), 500