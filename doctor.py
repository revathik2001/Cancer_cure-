from flask import *
from database import *
import uuid
doctor=Blueprint('doctor',__name__)

@doctor.route('/doctor_home')
def doctor_home():
    return render_template('doctor_home.html')


@doctor.route('/doctor_view_enq')
def doctor_view_enq():
    data={}
    q="SELECT * from enquiry inner join users using(user_id) where doctor_id='%s'"%(session['did'])
    data['view']=select(q)
    return render_template('doctor_view_enq.html',data=data)


@doctor.route('/admin_send_reply', methods=['get', 'post'])
def admin_send_reply():
    data = {}
    enquiry_id = request.args['equiry_id']

    if 'submit' in request.form:
        sendreply = request.form['sendreply']
        q = "update enquiry set enq_reply='%s' where equiry_id='%s'" % (sendreply, enquiry_id)
        update(q)
        return redirect(url_for('doctor.doctor_view_enq'))

    return render_template("admin_send_reply.html", data=data,enquiry_id=enquiry_id)