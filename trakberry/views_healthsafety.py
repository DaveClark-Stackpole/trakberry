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
	for i in tmp:
		if ctr < len_ctr:
			tt=[]
			tt.append(i[2]/float(10))
			tt.append(i[3]/float(10))
			tt.append(i[4]/float(10))
			tt.append(i[5])
			tmp1.append(tt)

		else:
			tt=[]
			tt.append(i[2]/float(10))
			tt.append(i[3]/float(10))
			tt.append(i[4]/float(10))
			tt.append(i[5])
			tmp2.append(tt)
		ctr = ctr + 1

	request.session['temp_monitors1'] = tmp1
	request.session['temp_monitors2'] = tmp2
	return render(request, "temp_monitors.html")

