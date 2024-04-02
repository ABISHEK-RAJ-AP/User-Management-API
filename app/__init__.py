import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
    db.init_app(app)
    JWTManager(app) 
    Migrate(app, db)
    
    with app.app_context():
     
        from . import models
        
 
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp)
      
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        return app
