from multiprocessing import dummy
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
from trakberry.forms import maint_closeForm, maint_loginForm, maint_searchForm, tech_loginForm, sup_downForm
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date, mgmt_display, mgmt_display_edit
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
from views_db import db_open, db_set,db_set_3,net1, db_set2 #,db_set_vant
from views_test2 import prediction1
from mod_tracking import Graph_Data
import datetime
# from datetime import datetime 
from time import strftime
import time

def day_breakdown(tt):
	mnth = ''
	wday = ''
	tm = time.localtime(tt)
	if tm[3] == 22:
		tt = tt + 10800
		tm = time.localtime(tt)
		hrr = tm[3]
	month1 = tm[1]
	day1 = tm[2]
	wd = tm[6]
	hr1 = tm[3]
	shift = 'None'
	if hr1 == 6:
		shift = 'Day'
	elif hr1 == 14:
		shift = 'Aft'
	elif hr1 == 1:
		shift ='Mid'
	if wd == 7:
		wd = 0
	if wd == 6:
		wday = 'Sunday'
	elif wd == 0:
		wday = 'Monday'
	elif wd == 1:
		wday = 'Tuesday'
	elif wd == 2:
		wday = 'Wednesday'
	elif wd == 3:
		wday = 'Thursday'
	elif wd == 4:
		wday = 'Friday'
	elif wd == 5:
		wday = 'Saturday'
	if month1 == 8:
		mnth = 'Aug'
	elif month1==7:
		mnth = 'Jul'
	elif month1==9:
		mnth='Sep'
	elif month1==10:
		mnth='Oct'
	elif month1==11:
		mnth='Nov'
	elif month1==12:
		mnth='Dec'
	elif month1==1:
		mnth='Jan'
	elif month1==2:
		mnth='Feb'
	elif month1==3:
		mnth='Mar'
	elif month1==4:
		mnth='Apr'
	elif month1==5:
		mnth='May'
	elif month1==6:
		mnth='Jun'
	return wday,mnth,day1,shift

def pdate_stamp(pdate):
	string=str(pdate)
	element = datetime.datetime.strptime(string,"%Y-%m-%d")
	tuple = element.timetuple()
	timestamp = time.mktime(tuple)
	return timestamp

def pdate_stamp2(pdate):
	string=str(pdate)
	element = datetime.datetime.strptime(string,"%Y-%m-%d %hh:%mm:%ss")
	tuple = element.timetuple()
	timestamp = time.mktime(tuple)
	return timestamp

def stamp_pdate(stamp):
	stamp=stamp+86400
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

def stamp_pdate2(stamp):

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

def stamp_pdate3(stamp):

	tm = time.localtime(stamp)
	ma = ''
	da = ''
	if tm[1] < 10: ma = '0'
	if tm[2] < 10: da = '0'
	y1 = str(tm[0])
	m1 = str(tm[1])
	d1 = str(tm[2])
	hr1 = str(tm[3])
	mi1 = str(tm[4])
	se1 = str(tm[5])
	if len(hr1)==1:
		hr1='0'+hr1
	if len(mi1)==1:
		mi1='0'+mi1
	if len(se1)==1:
		se1='0'+se1

	pdate = y1 + '-' + (ma + m1) + '-' + (da + d1) + ' ' + hr1 + ':' + mi1 + ':' + se1


	return pdate

def gf6_reaction(request):
	request.session['WL'] = 432000
	t=int(time.time())
	week_start_gf6(request,t)
	gf6_1713(request)
	gf6_3627(request)
	return render(request, "gf6_reaction.html")    

def gf6_reaction_prev(request):
	t=request.session['week_end7']
	t=t-604800
	week_start_gf6(request,t)
	gf6_1713(request)
	gf6_3627(request)
	return render(request, "gf6_reaction.html") 

def gf6_input(request):
	request.session['WL'] = 432000
	t=int(time.time())
	week_start_gf6(request,t)
	gf6_1731(request)
	gf6_3632(request)
	return render(request, "gf6_input.html")    

def gf6_input_prev(request):
	t=request.session['week_end7']
	t=t-604800
	week_start_gf6(request,t)
	gf6_1731(request)
	gf6_3632(request)
	return render(request, "gf6_input.html") 

def week_start_gf6(request,t):
	request.session['TCUR'] = t
	tm = time.localtime(t)
	a1 = tm[6] * 86400
	a2 = tm[3] * 60 * 60
	a3 = tm[4] * 60
	a4 = tm[5]
	week_start = t - a1 - a2 - a3 - a4
	week_end = week_start + 432000
	request.session['t'] = t
	request.session['week_start7'] = week_start
	request.session['week_end7'] = week_end
	return

def week_start_ab(request,t):
	request.session['TCUR'] = t
	tm = time.localtime(t)
	a1 = tm[6] * 86400
	a2 = tm[3] * 60 * 60
	a3 = tm[4] * 60
	a4 = tm[5]
	week_start = t - a1 - a2 - a3 - a4 - 3600
	week_end = week_start + 604800
	request.session['t'] = t
	request.session['week_start7'] = week_start
	request.session['week_end7'] = week_end
	return

def week_start_10r(request,t):
	request.session['TCUR'] = t

	tm = time.localtime(t)
	a1 = tm[6] * 86400
	a2 = tm[3] * 60 * 60
	a3 = tm[4] * 60
	a4 = tm[5]
	week_start = t - a1 - a2 - a3 - a4 - 7200
	week_end = week_start + 604800
	request.session['t'] = t
	request.session['week_start7'] = week_start
	request.session['week_end7'] = week_end
	return


def gf6_1713(request):
	# ******************  Below data entered for each part  ******************************
	goal = 1500   # Weekly6 Goal
	prt7 = '50-1713'
	db, cur = db_set(request) 
	# try:
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 1500

	db.close()

	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['576','595','635','628','676','667','900']
	part  = ['50-1713','50-1713','50-1713','50-1713','50-1713','50-1713','50-1713']
	operation = [10,10,20,20,40,50,90]
	# ************************************************************************************

	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)

	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list

	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)

	asset_tuple = tuple(asset)
	partno1 = '50-1713'

	# t=int(time.time())
	# request.session['TCUR'] = t
	# tm = time.localtime(t)
	# a1 = tm[6] * 86400
	# a2 = tm[3] * 60 * 60
	# a3 = tm[4] * 60
	# a4 = tm[5]
	# week_start = t - a1 - a2 - a3 - a4
	# week_end = week_start + 432000

	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']


	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate2(week_start)
	pdate_week.append(pdate_start)



	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate2(stamp1)
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
		
	# # *************************  Filter a list *****************************************************************
	# a1 = zip(*tmp)  # Unzip elements
	# a2 = [list(z) for z in zip(a1[0],a1[1],a1[2],a1[3],a1[4]) ]  # Rebuilt list so it's list of list
	# aa2 = [list(z) for z in zip(a1[4])]  # Rebuilt list so it's list of list
	# a3 = filter(lambda c:c[0]=='672',a2)  # Filter out '672' and form list a3
	# a22 = int(aa2[0][0])
	# a4 = filter(lambda c:c[2] == '3pm-11pm',a3)
	# # **********************************************************************************************************

	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
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
						op[op5] = op[op5] + int(m[4])
				except:
					a33 = 0
				tot.append(a33)
				tot2.append(tot)
		tot3.append(tot2)

	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)

	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_1713'] = tot3
	request.session['shift_1713'] = shift2
	request.session['pdate_1713'] = pdate_week
	request.session['op_totals_1713'] = op
	request.session['op_span_1713'] = operation_totals
	request.session['goal_1713'] = goal_todate
	inv_change =  int(operation_totals[6][3]) - int(goal_todate)
	request.session['inv_change_1713'] = inv_change
	return
  
def gf6_3627(request):
	# ******************  Below data entered for each part  ******************************
	goal = 6000   # Weekly6 Goal
	prt7 = '50-3627'
	db, cur = db_set(request) 
	# try:
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000
	db.close()
	color1 = '#93E08D'  # Color for line 1
	color2 = '#80C47B'  # Color for line 2
	asset = ['732','583','582','580','616','617','731','682','674','673','675','672','566','745','900']
	part  = ['50-3627','50-3627','50-3627','50-3627','50-3627','50-3627','50-3627','50-3627','50-3627','50-3627','50-3627','50-3627','50-3627','50-3627','50-3627']
	operation = [10,10,10,10,20,20,20,20,40,40,40,40,50,50,90]
	# ************************************************************************************

	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)

	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list

	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)

	asset_tuple = tuple(asset)
	partno1 = '50-3627'

	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	test2 = request.session['WL']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate2(week_start)
	pdate_week.append(pdate_start)

	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate2(stamp1)
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
		
	# # *************************  Filter a list *****************************************************************
	# a1 = zip(*tmp)  # Unzip elements
	# a2 = [list(z) for z in zip(a1[0],a1[1],a1[2],a1[3],a1[4]) ]  # Rebuilt list so it's list of list
	# aa2 = [list(z) for z in zip(a1[4])]  # Rebuilt list so it's list of list
	# a3 = filter(lambda c:c[0]=='672',a2)  # Filter out '672' and form list a3
	# a22 = int(aa2[0][0])
	# a4 = filter(lambda c:c[2] == '3pm-11pm',a3)
	# # **********************************************************************************************************

	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
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
						op[op5] = op[op5] + int(m[4])
				except:
					a33 = 0
				tot.append(a33)
				tot2.append(tot)
		tot3.append(tot2)

	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)

	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_3627'] = tot3
	request.session['shift_3627'] = shift2
	request.session['pdate_3627'] = pdate_week
	request.session['op_totals_3627'] = op
	request.session['op_span_3627'] = operation_totals
	request.session['goal_3627'] = goal_todate

	a = int(operation_totals[14][3])
	b = int(goal_todate)

	inv_change =  int(operation_totals[14][3]) - int(goal_todate)
	request.session['inv_change_3627'] = inv_change


	return

def gf6_1731(request):
	# ******************  Below data entered for each part  ******************************
	goal = 1500   # Weekly6 Goal

	prt7 = '50-1731'
	db, cur = db_set(request) 
	# try:
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 1500
	db.close()

	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['627','564','615','781','900']
	part  = ['50-1731','50-1731','50-1731','50-1731','50-1731']
	operation = [10,20,30,60,90]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(91)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2


	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-1731'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate2(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate2(stamp1)
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
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
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
						op[op5] = op[op5] + int(m[4])
				except:
					a33 = 0
				tot.append(a33)
				tot2.append(tot)
		tot3.append(tot2)
	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)


	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_1731'] = tot3
	request.session['shift_1731'] = shift2
	request.session['pdate_1731'] = pdate_week
	request.session['op_totals_1731'] = op
	request.session['op_span_1731'] = operation_totals
	request.session['goal_1731'] = goal_todate
	inv_change =  int(operation_totals[4][3]) - int(goal_todate)
	request.session['inv_change_1731'] = inv_change
	return
  
def gf6_3632(request):
	# ******************  Below data entered for each part  ******************************
	goal = 6000   # Weekly6 Goal
	prt7 = '50-3632'
	db, cur = db_set(request) 
	# try:
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000

	db.close()

	color1 = '#93E08D'  # Color for line 1
	color2 = '#80C47B'  # Color for line 2
	asset = ['686','574','614','620','564','750','749','781','900']
	part  = ['50-3632','50-3632','50-3632','50-3632','50-3632','50-3632','50-3632','50-3632','50-3632']
	operation = [10,10,20,20,20,30,30,60,90]
	# ************************************************************************************

	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(91)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-3632'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate2(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate2(stamp1)
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
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
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
						op[op5] = op[op5] + int(m[4])
				except:
					a33 = 0
				tot.append(a33)
				tot2.append(tot)
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_3632'] = tot3
	request.session['shift_3632'] = shift2
	request.session['pdate_3632'] = pdate_week
	request.session['op_totals_3632'] = op
	request.session['op_span_3632'] = operation_totals
	request.session['goal_3632'] = goal_todate
	inv_change =  int(operation_totals[8][3]) - int(goal_todate)
	request.session['inv_change_3632'] = inv_change
	return



def ab1v_8670(request):
	prt7 = '50-8670'
	pprt7='50-6420'
	prt8 = pprt7[-4:]
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1704R']
	asset6 = ['1703R']
	part  = ['50-8670']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-8670'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through

	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()


	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2



	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_8670'] = tot3
	request.session['shift_8670'] = shift2  #Need 
	request.session['pdate_8670'] = pdate_week  #Need
	request.session['op_totals_8670'] = op
	request.session['op_span_8670'] = operation_totals
	request.session['goal_8670'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_8670'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return


def ab1v_5404_1722(request):
	prt7 = '50-5404'
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1722']
	part  = ['50-5404']
	operation = [90]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-6114'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,fi1,asset[0],part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_5404_1722'] = tot3
	request.session['shift_5404_1722'] = shift2  #Need 
	request.session['pdate_5404_1722'] = pdate_week  #Need
	request.session['op_totals_5404_1722'] = op
	request.session['op_span_5404_1722'] = operation_totals
	request.session['goal_5404_1722'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_5404_1722'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return


def prod_6114_611(request):
	prt7 = '50-6114'
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['611']
	part  = ['50-6114']
	operation = [90]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-6114'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,fi1,asset[0],part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_6114'] = tot3
	request.session['shift_6114'] = shift2  #Need 
	request.session['pdate_6114'] = pdate_week  #Need
	request.session['op_totals_6114'] = op
	request.session['op_span_6114'] = operation_totals
	request.session['goal_6114'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_6114'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def ab1v_5401_oldd(request):
	prt7 = '50-5401'
	pprt7='50-6418'
	prt8 = pprt7[-4:]
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1704R']
	asset6 = ['1703R']
	part  = ['50-5401']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5401'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through

	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []


	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2



	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_5401'] = tot3
	request.session['shift_5401'] = shift2  #Need 
	request.session['pdate_5401'] = pdate_week  #Need
	request.session['op_totals_5401'] = op
	request.session['op_span_5401'] = operation_totals
	request.session['goal_5401'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_5401'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def ab1v_5214(request):
	prt7 = '50-5214'
	pprt7='50-5214'
	prt8 = pprt7[-4:]
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1704R']
	asset6 = ['1703R']
	part  = ['50-5214']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5214'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through

	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []


	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2



	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_5214'] = tot3
	request.session['shift_5214'] = shift2  #Need 
	request.session['pdate_5214'] = pdate_week  #Need
	request.session['op_totals_5214'] = op
	request.session['op_span_5214'] = operation_totals
	request.session['goal_5214'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_5214'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def ab1v_3214(request):
	prt7 = '50-3214'
	pprt7='50-3214'
	prt8 = pprt7[-4:]
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1704R']
	asset6 = ['1703R']
	part  = ['50-3214']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-3214'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through

	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []


	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2



	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_3214'] = tot3
	request.session['shift_3214'] = shift2  #Need 
	request.session['pdate_3214'] = pdate_week  #Need
	request.session['op_totals_3214'] = op
	request.session['op_span_3214'] = operation_totals
	request.session['goal_3214'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_3214'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def ab1v_5401_OLD(request):
	prt7 = '50-5401'
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1706']
	part  = ['AB1V Input']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5401'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,fi1,asset[0],part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_5401'] = tot3
	request.session['shift_5401'] = shift2  #Need 
	request.session['pdate_5401'] = pdate_week  #Need
	request.session['op_totals_5401'] = op
	request.session['op_span_5401'] = operation_totals
	request.session['goal_5401'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_5401'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def ab1v_8670_626(request):
	prt7 = '50-8670'
	pprt7='50-8670'
	prt8 = pprt7[-4:]
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['626']
	asset6 = ['1703R']
	part  = ['50-8670']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-8670'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through

	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)


	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []


	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2



	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_8670_626'] = tot3
	request.session['shift_8670_626'] = shift2  #Need 
	request.session['pdate_8670_626'] = pdate_week  #Need
	request.session['op_totals_8670_626'] = op
	request.session['op_span_8670_626'] = operation_totals
	request.session['goal_8670_626'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_8670_626'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return


def ab1v_8670_659(request):
	prt7 = '50-8670'
	pprt7='50-8670'
	prt8 = pprt7[-4:]
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['659']
	asset6 = ['1703R']
	part  = ['50-8670']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-8670'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through

	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)


	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []


	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2



	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_8670_659'] = tot3
	request.session['shift_8670_659'] = shift2  #Need 
	request.session['pdate_8670_659'] = pdate_week  #Need
	request.session['op_totals_8670_659'] = op
	request.session['op_span_8670_659'] = operation_totals
	request.session['goal_8670_659'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_8670_659'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def ab1v_8670(request):
	prt7 = '50-8670'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 7000
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1750']
	part  = ['50-8670']
	asset1 = '1750'
	asset2 = '1724'
	asset3 = '1725'
	if request.session['prev_10r'] == 0:
		asset1 = '1750'
		asset2 = '1724'
		asset3 = '1725'

	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-8670'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start

	request.session['WL'] = 604800
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date

	wll = request.session['WL']

	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and (Machine = '%s' OR Machine ='%s' OR Machine ='%s') and Part = '%s' ORDER BY  %s %s" % (week_start,week_end,asset1,asset2,asset3,partno1,'TimeStamp','ASC')
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
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1
				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	count1 = int(a3[0][3])
	week_time = 604800
	pred1 = (count1 / float(week_time_todate))*week_time
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	request.session['totals_8670'] = tot3
	request.session['shift_8670'] = shift2  #Need 
	request.session['pdate_8670'] = pdate_week  #Need
	request.session['op_totals_8670'] = op
	request.session['op_span_8670'] = operation_totals
	request.session['goal_8670'] = int(pred1)
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_8670'] = inv_change
	return 

def ab1v_5401(request):
	prt7 = '50-5401'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 7000
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1750']
	part  = ['50-5401']
	asset1 = '1750'
	asset2 = '1724'
	asset3 = '1725'
	if request.session['prev_10r'] == 0:
		asset1 = '1750'
		asset2 = '1724'
		asset3 = '1725'

	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5401'
	week_start = request.session['week_start7'] 
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start

	request.session['WL'] = 604800
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date

	wll = request.session['WL']

	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and (Machine = '%s' OR Machine ='%s' OR Machine ='%s') and Part = '%s' ORDER BY  %s %s" % (week_start,week_end,asset1,asset2,asset3,partno1,'TimeStamp','ASC')
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
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1
				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	count1 = int(a3[0][3])
	week_time = 604800
	pred1 = (count1 / float(week_time_todate))*week_time
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	request.session['totals_5401'] = tot3
	request.session['shift_5401'] = shift2  #Need 
	request.session['pdate_5401'] = pdate_week  #Need
	request.session['op_totals_5401'] = op
	request.session['op_span_5401'] = operation_totals
	request.session['goal_5401'] = int(pred1)
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_5401'] = inv_change
	return 

def ab1v_5401_old2(request):
	prt7 = '50-5401'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 32970
	#db.close()
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1750']
	part  = ['50-5401']
	asset1 = '1724'
	asset2 = '1725'
	asset3 = '1750'
	if request.session['prev_10r'] == 0:
		asset1 = '1724'
		asset2 = '1725'
		asset3 = '1750'

	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5401'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7'] + 172800
	t = request.session['t']
	week_time_todate = t - week_start

	
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date

	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through


	
	# Select all reactions in asset list for date range
	#db, cur = db_set(request) 
	# sql = "SELECT * FROM vw_laser_scan WHERE part_number='%s' and ts >= '%s' and ts <= '%s' ORDER BY  %s %s" %(prt7,week_start,week_end,'ts','ASC')
	#sql = "SELECT * FROM GFxPRoduction WHERE Part='%s' and TimeStamp >= '%s' and TimeStamp <= '%s' and (Machine = '%s' OR Machine ='%s' OR Machine ='%s') ORDER BY  %s %s" %(prt7,week_start,week_end,asset1,asset2,asset3,'TimeStamp','ASC')
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,week_end,asset[0],part[0])

	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	t1 = []
	t2 = []
	
	for i in tmp:
		t1=[]
		t1.append(i[1])
		t1.append(str(i[2]))
		t1.append(i[3])
		# t1.append(i[3])
		# t1.append(i[4])
		t2.append(t1)
	tot2 = []
	tot3 = []


	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[2]>st and c[2]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1

				tot.append(a33)


				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2

	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_5401'] = tot3
	request.session['shift_5401'] = shift2  #Need 
	request.session['pdate_5401'] = pdate_week  #Need
	request.session['op_totals_5401'] = op
	request.session['op_span_5401'] = operation_totals
	request.session['goal_5401'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_5401'] = inv_change
	return  

def ab1v_5404(request):
	prt7 = '50-5404'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 7000
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1750']
	part  = ['50-5404']
	asset1 = '1750'
	asset2 = '1724'
	asset3 = '1725'
	if request.session['prev_10r'] == 0:
		asset1 = '1750'
		asset2 = '1724'
		asset3 = '1725'

	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5404'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start

	request.session['WL'] = 604800
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date

	wll = request.session['WL']

	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and (Machine = '%s' OR Machine ='%s' OR Machine ='%s') and Part = '%s' ORDER BY  %s %s" % (week_start,week_end,asset1,asset2,asset3,partno1,'TimeStamp','ASC')
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
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1
				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	count1 = int(a3[0][3])
	week_time = 604800
	pred1 = (count1 / float(week_time_todate))*week_time
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	request.session['totals_5404'] = tot3
	request.session['shift_5404'] = shift2  #Need 
	request.session['pdate_5404'] = pdate_week  #Need
	request.session['op_totals_5404'] = op
	request.session['op_span_5404'] = operation_totals
	request.session['goal_5404'] = int(pred1)
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_5404'] = inv_change
	return 


def ab1v_0450(request):
	prt7 = '50-0450'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 7000
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1750']
	part  = ['50-0450']
	asset1 = '1750'
	asset2 = '1724'
	asset3 = '1725'
	if request.session['prev_10r'] == 0:
		asset1 = '1750'
		asset2 = '1724'
		asset3 = '1725'

	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-0450'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start

	request.session['WL'] = 604800
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date

	wll = request.session['WL']

	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and (Machine = '%s' OR Machine ='%s' OR Machine ='%s') and Part = '%s' ORDER BY  %s %s" % (week_start,week_end,asset1,asset2,asset3,partno1,'TimeStamp','ASC')
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
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1
				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	count1 = int(a3[0][3])
	week_time = 604800
	pred1 = (count1 / float(week_time_todate))*week_time
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	request.session['totals_0450'] = tot3
	request.session['shift_0450'] = shift2  #Need 
	request.session['pdate_0450'] = pdate_week  #Need
	request.session['op_totals_0450'] = op
	request.session['op_span_0450'] = operation_totals
	request.session['goal_0450'] = int(pred1)
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_0450'] = inv_change
	return 

def ab1v_0447(request):
	prt7 = '50-0447'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 7000
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1750']
	part  = ['50-0447']
	asset1 = '1750'
	asset2 = '1724'
	asset3 = '1725'
	if request.session['prev_10r'] == 0:
		asset1 = '1750'
		asset2 = '1724'
		asset3 = '1725'

	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-0447'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start

	request.session['WL'] = 604800
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date

	wll = request.session['WL']

	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and (Machine = '%s' OR Machine ='%s' OR Machine ='%s') and Part = '%s' ORDER BY  %s %s" % (week_start,week_end,asset1,asset2,asset3,partno1,'TimeStamp','ASC')
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
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1
				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	count1 = int(a3[0][3])
	week_time = 604800
	pred1 = (count1 / float(week_time_todate))*week_time
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	request.session['totals_0447'] = tot3
	request.session['shift_0447'] = shift2  #Need 
	request.session['pdate_0447'] = pdate_week  #Need
	request.session['op_totals_0447'] = op
	request.session['op_span_0447'] = operation_totals
	request.session['goal_0447'] = int(pred1)
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_0447'] = inv_change
	return 

def ab1v_0519(request):
	prt7 = '50-0519'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 7000
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1750']
	part  = ['50-0519']
	asset1 = '1750'
	asset2 = '1724'
	asset3 = '1725'
	if request.session['prev_10r'] == 0:
		asset1 = '1750'
		asset2 = '1724'
		asset3 = '1725'

	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-0519'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start

	request.session['WL'] = 604800
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date

	wll = request.session['WL']

	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and (Machine = '%s' OR Machine ='%s' OR Machine ='%s') and Part = '%s' ORDER BY  %s %s" % (week_start,week_end,asset1,asset2,asset3,partno1,'TimeStamp','ASC')
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
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1
				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	count1 = int(a3[0][3])
	week_time = 604800
	pred1 = (count1 / float(week_time_todate))*week_time
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	request.session['totals_0519'] = tot3
	request.session['shift_0519'] = shift2  #Need 
	request.session['pdate_0519'] = pdate_week  #Need
	request.session['op_totals_0519'] = op
	request.session['op_span_0519'] = operation_totals
	request.session['goal_0519'] = int(pred1)
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_0519'] = inv_change
	return 

def ab1v_5404_OLD(request):
	prt7 = '50-5404'
	prt8 = prt7[-4:]

	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1719']
	part  = ['50-5404']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5404'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range



	# OLD METHOD
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,fi1,asset[0],part[0])
	# cur.execute(sql)
	# tmp = cur.fetchall()
	# t1 = []
	# t2 = []
	# for i in tmp:
	# 	t1=[]
	# 	t1.append(i[0])
	# 	t1.append(str(i[1]))
	# 	t1.append(i[2])
	# 	t1.append(i[3])
	# 	t1.append(i[4])
	# 	t2.append(t1)
	# tot2 = []
	# tot3 = []

	# for i in asset:
	# 	op4 = filter(lambda c:c[0]==i,operation_totals)
	# 	op5 = op4[0][1]  # Current operation
	# 	tot2 =[]

	# 	st = week_start
	# 	ctr = 0

	# 	for j in pdate_week:
	# 		for k in shift:
	# 			ctr = ctr + 1
	# 			fi = st + 28800
	# 			tot =[]
	# 			tot.append(i)
	# 			tot.append(j)
	# 			tot.append(k)
	# 			a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
	# 			sum1 = len(a3)

	# 			a33 = sum1
	# 			op[op5] = op[op5] + sum1


	# 			tot.append(a33)
	# 			tot2.append(tot)
	# 			# if ctr > 2:
	# 			# 	r=3/0
	# 			st = st + 28800
	# 	tot3.append(tot2)
	# color_used = color2

	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0
		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1
				op[op5] = op[op5] + a33
				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_5404'] = tot3
	request.session['shift_5404'] = shift2  #Need 
	request.session['pdate_5404'] = pdate_week  #Need
	request.session['op_totals_5404'] = op
	request.session['op_span_5404'] = operation_totals
	request.session['goal_5404'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_5404'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def prod_4865__manual(request):
	# ******************  Below data entered for each part  ******************************
	prt7 = '50-4865'
	db, cur = db_set(request) 
	# try:
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000
	db.close()
	color1 = '#93E08D'  # Color for line 1
	color2 = '#80C47B'  # Color for line 2
	asset = ['900']
	asset8 = '900'
	part  = ['50-4865']
	operation = [90]
	# ************************************************************************************

	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)

	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list

	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)

	asset_tuple = tuple(asset)
	partno1 = '50-4865'

	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']

	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal

	pdate_start = stamp_pdate2(week_start)
	pdate_week.append(pdate_start)

	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate2(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through

	db, cur = db_set(request)   
	# Select all reactions in asset list for date range
	sql = "SELECT asset_num,pdate,shift,partno,actual_produced FROM sc_production1 WHERE pdate >= '%s' and pdate <= '%s' and (partno = '%s') and (asset_num='%s' or asset_num='%s')"%(pdate_week[0],pdate_week[6],part[0],asset[0],asset8)
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
		
	# # *************************  Filter a list *****************************************************************
	# a1 = zip(*tmp)  # Unzip elements
	# a2 = [list(z) for z in zip(a1[0],a1[1],a1[2],a1[3],a1[4]) ]  # Rebuilt list so it's list of list
	# aa2 = [list(z) for z in zip(a1[4])]  # Rebuilt list so it's list of list
	# a3 = filter(lambda c:c[0]=='672',a2)  # Filter out '672' and form list a3
	# a22 = int(aa2[0][0])
	# a4 = filter(lambda c:c[2] == '3pm-11pm',a3)
	# # **********************************************************************************************************

	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
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
						op[op5] = op[op5] + int(m[4])
				except:
					a33 = 0
				tot.append(a33)
				tot2.append(tot)
		tot3.append(tot2)

	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)

	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_4865'] = tot3
	request.session['shift_4865'] = shift2
	request.session['pdate_4865'] = pdate_week
	request.session['op_totals_4865'] = op
	request.session['op_span_4865'] = operation_totals
	request.session['goal_4865'] = goal_todate

	a = int(operation_totals[0][3])
	b = int(goal_todate)

	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_4865'] = inv_change


	return

def prod_4748_live(request):
	prt7 = '50-4748'
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['797']
	part  = ['50-4748']
	operation = [90]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-4748'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,fi1,asset[0],part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_4748'] = tot3
	request.session['shift_4748'] = shift2  #Need 
	request.session['pdate_4748'] = pdate_week  #Need
	request.session['op_totals_4748'] = op
	request.session['op_span_4748'] = operation_totals
	request.session['goal_4748'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_4748'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def prod_5081(request):
	prt7 = '50-5081'
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1617']
	part  = ['50-5081']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5081'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,fi1,asset[0],part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				# TEMPORARY ******************
				if ctr == 1:
					dummy=4
					# sum1 = 1557
				# ***************************

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_5081'] = tot3

	# ***********************************************************************
	# tot3[0][0][3] = 1557   # Temporary add this to days to make week accurate
	# ***********************************************************************

	request.session['shift_5081'] = shift2  #Need 
	request.session['pdate_5081'] = pdate_week  #Need
	request.session['op_totals_5081'] = op
	request.session['op_span_5081'] = operation_totals
	request.session['goal_5081'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_5081'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def prod_4865a(request):
	prt7 = '50-4865'
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1617']
	part  = ['50-4865']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-4865'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,fi1,asset[0],part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				# TEMPORARY ******************
				if ctr == 1:
					dummy=5
					# sum1 = 1557
				# ***************************

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_4865'] = tot3

	# ***********************************************************************
	# tot3[0][0][3] = 1557   # Temporary add this to days to make week accurate
	# ***********************************************************************

	request.session['shift_4865'] = shift2  #Need 
	request.session['pdate_4865'] = pdate_week  #Need
	request.session['op_totals_4865'] = op
	request.session['op_span_4865'] = operation_totals
	request.session['goal_4865'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_4865'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def prod_4865_LIVE(request):
	# ******************  Below data entered for each part  ******************************
	prt7 = '50-4865'
	db, cur = db_set(request) 
	# try:
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000
	db.close()
	color1 = '#93E08D'  # Color for line 1
	color2 = '#80C47B'  # Color for line 2
	asset = ['900']
	asset8 = '1617'
	part  = ['50-4865']
	operation = [90]
	# ************************************************************************************

	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)

	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list

	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)

	asset_tuple = tuple(asset)
	partno1 = '50-4865'

	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']

	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal

	pdate_start = stamp_pdate2(week_start)
	pdate_week.append(pdate_start)

	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate2(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through

	db, cur = db_set(request)   
	# Select all reactions in asset list for date range
	sql = "SELECT asset_num,pdate,shift,partno,actual_produced FROM sc_production1 WHERE pdate >= '%s' and pdate <= '%s' and (partno = '%s') and (asset_num='%s' or asset_num='%s')"%(pdate_week[0],pdate_week[6],part[0],asset[0],asset8)
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
		
	# # *************************  Filter a list *****************************************************************
	# a1 = zip(*tmp)  # Unzip elements
	# a2 = [list(z) for z in zip(a1[0],a1[1],a1[2],a1[3],a1[4]) ]  # Rebuilt list so it's list of list
	# aa2 = [list(z) for z in zip(a1[4])]  # Rebuilt list so it's list of list
	# a3 = filter(lambda c:c[0]=='672',a2)  # Filter out '672' and form list a3
	# a22 = int(aa2[0][0])
	# a4 = filter(lambda c:c[2] == '3pm-11pm',a3)
	# # **********************************************************************************************************

	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
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
						op[op5] = op[op5] + int(m[4])
				except:
					a33 = 0
				tot.append(a33)
				tot2.append(tot)
		tot3.append(tot2)

	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)

	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_4865'] = tot3
	request.session['shift_4865'] = shift2
	request.session['pdate_4865'] = pdate_week
	request.session['op_totals_4865'] = op
	request.session['op_span_4865'] = operation_totals
	request.session['goal_4865'] = goal_todate

	a = int(operation_totals[0][3])
	b = int(goal_todate)

	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_4865'] = inv_change


	return
def prod_4865(request):
	# ******************  Below data entered for each part  ******************************
	prt7 = '50-4865'
	db, cur = db_set(request) 
	# try:
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000
	db.close()
	color1 = '#93E08D'  # Color for line 1
	color2 = '#80C47B'  # Color for line 2
	asset = ['900']
	asset8 = '1617'
	part  = ['50-4865']
	operation = [90]
	# ************************************************************************************

	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)

	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list

	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)

	asset_tuple = tuple(asset)
	partno1 = '50-4865'

	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']

	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal

	pdate_start = stamp_pdate2(week_start)
	pdate_week.append(pdate_start)

	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate2(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through

	db, cur = db_set(request)   
	# Select all reactions in asset list for date range
	sql = "SELECT asset_num,pdate,shift,partno,actual_produced FROM sc_production1 WHERE pdate >= '%s' and pdate <= '%s' and (partno = '%s') and (asset_num='%s' or asset_num='%s')"%(pdate_week[0],pdate_week[6],part[0],asset[0],asset8)
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
		
	# # *************************  Filter a list *****************************************************************
	# a1 = zip(*tmp)  # Unzip elements
	# a2 = [list(z) for z in zip(a1[0],a1[1],a1[2],a1[3],a1[4]) ]  # Rebuilt list so it's list of list
	# aa2 = [list(z) for z in zip(a1[4])]  # Rebuilt list so it's list of list
	# a3 = filter(lambda c:c[0]=='672',a2)  # Filter out '672' and form list a3
	# a22 = int(aa2[0][0])
	# a4 = filter(lambda c:c[2] == '3pm-11pm',a3)
	# # **********************************************************************************************************

	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
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
						op[op5] = op[op5] + int(m[4])
				except:
					a33 = 0
				tot.append(a33)
				tot2.append(tot)
		tot3.append(tot2)

	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)

	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_4865'] = tot3
	request.session['shift_4865'] = shift2
	request.session['pdate_4865'] = pdate_week
	request.session['op_totals_4865'] = op
	request.session['op_span_4865'] = operation_totals
	request.session['goal_4865'] = goal_todate

	a = int(operation_totals[0][3])
	b = int(goal_todate)

	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_4865'] = inv_change


	return
def prod_4900(request):
	prt7 = '50-4900'
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['936']
	part  = ['50-4900']
	operation = [90]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-4900'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,fi1,asset[0],part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_4900'] = tot3
	request.session['shift_4900'] = shift2  #Need 
	request.session['pdate_4900'] = pdate_week  #Need
	request.session['op_totals_4900'] = op
	request.session['op_span_4900'] = operation_totals
	request.session['goal_4900'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_4900'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return
def prod_6729(request):
	prt7 = '50-6729'
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000


	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['936']
	part  = ['50-6729']
	operation = [90]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-6729'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,fi1,asset[0],part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	request.session['totals_6729'] = tot3
	request.session['shift_6729'] = shift2  #Need 
	request.session['pdate_6729'] = pdate_week  #Need
	request.session['op_totals_6729'] = op
	request.session['op_span_6729'] = operation_totals
	request.session['goal_6729'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_6729'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return

def prod_6729b(request):
	# ******************  Below data entered for each part  ******************************
	prt7 = '50-6729'
	db, cur = db_set(request) 
	# try:
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7'] + 172800
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	try:
		goal = int(tmp[0][2])
	except:
		goal = 6000
	db.close()
	color1 = '#93E08D'  # Color for line 1
	color2 = '#80C47B'  # Color for line 2
	asset = ['900']
	asset8 = '900'
	part  = ['50-6729']
	asset5 = '936'
	operation = [90]
	# ************************************************************************************

	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(140)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)

	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list

	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)

	asset_tuple = tuple(asset)
	partno1 = '50-6729'

	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']

	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal

	pdate_start = stamp_pdate2(week_start)
	pdate_week.append(pdate_start)

	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate2(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	db, cur = db_set(request)   
	# Select all reactions in asset list for date range
	sql = "SELECT asset_num,pdate,shift,partno,actual_produced FROM sc_production1 WHERE pdate >= '%s' and pdate <= '%s' and (partno = '%s') and (asset_num='%s' or asset_num='%s')"%(pdate_week[0],pdate_week[6],part[0],asset[0],asset8)
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
	sql5 = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,fi1,asset5,part[0])
	cur.execute(sql5)
	tmp5 = cur.fetchall()
	t15 = []
	t25 = []
	for i in tmp5:
		t15=[]
		t15.append(i[0])
		t15.append(str(i[1]))
		t15.append(i[2])
		t15.append(i[3])
		t15.append(i[4])
		t25.append(t15)
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		ctr5 = 0
		st=week_start
		for j in pdate_week:
			for k in shift:
				tot =[]
				fi = st + 28800
				tot.append(i)
				tot.append(j)
				tot.append(k)
				ctr5 = ctr5 + 1
				if ctr5 < 7:
					tt5=0
					a3 = filter(lambda c:c[0]==i and c[1]==j and c[2]==k,t2)  
				else:
					tt5=1
					a3 = filter(lambda c:c[4]>st and c[4]<fi,t25) 
					sum1 = len(a3)
				try:
					if ctr5>6:
						a33=sum1
					else:
						a33 = 0
						for m in a3:
							a33 = a33 + int(m[4])
							op[op5] = op[op5] + int(m[4])
				except:
					a33 = 0
				tot.append(a33)
				tot2.append(tot)
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_6729'] = tot3
	request.session['shift_6729'] = shift2
	request.session['pdate_6729'] = pdate_week
	request.session['op_totals_6729'] = op
	request.session['op_span_6729'] = operation_totals
	request.session['goal_6729'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_6729'] = inv_change


	return

def prod_9341(request):

	prt7 = '50-9341'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 32970
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1533']
	part  = ['50-9341']
	asset1 = '1533'
	asset2 = '1533'
	if request.session['prev_10r'] == 0:
		asset1 = '1533'
		asset2 = '1816'

	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2

	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-9341'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start

	request.session['WL'] = 604800
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date

	wll = request.session['WL']

	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal





	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range

	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and (Machine = '%s' OR Machine ='%s') and Part = '%s' ORDER BY  %s %s" % (week_start,week_end,asset1,asset2,partno1,'TimeStamp','ASC')
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
	tot2 = []
	tot3 = []

	
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1

				tot.append(a33)


				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2

	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)

	
	count1 = int(a3[0][3])
	week_time = 604800
	pred1 = (count1 / float(week_time_todate))*week_time

	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date


	request.session['totals_9341'] = tot3
	request.session['shift_9341'] = shift2  #Need 
	request.session['pdate_9341'] = pdate_week  #Need

	rrrr=3/0
	request.session['op_totals_9341'] = op
	request.session['op_span_9341'] = operation_totals
	request.session['goal_9341'] = int(pred1)
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_9341'] = inv_change
	return 

def prod_0455(request):
	prt7 = '50-0455'
	db, cur = db_set(request) 
	# try:
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7']
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	goal = int(tmp[0][2])
	# except:
	# 	goal = 12460
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1812']
	part  = ['50-0455']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-9341'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,week_end,asset[0],part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_0455'] = tot3
	request.session['shift_0455'] = shift2  #Need 
	request.session['pdate_0455'] = pdate_week  #Need
	request.session['op_totals_0455'] = op
	request.session['op_span_0455'] = operation_totals
	request.session['goal_0455'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_0455'] = inv_change

	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	return


def prod_3050(request):
	prt7 = '50-3050'
	db, cur = db_set(request) 
	# try:
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7']
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	goal = int(tmp[0][2])
	# except:
	# 	goal = 12460
	# ******************  Below data entered for each part  ******************************
	color1 = '#F1CE98'  # Color for line 1
	color2 = '#E1C394'  # Color for line 2
	asset = ['769']
	part  = ['50-3050']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-3050'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(week_start,week_end,asset[0],part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0



		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_3050'] = tot3
	request.session['shift_3050'] = shift2  #Need 
	request.session['pdate_3050'] = pdate_week  #Need
	request.session['op_totals_3050'] = op
	request.session['op_span_3050'] = operation_totals
	request.session['goal_3050'] = goal_todate
	request.session['total_prod_3050'] = int(operation_totals[0][3]) 
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_3050'] = inv_change

	return
def prod_1467(request):
	prt7 = '50-1467'
	db, cur = db_set(request) 
	st1 = request.session['week_start7']
	fi1 = request.session['week_end7']
	sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
	cur.execute(sql)
	tmp = cur.fetchall()
	goal = int(tmp[0][2])

	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['650L']
	asset2 = '650R'
	asset3 = '769'
	part  = ['50-1467']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-1467'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(request.session['WL'])) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	if request.session['WL'] == 77: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s') and Part = '%s'" %(week_start,week_end,asset[0],asset2,asset3,part[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_1467'] = tot3
	request.session['shift_1467'] = shift2  #Need 
	request.session['pdate_1467'] = pdate_week  #Need
	request.session['op_totals_1467'] = op
	request.session['op_span_1467'] = operation_totals
	request.session['goal_1467'] = goal_todate
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)
	request.session['inv_change_1467'] = inv_change

	return

def prod_counts1(request):
	t=1674061455
	request.session['TCURR'] = t
	request.session['WL'] = 432000
	request.session['TCURR'] = t
	week_start_ab(request,t)
	ab1v_3214(request)
	ab1v_5214(request)
	ab1v_8670(request)
	ab1v_5401(request)
	ab1v_8670_659(request)
	ab1v_8670_626(request)

	ab1v_5404_1722(request)
	ab1v_5404(request)
	prod_6114_611(request)
	return render(request, "prod_counts.html")   

def prod_counts2(request):
	t=1674470211
	request.session['TCURR'] = t
	request.session['WL'] = 432000
	request.session['TCURR'] = t
	week_start_ab(request,t)
	ab1v_3214(request)
	ab1v_5214(request)
	ab1v_8670(request)
	ab1v_5401(request)
	ab1v_5404_1722(request)
	ab1v_5404(request)
	prod_6114_611(request)
	return render(request, "prod_counts.html")   

def hourly_counts(request,index):
	pd = index[:10]
	dy = index[-3:]
	asset = '611'
	part = '50-6114'
	stamp2 = pdate_stamp(pd)
	if dy == 'Mid':
		stamp2 = stamp2 - 7200
	elif dy == 'Day':
		stamp2 = stamp2 + 25200
	else:
		stamp2 = stamp2 + 54000
	stamp_start = stamp2
	stamp_end = stamp_start + 28800


	request.session["count_6114"] = filter_prod2(request,stamp_start,stamp_end,'611','50-6114')
	request.session["count_1722"] = filter_prod2(request,stamp_start,stamp_end,'1722','50-5404')


	db, cur = db_set(request) 

	# sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (stamp_start,stamp_end,part)
	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s'" % (stamp_start,stamp_end)
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()



	request.session["count_6420"] = filter_prod(tmp,stamp_start,'6420')
	request.session["count_6418"] = filter_prod(tmp,stamp_start,'6418')
	request.session["count_5404"] = filter_prod(tmp,stamp_start,'5404')
	request.session["count_3214"] = filter_prod(tmp,stamp_start,'3214')
	request.session["count_5214"] = filter_prod(tmp,stamp_start,'5214')



	request.session["pdate2"] = pd
	request.session["day2"] = dy
	return render(request, "hourly_counts.html")  

def filter_prod2(request,stamp_start,stamp_end,asset,part):
	db, cur = db_set(request) 
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s' and Part = '%s'" %(stamp_start,stamp_end,asset,part)
	cur.execute(sql)
	tmp = cur.fetchall()
	cnt=[]
	cnt2 = []
	hr = [1,2,3,4,5,6,7,8]
	for i in hr:
		st = stamp_start + (60 * 60 *  (i-1) )
		fi = st + (60 * 60)
		a3 = filter(lambda c:c[4]>st and c[4]<fi,tmp)  
		a4 = len(a3)
		cnt.append(a4)
		cnt2.append(fi)
	db.close()
	return cnt

def filter_prod(tmp,stamp_start,part):
	cnt=[]
	cnt2 = []
	hr = [1,2,3,4,5,6,7,8]
	for i in hr:
		st = stamp_start + (60 * 60 *  (i-1) )
		fi = st + (60 * 60)
		a3 = filter(lambda c:c[2]>st and c[2]<fi and c[1][-4:] == part,tmp)  
		a4 = len(a3)
		cnt.append(a4)
		cnt2.append(fi)
	return cnt

def prod_10R_initial(request):
	t=int(time.time())
	request.session['TCURR'] = t
	request.session['working_address'] = 'prod_10R'
	return render(request, "test_update7.html")  

def prod_ab1v_initial(request):
	t=int(time.time())
	request.session['TCURR'] = t
	request.session['working_address'] = 'prod_ab1v'
	return render(request, "test_update7.html") 

def prod_10R(request):
	request.session['WL'] = 432000
	request.session['prev_10r'] = 0
	t=int(time.time())
	request.session['TCURR'] = t
	week_start_10r(request,t)
	prod_9341(request)
	prod_0455(request)
	prod_3050(request)
	prod_1467(request)
	week_start_gf6(request,t)
	# gf6_1713(request)
	# gf6_3627(request)
	# gf6_1731(request)
	# gf6_3632(request)
	ab1v_8670(request)
	ab1v_5401(request)
	ab1v_5404(request)
	ab1v_0450(request)
	ab1v_0519(request)
	ab1v_0447(request)
	# prod_4748_live(request)
	prod_4865a(request)
	prod_5081(request)
	# prod_6729(request)
	# prod_4900(request)
	request.session['working_address'] = 'prod_10R'
	return render(request, "prod_10R.html")    

def prod_10R_prev(request):
	request.session['WL'] = 77
	request.session['working_address'] = 'prod_10R'
	t=request.session['week_start7']
	s=request.session['week_end7']

	t=t-488000
	
	week_start_10r(request,t)

	st1 = request.session['week_start7']
	fi1 = request.session['week_end7']


	


	request.session['prev_10r'] = 1
	prod_9341(request)
	prod_0455(request)
	prod_3050(request)
	prod_1467(request)
	week_start_gf6(request,t)
	# gf6_1713(request)
	# gf6_3627(request)
	# gf6_1731(request)
	# gf6_3632(request)
	ab1v_8670_2(request)
	ab1v_5401(request)
	ab1v_5404(request)
	ab1v_0450(request)
	ab1v_0519(request)
	ab1v_0447(request)
	# prod_4748_live(request)
	prod_4865a(request)
	prod_5081(request)
	# prod_6729(request)
	# prod_4900(request)
	return render(request, "prod_10R.html")  

def prod_ab1v_reaction(request):
	request.session['WL'] = 432000
	request.session['prev_10r'] = 0
	t=int(time.time())
	request.session['TCURR'] = t
	week_start_ab(request,t)
	prod_ab1v_1703(request)
	prod_ab1v_1704(request)


	# prod_ab1v_1722(request)
	request.session['working_address'] = 'prod_ab1v_reaction'
	return render(request, "prod_ab1v_reaction.html")   

def prod_ab1v_reaction_prev(request):
	request.session['WL'] = 432000
	request.session['prev_10r'] = 0
	t=request.session['week_end7']
	t=t-604800
	request.session['TCURR'] = t
	week_start_ab(request,t)
	prod_ab1v_1703(request)
	prod_ab1v_1704(request)
	prod_10r_1529(request)
	request.session['working_address'] = 'prod_ab1v_reaction'
	return render(request, "prod_ab1v_reaction.html")   

def prod_10r_1529(request):
	prt7 = '50-0455'
	prt9 = '50-0455'
	prt8 = prt7[-4:]
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt9,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150
	color1 = '#96dbf8' 
	color2 = '#82BED7'  
	asset = ['1529']
	operation = [10]
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals) 
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) 
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	x1 = 0
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t1.append(i[4])
		t2.append(t1)
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0
		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[5]>st and c[5]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1
				op[op5] = op[op5] + a33
				tot.append(a33)
				tot.append(st)
				tot2.append(tot)
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_1529'] = tot3
	request.session['shift_1529'] = shift2  #Need 
	request.session['pdate_1529'] = pdate_week  #Need
	request.session['op_totals_1529'] = op
	request.session['op_span_1529'] = operation_totals
	request.session['goal_1529'] = goal_todate

	return

def prod_ab1v_1704(request):
	prt7 = '50-8670'
	prt9 = '50-8670'
	prt8 = prt7[-4:]
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt9,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150

	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1704R']
	part  = ['50-8670']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5401'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	x1 = 0
	for i in tmp:
		t1=[]
		x2 = i[4]
		if (x2-x1) > 150:
			t1.append(i[0])
			t1.append('GP12')
			t1.append(prt8)
			t1.append(i[5])
			t1.append(i[2])
			t1.append(i[4])
			t2.append(t1)
		x1 = i[4]


	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[5]>st and c[5]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot.append(st)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)


	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)


	request.session['totals_5399y'] = tot3
	request.session['shift_5399y'] = shift2  #Need 
	request.session['pdate_5399y'] = pdate_week  #Need
	request.session['op_totals_5399y'] = op
	request.session['op_span_5399y'] = operation_totals
	request.session['goal_5399y'] = goal_todate
	return

def prod_ab1v_1703(request):
	prt7 = '50-8670'
	prt9 = '50-8670'
	prt8 = prt7[-4:]
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt9,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150

	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['1703R']
	part  = ['50-8670']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5401'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	x1 = 0
	for i in tmp:
		t1=[]
		x2 = i[4]
		if (x2-x1) > 150:
			t1.append(i[0])
			t1.append('GP12')
			t1.append(prt8)
			t1.append(i[5])
			t1.append(i[2])
			t1.append(i[4])
			t2.append(t1)
		x1 = i[4]

	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[5]>st and c[5]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot.append(st)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)


	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)


	request.session['totals_5399x'] = tot3
	request.session['shift_5399x'] = shift2  #Need 
	request.session['pdate_5399x'] = pdate_week  #Need
	request.session['op_totals_5399x'] = op
	request.session['op_span_5399x'] = operation_totals
	request.session['goal_5399x'] = goal_todate
	return

def prod_ab1v(request):
	request.session['WL'] = 432000
	request.session['prev_10r'] = 0
	t=int(time.time())
	request.session['TCURR'] = t
	week_start_10r(request,t)
	prod_ab1v_5401(request)
	# prod_ab1v_5401_ag(request)
	prod_ab1v_5404(request)
	prod_ab1v_6420(request)
	prod_ab1v_3214(request)
	prod_ab1v_5214(request)

	request.session['working_address'] = 'prod_ab1v_prev'
	return render(request, "prod_ab1v.html")   

def prod_ab1v_prev(request):
	request.session['WL'] = 432000
	request.session['prev_10r'] = 0
	t=request.session['week_end7']
	t=t-604800
	request.session['TCURR'] = t
	week_start_10r(request,t)
	prod_ab1v_5401(request)
	# prod_ab1v_5401_ag(request)
	prod_ab1v_5404(request)
	prod_ab1v_6420(request)
	prod_ab1v_3214(request)
	prod_ab1v_5214(request)

	request.session['working_address'] = 'prod_ab1v'
	return render(request, "prod_ab1v.html")   

def prod_ab1v_5401(request):
	prt7 = '50-6418'
	prt9 = '50-5401'
	prt8 = prt7[-4:]
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt9,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150

	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['900']
	part  = ['50-5401']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5401'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_5401a'] = tot3
	request.session['shift_5401a'] = shift2  #Need 
	request.session['pdate_5401a'] = pdate_week  #Need
	request.session['op_totals_5401a'] = op
	request.session['op_span_5401a'] = operation_totals
	request.session['goal_5401a'] = goal_todate
	return

def prod_ab1v_5401_ag(request):
	prt7 = '50-6418'
	prt9 = '50-5401'
	prt8 = prt7[-4:]
	

	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt9,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150

	db.close()

	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['900']
	part  = ['50-5401']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5401'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)


	pd101 = stamp_pdate3(week_start)



	week_end = week_start + 604800
	pd202 = stamp_pdate3(week_end)

	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	pf = 1


	#db, cur = db_set_vant(request) 

	db, cur = db_set(request) 

	sql = "SELECT * from 1730_Vantage where created_at >= '%s' and created_at <= '%s' and part_number = '%s' and part_fail = '%s'" % (pd101,pd202,prt9,pf)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()

	db.close()


	t1 = []
	t2 = []

	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('100P')
		
		t1.append(prt8)


		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_5401ag'] = tot3
	request.session['shift_5401ag'] = shift2  #Need 
	request.session['pdate_5401ag'] = pdate_week  #Need
	request.session['op_totals_5401ag'] = op
	request.session['op_span_5401ag'] = operation_totals
	request.session['goal_5401ag'] = goal_todate
	return

def prod_ab1v_6420(request):
	prt7 = '50-6420'
	prt9 = '50-8670'
	prt8 = prt7[-4:]
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt9,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['900']
	part  = ['50-6420']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-6420'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_6420a'] = tot3
	request.session['shift_6420a'] = shift2  #Need 
	request.session['pdate_6420a'] = pdate_week  #Need
	request.session['op_totals_6420a'] = op
	request.session['op_span_6420a'] = operation_totals
	request.session['goal_6420a'] = goal_todate
	return

def prod_ab1v_5404(request):
	prt7 = '50-5404'
	prt8 = prt7[-4:]
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['900']
	part  = ['50-5404']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5404'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range




	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0
		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1
				op[op5] = op[op5] + a33
				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2






	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_5404a'] = tot3
	request.session['shift_5404a'] = shift2  #Need 
	request.session['pdate_5404a'] = pdate_week  #Need
	request.session['op_totals_5404a'] = op
	request.session['op_span_5404a'] = operation_totals
	request.session['goal_5404a'] = goal_todate




	return

def prod_ab1v_5214(request):
	prt7 = '50-5214'
	prt8 = prt7[-4:]
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['900']
	part  = ['50-5214']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5214'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_5214a'] = tot3
	request.session['shift_5214a'] = shift2  #Need 
	request.session['pdate_5214a'] = pdate_week  #Need
	request.session['op_totals_5214a'] = op
	request.session['op_span_5214a'] = operation_totals
	request.session['goal_5214a'] = goal_todate
	return

def prod_ab1v_5214(request):
	prt7 = '50-5214'
	prt8 = prt7[-4:]
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['900']
	part  = ['50-5214']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-5214'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_5214a'] = tot3
	request.session['shift_5214a'] = shift2  #Need 
	request.session['pdate_5214a'] = pdate_week  #Need
	request.session['op_totals_5214a'] = op
	request.session['op_span_5214a'] = operation_totals
	request.session['goal_5214a'] = goal_todate
	return

def prod_ab1v_3214(request):
	prt7 = '50-3214'
	prt8 = prt7[-4:]
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['900']
	part  = ['50-3214']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-3214'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through
	# Select all reactions in asset list for date range
	sql = "SELECT * from barcode where scrap >= '%s' and scrap <= '%s' and RIGHT(asset_num,4) = '%s'" % (week_start,week_end,prt8)
	# sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
	cur.execute(sql)
	tmp = cur.fetchall()
	t1 = []
	t2 = []
	for i in tmp:
		t1=[]
		t1.append(i[0])
		t1.append('GP12')
		t1.append(prt8)
		t1.append(i[5])
		t1.append(i[2])
		t2.append(t1)
	tot2 = []
	tot3 = []
	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]
		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)
				a33 = sum1

				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800
		tot3.append(tot2)
	color_used = color2
	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_3214a'] = tot3
	request.session['shift_3214a'] = shift2  #Need 
	request.session['pdate_3214a'] = pdate_week  #Need
	request.session['op_totals_3214a'] = op
	request.session['op_span_3214a'] = operation_totals
	request.session['goal_3214a'] = goal_todate
	return


def prod_3050_prod(request):
	prt7 = '50-1467'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['728O']
	part  = ['50-1467']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-1467'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	 
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				
				# Safegaurd to know when 3050s are running down
				if a33 < 400:
					a33 = 0


				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_3050p'] = tot3
	request.session['shift_3050p'] = shift2  #Need 
	request.session['pdate_3050p'] = pdate_week  #Need
	request.session['op_totals_3050p'] = op
	request.session['op_span_3050p'] = operation_totals
	request.session['goal_3050p'] = goal_todate
	return
def prod_728_over(request):
	prt7 = '50-1467'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['728O']
	part  = ['50-1467']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-1467'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	 
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				
				# Safegaurd to know when 3050s are running down
				if a33 > 400:
					a33 = 0


				op[op5] = op[op5] + a33

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_1467o'] = tot3
	request.session['shift_1467o'] = shift2  #Need 
	request.session['pdate_1467o'] = pdate_week  #Need
	request.session['op_totals_1467o'] = op
	request.session['op_span_1467o'] = operation_totals
	request.session['goal_1467o'] = goal_todate
	return


def prod_728_prod(request):
	prt7 = '50-1467'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['728']
	part  = ['50-1467']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-1467'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	 
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1


				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_1467p'] = tot3
	request.session['shift_1467p'] = shift2  #Need 
	request.session['pdate_1467p'] = pdate_week  #Need
	request.session['op_totals_1467p'] = op
	request.session['op_span_1467p'] = operation_totals
	request.session['goal_1467p'] = goal_todate
	return

def prod_728(request):
	prt7 = '50-1467'
	db, cur = db_set(request) 
	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt7,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 150
	# ******************  Below data entered for each part  ******************************
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['728R']
	part  = ['50-1467']
	operation = [10]
	# ************************************************************************************
	shift = ['11pm-7am','7am-3pm','3pm-11pm']
	shift2 = ['Mid','Day','Aft']
	pdate_week = []
	op = [0 for x in range(50)]	
	ctr_operation = []
	for i in operation:
		ctr = 0
		for ii in operation:
			if i == ii: ctr = ctr + 1
		ctr_operation.append(ctr)
	operation_totals = zip(asset,operation,ctr_operation)
	b1 = zip(*operation_totals)  # Unzip elements
	b2 = [list(z) for z in zip(b1[0],b1[1],b1[2]) ]  # Rebuilt list so it's list of list
	x = 0
	for i in b2:
		x = x + 1
		for c in range(x,len(b2)):
			if i[1] == b2[c][1]:
				b2[c][2] = 0
	operation_totals = b2
	total = zip(asset,part,operation)
	asset_tuple = tuple(asset)
	partno1 = '50-1467'
	week_start = request.session['week_start7']
	week_end = request.session['week_end7']
	t = request.session['t']
	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	 
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and Machine = '%s'" %(week_start,week_end,asset[0])
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
	tot2 = []
	tot3 = []

	for i in asset:
		op4 = filter(lambda c:c[0]==i,operation_totals)
		op5 = op4[0][1]  # Current operation
		tot2 =[]

		st = week_start
		ctr = 0

		for j in pdate_week:
			for k in shift:
				ctr = ctr + 1
				fi = st + 28800
				tot =[]
				tot.append(i)
				tot.append(j)
				tot.append(k)
				a3 = filter(lambda c:c[4]>st and c[4]<fi,t2)  
				sum1 = len(a3)

				a33 = sum1
				op[op5] = op[op5] + sum1

				tot.append(a33)
				tot2.append(tot)
				# if ctr > 2:
				# 	r=3/0
				st = st + 28800

		tot3.append(tot2)


	color_used = color2


	for i in operation_totals:
		i.append(op[i[1]])
		if i[2] != 0:
			if color_used == color2 :
				color_used = color1
			else:
				color_used = color2
		i.append(color_used)
	for i in tot3:
		for ii in i:
			a3 = filter(lambda c:c[0]==ii[0],operation_totals)  
			a4=a3[0][4]
			ii.append(a4)
	request.session['totals_1467b'] = tot3
	request.session['shift_1467b'] = shift2  #Need 
	request.session['pdate_1467b'] = pdate_week  #Need
	request.session['op_totals_1467b'] = op
	request.session['op_span_1467b'] = operation_totals
	request.session['goal_1467b'] = goal_todate
	return

def prod_728fault(request):
	t=int(time.time())
	week_start_10r(request,t)
	prod_728(request)
	prod_728_prod(request)
	prod_728_over(request)
	prod_3050_prod(request)
	return render(request, "trilobe_fault.html")  

def prod_728fault_prev(request):
	t=request.session['week_end7']
	t=t-604800
	week_start_10r(request,t)
	prod_728(request)
	prod_728_prod(request)
	prod_728_over(request)
	prod_3050_prod(request)
	return render(request, "trilobe_fault.html")  


def test_email_7(request):
	# b = "\r\n"
	# ctr = 0
	# current_part = ' For Dave Clark'
	# message_subject = 'Test Email'
	# message3 = "Just Checking this Email Route" + current_part 
	# toaddrs = ["dclark@stackpole.com"]
	# fromaddr = 'stackpole@stackpole.com'
	# frname = 'Dave'
	# server = SMTP('smtp.gmail.com', 587)
	# server.ehlo()
	# server.starttls()
	# server.ehlo()
	# server.login('StackpolePMDS@gmail.com', 'stacktest6060')
	# message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
	# message = message+message_subject + "\r\n\r\n" + "\r\n\r\n" + message3 + "\r\n\r\n" 
	# server.sendmail(fromaddr, toaddrs, message)
	# server.quit()
	# return render(request,"done_test2.html")

	# b = "\r\n"
	# ctr = 0
	# current_part = ' For Dave Clark'
	# message_subject = 'Test Email'
	# message3 = "Just Checking this Email Route" + current_part 
	# toaddrs = ["dclark@stackpole.com"]
	# fromaddr = 'stratford.reports@stackpole.com'
	# frname = '10R Production'
	# server = SMTP('smtp01.stackpole.ca')
	# server.ehlo()
	# server.starttls()
	# server.ehlo()
	# # server.login('stackpolepmds@gmail.com', 'stacktest6060')
	# message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
	# message = message+message_subject + "\r\n\r\n" + "\r\n\r\n" + message3 + "\r\n\r\n" 
	# server.sendmail(fromaddr, toaddrs, message)
	# server.quit()
	return render(request,"done_test2.html")

def track_single(request):
	request.session['data_area'] = 1
	request.session['target_area'] = 1
	request.session['part_area'] = '50-9341'
	request.session['rate_area'] = 217
	request.session['asset1_area'] = '1533'
	request.session['asset2_area'] = '1533'
	request.session['asset3_area'] = '1533'
	request.session['asset4_area'] = '1533'
	data1, gr_list1 = track_area_single(request)
	return render(request, "track_single.html",{'GList':gr_list1,"datax":data1})

def stamp_shift_start(request):
	# t = 1624725088  # Temporary time
	# stamp = t
	stamp=int(time.time())
	t=stamp
	tm = time.localtime(stamp)
	hour1 = tm[3]
	# t=int(time.time())
	tm = time.localtime(t)
	shift_start = -2
	current_shift = 3
	if tm[3]<22 and tm[3]>=14:
		shift_start = 14
	elif tm[3]<14 and tm[3]>=6:
		shift_start = 6
	cur_hour = tm[3]
	if cur_hour == 22:
		cur_hour = -1

	# Unix Time Stamp for start of shift Area 1
	u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])	

	# Amount of seconds run so far on the shift
	shift_time = t-u  

	# Amount of seconds left on the shift to run
	shift_left = 28800 - shift_time  

	# Unix Time Stamp for the end of the shift
	shift_end = t + shift_left

	return u,shift_time,shift_left,shift_end


def track_area_single(request):
	data_area = '1'
	target_area = int(request.session['rate_area'])
	prt = '50-1467'
	rate1 = request.session['rate_area']
	asset1 = '769'
	asset2 = '650L'
	asset3 = '650R'
	asset4 = '650R'
	target = rate1

	t=int(time.time())
	# t=1624725088.58 # Temp for local use only
	x = int(t - 489600)
	tm = time.localtime(t)
	request.session["time"] = t


	u,shift_time,shift_left,e = stamp_shift_start(request)

	request.session["shift_time"] = shift_time

	
	# Calculate start of week unix (Monday 00:00am)
	a1 = tm[6] * 86400
	a2 = tm[3] * 60 * 60
	a3 = tm[4] * 60
	a4 = tm[5]
	week_start1 = t - a1 - a2 - a3 - a4
	week_current_seconds = t - week_start1

	
	u=u-(60*60*8*84)
	db, cur = db_set(request)
	aql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (u,t,prt,asset1,asset2,asset3,asset4)
	cur.execute(aql)
	tmp2 = cur.fetchall()

	try:
		st1 = request.session['week_start7']
		fi1 = request.session['week_end7']
		sql = "SELECT * FROM tkb_weekly_goals WHERE part = '%s' and timeStamp >= '%s' and timeStamp <= '%s'" %(prt,st1,fi1)
		cur.execute(sql)
		tmp = cur.fetchall()
		goal = int(tmp[0][2])
	except:
		goal = 32970


	# tmp3 = tmp2[0]
	# cnt = tmp3[0]
	x=3/0



	t2=int(time.time())

	var1 = 'count' + data_area


	request.session[var1] = cnt
	if week_current_seconds > 43200:
		weekend_cnt = 0
		bql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (weekend_start,t,prt,asset1,asset2,asset3,asset4)
		cur.execute(bql)
		tmp8 = cur.fetchall()
		tmp9 = tmp8[0]
		weekend_cnt = tmp9[0]

	bql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (week_start1,t,prt,asset1,asset2,asset3,asset4)
	cur.execute(bql)
	tmp8 = cur.fetchall()
	tmp9 = tmp8[0]
	try:
		week_cnt = int(tmp9[0])
	except:
		week_cnt = 0
	bql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (week_start2,week_start1,prt,asset1,asset2,asset3,asset4)
	cur.execute(bql)
	tmp8 = cur.fetchall()
	tmp9 = tmp8[0]
	try:
		week_cnt2 = int(tmp9[0])
	except:
		week_cnt2 = 0
	bql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (week_start3,week_start2,prt,asset1,asset2,asset3,asset4)
	cur.execute(bql)
	tmp8 = cur.fetchall()
	tmp9 = tmp8[0]
	try:
		week_cnt3 = int(tmp9[0])
	except:
		week_cnt3 = 0

	week_cnt = 0
	week_cnt2 = 0
	week_cnt3 = 0



	u1, wd1, m1, day1, shift1, prev_cnt1 = [],[],[],[],[],[]
	utemp = u
	total_test = 0
	
	for i in range(1,16):
		unew = utemp - 28800
		x1, x2, x3, x4 = day_breakdown(unew)
		u1.append(str(unew))
		wd1.append(x1)
		m1.append(x2)
		day1.append(x3)
		shift1.append(x4)
		aql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (unew,utemp,prt,asset1,asset2,asset3,asset4)

		# aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (unew,utemp,prt,asset1,asset2,asset3,asset4)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]



		prev_cnt1.append(str(tmp3[0]))

		# prev_cnt1.append('0')

		try:
			total_test = total_test + int(tmp3[0])
		except:
			total_test = total_test + 0
		utemp = unew

	db.close()
	request.session['total_test'] = total_test

	# 5 day week 432000
	# 7 day week 604800
	# the weekend is 172800
	wrm = 0
	if prt == '50-9341':
		wrm = 0
	elif prt == '50-1467':
		wrm = 1
	elif prt == '50-3050':
		wrm = 1

	weekend_projection = 1
	if week_current_seconds < 432000:
		week_left = 432000 - week_current_seconds
		week_rate = week_cnt / float(week_current_seconds)
		week_projection = int(week_rate * (week_left)) + week_cnt 
		weekend_projection = int(week_rate * (172800)* wrm) 
		# week_projection = week_projection + weekend_projection

	else:
		weekend_left = 172800 - weekend_current_seconds
		weekend_rate = weekend_cnt / float(weekend_current_seconds)
		week_projection = int(weekend_rate * (weekend_left)) + week_cnt

	if prt == '50-9341' or prt == '50-1467' or prt == '50-3050':
		# week_rate2 = week_rate / float(2)
		# week_rate2 = week_rate2 * 172800
		week_projection = week_projection + weekend_projection
		if prt == '50-9341':
			week_projection = week_projection + 4500
	if prt == '50-0455':
		week_projection = week_projection + 2250

	current_rate = cnt / float(shift_time)
	projection = int(current_rate * (shift_left)) + cnt
	
	oa = cnt / float(target)
	oa = (int(oa * 10000)) / float(100)
	check_area = request.session['data_area']
	if check_area == 1:
		request.session["oa1"] = oa
		
		# if asset1 == '1533':
		#	interval1 = 900
		#	m, b, start_count = prediction1(request,u,t,interval1,u)
		#	projection = m*e + b
		#	projection = projection - start_count

		#	intervalst = 1610325078
		#	interval1 = 2880
		#	m, b, start_count = prediction1(request,intervalst,t,interval1,intervalst)
		#	week_projection = m*ew + b
		#	week_projection = week_projection - start_count
			

		request.session["projection1"] = int(projection)
		request.session["count1"] = cnt
		request.session["week_count1"] = week_cnt
		request.session["week_projection1"] = week_projection
		request.session["week_count1a"] = week_cnt2
		request.session["week_count1b"] = week_cnt3
		request.session['target1'] = int(target)
	else:
		request.session["oa2"] = oa
		if asset1 == '1533':
			interval1 = 3600
			m, b, start_count = prediction1(request,u,t,interval1,u)
			projection = m*e + b
			projection = projection - start_count
		request.session["projection2"] = int(projection)
		request.session["count2"] = cnt
		request.session["week_count2"] = week_cnt
		request.session["week_projection2"] = week_projection
		request.session["week_count2a"] = week_cnt2
		request.session["week_count2b"] = week_cnt3
		request.session['target2'] = int(target)

	gr_list = track_data(request,t,u,prt,rate1) # Get the Graph Data
	data1 = zip(u1,wd1,m1,day1,shift1,prev_cnt1)
	return data1, gr_list

def track_data(request,t,u,part,rate):
	m = '1533'
	asset1 = request.session['asset1_area']
	asset2 = request.session['asset2_area']
	asset3 = request.session['asset3_area']
	asset4 = request.session['asset4_area']
	# mrr = (337*(28800))/float(28800)
	mrr = (rate*(28800))/float(28800)
	db, cursor = db_set(request)
	sql = "SELECT * FROM GFxPRoduction where TimeStamp >= '%d' and TimeStamp< '%d' and part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" %(u,t,part,asset1,asset2,asset3,asset4)
	cursor.execute(sql)
	tmp = cursor.fetchall()	
	db.close()
	gr_list, brk1, brk2, multiplier	 = Graph_Data(t,u,m,tmp,mrr)
	return gr_list

def live_10R(request):
	return render(request, "live_10R.html")  

def live_update1(request):
	try:
		ctr = request.session['ctr1']
	except:
		request.session['ctr1'] = 1
		ctr = 1
	ctr = ctr + 2
	time.sleep(1)
	request.session['ctr1'] = ctr
	return render(request, "test99.html",{'ctr':ctr})  


def pareto_test(request):
	db, cursor = db_set(request)
	d1 = str(request.session['downtime_month'])
	p1 = str(request.session['product_line'])
	d2_1 = d1[:5]
	d2_2 = d1[-2:]
	d2_2 = str(int(d2_2) + 1)
	if len(d2_2) < 2: d2_2 = '0' + d2_2
	d2 = d2_1 + d2_2



	aa = ['1504','1506','1518','1519','1520','1521','1522','1523','1502','1507','1539','1540','1515','1501','1524','1525','1508','1532','1538','1509','1513','1533','1503','1530','1511','1528']
	aw = [8,8,8,8,8,8,8,8,5,5,5,5,5,5,5,5,4,4,4,3,2,1,2,2,2,2]

	asset1=request.session['top_asset']
	ccat = request.session['top_category']
	

	c1 = 'Hydraulic'
	# sql = "SELECT * FROM Maintenance_Data where asset = '%s' and completedtime> '%s' and completedtime < '%s' and category = '%s'" %(asset1,d1,d2,c1)

	if p1 == '10R80':
		sql = "SELECT asset,problem,remedy,(ROUND(ROUND(Downtime,0)/3600,2))/asset_duplicates AS Hrs ,category FROM vw_Maintenance_Data_10R80 where completedtime> '%s' and completedtime < '%s' and asset='%s' and category='%s' ORDER BY %s %s " %(d1,d2,asset1,ccat,'Downtime','DESC')
		wql = "SELECT asset,category,sum(Downtime)/asset_duplicates FROM vw_Maintenance_Data_10R80 where completedtime> '%s' and completedtime < '%s' Group by asset,category" %(d1,d2)
		request.session['downtime_title'] = 'Downtime 10R80 Pareto ' + d1
	elif p1 == 'AB1V Inputs':
		sql = "SELECT asset,problem,remedy,(ROUND(ROUND(Downtime,0)/3600,2))/asset_duplicates AS Hrs ,category FROM vw_Maintenance_Data_AB1V_Inputs where completedtime> '%s' and completedtime < '%s' and asset='%s' and category='%s' ORDER BY %s %s " %(d1,d2,asset1,ccat,'Downtime','DESC')
		wql = "SELECT asset,category,sum(Downtime)/asset_duplicates FROM vw_Maintenance_Data_AB1V_Inputs where completedtime> '%s' and completedtime < '%s' Group by asset,category" %(d1,d2)
		request.session['downtime_title'] = 'Downtime AB1V Inputs Pareto ' + d1
	elif p1 == 'AB1V Overdrives':
		sql = "SELECT asset,problem,remedy,(ROUND(ROUND(Downtime,0)/3600,2))/asset_duplicates AS Hrs ,category FROM vw_Maintenance_Data_AB1V_Overdrives where completedtime> '%s' and completedtime < '%s' and asset='%s' and category='%s' ORDER BY %s %s " %(d1,d2,asset1,ccat,'Downtime','DESC')
		wql = "SELECT asset,category,sum(Downtime)/asset_duplicates FROM vw_Maintenance_Data_AB1V_Overdrives where completedtime> '%s' and completedtime < '%s' Group by asset,category" %(d1,d2)
		request.session['downtime_title'] = 'Downtime AB1V Overdrives Pareto ' + d1
	else: 
		sql = "SELECT asset,problem,remedy,(ROUND(ROUND(Downtime,0)/3600,2))/asset_duplicates AS Hrs ,category FROM vw_Maintenance_Data_AB1V_Reactions where completedtime> '%s' and completedtime < '%s' and asset='%s' and category='%s' ORDER BY %s %s " %(d1,d2,asset1,ccat,'Downtime','DESC')
		wql = "SELECT asset,category,sum(Downtime)/asset_duplicates FROM vw_Maintenance_Data_AB1V_Reactions where completedtime> '%s' and completedtime < '%s' Group by asset,category" %(d1,d2)
		request.session['downtime_title'] = 'Downtime AB1V Reactions Pareto ' + d1


	cursor.execute(sql)
	tmp = cursor.fetchall()	

	cursor.execute(wql)
	tmp2 = cursor.fetchall()


	tmp4=sorted(tmp2,key=lambda x:(x[2]),reverse=True)

	asset1 = []
	cat1 = []
	time1 = []
	link1 = []

	ctr = 0
	for i in tmp4:
		asset1.append(i[0])
		cat1.append(i[1])
		
		t1 = int(i[2])
		t1 = t1 / float(60)
		t1 = t1 / float(60)
		time1.append(t1)
		link1.append(i[0]+'*'+i[1])
		ctr = ctr + 1
		if ctr > 9: break
	data2=zip(asset1,cat1,time1,link1)


	db.close()

	return render(request, "pareto_test.html",{'data1':tmp,'data2':data2})  

def downtime_month_selection(request):
	request.session['top_asset'] = ''
	request.session['top_category'] = ''
	if request.POST:
		month = request.POST.get("start")
		pline = request.POST.get("pline")
		request.session['downtime_month'] = month
		request.session['product_line'] = pline

		return render(request, "redirect_pareto_test.html")


	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'downtime_month_selection.html',{'args':args})



def downtime_category_selection(request,index):
	a=index
	f1 = a.find('*')
	b1 = a[:f1]
	f1 = (len(a)-f1-1)*-1
	b2 = a[f1:]
	request.session['top_asset'] = b1
	request.session['top_category'] = b2


	return render(request, "redirect_pareto_test.html") 

def downtime_category_history(request,index):



	a=index
	f1 = a.find('*')
	b1 = str(a[:f1])
	f1 = (len(a)-f1-1)*-1
	b2 = str(a[f1:])
	request.session['top_asset'] = b1
	request.session['top_category'] = b2
	request.session['pareto_history_title'] = b1 + ' ' + b2

	dd = ['2023-04','2023-05','2023-06','2023-07']
	data1 =[]
	a=[]
	db, cursor = db_set(request)
	for i in dd:
		d1 = i
		d2_1 = d1[:5]
		d2_2 = d1[-2:]
		d2_2 = str(int(d2_2) + 1)
		if len(d2_2) < 2: d2_2 = '0' + d2_2
		d2 = d2_1 + d2_2

		
		sql = "SELECT sum(Downtime) FROM vw_Maintenance_Data_10R80 where asset = '%s' and category = '%s' and completedtime > '%s' and completedtime < '%s'" %(b1,b2,d1,d2)
		cursor.execute(sql)
		tmp4 = cursor.fetchall()	

		sql = "SELECT sum(Downtime) FROM vw_Maintenance_Data_AB1V_Overdrives where asset = '%s' and category = '%s' and completedtime > '%s' and completedtime < '%s'" %(b1,b2,d1,d2)
		cursor.execute(sql)
		tmp1 = cursor.fetchall()	

		sql = "SELECT sum(Downtime) FROM vw_Maintenance_Data_AB1V_Inputs where asset = '%s' and category = '%s' and completedtime > '%s' and completedtime < '%s'" %(b1,b2,d1,d2)
		cursor.execute(sql)
		tmp2 = cursor.fetchall()	

		sql = "SELECT sum(Downtime) FROM vw_Maintenance_Data_AB1V_Reactions where asset = '%s' and category = '%s' and completedtime > '%s' and completedtime < '%s'" %(b1,b2,d1,d2)
		cursor.execute(sql)
		tmp3 = cursor.fetchall()	


		
		q1 = tmp4[0][0]
		q2 = tmp3[0][0]
		q3 = tmp2[0][0]
		q4 = tmp1[0][0]

		if q1 == None: q1 = 0
		if q2 == None: q2 = 0
		if q3 == None: q3 = 0
		if q4 == None: q4 = 0

		q5=q1+q2+q3+q4
	





		data1.append(q5)
	


	# for i in data1:
	# 	try:
	# 		x=int(i[0])
	# 	except:
	# 		x=0
	# 	a.append(x)






	


	return render(request, "pareto_history.html",{'data1':data1}) 