from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))


# DB 설정 임포트
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URL')
db = SQLAlchemy(app)
# 테이블 입갤
from api.model.chats import chats
from api.model.menues import menues
from api.model.sentences import sentences

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)
from api import main
