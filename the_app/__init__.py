from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY']='mysecret'

##############################################
### DATABASE SETUP ###
##############################################
# basedir=os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db=SQLAlchemy(app)
# Migrate(app,db)
##############################################


##############################################
### LOGIN CONFIG ###
##############################################
login_manager = LoginManager() #login manager object creation
login_manager.init_app(app) # paasing app to login manager
login_manager.login_view='authBP.login' #tell users what view to go to login , need to be creATED AND REGISTERED BLUPORINT FOR  USER -> LOGIN
##############################################




##############################################
### BLUEPRINT REGISTRATION ###
##############################################
from the_app._core.views import coreBP
app.register_blueprint(coreBP)

from the_app._authorisation.views import authBP
app.register_blueprint(authBP)

from the_app._losowa.views import losowaBP
app.register_blueprint(losowaBP)

from the_app._bank.views import bankBP
app.register_blueprint(bankBP)



# from puppycompanyblog.error_pages.handlers import error_pages
# app.register_blueprint(error_pages)

# from puppycompanyblog.users.views import users # blueprint zdefiniowany w user\views\ => users = Blueprint('users',__name__)
# app.register_blueprint(users)


