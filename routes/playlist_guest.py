from flask import Blueprint, render_template

playlist_guest_bp = Blueprint('playlist_guest', __name__)

@playlist_guest_bp.route('/playlist/guest')
def playlist_guest():
    return render_template('components/play_list_guest.html')