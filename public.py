from flask import *
from database import *
import uuid
public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template("index.html")


@public.route('/login',methods=['get','post'])
def login():
	session.clear()
	if 'login' in request.form:
		username=request.form['uname']
		password=request.form['passwd']
		q="SELECT * FROM `login` WHERE `username`='%s' AND `password`='%s'"%(username,password)
		res=select(q)
		if not res:
			flash('INCORRECT USERNAME OR PASSWORD')
		if res:
			session['lid']=res[0]['login_id']
			if res[0]['usertype']=='admin':
				flash('WELCOME ADMIN')
				return redirect(url_for("admin.admin_home"))
			if res[0]['usertype']=='user':
				q="SELECT * FROM `users` WHERE `login_id`='%s'"%(res[0]['login_id'])
				res2=select(q)
				if res2:
					session['id']=res2[0]['user_id']
					flash('WELCOME TO USERS HOME')
					return redirect(url_for("user.user_home"))
			if res[0]['usertype']=='doctor':
				q="SELECT * FROM `doctor` WHERE `login_id`='%s'"%(res[0]['login_id'])
				res2=select(q)
				if res2:
					session['did']=res2[0]['doctor_id']
					flash('WELCOME TO DOCTOR HOME')
					return redirect(url_for("doctor.doctor_home"))
			
	return render_template("login.html")



@public.route('/user_Register',methods=['get','post'])
def user_Register():
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['place']
		phno=request.form['phno']
		email=request.form['email']
		uname=request.form['uname']
		pwd=request.form['pwd']
		q="SELECT * FROM `login` WHERE `username`='%s'"%(uname)
		res=select(q)
		if res:
			flash('USER NAME ALREADY EXIST')
			return redirect(url_for('public.user_Register'))
		else:
			q="INSERT INTO `login`(`username`,`password`,`usertype`) VALUES ('%s','%s','user')"%(uname,pwd)
			id=insert(q)
			q="INSERT INTO `users`(`login_id`,`firstname`,`lastname`,`place`,`phone`,`email`) VALUES ('%s','%s','%s','%s','%s','%s')"%(id,fname,lname,place,phno,email)
			insert(q)
			flash('REGISTERED')
			return redirect(url_for('public.user_Register'))
	return render_template('user_Register.html')


