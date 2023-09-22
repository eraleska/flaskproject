import os

# basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will not pass'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/db_for_flask"


UPLOAD_FOLDER = 'app/static/images/'
