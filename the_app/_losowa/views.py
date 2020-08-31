from flask import render_template, redirect, url_for, flash, request, Blueprint,session
from flask_login import  current_user,  login_required
from the_app._losowa.forms import LosowaForm
import random
from the_app._losowa.models import The_game


#from gmportal import db
#from gmportal.models import User  #, BlogPost
#from gmportal._users.forms import RegistrationForm, LoginForm, UpdateUserForm
#from puppycompanyblog.users.picture_handler import add_profile_pic

losowaBP = Blueprint('losowaBP',__name__,template_folder='templates')

@losowaBP.route('/prelosowa',  methods=['GET', 'POST'])
@login_required
def prelosowa():
    rnd_num=random.randint(1,100)
    game=The_game(rnd_num=rnd_num,current_result='',actual_turn='',i=0,result_pile=[],game_ending=False)
    #zapisac do sesji
    session['game_json']=game.to_json()
    return redirect(url_for('losowaBP.losowa'))


@losowaBP.route('/losowa',  methods=['GET', 'POST'])
@login_required
def losowa():
    form = LosowaForm()
    
    game_json=session['game_json']
    game=The_game(rnd_num=game_json['rnd_num'],current_result=game_json['current_result'],actual_turn=game_json['actual_turn'],i=game_json['i'],result_pile=game_json['result_pile'],game_ending=game_json['game_ending'])


    w2="To jest w2 super"
    

    if form.validate_on_submit():
        n=form.input_value.data
        try:
            i=int(n)
            game.go_turn(n)
            warn_msg=''
        except ValueError:
            form.input_value.data='0'
            game.go_turn(4021)
            warn_msg='NIWŁAŚCIWA WARTOŚĆ - MUSI BYĆ LICZBA POMIEDZY 1 a 100'
            

        form.input_value.data=''
        session['game_json']=game.to_json()
        return render_template('losowa.html', form=form, current_result=game.current_result,  actual_turn=game.actual_turn,game_ending=game.game_ending,list_of_turns=game.result_pile, warn_msg=warn_msg)

    return render_template('losowa.html', form=form)