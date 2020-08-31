from the_app import login_manager
from flask import render_template, Blueprint, flash,redirect, url_for, request, escape
from flask_login import  login_required, current_user  , login_user , UserMixin, logout_user
from the_app._authorisation.forms import LoginForm, RegistrationForm,UpdateUserForm
from the_app._authorisation.models import NewUser, addNewUser, authenticate_user, loader_user


authBP=Blueprint('authBP',__name__,template_folder='templates')

@login_manager.user_loader
def load_user(user_id):
    user=loader_user(user_id)
    user_auth = User(id=user[0],email=user[1],username=user[2],role=user[3],password=user[4])
    return user_auth

class User(UserMixin):
    def __init__(self, id, email, username, role,password):
        self.id=id
        self.email=email
        self.username=username
        self.role=role
        self.password=password

    def get_id(self):
        return self.email



@authBP.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        u_remote_addr = request.remote_addr
        u_agent = escape(request.user_agent)

        user = authenticate_user(email = form.email.data,password = form.password.data, user_remote_addr=u_remote_addr,user_agent=u_agent) 
        if user is not None:
            user_auth= User(id=user[0],email=user[1],username=user[2],role=user[3],password=user[4])
            login_user(user_auth)
            #flash('Log in Success!')

            next=request.args.get('next')
            if next==None or not next[0]=='/':
                next=url_for('coreBP.home')
            
            return redirect(next)
        else:
            return redirect(url_for('authBP.bad_login'))
        return redirect(url_for('authBP.bad_login'))

    return render_template('login.html', form=form)


@authBP.route('/register', methods=['GET','POST'])
def register():
    form=RegistrationForm()

    if form.validate_on_submit():

        check_point=addNewUser(email=form.email.data, username=form.username.data, password=form.password.data)
        if check_point.overall_result==True:     
            flash('Thanks for registration!')
            return redirect(url_for('authBP.login'))
        else:
            #flash("Upss, coś poszło nie tak!")
            if check_point.email_exists==True:  
                flash("Taki e-mail już istnieje w naszej bazie!")

            if check_point.username_exists==True:  
                flash("Taki użytkownik już istnieje w naszej bazie!")
            
            return redirect(url_for('authBP.register'))

    return render_template ('register.html', form=form)

@authBP.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('coreBP.index'))

@authBP.route('/bad_login')
def bad_login():
    return render_template('login_bad.html')
