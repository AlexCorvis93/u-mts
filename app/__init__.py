from flask import Flask
import os, config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.cli import FlaskGroup
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.BaseConfig')


db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)
cli = FlaskGroup(app)
images = UploadSet('images', IMAGES)
configure_uploads(app, [images])
from .views import index, equipment





