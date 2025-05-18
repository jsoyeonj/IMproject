from flask import Blueprint, render_template, session

# 블루프린트 생성 (Flask에서 라우트를 모듈화하는 방법)
routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    # 사용자 로그인 상태 확인 (세션에서)
    is_member = session.get('is_member', False)
    return render_template('home.html', is_member=is_member)

@routes.route('/createMember')
def create_member():
    return render_template('create_member.html')

@routes.route('/createGuest')
def create_guest():
    return render_template('create_guest.html')

@routes.route('/createLike')
def create_like():
    return render_template('create_like.html')

@routes.route('/createEnd')
def create_end():
    return render_template('create_end.html')

# 404 경로 - 나머지 모든 경로는 홈페이지로 리다이렉트
@routes.route('/<path:path>')
def catch_all(path):
    return render_template('home.html')


@routes.route('/createMember')
def create_member():
    # 로그인 상태 확인
    if 'user_id' not in session:
        # 로그인되지 않은 경우 홈페이지로 리디렉션
        return redirect(url_for('routes.home'))

    return render_template('create_member.html')
@routes.route('/createGuest')
def create_guest():
    return render_template('create_guest.html')