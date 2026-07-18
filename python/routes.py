from flask import Blueprint, render_template, send_from_directory

# 建立一個 Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/LED')
def led():
    return render_template('LED.html')

@main_bp.route('/willy')
def willy():
    return render_template('willy.html')

@main_bp.route('/hsiang')
def hsiang():
    return render_template('hsiang.html')

@main_bp.route('/yuwei')
def yuwei():
    return render_template('yuwei.html')

@main_bp.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory('../image', filename)

