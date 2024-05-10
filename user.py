from flask import *
from database import *
import uuid
from newcnn import *
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

user=Blueprint('user',__name__)

@user.route('/user_home',methods=['get','post'])
def user_home():
	if not session.get("lid") is None:
		data={}
		return render_template("user_home.html",data=data)
	else:
		return redirect(url_for('public.login'))


@user.route('/user_View_alzimer_details_and_symptoms',methods=['get','post'])
def user_View_alzimer_details_and_symptoms():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM `alzimers` inner JOIN symptoms using(alzimers_id) "
		data['alz']=select(q)
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='sym':
			q="SELECT * FROM `symptoms` WHERE `alzimers_id`='%s' ORDER BY `symptom_id` DESC"%(id)
			data['sym']=res=select(q)
			if not res:
				flash('!! NO DATA FOUND !!')
		return render_template("user_View_cancer_details_and_symptoms.html",data=data)
	else:
		return redirect(url_for('public.login'))


@user.route('/user_View_predicted_output',methods=['get','post'])
def user_View_predicted_output():
		data={}
		if not session.get("lid") is None:
			
			if "submit" in request.form:
				ss=request.files['datass']
				path="static/assets"+str(uuid.uuid4())+ss.filename
				ss.save(path)
				out=preprocess_image(path)
				if out== 'Breast benign':
					myout="Oral antibiotics for infections like mastitis.,Surgery to remove lumps.,"
				elif out=="Breast malignant":
					myout="Surgery, Hormone therapy, Radiation therapy, Chemotherapy, Targeted therapy, Immunotherapy"
				elif out=="Breast normal":
					myout="Some swelling and tenderness just before your period is normal."
				elif out=="Kidney Normal":
					myout=""
				elif out=="Kidney Tumor":
					myout="Blood in your pee (hematuria)..,A lump or mass in your kidney area..,Flank pain..,Tiredness."
				elif out=="Lung Benign cases":
					myout=" persistent cough, recurrent respiratory infections such as pneumonia..,coughing up blood (hemoptysis)."
				elif out=="Lung Malignant cases":
					myout="Trouble breathing or shortness of breath (dyspnea)..,Hoarseness..,Loss of appetite..,Unexplained weight loss."
				elif out=="Lung Normal cases":
					myout=""
				elif out=="Prostate normal":
					myout=""
				elif out=="Prostate tumor":
					myout="Loss of bowel control(fecal incontinence)..,Painful ejaculation and erectile dysfunction (ED)."
				elif out=="unknown":
					myout="unknown"

				print("============",out)
				print("{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}",myout)
				
				
					
				q="INSERT INTO `prediction` VALUES (null,'%s','%s','%s','%s')"%(session['id'],path,out,myout)
				print(q)
				insert(q)
				flash('UPLOADED')
				return redirect(url_for('user.user_View_predicted_output'))
			q="SELECT *,CONCAT(`firstname`,' ',`lastname`) AS `user` FROM `prediction` INNER JOIN `users` USING (`user_id`) WHERE user_id='%s' ORDER BY `prediction_id` DESC"%(session['id'])
			data['pre']=select(q)
			return render_template("user_View_predicted_output.html",data=data)
		else:
			return redirect(url_for('public.login'))
		

@user.route('/user_Upload_rating_for_the_output',methods=['get','post'])
def user_Upload_rating_for_the_output():
	if not session.get("lid") is None:
		data={}
		q="SELECT *,CONCAT(`firstname`,' ',`lastname`) AS `user` FROM `rating` INNER JOIN `users` USING (`user_id`) WHERE user_id='%s' ORDER BY `rating_id` DESC"%(session['id'])
		data['rate']=res=select(q)
		if 'submit' in request.form:
			rate=request.form['rate']
			feed=request.form['feed']
			if res:
				q="UPDATE `rating` SET `rated`='%s' , feedback='%s', `date`=CURDATE() WHERE `user_id`='%s'"%(rate,feed,session['id'])
				update(q)
				flash('RATED')
				return redirect(url_for('user.user_Upload_rating_for_the_output'))
			else:
				q="INSERT INTO `rating` (`user_id`,`rated`,`feedback`,`date`) VALUES ('%s','%s','%s',CURDATE())"%(session['id'],rate,feed)
				insert(q)
				flash('RATED')
				return redirect(url_for('user.user_Upload_rating_for_the_output'))
		return render_template("user_Upload_rating_for_the_output.html",data=data)
	else:
		return redirect(url_for('public.login'))




@user.route('/user_send_enquiry',methods=['get','post'])
def user_send_enquiry():
	data={}
	did=request.args['did']

	# yy="select * from doctor"
	# data['view_list']=select(yy)

	
	


	if 'submit' in request.form:
		enq=request.form['enq']	
		file=request.files['file']
		path="static/"+str(uuid.uuid4())+file.filename
		file.save(path)

		p="select * from doctor where doctor_id='%s'"%(did)
		vl=select(p)
		print(vl)
		for i in vl:
			email = i['email']

		pwd="An enquiry received"
		
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

		pwd['From'] = 'hariharan0987pp@gmail.com'

		try:
			gmail.send_message(pwd)

			flash("EMAIL SEND SUCCESFULLY")

		except Exception as e:
			print("COULDN'T SEND EMAIL", str(e))
		else:
			flash("INVALID DETAILS")
			flash('ADDED...')
		q="insert into `enquiry` VALUES(NULL,'%s','%s','%s',CURDATE(),'pending','%s')"%(session['id'],did,enq,path)
		insert(q)

		return redirect(url_for('user.user_send_enquiry',did=did))
	
	p="select *from enquiry where user_id='%s'"%(session['id'])
	eres=select(p)
	data['enquiry']=eres

	

	if 'action' in request.args:
		action=request.args['action']
		cid=request.args['id']
	else:
		action=None

	if action=="delete":
		qs="delete from enquiry where equiry_id='%s'"%(cid)
		delete(qs)

		
		return redirect(url_for('user.user_send_enquiry'))
	return render_template('user_send_enquiry.html',data=data)

@user.route('/user_view_doctors',methods=['get','post'])
def user_view_doctors():
	data={}
	prediction_id=request.args['prediction_id']
	q="SELECT * FROM `doctor` "
	data['view']=select(q)
	

	return render_template('user_view_doctors.html',data=data,prediction_id=prediction_id)



@user.route('/user_make_payment',methods=['get','post'])
def user_make_payment():
	data={}
	total=request.args['total']
	appointment_id=request.args['appointment_id']

	if 'btn' in request.form:
		name=request.form['name']
		number=request.form['number']
		exry=request.form['exry']
		q="INSERT INTO `payment` VALUES(NULL,'%s','%s',CURDATE())"%(appointment_id,total)
		insert(q)
		q="update appointment set appoin_status='paid' where appointment_id='%s'"%(appointment_id)
		update(q)

		flash(" Payment Successfull")
		return redirect(url_for('user.user_home',total=total,appointment_id=appointment_id))
	return render_template('user_make_payment.html',data=data,total=total,appointment_id=appointment_id)
@user.route('/user_view_remadys',methods=['get','post'])
def user_view_remadys():
	data={}
	q="SELECT * FROM `remady` WHERE `user_id`='%s'"%(session['id'])
	data['view']=select(q)
	
	return render_template('user_view_remadys.html',data=data)

@user.route('/user_View_doctors',methods=['get','post'])
def user_View_doctors():
	data={}
	s="select * from doctor"
	data['view']=select(s)
	return render_template('user_View_doctors.html',data=data)




