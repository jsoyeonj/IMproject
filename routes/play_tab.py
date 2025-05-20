from flask import Blueprint, render_template, url_for, session

play_tab_bp = Blueprint('play_tab', __name__)


@play_tab_bp.route('/play-tab')
def play_tab():
    # 세션에서 현재 음악 정보 가져오기
    current_music_url = session.get('current_music_url', '')
    current_music_id = session.get('current_music_id', 0)

    # 세션에 음악 URL이 없으면 기본값 설정
    if not current_music_url:
        filename = 'audio/sumu - apart [NCS Release].mp3'
        current_music_url = url_for('static', filename=filename)

    return render_template('components/play_tab.html',
                           music_url=current_music_url,
                           music_id=current_music_id)


# 특정 음악을 재생하기 위한 추가 라우트 (선택 사항)
@play_tab_bp.route('/play-tab/<int:music_id>')
def play_specific_tab(music_id):
    # 여기서는 music_id를 기반으로 데이터베이스에서 음악 정보를 조회하는 로직이 필요함
    # 예시 코드:
    # music = Music.query.get(music_id)
    # if music:
    #     music_url = music.music_url
    # else:
    #     music_url = ''

    # 테스트용 임시 코드
    music_url = url_for('static', filename='audio/sumu - apart [NCS Release].mp3')

    # 세션에 현재 음악 정보 저장
    session['current_music_id'] = music_id
    session['current_music_url'] = music_url

    return render_template('components/play_tab.html',
                           music_url=music_url,
                           music_id=music_id)