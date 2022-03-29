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
from views_db import db_open, db_set,net1, db_set2
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
	goal = 3000   # Weekly6 Goal
	color1 = '#96dbf8'  # Color for line 1
	color2 = '#82BED7'  # Color for line 2
	asset = ['576','595','635','628','672','667','900']
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
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
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

	return
  
def gf6_3627(request):
	# ******************  Below data entered for each part  ******************************
	goal = 7500   # Weekly6 Goal
	color1 = '#93E08D'  # Color for line 1
	color2 = '#80C47B'  # Color for line 2
	asset = ['732','583','582','580','616','617','731','682','674','673','675','676','566','745','900']
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

	week_time_todate = t - week_start
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal

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
	return

def gf6_1731(request):
	# ******************  Below data entered for each part  ******************************
	goal = 3000   # Weekly6 Goal
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
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
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

	return
  
def gf6_3632(request):
	# ******************  Below data entered for each part  ******************************
	goal = 7500   # Weekly6 Goal
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
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
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
	asset1 = '1511'
	asset2 = '1528'
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
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
	pdate_start = stamp_pdate(week_start)
	pdate_week.append(pdate_start)
	for i in range(1,7):
		stamp1 = week_start + (86400 * i)
		pdate1 = stamp_pdate(stamp1)
		pdate_week.append(pdate1) # This is the tuple of days in the week to cycle through



	 
	# Select all reactions in asset list for date range
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%s' and TimeStamp <= '%s' and (Machine = '%s' OR Machine ='%s')" %(week_start,week_end,asset1,asset2)
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
	request.session['totals_9341'] = tot3
	request.session['shift_9341'] = shift2  #Need 
	request.session['pdate_9341'] = pdate_week  #Need
	request.session['op_totals_9341'] = op
	request.session['op_span_9341'] = operation_totals
	request.session['goal_9341'] = goal_todate
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
	asset = ['1816']
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
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
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
	request.session['total_prod_3050'] = int(operation_totals[0][3]) + 724
	inv_change =  int(operation_totals[0][3]) - int(goal_todate)+724
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
	goal_todate = int((goal / float(432000)) * week_time_todate)  # Current Goal to date
	if goal_todate > goal: goal_todate = goal
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
def prod_10R(request):
	t=int(time.time())
	week_start_10r(request,t)
	prod_9341(request)
	prod_0455(request)
	prod_3050(request)
	prod_1467(request)
	return render(request, "prod_10R.html")    

def prod_10R_prev(request):
	t=request.session['week_end7']
	t=t-604800
	week_start_10r(request,t)
	prod_9341(request)
	prod_0455(request)
	prod_3050(request)
	prod_1467(request)
	return render(request, "prod_10R.html")  

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
	return render(request, "trilobe_fault.html")  

def prod_728fault_prev(request):
	t=request.session['week_end7']
	t=t-604800
	week_start_10r(request,t)
	prod_728(request)
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

	b = "\r\n"
	ctr = 0
	current_part = ' For Dave Clark'
	message_subject = 'Test Email'
	message3 = "Just Checking this Email Route" + current_part 
	toaddrs = ["dclark@stackpole.com"]
	fromaddr = 'stratford.reports@stackpole.com'
	frname = '10R Production'
	server = SMTP('smtp01.stackpole.ca')
	server.ehlo()
	server.starttls()
	server.ehlo()
	# server.login('stackpolepmds@gmail.com', 'stacktest6060')
	message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
	message = message+message_subject + "\r\n\r\n" + "\r\n\r\n" + message3 + "\r\n\r\n" 
	server.sendmail(fromaddr, toaddrs, message)
	server.quit()
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
	t = 1624725088  # Temporary time
	stamp = t
	# stamp=int(time.time())
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
	prt = request.session['part_area']
	rate1 = request.session['rate_area']
	asset1 = str(request.session['asset1_area'])
	asset2 = str(request.session['asset2_area'])
	asset3 = str(request.session['asset3_area'])
	asset4 = str(request.session['asset4_area'])
	target = rate1

	t=int(time.time())
	t = 1624725088  # Temporary time
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
	weekend_start = week_start1 + 43200
	weekend_current_seconds = t - weekend_start

	week_start2 = week_start1 - 604800
	week_start3 = week_start2 - 604800
	ew = week_start1 + 604800

	# var1 = 'target' + data_area
	target = target_area / float(3600) 
	target = shift_time * target

	# request.session[var1] = int(shift_time * target)
	
	wd, m, day, shift = day_breakdown(u)
	request.session['wd'] = wd
	request.session['m'] = m
	request.session['shift'] = shift
	request.session['day'] = day
	request.session['yr'] = '2021'
	
	
	db, cur = db_set(request)
	aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (u,t,prt,asset1,asset2,asset3,asset4)

	cur.execute(aql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	cnt = tmp3[0]
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