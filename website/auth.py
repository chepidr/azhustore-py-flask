from flask import Blueprint, render_template, request , current_app as app,url_for,flash
from flask_mail import Message,Mail
from twilio.rest import Client

account_sid='AC0036a5982372f4294b66251099677663'
account_auth='7e25d42e9e4281ea47faa5168ba75b47'
smsClient=Client(account_sid, account_auth)

auth=Blueprint('auth',__name__)

@auth.route('/logout')
def logout():
    return auth.mail

@auth.route('/sign', methods=['GET', 'POST'])
def sign():    
    if request.method == 'POST':
        email = request.form['email']
        token = serializer.dumps(email, salt='peoplewontbelieve')

        with app.app_context():
                mail=Mail(app)

        msg = Message('Подтвердите почту AZHUSTORE', sender='chepidr8@gmail.com', recipients=[email])

        link = url_for('auth.confirm_email', token=token, _external=True)

        msg.body = 'Перейдите по ссылке {}'.format(link)

        mail.send(msg)
    
    return render_template('sign.html')
    
    # if request.method=='POST':
    #     email=request.form['email']

    #     token=serializer.dumps(email, salt='peoplewontbelieve')

        

    #     msg=Message('Подвтердите почту AZHUSTORE', sender='chepidr13@gmail.com', recipients=[email])
    #     confirmationLink=url_for('confirm_email', token=token, _eternal=True)
    #     msg.body='Перейдите по этой ссылке {}'.format(confirmationLink)

    #     mail.send(msg)


    
    
    
@auth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email=serializer.loads(token, salt='peoplewontbelieve', max_age=3600)
    except SignatureExpired:
        return '<h1>Время токена истекло</h1>'
    except:
        return '<h1>Такого токена не существует</h1>'
    return '<h1>URA</h1>'