from flask import Blueprint, render_template, session, redirect, url_for

# 블루프린트 생성 (Flask에서 라우트를 모듈화하는 방법)
routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    # 사용자 로그인 상태 확인 (세션에서)
    is_member = session.get('is_member', False)
    return render_template('home.html', is_member=is_member)

@routes.route('/createGuest')
def create_guest():
    # 세션에 게스트 상태 저장 (추가)
    session['is_member'] = False
    return render_template('create_guest.html')

@routes.route('/createMember')
def create_member():
    # 로그인 상태 확인
    if 'user_id' not in session:
        # 로그인되지 않은 경우 홈페이지로 리디렉션
        return redirect(url_for('routes.home'))
    # 세션에 회원 상태 저장 (추가)
    session['is_member'] = True
    return render_template('create_member.html')

@routes.route('/createLike')
def create_like():
    # 실시간 생성 중인 음악 목록 가져오기
    play_list = get_play_list()

    # 인기 음악 목록 가져오기
    popular_play_list = get_popular_play_list()

    # 사용자 로그인 상태 확인
    is_member = 'user_id' in session

    return render_template('create_like.html',
                           play_list=play_list,
                           popular_play_list=popular_play_list,
                           is_member=is_member)

@routes.route('/createEnd')
def create_end():
    return render_template('create_end.html')

# 컴포넌트 부분 로드를 위한 라우트
@routes.route('/components/create_controller')
def create_controller_component():
    return render_template('components/create_controller.html')

@routes.route('/components/create_image')
def create_image_component():
    return render_template('components/create_image.html')

# 404 경로 - 나머지 모든 경로는 홈페이지로 리다이렉트
@routes.route('/<path:path>')
def catch_all(path):
    return render_template('home.html')

# 음악 목록 가져오기 함수
def get_play_list():
    # 여기에 실제 데이터베이스에서 음악 목록을 가져오는 코드를 구현
    # 예시 데이터:
    return [
        {
            'music_id': 1,
            'title': '신나는 음악 1',
            'like': 10,
            'pressed': False,
            'audio_url': '/static/audio/music1.mp3'
        },
        {
            'music_id': 2,
            'title': '감성적인 음악 2',
            'like': 15,
            'pressed': True,
            'audio_url': '/static/audio/music2.mp3'
        }
    ]

# 인기 음악 목록 가져오기 함수
def get_popular_play_list():
    # 여기에 실제 데이터베이스에서 인기 음악 목록을 가져오는 코드를 구현
    # 예시 데이터:
    return [
        {
            'music_id': 3,
            'title': '인기 음악 1',
            'like': 30,
            'pressed': False,
            'audio_url': '/static/audio/popular1.mp3'
        },
        {
            'music_id': 4,
            'title': '인기 음악 2',
            'like': 25,
            'pressed': True,
            'audio_url': '/static/audio/popular2.mp3'
        }
    ]