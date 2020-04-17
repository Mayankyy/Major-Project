import requests
from flask import Flask, render_template,request, url_for, redirect
import pandas as pd
from flask_mail import Mail, Message
import json

app = Flask(__name__)
app.config['DEBUG']=True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465

#Add email ID
app.config['MAIL_USERNAME'] = ''

#Add password
app.config['MAIL_PASSWORD'] = ''

app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/index")
def index():
	print('inside index')

	#Get data
	url1 = 'https://api.thingspeak.com/channels/992056/fields/1.json?api_key=57MQYTPTFGYKBGJ2'
	r1 = requests.get(url1).json()
	#print(r1)
	pulse_df = pd.DataFrame(columns=['Date','Time','Pulse'])
	for i in range(0,len(r1['feeds'])):
		pulse_df = pulse_df.append({'Date':r1['feeds'][i]['created_at'].split('T')[0],'Time':r1['feeds'][i]['created_at'].split('T')[1][:-1],'Pulse':r1['feeds'][i]['field1']},ignore_index=True)

	url2 = 'https://api.thingspeak.com/channels/992056/fields/2.json?api_key=57MQYTPTFGYKBGJ2'
	r2 = requests.get(url2).json()
	#print(r2)
	temp_df = pd.DataFrame(columns=['Date','Time','Temp'])
	for i in range(0,len(r2['feeds'])):
		temp_df = temp_df.append({'Date':r2['feeds'][i]['created_at'].split('T')[0],'Time':r2['feeds'][i]['created_at'].split('T')[1][:-1],'Temp':r2['feeds'][i]['field2']},ignore_index=True)

	print(temp_df['Temp'].iloc[-1])

	fever = False
	pulse_details = pd.DataFrame(columns=['Date','Time','Pulse'])

	#Send email
	msg = Message('no-reply:RPS', sender = 'anandita16csu440@ncuindia.edu', recipients = ['sharma.kalpana97@gmail.com'])
	if float(temp_df['Temp'].iloc[-1])>98.6:
		msg.body = "DEVICE_ALERT: You may be running a fever"
		mail.send(msg)	
	for i in range(0,pulse_df.shape[0]):
		print(pulse_df['Pulse'].iloc[i])
		if(int(pulse_df['Pulse'].iloc[i])>100 or int(pulse_df['Pulse'].iloc[i])<60):
			print(pulse_df['Pulse'].iloc[i])
			pulse_details = pulse_details.append({'Date':pulse_df['Date'].iloc[i],'Time':pulse_df['Time'].iloc[i],'Pulse':pulse_df['Pulse'].iloc[i]},ignore_index=True)
			
	print(pulse_details)

	msg.body = "Hello! Your parameters for this month"+"\n"+pulse_df.to_string()+'\n\n'+temp_df.to_string()
	mail.send(msg)
	msg.body = "DEVICE_ALERT: There was a variation in your pulse"+"\n\n"+pulse_details.to_string()
	mail.send(msg)



	print('Going to print charts')
	#Graph display
	legend = 'Health Parameters'
	labels = list(pulse_df['Date']+" : "+pulse_df['Time'])
	#print("Labels: ",labels)
	temp_list = list(temp_df['Temp'])
	pulse_list = list(pulse_df['Pulse'])
	vaar = "hi"
	return render_template('data1.html',temp_list=temp_list,pulse_list=pulse_list,labels=labels, legend=legend, vaar = vaar)
# def login():
# 	return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login_post():
	if request.method=='GET':
		return render_template('login.html')
	elif request.method=='POST':
		if request.form['username']=='admin' and request.form['password']=='admin':
			index()
			return redirect(url_for('index'))
		else:
			flash('Incorrect login details')
			return render_template('login.html')

if(__name__ == "__main__"):
	app.run(debug=True)
