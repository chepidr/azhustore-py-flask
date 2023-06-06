from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

database=SQLAlchemy()
DB_NAME='azhustore-database.db'
login_manager=LoginManager()

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='asdaibaraibar'

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=465
    app.config['MAIL_USERNAME']='chepidr8@gmail.com'
    app.config['MAIL_PASSWORD']='lerpkrioslbkbofa'
    app.config['MAIL_USE_TLS']=False
    app.config['MAIL_USE_SSL']=True

    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'

    database.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.sign'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User,User_address,Address,Country,User_payment_method,Payment_type,Shopping_cart,Shopping_cart_item,Product,Product_item,Product_category,Product_image,Variation,Variation_option,Shop_order,Shipping_method,Order_status,Order_line,User_review 

    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/'+DB_NAME):
        with app.app_context():
            database.create_all()
        print('Database created!')