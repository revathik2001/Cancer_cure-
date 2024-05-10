from flask import *
from database import *
import uuid

import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
admin=Blueprint('admin',__name__)

@admin.route('/admin_home',methods=['get','post'])
def admin_home():
	if not session.get("lid") is None:
		data={}
		return render_template("admin_home.html",data=data)
	else:
		return redirect(url_for('public.login'))

@admin.route('/admin_Manage_cancer',methods=['get','post'])
def admin_Manage_cancer():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `alzimers` ORDER BY `alzimers_id` DESC"
		data['alz']=select(q)
		if 'submit' in request.form:
			name=request.form['name']
			det=request.form['det']
			q="INSERT INTO `alzimers` (`alzimers`,`details`) VALUES ('%s','%s')"%(name,det)
			insert(q)
			flash('CANCER PROBLEM ADDED')
			return redirect(url_for('admin.admin_Manage_cancer'))
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='delete':
			q="DELETE FROM `alzimers` WHERE `alzimers_id`='%s'"%(id)
			delete(q)
			flash('DELETED')
			return redirect(url_for('admin.admin_Manage_cancer'))
		if action=='update':
			q="SELECT * FROM `alzimers` WHERE `alzimers_id`='%s'"%(id)
			data['al_up']=select(q)
		if 'updatez' in request.form:
			name=request.form['name']
			det=request.form['det']
			q="update alzimers set alzimers='%s',details='%s' where alzimers_id='%s'"%(name,det,id)
			update(q)
			flash('UPDATED')
			return redirect(url_for('admin.admin_Manage_cancer'))
		return render_template("admin_Manage_cancer.html",data=data)
	else:
		return redirect(url_for('public.login'))






@admin.route('/admin_Add_symptoms',methods=['get','post'])
def admin_Add_symptoms():
	if not session.get("lid") is None:
		data={}
		id=request.args['id']
		if 'submit' in request.form:
			sym=request.form['sym']
			q="INSERT INTO `symptoms`  (`alzimers_id`,`symptoms`) VALUES ('%s','%s')"%(id,sym)
			insert(q)
			flash('SYMPTOMS ADDED')
			return redirect(url_for('admin.admin_Add_symptoms',id=id))
		q="SELECT * FROM `symptoms` WHERE `alzimers_id`='%s' ORDER BY `symptom_id` DESC"%(id)
		data['sym']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			did=request.args['did']
		else:
			action=None
		if action=='delete':
			q="DELETE FROM `symptoms` WHERE `symptom_id`='%s'"%(did)
			delete(q)
			flash('DELETED')
			return redirect(url_for('admin.admin_Add_symptoms',id=id))
		if action=='update':
			q="select * from symptoms where symptom_id='%s'"%(did)
			data['up']=select(q)
		if 'update' in request.form:
			sym=request.form['sym']
			q="update symptoms set symptoms='%s' where symptom_id='%s'"%(sym,did)
			update(q)
			return redirect(url_for('admin.admin_Manage_cancer'))

		return render_template("admin_Add_symptoms.html",data=data)
	else:
		return redirect(url_for('public.login'))






@admin.route('/admin_View_predicted_output',methods=['get','post'])
def admin_View_predicted_output():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`firstname`,' ',`lastname`) AS `user` FROM `prediction` INNER JOIN `users` USING (`user_id`) ORDER BY `prediction_id` DESC"
		data['pre']=select(q)
		return render_template("admin_View_predicted_output.html",data=data)
	else:
		return redirect(url_for('public.login'))






@admin.route('/admin_View_rating',methods=['get','post'])
def admin_View_rating():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`firstname`,' ',`lastname`) AS `user` FROM `rating` INNER JOIN `users` USING (`user_id`) ORDER BY `rating_id` DESC"
		data['rate']=select(q)
		return render_template("admin_View_rating.html",data=data)
	else:
		return redirect(url_for('public.login'))

@admin.route('/admin_view_appointment',methods=['get','post'])
def admin_view_appointment():

	data={}
	q="SELECT * FROM `appointment` INNER JOIN `users` USING(`user_id`) ORDER by appoin_date asc"
	print(q)
	data['view']=select(q)

	if 'action' in request.args:
		action=request.args['action']
		appointment_id=request.args['appointment_id']
	else:
		action=None

	if action=='accept':
		q="UPDATE `appointment` SET `appoin_status`='accept your appoinment' WHERE `appointment_id`='%s' "%(appointment_id)
		print(q)
		update(q)
		return redirect(url_for('admin.admin_view_appointment'))
	
	return render_template('admin_view_appointment.html',data=data)

@admin.route('/admin_view_bookingdetails')
def admin_view_bookingdetails():
	data={}
	p="SELECT * FROM `users` INNER JOIN `prediction` USING(`user_id`) INNER JOIN `appointment` USING (`user_id`) INNER JOIN `doctor` USING (`doctor_id`)  INNER JOIN `payment` USING(`appointment_id`)  GROUP BY `appointment_id`"
	ares=select(p)
	data['view']=ares

	return render_template('admin_view_bookingdetails.html',data=data)

@admin.route('/admin_view_doctors',methods=['get','post'])
def admin_view_doctors():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		login_id=request.args['login_id']
	else:
		action=None

	if action=='delete':
		q="DELETE FROM `login` WHERE `login_id`='%s'"%(login_id)
		delete(q)
		q="DELETE FROM `doctor` WHERE `login_id`='%s'"%(login_id)
		delete(q)
	
	if action=='approve':
		q="update login set usertype='doctor' where login_id='%s'"%(login_id)
		delete(q)
		return redirect(url_for("admin.admin_view_doctors"))

	if action=='reject':
		q="update login set usertype='Rejected' where login_id='%s'"%(login_id)
		delete(q)
		return redirect(url_for("admin.admin_view_doctors"))
	q="SELECT * FROM  `doctor` inner join login using (login_id)"
	data['view']=select(q)
	return render_template('admin_view_doctors.html',data=data)

@admin.route('/admin_view_users',methods=['get','post'])
def admin_view_users():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		login_id=request.args['login_id']
	else:
		action=None

	if action=='delete':
		q="DELETE FROM `login` WHERE `login_id`='%s'"%(login_id)
		delete(q)
		q="DELETE FROM `users` WHERE `login_id`='%s'"%(login_id)
		delete(q)


	q="SELECT * FROM  `users`"
	data['view']=select(q)
	return render_template('admin_view_users.html',data=data)




@admin.route('/admin_Manage_doctor',methods=['get','post'])
def admin_Manage_doctor():
	data={}
	if 'add_doctor' in request.form:
		doc_fname=request.form['doc_fname']
		doc_lname=request.form['doc_lname']
		place=request.form['place']
		phone=request.form['phone']
		doc_email=request.form['doc_email']
		qualification=request.form['qualification']
		name=request.form['name']
		password=request.form['pass']
		q="SELECT * FROM `login` WHERE `username`='%s'"%(name)
		res=select(q)
		if res:
			flash('USER NAME ALREADY EXIST')
			return redirect(url_for('public.user_Register'))
		else:
			q="insert into login values(null,'%s','%s','pending')"%(name,password)
			lid=insert(q)

			q="insert into doctor Values(null,'%s','%s','%s','%s','%s','%s','%s')"%(lid,doc_fname,doc_lname,place,phone,doc_email,qualification)
			insert(q)
	if 'action' in request.args:
		action=request.args['action']
		doctor_id=request.args['doctor_id']
		login_id=request.args['login_id']
	else:
		action=None
	if action=='update':
		q="select * from doctor inner join login using(login_id) where doctor_id='%s'"%(doctor_id)
		data['up']=select(q)
	if action=='delete':
		q="delete from doctor where doctor_id='%s'"%(doctor_id)
		delete(q)
	if 'update' in request.form:
		doc_fname=request.form['doc_fname']
		doc_lname=request.form['doc_lname']
		place=request.form['place']
		phone=request.form['phone']
		doc_email=request.form['doc_email']
		qualification=request.form['qualification']
	
		q="update doctor set fname='%s',lname='%s',place='%s',phone='%s',email='%s',qualification='%s' where doctor_id='%s'"%(doc_fname,doc_lname,place,phone,doc_email,qualification,doctor_id)
		update(q)
		return redirect(url_for('admin.admin_Manage_doctor'))

	q="select * from doctor"
	data['view']=select(q)
	return render_template('admin_Manage_doctor.html',data=data)






@admin.route('/admin_View_enquriy',methods=['get','post'])
def admin_View_enquriy():
	if not session.get("lid") is None:
		data={}
		q="SELECT * from enquiry inner join users using(user_id)"
		data['view']=select(q)
		return render_template("admin_View_enquriy.html",data=data)
	else:
		return redirect(url_for('public.login'))
	


	
@admin.route('/admin_manage_doctor',methods=['get','post'])
def admin_manage_doctor():
	data={}
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		phone=request.form['phone']
		email=request.form['email']
		place=request.form['place']
		image=request.files['image']
		path="static/"+str(uuid.uuid4())+image.filename
		image.save(path)
		uname=request.form['uname']
		pwd=request.form['pwd']
		kk="insert into login values(null,'%s','%s','doctor')"%(uname,pwd)
		res=insert(kk)
		kkl="insert into doctor values(null,'%s','%s','%s','%s','%s','%s','%s')"%(res,fname,lname,phone,email,place,path)
		insert(kkl)
		flash("SUCCESS...........!")



		email = email

		pwd="Username:"+uname+"Password:"+pwd
		
		try:
			gmail = smtplib.SMTP('smtp.gmail.com', 587)
			gmail.ehlo()
			gmail.starttls()
			gmail.login('hariharan0987pp@gmail.com', 'rjcbcumvkpqynpep')     
		except Exception as e:
			print("Couldn't setup email!!" + str(e))

		pwd = MIMEText(pwd)

		pwd['Subject'] = 'Your order details:'

		pwd['To'] = email

		pwd['From'] = 'hariharan0987pp@gmailcom'

		try:
			gmail.send_message(pwd)

			flash("EMAIL SEND SUCCESFULLY")

		except Exception as e:
			print("COULDN'T SEND EMAIL", str(e))
		else:
			flash("INVALID DETAILS")
			flash('ADDED...')
		return redirect(url_for('admin.admin_manage_doctor'))
	dd="select * from doctor"
	data['view']=select(dd)
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=='delete':
		hh="delete from doctor where login_id='%s'"%(id)
		delete(hh)
		hh="delete from login where login_id='%s'"%(id)
		delete(hh)
		flash("DELETED...........!")
		return redirect(url_for('admin.admin_manage_doctor'))
	return render_template('admin_manage_doctor.html',data=data)