from flask import Blueprint, render_template

# 建立一個 Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title="首頁", message="hihi！")