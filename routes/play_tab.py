from flask import Blueprint, render_template, url_for
import urllib.parse

play_tab_bp = Blueprint('play_tab', __name__)

@play_tab_bp.route('/play-tab')
def play_tab():
    # 파일명 URL 인코딩을 명시적으로 처리
    filename = 'audio/sumu - apart [NCS Release].mp3'
    music_url = url_for('static', filename=filename)
    return render_template('components/play_tab.html', music_url=music_url)