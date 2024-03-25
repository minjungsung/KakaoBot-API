from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import api.config.config as conf
from flask_migrate import Migrate


app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))


# DB 설정 임포트
app.config["SQLALCHEMY_DATABASE_URI"] = conf.DB_url
db = SQLAlchemy(app)
# 테이블 입갤
from api.model.chats import chats
from api.model.menues import menues
from api.model.sentences import sentences
from api.model.enhancement_game import enhancement_game
from api.model.enhancement_guiness import enhancement_guiness
from api.model.enhancement_history import enhancement_history

with app.app_context():
    db.create_all()

migrate = Migrate(app, db)
from api.main import main
