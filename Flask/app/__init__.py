from flask import Flask
from flask_mail import Mail
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import UPLOAD_FOLDER

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'flasktestiis@yandex.ru'
app.config['MAIL_PASSWORD'] = 'pobqwmpotcpwrytg'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import routes

