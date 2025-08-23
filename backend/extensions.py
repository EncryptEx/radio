from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# singletons to be initialized by create_app
db = SQLAlchemy()
jwt = JWTManager()
