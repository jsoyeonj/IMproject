from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import requests  # API 요청을 위해 필요

create_controller_bp = Blueprint('create_controller', __name__)


# useGenerate.ts에서 가져온 추가 기능
def initialize_session():
    """세션 초기화 함수"""
    if 'speed' not in session:
        session['speed'] = 0
    if 'mood' not in session:
        session['mood'] = ''
    if 'place' not in session:
        session['place'] = ''
    if 'str_prompt' not in session:
        session['str_prompt'] = ''
    if 'is_loading' not in session:
        session['is_loading'] = False
    if 'on_next_step' not in session:
        session['on_next_step'] = False


def get_prompt_state():
    """현재 프롬프트 상태 반환"""
    initialize_session()
    return {
        'speed': session.get('speed', 0),
        'mood': session.get('mood', ''),
        'place': session.get('place', ''),
        'str_prompt': session.get('str_prompt', '')
    }


def update_prompt_state(speed=None, mood=None, place=None, str_prompt=None):
    """프롬프트 상태 업데이트"""
    if speed is not None:
        session['speed'] = int(speed)
    if mood is not None:
        session['mood'] = mood
    if place is not None:
        session['place'] = place
    if str_prompt is not None:
        session['str_prompt'] = str_prompt
    session.modified = True


def set_music_url_local_storage(music_url):
    """음악 URL을 세션에 저장"""
    session['current_music_url'] = music_url
    session.modified = True


def fetch_play_list():
    """재생 목록 가져오기"""
    try:
        # 실제 API 연동으로 대체 필요
        # response = get_play_list()
        response = []  # 임시 빈 목록
        return response
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        return []


def ready_on_next_step():
    """다음 단계로 진행 가능한지 확인"""
    prompt_state = get_prompt_state()
    speed = prompt_state['speed']
    mood = prompt_state['mood']
    place = prompt_state['place']

    if speed == 0 or not mood or not place:
        session['on_next_step'] = False
    else:
        session['on_next_step'] = True

    session.modified = True
    return session['on_next_step']


def handle_image_upload(form_data):
    """이미지 업로드를 통한 음악 생성"""
    try:
        # 로딩 상태 설정
        session['is_loading'] = True

        # API 호출 (실제 연동 필요)
        # response = post_form_data(form_data)
        response = {"success": True, "response": {"musicUrl": "/static/audio/sample.mp3"}}  # 임시 응답

        if response.get('success'):
            # 음악 URL 저장
            music_url = response.get('response', {}).get('musicUrl')
            set_music_url_local_storage(music_url)

            # 로딩 상태 해제
            session['is_loading'] = False

            return jsonify({
                "success": True,
                "message": "음악이 성공적으로 생성되었습니다.",
                "redirect": "/create-end"
            })
        else:
            # 로딩 상태 해제
            session['is_loading'] = False
            return jsonify({"error": "이미지 업로드에 실패했습니다."}), 500

    except Exception as e:
        # 로딩 상태 해제
        session['is_loading'] = False
        return jsonify({"error": "이미지 업로드에 실패했습니다.", "details": str(e)}), 500


# 기존 라우트 함수들
@create_controller_bp.route('/create/controller', methods=['GET'])
def create_controller():
    """음악 생성 컨트롤러 페이지를 표시합니다."""
    # 세션 초기화
    initialize_session()

    # 세션에서 값을 가져오거나 기본값을 설정
    speed = session.get('speed', 50)
    mood = session.get('mood', '')
    place = session.get('place', '')
    str_prompt = session.get('str_prompt', '')
    prompt_step = session.get('prompt_step', 1)

    return render_template('components/create_controller.html',
                           speed=speed,
                           mood=mood,
                           place=place,
                           str_prompt=str_prompt,
                           prompt_step=prompt_step)


@create_controller_bp.route('/create/controller/next-step', methods=['POST'])
def next_step():
    """폼의 다음 단계로 이동합니다."""
    # 현재 단계의 데이터 저장
    speed = request.form.get('speed', 50)
    mood = request.form.get('mood', '')
    place = request.form.get('place', '')

    # 세션에 데이터 저장
    update_prompt_state(speed=speed, mood=mood, place=place)
    session['prompt_step'] = 2  # 다음 단계(2)로 설정

    return redirect(url_for('create_controller.create_controller'))


@create_controller_bp.route('/create/controller/generate', methods=['POST'])
def generate_music():
    """음악 생성 API를 호출합니다."""
    # 폼 데이터 가져오기
    prompt_state = get_prompt_state()
    speed = prompt_state['speed']
    mood = prompt_state['mood']
    place = prompt_state['place']
    str_prompt = request.form.get('str_prompt', '')

    # 세션에 str_prompt 저장
    update_prompt_state(str_prompt=str_prompt)

    # 사용자 로그인 상태 확인
    is_member = 'access_token' in session

    try:
        # 필수 입력값 확인
        if speed == 0 or not mood or not place:
            return render_template('components/create_controller.html',
                                   speed=speed,
                                   mood=mood,
                                   place=place,
                                   str_prompt=str_prompt,
                                   prompt_step=2,
                                   error="모든 항목을 입력해주세요.")

        # 로딩 상태 설정
        session['is_loading'] = True

        # 백엔드 API URL 설정
        api_url = "http://127.0.0.1:5000/api/generate-music"

        # API 요청 데이터
        data = {
            'speed': speed,
            'mood': mood,
            'place': place,
            'strPrompt': str_prompt
        }

        # 로그인 상태에 따라 다른 헤더 설정
        headers = {}
        if is_member:
            headers['Authorization'] = f"Bearer {session['access_token']}"

        # API 호출
        response = requests.post(api_url, json=data, headers=headers)

        # 로딩 상태 해제
        session['is_loading'] = False

        if response.status_code == 200:
            result = response.json()
            # 생성된 음악 URL을 세션에 저장
            set_music_url_local_storage(result.get('musicUrl', ''))
            # 음악 생성 완료 페이지로 리다이렉트
            return redirect(url_for('routes.create_end'))
        else:
            # API 오류 처리
            return render_template('components/create_controller.html',
                                   speed=speed,
                                   mood=mood,
                                   place=place,
                                   str_prompt=str_prompt,
                                   prompt_step=2,
                                   error="음악 생성에 실패했습니다. 다시 시도해주세요.")

    except Exception as e:
        # 로딩 상태 해제
        session['is_loading'] = False
        print(f"Error: {e}")
        return render_template('components/create_controller.html',
                               speed=speed,
                               mood=mood,
                               place=place,
                               str_prompt=str_prompt,
                               prompt_step=2,
                               error="서버 오류가 발생했습니다. 다시 시도해주세요.")


# 이미지 업로드로 음악 생성하는 라우트 추가
@create_controller_bp.route('/create/controller/generate-by-image', methods=['POST'])
def generate_music_by_image():
    """이미지 업로드를 통한 음악 생성"""
    # 이미지 파일 확인
    if 'image' not in request.files:
        return jsonify({"error": "이미지 파일이 없습니다."}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({"error": "선택된 파일이 없습니다."}), 400

    # 폼 데이터 생성
    form_data = {'image': image_file}

    # 이미지 처리 및 음악 생성
    return handle_image_upload(form_data)


# API 엔드포인트 추가
@create_controller_bp.route('/api/prompt-state', methods=['GET'])
def get_prompt_state_api():
    """프롬프트 상태를 JSON으로 반환"""
    return jsonify(get_prompt_state())


@create_controller_bp.route('/api/set-speed', methods=['POST'])
def set_speed_api():
    """속도 설정 API"""
    data = request.json
    update_prompt_state(speed=data.get('speed'))
    return jsonify({"success": True})


@create_controller_bp.route('/api/set-mood', methods=['POST'])
def set_mood_api():
    """분위기 설정 API"""
    data = request.json
    update_prompt_state(mood=data.get('mood'))
    return jsonify({"success": True})


@create_controller_bp.route('/api/set-place', methods=['POST'])
def set_place_api():
    """장소 설정 API"""
    data = request.json
    update_prompt_state(place=data.get('place'))
    return jsonify({"success": True})


@create_controller_bp.route('/api/set-str-prompt', methods=['POST'])
def set_str_prompt_api():
    """추가 텍스트 설정 API"""
    data = request.json
    update_prompt_state(str_prompt=data.get('strPrompt'))
    return jsonify({"success": True})


@create_controller_bp.route('/api/ready-next-step', methods=['GET'])
def check_next_step():
    """다음 단계 확인 API"""
    ready = ready_on_next_step()
    return jsonify({"ready": ready})