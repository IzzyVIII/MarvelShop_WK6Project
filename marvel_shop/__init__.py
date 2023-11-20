from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from .models import login_manager,db
from .blueprints.auth.routes import auth
from .blueprints.app.routes import site
from .blueprints.api.routes import api
from .helpers import JSONEncoder


# instantianting our Flask app
app = Flask(__name__)           # passing in the __name__ varieble which just takes the name of the folder we're in
app.config.from_object(Config)
jwt = JWTManager(app)           # allows our app to use JWTManager from anywhere (added security for our api routes)


login_manager.init_app(app)
login_manager.login_view = 'auth.sign_in'
login_manager.login_message = 'Hey you! Log in please!'
login_manager.login_message_category = 'Warning'

app.register_blueprint(auth)
app.register_blueprint(site)
app.register_blueprint(api)

db.init_app(app)
migrate = Migrate(app, db)
app.json_encoder = JSONEncoder  # we are not instantiating an object we are simply pointing to this class we made when we need to encode data objects
cors = CORS(app)        