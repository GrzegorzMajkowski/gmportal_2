from flask import render_template, Blueprint
from flask_login import  login_required, current_user  

coreBP=Blueprint('coreBP',__name__,template_folder='templates')

@coreBP.route('/')
def index():
    return render_template('index.html')

@coreBP.route('/home')
@login_required
def home():
    return render_template('index_auth.html', username=current_user.username, role=current_user.role)