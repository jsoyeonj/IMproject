from flask import Blueprint, jsonify, request, redirect, url_for, session, flash
import requests
import os
from werkzeug.utils import secure_filename

generate_query_bp = Blueprint('generate_query', __name__)

# 음악 생성 API URL (실제 API 주소로 변경 필요)
MUSIC_GENERATION_API = "http://your-api-url/api/generate-music"
IMAGE_UPLOAD_API = "http://your-api-url/api/upload-image"

# 파일 업로드 설정
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@generate_query_bp.route('/api/generate-music', methods=['POST'])
def generate_music():
    """사용자 입력 매개변수로 음악을 생성하는 API 엔드포인트"""
    try:
        # 폼 데이터 가져오기
        speed = request.form.get('speed', 50)
        mood = request.form.get('mood', '')
        place = request.form.get('place', '')
        str_prompt = request.form.get('str_prompt', '')

        # 매개변수 검증
        if not mood or not place:
            return jsonify({
                'success': False,
                'message': '모든 필수 항목을 입력해주세요.'
            }), 400

        # 로그인 상태 확인
        is_member = 'access_token' in session

        # API 요청 데이터 준비
        data = {
            "prompt1": f"속도가 {speed}%로 분위기가 {mood} 장소가 {place}인 음악",
            "prompt2": str_prompt
        }

        # API 헤더 설정
        headers = {}
        if is_member:
            headers['Authorization'] = f"Bearer {session['access_token']}"

        # 실제 구현에서는 외부 API 호출
        # response = requests.post(MUSIC_GENERATION_API, json=data, headers=headers)
        # result = response.json()

        # 테스트용 임시 응답
        result = {
            'success': True,
            'response': {
                'musicUrl': url_for('static', filename='audio/sample.mp3'),
                'musicId': 123,
                'title': f"{mood}한 {place} 음악"
            }
        }

        # 세션에 생성된 음악 URL 저장
        session['current_music_url'] = result['response']['musicUrl']
        session['current_music_id'] = result['response']['musicId']

        return jsonify(result), 200

    except Exception as e:
        print(f"음악 생성 오류: {e}")
        return jsonify({
            'success': False,
            'message': '음악 생성 중 오류가 발생했습니다.'
        }), 500


@generate_query_bp.route('/api/generate-music-member', methods=['POST'])
def generate_music_member():
    """회원 전용 음악 생성 API 엔드포인트"""
    # 로그인 상태 확인
    if 'access_token' not in session:
        return jsonify({
            'success': False,
            'message': '로그인이 필요한 서비스입니다.'
        }), 401

    # 일반 음악 생성과 동일한 로직 사용
    return generate_music()


@generate_query_bp.route('/api/upload-image', methods=['POST'])
def upload_image():
    """이미지를 업로드하고 음악을 생성하는 API 엔드포인트"""
    try:
        # 파일이 요청에 포함되어 있는지 확인
        if 'image' not in request.files:
            flash('이미지 파일이 없습니다.')
            return jsonify({
                'success': False,
                'message': '이미지 파일이 없습니다.'
            }), 400

        file = request.files['image']

        # 파일명이 비어있는지 확인
        if file.filename == '':
            flash('선택된 파일이 없습니다.')
            return jsonify({
                'success': False,
                'message': '선택된 파일이 없습니다.'
            }), 400

        # 파일 형식 검증
        if file and allowed_file(file.filename):
            # 안전한 파일명으로 변환
            filename = secure_filename(file.filename)

            # 업로드 폴더가 없으면 생성
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # 파일 저장
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # 로그인 상태 확인
            is_member = 'access_token' in session

            # API 헤더 설정
            headers = {}
            if is_member:
                headers['Authorization'] = f"Bearer {session['access_token']}"

            # 실제 구현에서는 multipart/form-data로 이미지 전송
            # with open(file_path, 'rb') as img_file:
            #     files = {'image': (filename, img_file)}
            #     response = requests.post(IMAGE_UPLOAD_API, files=files, headers=headers)
            #     result = response.json()

            # 테스트용 임시 응답
            result = {
                'success': True,
                'response': {
                    'musicUrl': url_for('static', filename='audio/image_generated.mp3'),
                    'musicId': 124,
                    'title': f"이미지 기반 음악"
                }
            }

            # 세션에 생성된 음악 URL 저장
            session['current_music_url'] = result['response']['musicUrl']
            session['current_music_id'] = result['response']['musicId']

            # 성공 응답
            return jsonify(result), 200
        else:
            # 잘못된 파일 형식
            return jsonify({
                'success': False,
                'message': '허용되지 않는 파일 형식입니다.'
            }), 400

    except Exception as e:
        print(f"이미지 업로드 오류: {e}")
        return jsonify({
            'success': False,
            'message': '이미지 처리 중 오류가 발생했습니다.'
        }), 500


@generate_query_bp.route('/api/loading-status', methods=['GET'])
def loading_status():
    """음악 생성 작업의 로딩 상태를 확인하는 API 엔드포인트"""
    # 실제 구현에서는 작업 ID를 통해 상태 확인
    # 예: Celery 작업 ID 또는 데이터베이스 저장 상태

    # 테스트용 임시 응답 (항상 완료됨)
    return jsonify({
        'success': True,
        'response': {
            'status': 'completed',
            'progress': 100
        }
    }), 200