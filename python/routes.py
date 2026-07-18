from flask import Blueprint, render_template, send_from_directory

# 建立一個 Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory('../image', filename)