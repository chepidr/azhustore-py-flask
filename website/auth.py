from flask import Blueprint, render_template, request, current_app as app, url_for, flash,redirect
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
import re
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import database
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

serializer=URLSafeTimedSerializer('aibar12341234')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', category='error')
    return redirect(url_for('auth.sign'))


@auth.route('/sign', methods=['GET', 'POST'])
def sign():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        signType = request.form['sign_type']

        if signType == 'sign_up':
            name = request.form['name']
            email = request.form['email']
            phone = re.sub(r'[^0-9]', '', request.form['phone'])
            password = request.form['password']
            confirmedPassword = request.form['confirm_password']

            user = User.query.filter_by(email=email).first()
            if user:
                flash('Аккаунт с такой почтой уже существует.', category='error') 
            elif len(password) < 5:
                flash('Пароль должен быть не менее 5 символов', category='error')
            elif len(phone) != 11:
                flash('Неправильный телефон.', category='error')
            elif len(name) < 1:
                flash('Имя должно быть не меньше 1 символа.', category='error')
            elif password != confirmedPassword:
                flash('Пароли не совпадают.', category='error')
            else:
                hashedPassword=generate_password_hash(password,method='sha256',salt_length=8)

                newUser=User(email=email,name=name,phone=phone,password=hashedPassword)

                database.session.add(newUser)
                database.session.commit()
                login_user(user, remember=True)

                sendConfirmationTokenToEmail(email)

                flash('Проверьте свою почту и подтвердите ее.', category='success')
                return redirect(url_for('views.home'))

        elif signType=='sign_in':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Вы успешно вошли в аккаунт!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Неправильный пароль попробуйте снова или сбросьте пароль.', category='error')
            else:
                flash('Аккаунта с такой почтой не существует.', category='error')

    return render_template('sign.html')


@auth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email=serializer.loads(token, salt='peoplewontbelieve', max_age=3600)
        user = User.query.filter_by(email=email).first_or_404()
        if user.email_confirmed:
            flash('Аккаунт уже подтвержден.', 'success')
            return redirect(url_for('auth.sign'))
        else:
            confirmUserEmail(user)

            flash('Вы подтвердили свой аккаунт и успешно вошли в него. Спасибо!', 'success')
            return redirect(url_for('views.home'))
    except SignatureExpired:
        flash('Время токена истекло.', 'error')
        return redirect(url_for('auth.sign'))
    except:
        flash('Такого токена не существует.', 'error')
        return redirect(url_for('auth.sign'))
    

@auth.route('/reset',methods=['GET','POST'])
def reset():
    if current_user.is_authenticated:
        flash('Вы уже вошли в аккаунт.', 'error')
        return redirect(url_for('views.home'))
    if request.method=='POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            sendResetTokenToEmail(email)
            flash('Проверьте свою почту для сброса пароля.', category='success')
        else:
            flash('Аккаунта с такой почтой не существует.', category='error')
    return render_template('reset.html')


@auth.route('/reset-password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash('Вы уже вошли в аккаунт.', 'error')
        return redirect(url_for('views.home'))
    if request.method=='POST':
        try:
            newPassword = request.form['password']

            email=serializer.loads(token, salt='peoplebillbelieve', max_age=3600)
            user = User.query.filter_by(email=email).first_or_404()
            
            resetUserPasswordAndConfirmEmail(user,newPassword)

            login_user(user, remember=True)

            flash('Вы подтвердили свой аккаунт, сбросили пароль и успешно вошли в него. Спасибо!', 'success')
            return redirect(url_for('views.home'))
        except SignatureExpired:
            flash('Время токена истекло.', 'error')
            return redirect(url_for('auth.sign'))
        except:
            flash('Такого токена не существует.', 'error')
            return redirect(url_for('auth.sign'))
    return render_template('reset-password.html')


def sendConfirmationTokenToEmail(email):
    token=generateConfirmationToken(email)

    with app.app_context():
        mail = Mail(app)

    message = Message('Подтвердите почту AZHUSTORE', sender='chepidr8@gmail.com', recipients=[email])

    link = url_for('auth.confirm_email', token=token, _external=True)

    message.body = '''Перейдите по ссылке для подтверждения почты 
    {}
    
    Если этот запрос был сделан не вами, просто проигнорируйте это сообщение'''.format(link)

    mail.send(message)

def sendResetTokenToEmail(email):
    token=generateResetToken(email)

    with app.app_context():
        mail = Mail(app)

    message = Message('Подтвердите почту AZHUSTORE', sender='chepidr8@gmail.com', recipients=[email])

    link = url_for('auth.reset_password', token=token, _external=True)

    message.body = '''Перейдите по ссылке для сброса пароля
    {}
    
    Если этот запрос был сделан не вами, то просто проигнорируйте это сообщение'''.format(link)

    mail.send(message)

def generateConfirmationToken(email):
    token = serializer.dumps(email, salt='peoplewontbelieve')
    return token

def generateResetToken(email):
    token = serializer.dumps(email, salt='peoplebillbelieve')
    return token

def resetUserPasswordAndConfirmEmail(user,password):
    hashedPassword=generate_password_hash(password,method='sha256',salt_length=8)
    user.password = hashedPassword
    if user.email_confirmed:
        pass
    else:
        user.email_confirmed=True
        user.email_confirm_date = datetime.now()
    database.session.add(user)
    database.session.commit()

def confirmUserEmail(user):
    user.email_confirmed = True
    user.email_confirm_date = datetime.now()
    database.session.add(user)
    database.session.commit()