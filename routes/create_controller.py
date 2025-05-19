from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import requests  # API 요청을 위해 필요

create_controller_bp = Blueprint('create_controller', __name__)


@create_controller_bp.route('/create/controller', methods=['GET'])
def create_controller():
    """
    음악 생성 컨트롤러 페이지를 표시합니다.
    """
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
    """
    폼의 다음 단계로 이동합니다.
    """
    # 현재 단계의 데이터 저장
    speed = request.form.get('speed', 50)
    mood = request.form.get('mood', '')
    place = request.form.get('place', '')

    # 세션에 데이터 저장
    session['speed'] = int(speed)
    session['mood'] = mood
    session['place'] = place
    session['prompt_step'] = 2  # 다음 단계(2)로 설정

    return redirect(url_for('create_controller.create_controller'))


@create_controller_bp.route('/create/controller/generate', methods=['POST'])
def generate_music():
    """
    음악 생성 API를 호출합니다.
    """
    # 폼 데이터 가져오기
    speed = session.get('speed', 50)
    mood = session.get('mood', '')
    place = session.get('place', '')
    str_prompt = request.form.get('str_prompt', '')

    # 세션에 str_prompt 저장
    session['str_prompt'] = str_prompt

    # 사용자 로그인 상태 확인
    is_member = 'access_token' in session

    try:
        # API URL 설정 (실제 API URL로 변경 필요)
        api_url = "http://your-api-url/api/generate-music"

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

        if response.status_code == 200:
            result = response.json()
            # 생성된 음악 URL을 세션에 저장
            session['current_music_url'] = result.get('musicUrl', '')
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
        print(f"Error: {e}")
        return render_template('components/create_controller.html',
                               speed=speed,
                               mood=mood,
                               place=place,
                               str_prompt=str_prompt,
                               prompt_step=2,
                               error="서버 오류가 발생했습니다. 다시 시도해주세요.")