from multiprocessing import dummy
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
from trakberry.forms import maint_closeForm, maint_loginForm, maint_searchForm, tech_loginForm, sup_downForm
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date, mgmt_display, mgmt_display_edit
from views_mod2 import stamp_shift_start
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2_1, vacation_set_current5,vacation_set_current6,vacation_set_current77
from views_vacation import vacation_1
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
from smtplib import SMTP
from django.core.context_processors import csrf
from views_routes import direction
from time import mktime
from datetime import datetime, date
from views_db import db_open, db_set,net1, db_set2
from views_test2 import prediction1
from mod_tracking import Graph_Data
import datetime
# from datetime import datetime 
from time import strftime
import time

def pdate_stamp(pdate):
	string=str(pdate)
	element = datetime.datetime.strptime(string,"%Y-%m-%d")
	tuple = element.timetuple()
	timestamp = time.mktime(tuple)
	return timestamp

def stamp_pdate(stamp):
	tm = time.localtime(stamp)
	ma = ''
	da = ''
	if tm[1] < 10: ma = '0'
	if tm[2] < 10: da = '0'
	y1 = str(tm[0])
	m1 = str(tm[1])
	d1 = str(tm[2])
	pdate = y1 + '-' + (ma + m1) + '-' + (da + d1)
	return pdate

def gf6_reaction(request):
	asset = ['576','628','672','667','696','900']
	part  = ['50-1713','50-1713','50-1713','50-1713','50-1713','50-1713']
	operation = [10,20,40,50,80,90]
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	total = zip(asset,part,operation)

	asset_tuple = tuple(asset)
	partno1 = '50-1713'
	partno2 = '50-3627'

	t=int(time.time())
	tm = time.localtime(t)
	a1 = tm[6] * 86400
	a2 = tm[3] * 60 * 60
	a3 = tm[4] * 60
	a4 = tm[5]
	week_start = t - a1 - a2 - a3 - a4
	week_end = week_start + 432000
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)

	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through

	db, cur = db_set(request)   

	# Select all reactions in asset list for date range
	sql = "SELECT asset_num,pdate,shift,partno,actual_produced FROM sc_production1 WHERE pdate >= '%s' and pdate <= '%s' and (partno = '%s') and asset_num IN {}; ".format(asset_tuple) %(pdate_week[0],pdate_week[6],partno1)
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append(str(i[1]))
		t1.append(i[2])
		t1.append(i[3])
		t1.append(i[4])
		t2.append(t1)
		
	# *************************  Filter a list *****************************************************************
	a1 = zip(*tmp)  # Unzip elements
	a2 = [list(z) for z in zip(a1[0],a1[1],a1[2],a1[3],a1[4]) ]  # Rebuilt list so it's list of list
	aa2 = [list(z) for z in zip(a1[4])]  # Rebuilt list so it's list of list
	a3 = filter(lambda c:c[0]=='672',a2)  # Filter out '672' and form list a3
	# **********************************************************************************************************

	a22 = int(aa2[0][0])

	a4 = filter(lambda c:c[2] == '3pm-11pm',a3)



	tot2 = []
	tot3 = []
	for i in asset:
		tot2 =[]
		for j in pdate_week:
			for k in shift:
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)

				a3 = filter(lambda c:c[0]==i and c[1]==j and c[2]==k,t2)  
				try:
					a33 = 0
					for m in a3:
						a33 = a33 + int(m[4])
				except:
					a33 = 0
				tot.append(a33)
				tot2.append(tot)
		tot3.append(tot2)
	request.session['totals'] = tot3
	request.session['shift'] = shift2
	request.session['pdate'] = pdate_week

	return render(request, "gf6_reaction.html")    


