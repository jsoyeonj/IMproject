from flask import Blueprint, jsonify, request, session
import requests

audio_query_bp = Blueprint('audio_query', __name__)


@audio_query_bp.route('/api/audio/query', methods=['GET'])
def get_audio_query():
    """오디오 정보를 쿼리하는 API 엔드포인트"""
    try:
        # 여기에 음악 정보 조회 로직 구현
        # 예: 데이터베이스 또는 외부 API에서 음악 데이터 가져오기

        # 임시 응답 데이터
        audio_data = {
            'success': True,
            'response': {
                'musicId': 1,
                'title': '샘플 음악',
                'musicUrl': '/static/audio/sample.mp3',
                'isPlaying': False
            }
        }

        return jsonify(audio_data), 200
    except Exception as e:
        print(f"오디오 쿼리 오류: {e}")
        return jsonify({
            'success': False,
            'message': '오디오 정보를 가져오는 중 오류가 발생했습니다.'
        }), 500


@audio_query_bp.route('/api/audio/current', methods=['GET'])
def get_current_audio():
    """현재 재생 중인 오디오 정보를 반환하는 API 엔드포인트"""
    try:
        # 세션에서 현재 음악 ID 가져오기
        current_music_id = session.get('current_music_id', 0)

        if current_music_id == 0:
            return jsonify({
                'success': False,
                'message': '현재 재생 중인 음악이 없습니다.'
            }), 404

        # 음악 ID로 정보 조회 로직
        # 실제 구현에서는 데이터베이스에서 조회

        # 임시 응답 데이터
        audio_data = {
            'success': True,
            'response': {
                'musicId': current_music_id,
                'title': '현재 재생 중인 음악',
                'musicUrl': '/static/audio/current.mp3',
                'isPlaying': True
            }
        }

        return jsonify(audio_data), 200
    except Exception as e:
        print(f"현재 오디오 정보 조회 오류: {e}")
        return jsonify({
            'success': False,
            'message': '현재 재생 중인 음악 정보를 가져오는 중 오류가 발생했습니다.'
        }), 500