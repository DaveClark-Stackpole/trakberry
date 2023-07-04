from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from trakberry.forms import login_Form, login_password_update_Form, kiosk_dispForm4
from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os,sys
from django.core.context_processors import csrf
from shutil import copyfile
import MySQLdb
import time
import os
import smtplib
from smtplib import SMTP
import xlrd
#import pandas
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current2,vacation_set_current6, vacation_set_current4
from views_vacation import vacation_set_current5
from views3 import matrix_read,shift_area


# *********************************************************************************************************
# MAIN Production View
# This is the main Administrator View to tackle things like cycle times, view production etc.
# *********************************************************************************************************


def temp_display(request):
	# request.session["local_switch"] = 0
	# request.session["local_toggle"] = "/trakberry"
	try:
		trigger7 = request.session['trigger7']
	except:
		request.session['trigger7'] = 0
		trigger7 = 0

	try:
		request.session['temp_email'] 
	except:
		request.session['temp_email'] = 0

	db, cur = db_set(request)
	sql1 = "select * from temp_monitors"
	cur.execute(sql1)
	tmp=cur.fetchall()
	db.close()
	tmp=sorted(tmp,key=lambda x:(x[4]),reverse=True)
	request.session['temp_monitors'] = tmp
	len1=len(tmp)
	len_ctr = len1/float(2)
	tmp1=[]
	tmp2=[]
	tmp3=[]
	ctr = 0
	alert1 = 0
	for i in tmp:

		zz=i[5]
		z=i[5]
		if z==6:zz='Z6: Area 1 Unload ' 
		if z==2:zz='Z2: Area 1 NCL Unload'
		if z==28:zz='Z28: Area 3 Plant 5 (Rear) 1705'
		if z==29:zz='Z29: Area 3 Mach 788 Plant 5'
		if z==12:zz='Z12: Area 3 GFx'
		if z==19:zz= '19'


		if ctr < len_ctr:
			tt=[]
			tt.append(i[2]/float(10))
			tt.append(i[3]/float(10))

			if ctr == 0 and trigger7 == 1:
				temp7 = 440
			else:		
				temp7 = i[4]		

			# Check if need to send email
			temp_email = request.session['temp_email']
			if temp7 > 420 and temp_email ==0:
				alert1=1
				request.session['temp_email'] = 1



			tt.append(temp7/float(10))
			tt.append(z)
			tmp1.append(tt)
			tmp3.append(tt)

		else:
			tt=[]
			tt.append(i[2]/float(10))
			tt.append(i[3]/float(10))
			tt.append(i[4]/float(10))
			
			tt.append(z)

			tmp2.append(tt)
			tmp3.append(tt)
		ctr = ctr + 1


	# if alert1 == 1:
	# 	b = "\r\n"
	# 	ctr = 0
	# 	message_subject = 'Check Heat Alert Display ' 
	# 	message3 = ''
	# 	message3 = message3 + 'Heat Alert'
	# 	toaddrs = ["dclark@stackpole.com"]
	# 	#toaddrs = ["dclark@stackpole.com","sherman@stackpole.com"]

	# 	#toaddrs = ["rrompen@stackpole.com","rbiram@stackpole.com","rzylstra@stackpole.com","lbaker@stackpole.com","dmilne@stackpole.com","sbrownlee@stackpole.com","pmurphy@stackpole.com","pstreet@stackpole.com","kfrey@stackpole.com","asmith@stackpole.com","smcmahon@stackpole.com","gharvey@stackpole.com","ashoemaker@stackpole.com","jreid@stackpole.com"]
	# 	fromaddr = 'stratford.reports@stackpole.com'
	# 	frname = 'Heat Alert'
	# 	server = SMTP('mesg06.stackpole.ca')
	# 	server.ehlo()
	# 	server.starttls()
	# 	server.ehlo()
	# 	# server.login('stackpolepmds@gmail.com', 'stacktest6060')
	# 	message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
	# 	message = message+message_subject + "\r\n\r\n" + message3 + "\r\n\r\n" 
	# 	server.sendmail(fromaddr, toaddrs, message)
	# 	server.quit()


	request.session['temp_monitors1'] = tmp1
	request.session['temp_monitors2'] = tmp2
	tmp4 = []
	for i in tmp3:
		tt = []
		humidex = int(i[2])
		level = 0
		# if humidex > 26 : level = 1
		# if humidex > 27 : level = 2
		# if humidex > 28 : level = 3
		# if humidex > 29 : level = 4
		# if humidex > 30: level = 5
		# if humidex > 31 : level = 6
		# if humidex > 33 : level = 7

		if humidex > 32 : level = 1
		if humidex > 36 : level = 2
		if humidex > 40 : level = 3
		if humidex > 42 : level = 4
		if humidex > 45: level = 5
		if humidex > 47 : level = 6
		if humidex > 50 : level = 7
		tt.append(level)
		tt.append(humidex)
		tt.append(i[3])
		tmp4.append(tt)  # The current Level , Humidex , Zone Chart

	# Checking if email required
	alert1 = 0  
	db, cur = db_set(request)
	sql1 = "select * from temp_current"
	cur.execute(sql1)
	tmp=cur.fetchall()
	
	chng2 = []

	for i in tmp4:
		for ii in tmp:
			if (i[2] == ii[2]) and (i[0] != ii[0]):
				alert1 = 1
				chng1 = []
				if i[0] > ii[0]:
					chng1.append(i[2])
					chng1.append(i[1])
					chng1.append('Moved Up To')
					chng1.append(i[0])
					chng2.append(chng1)
				else:
					chng1.append(i[2])
					chng1.append(i[1])
					chng1.append('Moved Down To')
					chng1.append(i[0])
					chng2.append(chng1)
			

		sql =( 'update temp_current SET level="%s" WHERE zone="%s"' % (i[0],i[2]))
		cur.execute(sql)
		db.commit()
		sql =( 'update temp_current SET humidex="%s" WHERE zone="%s"' % (i[1],i[2]))
		cur.execute(sql)
		db.commit()
	
	if alert1 == 1:
		for i in chng2:
			t=str(int(time.time()))
			h=str(i[1])
			z=str(int(i[0]))
			l=str(i[3])
			d=str(i[2])
			d1 = 0
			sql =( 'insert into temp_alert_history(timestamp,humidex,zone,level,direction) values("%s","%s","%s","%s","%s")' % (t,h,z,l,d))
			cur.execute(sql)
			db.commit()

		# EMAIL SUPERVISORS
		b = "\r\n"
		ctr = 0
		message_subject = 'Check Heat Alert Display ' 
		message3 = ''
		message3 = message3 + 'Heat Alert'
		# toaddrs = ["dclark@stackpole.com"]
		toaddrs = ["dclark@stackpole.com","nkleingeltink@stackpole.com","amckinlay@stackpole.com","dgodbout@stackpole.com","asmith@stackpole.com","dmclaren@stackpole.com","egeorge@stackpole.com","gharvey@stackpole.com","jpearce@stackpole.com","jskillings@stackpole.com","kfrey@stackpole.com","pstreet@stackpole.com","sbhardwaj@stackpole.com","sherman@stackpole.com","sbrownlee@stackpole.com","pcurrie@stackpole.com","smcmahon@stackpole.com"]
		fromaddr = 'stratford.reports@stackpole.com'
		frname = 'Heat Alert'
		server = SMTP('mesg06.stackpole.ca')
		server.ehlo()
		server.starttls()
		server.ehlo()
		message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
		message = message+message_subject + "\r\n\r\n" + message3 + "\r\n\r\n" 

		for i in chng2:
			zone1 = str(i[0])
			temp1 = str(i[1])
			direction1 = str(i[2])
			level1 = str(i[3])
			x = ''
			if int(level1) == 1:
				x = 'Supply water to workers on an as needed basis'
			elif int(level1) == 0:
				x = 'There is no Heat Stress Warning'
			elif int(level1) == 2:
				x = 'post Heat Stress Alert notice: encourage workers to drink extra water.  Start recording hourly temperature and relative humitidy'
			elif int(level1) == 3:
				x = 'post Heat Stress Warning notice.  Notify workers that they need to drink extra water.  Ensure workers are trained to recognize symptoms' 
			elif int(level1) == 4:
				x = 'work with 15 minutes relief per hour can continue.  Provide adequate cool 10-15C water at least 1 cup of water every 20minutes.  worker with sypmtoms should seek medical attention.' 
			elif int(level1) == 5:
				x = 'work with 30 minutes relief per hour can continue. Provide adequate cool 10-15C water at least 1 cup of water every 20minutes.  worker with sypmtoms should seek medical attention.' 
			elif int(level1) == 6:
				x = 'if feasible work with 45 minutes relief per hour can continue.  Provide adequate cool 10-15C water at least 1 cup of water every 20minutes.  worker with sypmtoms should seek medical attention.' 
			elif int(level1) == 7:
				x = 'only medically supervised work can continue' 

			b = "\r\n"
			message = message + " Zone " + zone1 + " is currently at " + temp1 + " Humidex and has " + direction1 + " level " + level1 + " " + b + x + b + b

		message = message + " Please click on the below link to acknowledge the appropriate action has been taken" + b + b
		#message = message + "http://pmdsdata.stackpole.ca:8986/trakberry/master2/"+str(t) + b + b + b + b + b 
		message = message + "http://pmdsdata.stackpole.ca:8986/trakberry/temp_ack/get/"+str(t) + b + b + b + b + b 
		


		server.sendmail(fromaddr, toaddrs, message)
		server.quit()






	db.close()




	return render(request, "temp_monitors.html")


def temp_ack(request,index):
	request.session['temp_ack_time'] = index
	db, cur = db_set(request)
	ack = 0
	sql = "select * from temp_alert_history where timestamp = '%s'" % (index)
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	request.session['temp_ack_button'] = 1
	rrr=abs(int(tmp[0][5])-1)


		
	request.session['temp_alerts'] = tmp
	request.session['temp_ack_button'] = rrr

	return render(request, "temp_ack.html")

def temp_ack_taken(request):
	index = request.session['temp_ack_time']
	ack = 1
	ack2 = 0
	db, cur = db_set(request)
	sql =( 'update temp_alert_history SET acknowledge="%s" WHERE acknowledge ="%s"' % (ack,ack2))
	cur.execute(sql)
	db.commit()
	db.close()


	return temp_ack(request,index)
	#return render(request, "temp_monitors.html")
	


def temp_test1(request):
	request.session['temp_email'] = 0
	request.session['trigger7'] = 1
	return render(request, "redirect_temp_display.html")

def temp_test_reset(request):
	request.session['temp_email'] = 0
	request.session['trigger7'] = 0
	return render(request, "redirect_temp_display.html")



