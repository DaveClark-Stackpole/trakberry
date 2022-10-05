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
	ctr = 0
	alert1 = 0
	for i in tmp:

		zz=i[5]
		z=i[5]
		if z==6:zz='Area 1 Unload'
		if z==2:zz='Area 1 NCL Unload'
		if z==28:zz='Area 3 Plant 5 (Rear) 1705'
		if z==29:zz='Area 3 Mach 788 Plant 5'
		if z==12:zz='Area 3 GFx'


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
			tt.append(zz)
			tmp1.append(tt)

		else:
			tt=[]
			tt.append(i[2]/float(10))
			tt.append(i[3]/float(10))
			tt.append(i[4]/float(10))
			
			tt.append(zz)

			tmp2.append(tt)
		ctr = ctr + 1


	if alert1 == 1:
			# Email information
		# Unblock when good 
		b = "\r\n"
		ctr = 0
		message_subject = 'Check Heat Alert Display ' 
		message3 = ''
		message3 = message3 + 'Heat Alert'
		# toaddrs = ["dave7995@gmail.com","jmcmaster@stackpole.com"]
		toaddrs = ["dclark@stackpole.com","sherman@stackpole.com"]

		#toaddrs = ["rrompen@stackpole.com","rbiram@stackpole.com","rzylstra@stackpole.com","lbaker@stackpole.com","dmilne@stackpole.com","sbrownlee@stackpole.com","pmurphy@stackpole.com","pstreet@stackpole.com","kfrey@stackpole.com","asmith@stackpole.com","smcmahon@stackpole.com","gharvey@stackpole.com","ashoemaker@stackpole.com","jreid@stackpole.com"]
		fromaddr = 'stratford.reports@stackpole.com'
		frname = 'Heat Alert'
		server = SMTP('mesg06.stackpole.ca')
		server.ehlo()
		server.starttls()
		server.ehlo()
		# server.login('stackpolepmds@gmail.com', 'stacktest6060')
		message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
		message = message+message_subject + "\r\n\r\n" + message3 + "\r\n\r\n" 
		server.sendmail(fromaddr, toaddrs, message)
		server.quit()


	request.session['temp_monitors1'] = tmp1
	request.session['temp_monitors2'] = tmp2


	return render(request, "temp_monitors.html")


def temp_test1(request):
	request.session['temp_email'] = 0
	request.session['trigger7'] = 1
	return render(request, "redirect_temp_display.html")

def temp_test_reset(request):
	request.session['temp_email'] = 0
	request.session['trigger7'] = 0
	return render(request, "redirect_temp_display.html")



