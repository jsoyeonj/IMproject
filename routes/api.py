from flask import Blueprint, request, jsonify, session
import os
import time
api = Blueprint('api', __name__)


@api.route('/api/like-music', methods=['POST'])
def add_like_music():  # 함수 이름을 like_music에서 add_like_music으로 변경
    # 로그인 확인
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'login_required'})

    data = request.json
    music_id = data.get('music_id')

    # 여기에 실제 데이터베이스에 좋아요 정보를 저장하는 코드 구현
    # 예: update_like_in_database(session['user_id'], music_id)

    return jsonify({'success': True})


@api.route('/api/generate-music-from-image', methods=['POST'])
def generate_music_from_image():
    # 파일이 요청에 포함되어 있는지 확인
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': '이미지가 없습니다.'})

    image_file = request.files['image']

    # 유효한 파일인지 확인
    if image_file.filename == '':
        return jsonify({'success': False, 'error': '선택된 파일이 없습니다.'})

    if image_file:
        # 파일 저장 (선택 사항)
        # filename = secure_filename(image_file.filename)
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # image_file.save(file_path)

        # 여기서 이미지를 기반으로 음악을 생성하는 로직을 구현
        # 실제 구현에서는 AI 모델이나 외부 API를 호출할 수 있음
        # 예시로는 더미 음악 URL 반환

        # 임시 테스트용 지연 (2초)
        import time
        time.sleep(2)

        # 더미 음악 URL 반환 (실제 구현에서는 생성된 음악 파일의 URL)
        music_url = '/static/audio/generated_music.mp3'

        return jsonify({
            'success': True,
            'musicUrl': music_url
        })

    return jsonify({'success': False, 'error': '파일 처리 중 오류가 발생했습니다.'})


@api.route('/api/generate-music', methods=['POST'])
def generate_music():
    try:
        data = request.json
        prompt1 = data.get('prompt1', '')
        prompt2 = data.get('prompt2', '')

        # 프롬프트 검증
        if not prompt1 and not prompt2:
            return jsonify({
                'success': False,
                'error': '최소한 하나의 프롬프트가 필요합니다.'
            }), 400

        # 음악 생성 처리 시간을 시뮬레이션 (실제로는 AI 모델을 호출)
        time.sleep(2)

        # 더미 음악 URL 반환 (실제로는 생성된 음악 파일의 URL)
        music_url = '/static/audio/generated_music.mp3'

        return jsonify({
            'success': True,
            'response': {
                'musicUrl': music_url
            },
            'error': None
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/api/member/generate-music', methods=['POST'])
def generate_member_music():
    # 로그인 확인
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'error': '로그인이 필요합니다.'
        }), 401

    try:
        data = request.json
        prompt1 = data.get('prompt1', '')
        prompt2 = data.get('prompt2', '')

        # 프롬프트 검증
        if not prompt1 and not prompt2:
            return jsonify({
                'success': False,
                'error': '최소한 하나의 프롬프트가 필요합니다.'
            }), 400

        # 음악 생성 처리 시간을 시뮬레이션 (실제로는 AI 모델을 호출)
        time.sleep(2)

        # 더미 음악 URL 반환 (실제로는 생성된 음악 파일의 URL)
        music_url = '/static/audio/generated_member_music.mp3'

        # 회원 정보를 포함한 응답
        user_id = session.get('user_id')

        return jsonify({
            'success': True,
            'response': {
                'musicUrl': music_url,
                'user_id': user_id
            },
            'error': None
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/api/music/<int:music_id>/like', methods=['POST'])
def like_music(music_id):
    # 로그인 확인
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'error': '로그인이 필요합니다.'
        }), 401

    try:
        user_id = session['user_id']

        # 이미 좋아요를 눌렀는지 확인 (실제 구현에서는 데이터베이스 검사)
        # 예시 코드:
        # already_liked = check_already_liked(user_id, music_id)
        # if already_liked:
        #     return jsonify({
        #         'success': False,
        #         'error': '이미 좋아요를 누른 음악입니다.'
        #     }), 409

        # 좋아요 추가 (실제 구현에서는 데이터베이스에 저장)
        # add_like(user_id, music_id)

        return jsonify({
            'success': True,
            'message': '좋아요가 추가되었습니다.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500