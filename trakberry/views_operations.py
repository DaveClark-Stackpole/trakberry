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
	request.session['totals_9341'] = tot3
	request.session['shift_9341'] = shift2  #Need 
	request.session['pdate_9341'] = pdate_week  #Need
	request.session['op_totals_9341'] = op
	request.session['op_span_9341'] = operation_totals
	request.session['goal_9341'] = goal_todate

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

	return

def prod_10R(request):
	t=int(time.time())
	week_start_10r(request,t)
	prod_9341(request)
	prod_0455(request)
	return render(request, "prod_10R.html")    

def prod_10R_prev(request):
	t=request.session['week_end7']
	t=t-604800
	week_start_10r(request,t)
	prod_9341(request)
	prod_0455(request)
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