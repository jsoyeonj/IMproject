from flask import Blueprint, render_template, session, redirect, url_for

create_like_bp = Blueprint('create_like', __name__)

@create_like_bp.route('/createLike')
def create_like():
    """
    좋아요 음악 목록 페이지 렌더링
    """
    return render_template('components/create_like.html')