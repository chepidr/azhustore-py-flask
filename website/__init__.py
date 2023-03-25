from flask import Flask
from flask_mail import Message,Mail


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='asdaibaraibar'

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=465
    app.config['MAIL_USERNAME']='chepidr8@gmail.com'
    app.config['MAIL_PASSWORD']='lerpkrioslbkbofa'
    app.config['MAIL_USE_TLS']=False
    app.config['MAIL_USE_SSL']=True

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app