from flask import *
from newcnn import *
import smtplib
from email.mime.text import MIMEText   
from flask_mail import Mail
from public import public
from user import user
from admin import admin
from doctor import doctor

app=Flask(__name__)
app.register_blueprint(public)
app.register_blueprint(user)
app.register_blueprint(admin)
app.register_blueprint(doctor)


mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'hariharan0987pp@gmail.com'
app.config['MAIL_PASSWORD'] = 'rjcbcumvkpqynpep'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


app.secret_key='JG'


app.run(debug=True,port=5005)
