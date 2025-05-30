from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import json
import uuid
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# 설정
UPLOAD_FOLDER = 'uploads'
MUSIC_DATA_FILE = 'data/music_data.json'

# 폴더 생성
for folder in [UPLOAD_FOLDER, 'data', 'static/music']:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_music_data():
    """음악 데이터 로드"""
    if os.path.exists(MUSIC_DATA_FILE):
        with open(MUSIC_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_music_data(data):
    """음악 데이터 저장"""
    with open(MUSIC_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/create')
def create():
    """음악 생성 페이지"""
    return render_template('create.html')


@app.route('/generate-music', methods=['POST'])
def generate_music():
    """기본 설정 저장"""
    try:
        data = request.get_json()

        if not data or 'mood' not in data or 'location' not in data:
            return jsonify({
                'success': False,
                'error': '분위기와 장소를 선택해주세요'
            }), 400

        # 세션에 설정 저장
        session['music_settings'] = {
            'speed': data.get('speed', 50),
            'mood': data.get('mood'),
            'location': data.get('location')
        }

        temp_id = str(uuid.uuid4())

        return jsonify({
            'success': True,
            'music_id': temp_id,
            'next_step': url_for('detail_input', music_id=temp_id)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'서버 오류: {str(e)}'
        }), 500


@app.route('/detail-input')
def detail_input():
    """상세 입력 페이지"""
    music_id = request.args.get('music_id', '')
    return render_template('detail_input.html', music_id=music_id)


@app.route('/generate-music-with-detail', methods=['POST'])
def generate_music_with_detail():
    """최종 음악 생성"""
    try:
        data = request.get_json()

        if 'detail_text' not in data:
            return jsonify({
                'success': False,
                'error': '상세 내용을 입력해주세요'
            }), 400

        detail_text = data.get('detail_text')
        music_settings = session.get('music_settings', {})

        # 음악 데이터 생성
        music_id = str(uuid.uuid4())
        new_music = {
            'id': music_id,
            'title': detail_text[:30] + ('...' if len(detail_text) > 30 else ''),
            'mood': music_settings.get('mood', ''),
            'location': music_settings.get('location', ''),
            'speed': music_settings.get('speed', 50),
            'detail_text': detail_text,
            'created_at': datetime.datetime.now().isoformat(),
            'file_path': f'music_{music_id}.mp3'
        }

        # 데이터 저장
        music_list = load_music_data()
        music_list.append(new_music)
        save_music_data(music_list)

        # 세션 정리
        session.pop('music_settings', None)

        return jsonify({
            'success': True,
            'music_id': music_id,
            'redirect_url': url_for('generation_complete', music_id=music_id)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'서버 오류: {str(e)}'
        }), 500


@app.route('/generation-complete')
def generation_complete():
    """음악 생성 완료 페이지"""
    music_id = request.args.get('music_id', '')
    return render_template('generation_complete.html', music_id=music_id)


@app.route('/image-create')
def image_create():
    """이미지로 음악 생성 페이지"""
    mode = request.args.get('mode', 'image')  # image 또는 video
    return render_template('image_create.html', mode=mode)


@app.route('/generate-music-from-image', methods=['POST'])
def generate_music_from_image():
    """이미지 기반 음악 생성"""
    try:
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': '이미지 파일이 필요합니다'
            }), 400

        file = request.files['image']

        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': '올바른 이미지 파일을 선택해주세요'
            }), 400

        # 파일 저장
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # 음악 데이터 생성
        music_id = str(uuid.uuid4())
        new_music = {
            'id': music_id,
            'title': f'이미지 음악 {datetime.datetime.now().strftime("%H:%M")}',
            'mood': '이미지 기반',
            'location': '이미지',
            'source_file': filename,
            'created_at': datetime.datetime.now().isoformat(),
            'file_path': f'music_{music_id}.mp3'
        }

        music_list = load_music_data()
        music_list.append(new_music)
        save_music_data(music_list)

        return jsonify({
            'success': True,
            'music_id': music_id,
            'redirect_url': url_for('generation_complete', music_id=music_id)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'서버 오류: {str(e)}'
        }), 500


@app.route('/generate-music-from-video', methods=['POST'])
def generate_music_from_video():
    """동영상 기반 음악 생성"""
    try:
        if 'video' not in request.files:
            return jsonify({
                'success': False,
                'error': '동영상 파일이 필요합니다'
            }), 400

        file = request.files['video']

        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': '올바른 동영상 파일을 선택해주세요'
            }), 400

        # 파일 저장
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # 음악 데이터 생성
        music_id = str(uuid.uuid4())
        new_music = {
            'id': music_id,
            'title': f'동영상 음악 {datetime.datetime.now().strftime("%H:%M")}',
            'mood': '동영상 기반',
            'location': '동영상',
            'source_file': filename,
            'created_at': datetime.datetime.now().isoformat(),
            'file_path': f'music_{music_id}.mp3'
        }

        music_list = load_music_data()
        music_list.append(new_music)
        save_music_data(music_list)

        return jsonify({
            'success': True,
            'music_id': music_id,
            'redirect_url': url_for('generation_complete', music_id=music_id)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'서버 오류: {str(e)}'
        }), 500


@app.route('/playlist')
def playlist():
    """플레이리스트 페이지"""
    music_list = load_music_data()
    # 최신순으로 정렬
    music_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return render_template('playlist.html', music_list=music_list)


@app.route('/play/<music_id>')
def play_music(music_id):
    """음악 재생 (데모용)"""
    return jsonify({
        'success': True,
        'url': url_for('static', filename='audio/demo.mp3'),
        'message': '데모 음악이 재생됩니다'
    })


# 에러 핸들러
@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '서버 내부 오류가 발생했습니다'}), 500


if __name__ == '__main__':
    print("🎵 IM Mobile 서버 시작!")
    print("📱 모바일에서 접속: http://[컴퓨터IP]:5000")
    print("💻 로컬에서 접속: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)