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


# *********************************************************************************************************
# MAIN Production View
# This is the main Administrator View to tackle things like cycle times, view production etc.
# *********************************************************************************************************
def pdate_stamp(pdate):
	string=str(pdate)
	element = datetime.datetime.strptime(string,"%Y-%m-%d")
	tuple = element.timetuple()
	timestamp = time.mktime(tuple)
	return timestamp

def track_graph_10r_prev(request, index):
	u = int(index)
	t = int(index) + 28800
	gr_list = track_10r_data(request,t,u) # Get the Graph Data
	return render(request, "10r_graph_prev.html",{'GList':gr_list})

def track_graph_prev1(request, index):
	prt= request.session['part_area1']
	rate = request.session['rate_area1']
	request.session['asset1_area'] = request.session['asset1_area1']
	request.session['asset2_area'] = request.session['asset2_area1']
	request.session['asset3_area'] = request.session['asset3_area1']
	request.session['asset4_area'] = request.session['asset4_area1']
	u = int(index)
	t = int(index) + 28800
	gr_list = track_data(request,t,u,prt,rate) # Get the Graph Data
	return render(request, "graph_prev1.html",{'GList':gr_list})

def track_graph_track(request, index):
	prt= '50-9341'
	request.session['track_track'] = 'Shift Track for Machine '+ str(index)
	machines7 = ['1504','1506','1519','1520','1502','1507','1501','1515','1508','1532','1509','1514','1510','1503','1511','1518','1521','1522','1523','1539','1540','1524','1525','1538','1541','1531','1527','1530','1528','1513','1533','1800','1801','1802','1529','1543','776','1824','1804','1805','1806','1808','1810','1815','1812','1816']
	rate7 = [8,8,8,8,4,4,4,4,3,3,2,2,2,2,2,8,8,8,8,4,4,4,4,3,2,2,2,2,2,1,1,2,2,2,4,4,4,4,2,2,1,1,1,1,1,1]
	part7 = ['50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455']

	# machines1 = ['1800','1801','1802','1529','1543','776','1824','1804','1805','1806','1808','1810','1815','1812','1816']
	# rate = [2,2,2,4,4,4,4,2,2,1,1,1,1,1,1]
	# line1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	# operation1 = [10,10,10,30,30,30,30,40,40,50,60,70,80,100,120]


	mr7=zip(machines7,rate7,part7)
	for i in mr7:
		if i[0] == index :
			rate = i[1]
			prt= i[2]
	rate2 = 3200 / float(rate)
	rate = rate2 / float(8)

	request.session['asset1_area'] = index
	request.session['asset2_area'] = index
	request.session['asset3_area'] = index
	request.session['asset4_area'] = index
	u = int(request.session['shift_start'])
	t = int(u) + 28800
	t=int(time.time())

	gr_list = track_data(request,t,u,prt,rate) # Get the Graph Data
	return render(request, "graph_track_track.html",{'GList':gr_list})


def track_graph_prev2(request, index):
	prt= request.session['part_area2']
	rate = request.session['rate_area2']
	request.session['asset1_area'] = request.session['asset1_area2']
	request.session['asset2_area'] = request.session['asset2_area2']
	request.session['asset3_area'] = request.session['asset3_area2']
	request.session['asset4_area'] = request.session['asset4_area2']
	u = int(index)
	t = int(index) + 28800

	gr_list = track_data(request,t,u,prt,rate) # Get the Graph Data
	return render(request, "graph_prev2.html",{'GList':gr_list})

def track_graph_tri_prev(request, index):
	u = int(index)
	t = int(index) + 28800
	gr_list = track_tri_data(request,t,u) # Get the Graph Data
	return render(request, "tri_graph_prev.html",{'GList':gr_list})

def track_10r_data(request,t,u):
	m = '1533'
	mrr = (337*(28800))/float(28800)
	db, cursor = db_set(request)
	sql = "SELECT * FROM GFxPRoduction where TimeStamp >= '%d' and TimeStamp< '%d' and machine = '%s'" %(u,t,m)
	cursor.execute(sql)
	tmp = cursor.fetchall()	
	db.close()
	gr_list, brk1, brk2, multiplier	 = Graph_Data(t,u,m,tmp,mrr)
	return gr_list

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

def track_10R80data(request,t,u,part,rate):
	m = '1533'
	asset1 = request.session['8asset1_area']
	asset2 = request.session['8asset2_area']
	asset3 = request.session['8asset3_area']
	asset4 = request.session['8asset4_area']
	# mrr = (337*(28800))/float(28800)
	mrr = (rate*(28800))/float(28800)
	db, cursor = db_set(request)
	sql = "SELECT * FROM GFxPRoduction where TimeStamp >= '%d' and TimeStamp< '%d' and part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" %(u,t,part,asset1,asset2,asset3,asset4)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close()
	gr_list, brk1, brk2, multiplier	 = Graph_Data(t,u,m,tmp,mrr)

	# try:
	#	gr_list, brk1, brk2, multiplier	 = Graph_Data(t,u,m,tmp,mrr)
	# except:
	#	gr1=[]
	#	gr2=[]
	#	gr3=[]
	#	gr4=[]
	#	gr_list = zip(gr1,gr2,gr3,gr4)
	return gr_list

def track_tri_data(request,t,u):
	# m1 = '650R'
	m = '650'
	pt = '50-1467'
	mrr = (189*(28800))/float(28800)
	db, cursor = db_set(request)
	sql = "SELECT Id,Machine,Part,PerpetualCount,TimeStamp FROM GFxPRoduction where TimeStamp >= '%d' and TimeStamp< '%d' and Part = '%s'" %(u,t,pt)
	cursor.execute(sql)
	tmp = cursor.fetchall()	
	db.close()
	t=4/0
	gr_list, brk1, brk2, multiplier	 = Graph_Data(t,u,m,tmp,mrr)
	return gr_list

	# return render(request, "track.html",{"GList":gr_list})

	# return render(request, "10RGraph.html",{"tmp":gr_list})

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

# Quickly calculates p
def track_email(request):
	t=int(time.time())
	tm = time.localtime(t)
	request.session["time"] = t
	shift_start = -2
	current_shift = 3
	if tm[3]<22 and tm[3]>=14:
		shift_start = 14
	elif tm[3]<14 and tm[3]>=6:
		shift_start = 6
	cur_hour = tm[3]
	if cur_hour == 22:
		cur_hour = -1
	u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])	 # Starting unix of shift

	db, cur = db_set(request)

	# Calculate 9341 Predictions
	prt = '50-9341'
	asset1 = ['1507','1502','1539','1540','1528','1511','1533']
	count1 = []
	for i in asset1:
		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (u,t,prt,i,i,i,i)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		c = tmp3[0] / float ( t-u)
		c = int(c * 28800)
		count1.append(c)
	pred1 = zip(asset1,count1)

	# Calculate 0455 Predictions
	prt = '50-0455'
	asset2 = ['776','1529','1543','1816']
	count2 = []
	for i in asset2:
		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (u,t,prt,i,i,i,i)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		c = tmp3[0] / float ( t-u)
		c = int(c * 28800)
		count2.append(c)
	pred2 = zip(asset2,count2)


	# Calculate 1467 Predictions
	prt = '50-1467'
	a1='650L'
	a2='650R'
	a3='769'
	aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s')" % (u,t,prt,a1,a2,a3)
	cur.execute(aql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	count3 = tmp3[0] / float ( t-u)
	count3 = int(count3 * 28800)

	# Calculate 3050 Predictions
	prt = '50-3050'
	a4='769'
	aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s')" % (u,t,prt,a3)
	cur.execute(aql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	count4 = tmp3[0] / float ( t-u)
	count4 = int(count4 * 28800)


	db.close()

	tm = time.localtime(t)	 # Local time
	mm = str(tm[4])
	if len((mm)) < 2:
		mm = '0'+ mm
	pdate = str(tm[1]) + '-' + str(tm[2]) + '-' + str(tm[0]) + '  ' + str(tm[3]) + ':' + mm	 # Date and time of reading


	# Email information
	# Unblock when good 
	b = "\r\n"
	ctr = 0
	message_subject = '10R80 End Of Shift Prediction at: ' + pdate
	message3 = ''
	message3 = message3 + '10R80 Production'
	for i in pred1:
		message3 = message3 + b + "Machine:" + i[0] + " Prediction: " + str(i[1])

	message3 = message3 + b + b 
	message3 = message3 + '10R60 Production'
	for i in pred2:
		message3 = message3 + b + "Machine:" + i[0] + " Prediction: " + str(i[1])

	message3 = message3 + b + b 
	message3 = message3 + 'Trilobe Production'
	message3 = message3 + b + "Machine: 650/769" + " Prediction: " + str(count3)

	message3 = message3 + b + b 
	message3 = message3 + 'Optimized Production'
	message3 = message3 + b + "Machine: 769" + " Prediction: " + str(count4)


	toaddrs = ["dclark@stackpole.com","jmcmaster@stackpole.com"]
	#toaddrs = ["rrompen@stackpole.com","rbiram@stackpole.com","rzylstra@stackpole.com","lbaker@stackpole.com","dmilne@stackpole.com","sbrownlee@stackpole.com","pmurphy@stackpole.com","pstreet@stackpole.com","kfrey@stackpole.com","asmith@stackpole.com","smcmahon@stackpole.com","gharvey@stackpole.com","ashoemaker@stackpole.com","jreid@stackpole.com"]
	fromaddr = 'stackpole@stackpole.com'
	frname = 'Dave'
	server = SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('StackpolePMDS@gmail.com', 'stacktest6060')
	message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
	message = message+message_subject + "\r\n\r\n" + message3 + "\r\n\r\n" 
	server.sendmail(fromaddr, toaddrs, message)
	server.quit()
	return 





def track_area(request):

	data_area = request.session['data_area'] # Data for 1 or 2 chart
	target_area = int(request.session['rate_area'])
	prt = request.session['part_area']
	rate1 = request.session['rate_area']
	asset1 = str(request.session['asset1_area'])
	asset2 = str(request.session['asset2_area'])
	asset3 = str(request.session['asset3_area'])
	asset4 = str(request.session['asset4_area'])
	target = rate1

	t=int(time.time())
	# t=int(1610761821)	 # Temporary time.	 just force it for this time
	x = int(t - 489600)
	tm = time.localtime(t)
	request.session["time"] = t

	
	# shift_start = -2
	# current_shift = 3
	# if tm[3]<22 and tm[3]>=14:
	# 	shift_start = 14
	# elif tm[3]<14 and tm[3]>=6:
	# 	shift_start = 6
	# cur_hour = tm[3]
	# if cur_hour == 22:
	# 	cur_hour = -1
	# u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])	 # Starting unix of shift
	# shift_time = t-u
	# shift_left = 28800 - shift_time
	# e = t + shift_left

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

	# var1 = 'count' + data_area
	# request.session[var1] = cnt
	if week_current_seconds > 43200:
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

	u1, wd1, m1, day1, shift1, prev_cnt1 = [],[],[],[],[],[]
	utemp = u
	total_test = 0
	
	for i in range(1,18):
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

def track_area80(request):
	data_area = request.session['8data_area'] # Data for 1 or 2 chart
	target_area = int(request.session['8rate_area'])
	prt = request.session['8part_area']
	rate1 = request.session['8rate_area']
	asset1 = request.session['8asset1_area']
	asset2 = request.session['8asset2_area']
	asset3 = request.session['8asset3_area']
	asset4 = request.session['8asset4_area']
	target = rate1

	t=int(time.time())
	# t=int(1614366060)	 # Temporary time.	 just force it for this time
	x = int(t - 489600)
	tm = time.localtime(t)
	request.session["time"] = t
	shift_start = -2
	current_shift = 3
	if tm[3]<22 and tm[3]>=14:
		shift_start = 14
	elif tm[3]<14 and tm[3]>=6:
		shift_start = 6
	cur_hour = tm[3]
	if cur_hour == 22:
		cur_hour = -1
	u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])	 # Starting unix of shift

	shift_time = t-u
	shift_left = 28800 - shift_time
	e = t + shift_left
	request.session["shift_time"] = shift_time

	target = target_area / float(3600) 
	target = shift_time * target

	wd, m, day, shift = day_breakdown(u)
	request.session['wd'] = wd
	request.session['m'] = m
	request.session['shift'] = shift
	request.session['day'] = day

	db, cur = db_set(request)
	aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (u,t,prt,asset1,asset2,asset3,asset4)
	cur.execute(aql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	cnt = tmp3[0]

	db.close()
	try:
		current_rate = cnt / float(shift_time)
	except:
		current_rate = 0
	oa = cnt / float(target)
	oa = (int(oa * 10000)) / float(100)
	check_area = request.session['8data_area']

	gr_list = track_10R80data(request,t,u,prt,rate1) # Get the Graph Data
	return gr_list


def track_10r(request):
	t=int(time.time())
	# t = 1596054870
	tm = time.localtime(t)
	request.session["time"] = t
	shift_start = -2
	current_shift = 3
	if tm[3]<22 and tm[3]>=14:
		shift_start = 14
	elif tm[3]<14 and tm[3]>=6:
		shift_start = 6
	cur_hour = tm[3]
	if cur_hour == 22:
		cur_hour = -1
	u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])	 # Starting unix of shift

	shift_time = t-u
	shift_left = 28800 - shift_time
	request.session["shift_time"] = shift_time
	target = 332 / float(3600) # 10R Target

	target = shift_time * target
	request.session["target"] = int(target)

	wd, m, day, shift = day_breakdown(u)
	request.session['wd'] = wd
	request.session['m'] = m
	request.session['shift'] = shift
	request.session['day'] = day

	prt = '50-9341'
	db, cur = db_set(request)
	aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u,t,prt)
	cur.execute(aql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	cnt = tmp3[0]
	request.session["count"] = cnt

	try:
		pwd = request.session['prev_wd']
		pm = request.session['prev_m']
		pday = request.session['prev_day']
		pshift = request.session['prev_shift']
	except:
		pwd = 0
		pm = 0
		pday = 0
		pshift = 0
	aaa = 0
	if aaa == 0 :
	# if pwd != wd and pm!=m and pday!=day and pshift!=shift:	
		u1 = u - 28800
		request.session['wd1'],request.session['m1'],request.session['day1'], request.session['shift1'] = day_breakdown(u1) 
		u2 = u1 - 28800
		request.session['wd2'],request.session['m2'],request.session['day2'], request.session['shift2'] = day_breakdown(u2) 
		u3 = u2 - 28800
		request.session['wd3'],request.session['m3'],request.session['day3'], request.session['shift3'] = day_breakdown(u3) 
		u4 = u3 - 28800
		request.session['wd4'],request.session['m4'],request.session['day4'], request.session['shift4'] = day_breakdown(u4) 
		u5 = u4 - 28800
		request.session['wd5'],request.session['m5'],request.session['day5'], request.session['shift5'] = day_breakdown(u5) 
		u6 = u5 - 28800
		request.session['wd6'],request.session['m6'],request.session['day6'], request.session['shift6'] = day_breakdown(u6) 
		u7 = u6 - 28800
		request.session['wd7'],request.session['m7'],request.session['day7'], request.session['shift7'] = day_breakdown(u7) 
		u8 = u7 - 28800
		request.session['wd8'],request.session['m8'],request.session['day8'], request.session['shift8'] = day_breakdown(u8) 
		u9 = u8 - 28800
		request.session['wd9'],request.session['m9'],request.session['day9'], request.session['shift9'] = day_breakdown(u9) 
		request.session['prev_wd'] = wd
		request.session['prev_m'] = m
		request.session['prev_shift'] = shift
		request.session['prev_day'] = day

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u1,u,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt1 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u2,u1,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt2 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u3,u2,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt3 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u4,u3,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt4 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u5,u4,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt5 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u6,u5,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt6 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u7,u6,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt7 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u8,u7,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt8 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u9,u8,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt9 = tmp3[0]

		request.session["count1"] = prev_cnt1
		request.session["count2"] = prev_cnt2
		request.session["count3"] = prev_cnt3
		request.session["count4"] = prev_cnt4
		request.session["count5"] = prev_cnt5
		request.session["count6"] = prev_cnt6
		request.session["count7"] = prev_cnt7
		request.session["count8"] = prev_cnt8
		request.session["count9"] = prev_cnt9

	db.close()

	current_rate = cnt / float(shift_time)
	projection = int(current_rate * (shift_left)) + cnt
	request.session["projection"] = projection
	oa = cnt / float(target)
	oa = (int(oa * 10000)) / float(100)
	request.session["oa"] = oa

	gr_list = track_10r_data(request,t,u) # Get the Graph Data
	
	return u,tm,gr_list
	return render(request, "track.html",{"tm":u,"dt":tm,'GList':gr_list})

def track_tri(request):
	t=int(time.time())
	# t = 1596054870
	tm = time.localtime(t)
	request.session["time"] = t
	shift_start = -2
	current_shift = 3
	if tm[3]<22 and tm[3]>=14:
		shift_start = 14
	elif tm[3]<14 and tm[3]>=6:
		shift_start = 6
	cur_hour = tm[3]
	if cur_hour == 22:
		cur_hour = -1
	u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])	 # Starting unix of shift

	shift_time = t-u
	shift_left = 28800 - shift_time
	request.session["shift_time"] = shift_time
	target = 189 / float(3600) # Trilobe Target

	target = shift_time * target
	request.session["targeta"] = int(target)

	wd, m, day, shift = day_breakdown(u)

	request.session['wd'] = wd
	request.session['m'] = m
	request.session['shift'] = shift
	request.session['day'] = day

	prt = '50-1467'
	db, cur = db_set(request)
	aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u,t,prt)
	cur.execute(aql)
	tmp2 = cur.fetchall()
	tmp3 = tmp2[0]
	cnt = tmp3[0]
	request.session["counta"] = cnt

	try:
		pwd = request.session['prev_wd']
		pm = request.session['prev_m']
		pday = request.session['prev_day']
		pshift = request.session['prev_shift']
	except:
		pwd = 0
		pm = 0
		pday = 0
		pshift = 0
	aaa = 0
	if aaa == 0 :
	# if pwd != wd and pm!=m and pday!=day and pshift!=shift:	
		u1 = u - 28800
		request.session['wd1'],request.session['m1'],request.session['day1'], request.session['shift1'] = day_breakdown(u1) 
		u2 = u1 - 28800
		request.session['wd2'],request.session['m2'],request.session['day2'], request.session['shift2'] = day_breakdown(u2) 
		u3 = u2 - 28800
		request.session['wd3'],request.session['m3'],request.session['day3'], request.session['shift3'] = day_breakdown(u3) 
		u4 = u3 - 28800
		request.session['wd4'],request.session['m4'],request.session['day4'], request.session['shift4'] = day_breakdown(u4) 
		u5 = u4 - 28800
		request.session['wd5'],request.session['m5'],request.session['day5'], request.session['shift5'] = day_breakdown(u5) 
		u6 = u5 - 28800
		request.session['wd6'],request.session['m6'],request.session['day6'], request.session['shift6'] = day_breakdown(u6) 
		u7 = u6 - 28800
		request.session['wd7'],request.session['m7'],request.session['day7'], request.session['shift7'] = day_breakdown(u7) 
		u8 = u7 - 28800
		request.session['wd8'],request.session['m8'],request.session['day8'], request.session['shift8'] = day_breakdown(u8) 
		u9 = u8 - 28800
		request.session['wd9'],request.session['m9'],request.session['day9'], request.session['shift9'] = day_breakdown(u9) 
		request.session['prev_wd'] = wd
		request.session['prev_m'] = m
		request.session['prev_shift'] = shift
		request.session['prev_day'] = day

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u1,u,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt1 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u2,u1,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt2 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u3,u2,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt3 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u4,u3,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt4 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u5,u4,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt5 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u6,u5,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt6 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u7,u6,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt7 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u8,u7,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt8 = tmp3[0]

		aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s'" % (u9,u8,prt)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		prev_cnt9 = tmp3[0]

		request.session["count1a"] = prev_cnt1
		request.session["count2a"] = prev_cnt2
		request.session["count3a"] = prev_cnt3
		request.session["count4a"] = prev_cnt4
		request.session["count5a"] = prev_cnt5
		request.session["count6a"] = prev_cnt6
		request.session["count7a"] = prev_cnt7
		request.session["count8a"] = prev_cnt8
		request.session["count9a"] = prev_cnt9

		request.session["u1"] = u1
		request.session["u2"] = u2
		request.session["u3"] = u3
		request.session["u4"] = u4
		request.session["u5"] = u5
		request.session["u6"] = u6
		request.session["u7"] = u7
		request.session["u8"] = u8
		request.session["u9"] = u9

	db.close()

	current_rate = cnt / float(shift_time)
	projection = int(current_rate * (shift_left)) + cnt
	request.session["projectiona"] = projection
	oa = cnt / float(target)
	oa = (int(oa * 10000)) / float(100)
	request.session["oaa"] = oa

	gr_list = track_tri_data(request,t,u) # Get the Graph Data
	
	return u,tm,gr_list
	# return render(request, "track.html",{"tm":u,"dt":tm,'GList':gr_list})


def tracking(request):

	# This section will check every 30min and email out counts to Jim and Myself
	try:
		db, cur = db_set(request)
		cur.execute("""CREATE TABLE IF NOT EXISTS tkb_email_10r(Id INT PRIMARY KEY AUTO_INCREMENT,dummy1 INT(30),stamp INT(30) )""")
		eql = "SELECT MAX(stamp) FROM tkb_email_10r"
		cur.execute(eql)
		teql = cur.fetchall()
		teql2 = int(teql[0][0])
		ttt=int(time.time())
		elapsed_time = ttt - teql2
		if elapsed_time > 1800:
			x = 1
			dummy = 8
			cur.execute('''INSERT INTO tkb_email_10r(dummy1,stamp) VALUES(%s,%s)''', (dummy,ttt))
			db.commit()
			track_email(request)  
		db.close()
	except:
		dummy2 = 0

	# net1(request)	  # Sets the app to server or local
	# force changes
	try:
		try:
			request.session['data_area'] = 1
			request.session['target_area'] = 1
			request.session['part_area'] = request.session['part_area1']
			request.session['rate_area'] = request.session['rate_area1']
			request.session['asset1_area'] = request.session['asset1_area1']
			request.session['asset2_area'] = request.session['asset2_area1']
			request.session['asset3_area'] = request.session['asset3_area1']
			request.session['asset4_area'] = request.session['asset4_area1']
			data1, gr_list1 = track_area(request)
			request.session['data_area'] = 2
			request.session['target_area'] = 2
			request.session['part_area'] = request.session['part_area2']
			request.session['rate_area'] = request.session['rate_area2']
			request.session['asset1_area'] = request.session['asset1_area2']
			request.session['asset2_area'] = request.session['asset2_area2']
			request.session['asset3_area'] = request.session['asset3_area2']
			request.session['asset4_area'] = request.session['asset4_area2']
			data2, gr_list2 = track_area(request)
		except:
			request.session['area1'] = '50-1467 Inspection'
			request.session['data_area'] =1 # Data for 1 or 2 chart
			request.session['target_area'] = 1
			request.session['part_area'] = '50-1467'
			request.session['part_area1'] = '50-1467'
			request.session['rate_area'] = 216
			request.session['rate_area1'] = 216
			request.session['asset1_area'] = '650L'
			request.session['asset2_area'] = '650R'
			request.session['asset3_area'] = '769'
			request.session['asset4_area'] = '769'
			request.session['asset1_area1'] = '650L'
			request.session['asset2_area1'] = '650R'
			request.session['asset3_area1'] = '769'
			request.session['asset4_area1'] = '769'
			data1, gr_list1 = track_area(request)
			request.session['area2'] = '50-3050 Inspection'
			request.session['data_area'] =2 # Data for 1 or 2 chart
			request.session['target_area'] = 2
			request.session['part_area'] = '50-3050'
			request.session['part_area2'] = '50-3050'
			request.session['rate_area'] = 15
			request.session['rate_area2'] = 15
			request.session['asset1_area'] = '769'
			request.session['asset2_area'] = '769'
			request.session['asset3_area'] = '769'
			request.session['asset4_area'] = '769'
			request.session['asset1_area2'] = '769'
			request.session['asset2_area2'] = '769'
			request.session['asset3_area2'] = '769'
			request.session['asset4_area2'] = '769'
			data2, gr_list2 = track_area(request)


		return render(request, "track.html",{'GList':gr_list1,"datax":data1,'GList2':gr_list2, "datax2":data2})
	except:
		return render(request, "track_error.html")

def tracking_10R80_screen(request):

	return render(request,'redirect_cell_track_9341.html')   # Remove this later


	try:
		# net1(request)	  # Sets the app to server or local
		request.session['8area4'] = '50-9341 Finishing'
		request.session['8data_area'] =4 # Data for 1 or 2 chart
		request.session['8target_area'] = 4
		request.session['8part_area'] = '50-9341'
		request.session['8part_area1'] = '50-9341'
		request.session['8rate_area'] = 400
		request.session['8rate_area1'] = 400
		request.session['8asset1_area'] = '1533'
		request.session['8asset2_area'] = '1533'
		request.session['8asset3_area'] = '1533'
		request.session['8asset4_area'] = '1533'
		request.session['8asset1_area1'] = '1533'
		request.session['8asset2_area1'] = '1533'
		request.session['8asset3_area1'] = '1533'
		request.session['8asset4_area1'] = '1533'
		gr_list4 = track_area80(request)
		request.session['8area1'] = '50-9341 OP 30 Oil Hole'
		request.session['8data_area'] =1 # Data for 1 or 2 chart
		request.session['8target_area'] = 1
		request.session['8part_area'] = '50-9341'
		request.session['8part_area2'] = '50-9341'
		request.session['8rate_area'] = 400
		request.session['8rate_area2'] = 400
		request.session['8asset1_area'] = '1502'
		request.session['8asset2_area'] = '1507'
		request.session['8asset3_area'] = '1539'
		request.session['8asset4_area'] = '1540'
		request.session['8asset1_area2'] = '1502'
		request.session['8asset2_area2'] = '1507'
		request.session['8asset3_area2'] = '1539'
		request.session['8asset4_area2'] = '1540'
		gr_list1 = track_area80(request)
		request.session['8area2'] = '50-9341 OP 80 Grinding'
		request.session['8data_area'] =2 # Data for 1 or 2 chart
		request.session['8target_area'] = 2
		request.session['8part_area'] = '50-9341'
		request.session['8part_area1'] = '50-9341'
		request.session['8rate_area'] = 400
		request.session['8rate_area1'] = 400
		request.session['8asset1_area'] = '1510'
		request.session['8asset2_area'] = '1510'
		request.session['8asset3_area'] = '1527'
		request.session['8asset4_area'] = '1527'
		request.session['8asset1_area1'] = '1510'
		request.session['8asset2_area1'] = '1510'
		request.session['8asset3_area1'] = '1527'
		request.session['8asset4_area1'] = '1527'
		gr_list2 = track_area80(request)
		request.session['8area3'] = '50-9341 OP 110 Polishing'
		request.session['8data_area'] =3 # Data for 1 or 2 chart
		request.session['8target_area'] = 3
		request.session['8part_area'] = '50-9341'
		request.session['8part_area2'] = '50-9341'
		request.session['8rate_area'] = 400
		request.session['8rate_area2'] = 400
		request.session['8asset1_area'] = '1511'
		request.session['8asset2_area'] = '1511'
		request.session['8asset3_area'] = '1528'
		request.session['8asset4_area'] = '1528'
		request.session['8asset1_area2'] = '1511'
		request.session['8asset2_area2'] = '1511'
		request.session['8asset3_area2'] = '1528'
		request.session['8asset4_area2'] = '1528'
		gr_list3 = track_area80(request)
		return render(request, "track_10R80_screen.html",{'GList':gr_list1,'GList2':gr_list2,'GList3':gr_list3,'GList4':gr_list4})
	except:
		return render(request, "track_10R80_screen_error.html")

def tracking_10R80_resume(request):
	t=int(time.time())
	request.session['track_10R80_up'] = t + 3600
	return render(request, "redirect_tracking_10R80.html")

def tracking_10R80(request):

	# Determine pause time for tracking
	t=int(time.time())
	try:
		up_time1 = request.session['track_10R80_up']
	except:
		request.session['track_10R80_up'] = t + 3600
		up_time1 = request.session['track_10R80_up']
	if t > up_time1:
		return render(request, "track_10R80_pause.html")



	try:
		# net1(request)	  # Sets the app to server or local
		request.session['8area4'] = '50-9341 Finishing'
		request.session['8data_area'] =4 # Data for 1 or 2 chart
		request.session['8target_area'] = 4
		request.session['8part_area'] = '50-9341'
		request.session['8part_area1'] = '50-9341'
		request.session['8rate_area'] = 400
		request.session['8rate_area1'] = 400
		request.session['8asset1_area'] = '1533'
		request.session['8asset2_area'] = '1533'
		request.session['8asset3_area'] = '1533'
		request.session['8asset4_area'] = '1533'
		request.session['8asset1_area1'] = '1533'
		request.session['8asset2_area1'] = '1533'
		request.session['8asset3_area1'] = '1533'
		request.session['8asset4_area1'] = '1533'
		gr_list4 = track_area80(request)
		request.session['8area1'] = '50-9341 OP 30 Oil Hole'
		request.session['8data_area'] =1 # Data for 1 or 2 chart
		request.session['8target_area'] = 1
		request.session['8part_area'] = '50-9341'
		request.session['8part_area2'] = '50-9341'
		request.session['8rate_area'] = 400
		request.session['8rate_area2'] = 400
		request.session['8asset1_area'] = '1502'
		request.session['8asset2_area'] = '1507'
		request.session['8asset3_area'] = '1539'
		request.session['8asset4_area'] = '1540'
		request.session['8asset1_area2'] = '1502'
		request.session['8asset2_area2'] = '1507'
		request.session['8asset3_area2'] = '1539'
		request.session['8asset4_area2'] = '1540'
		gr_list1 = track_area80(request)
		request.session['8area2'] = '50-9341 OP 80 Grinding'
		request.session['8data_area'] =2 # Data for 1 or 2 chart
		request.session['8target_area'] = 2
		request.session['8part_area'] = '50-9341'
		request.session['8part_area1'] = '50-9341'
		request.session['8rate_area'] = 400
		request.session['8rate_area1'] = 400
		request.session['8asset1_area'] = '1510'
		request.session['8asset2_area'] = '1510'
		request.session['8asset3_area'] = '1527'
		request.session['8asset4_area'] = '1527'
		request.session['8asset1_area1'] = '1510'
		request.session['8asset2_area1'] = '1510'
		request.session['8asset3_area1'] = '1527'
		request.session['8asset4_area1'] = '1527'
		gr_list2 = track_area80(request)
		request.session['8area3'] = '50-9341 OP 110 Polishing'
		request.session['8data_area'] =3 # Data for 1 or 2 chart
		request.session['8target_area'] = 3
		request.session['8part_area'] = '50-9341'
		request.session['8part_area2'] = '50-9341'
		request.session['8rate_area'] = 400
		request.session['8rate_area2'] = 400
		request.session['8asset1_area'] = '1511'
		request.session['8asset2_area'] = '1511'
		request.session['8asset3_area'] = '1528'
		request.session['8asset4_area'] = '1528'
		request.session['8asset1_area2'] = '1511'
		request.session['8asset2_area2'] = '1511'
		request.session['8asset3_area2'] = '1528'
		request.session['8asset4_area2'] = '1528'
		gr_list3 = track_area80(request)
		return render(request, "track_10R80.html",{'GList':gr_list1,'GList2':gr_list2,'GList3':gr_list3,'GList4':gr_list4})
	except:
		return render(request, "track_10R80_error.html")

def chart1_1467(request):
		request.session['area1'] = '50-1467 Inspection'
		request.session['part_area1'] = '50-1467'
		request.session['rate_area1'] = 216
		request.session['asset1_area1'] = '650L'
		request.session['asset2_area1'] = '650R'
		request.session['asset3_area1'] = '769'
		request.session['asset4_area1'] = '769'
		return render(request, "redirect_tracking.html")
def chart2_1467(request):
		request.session['area2'] = '50-1467 Inspection'
		request.session['part_area2'] = '50-1467'
		request.session['rate_area2'] = 216
		request.session['asset1_area2'] = '650L'
		request.session['asset2_area2'] = '650R'
		request.session['asset3_area2'] = '769'
		request.session['asset4_area2'] = '769'
		return render(request, "redirect_tracking.html")
def chart1_1467b(request):
		request.session['area1'] = '728 Induction Faults'
		request.session['part_area1'] = '50-1467'
		request.session['rate_area1'] = 1
		request.session['asset1_area1'] = '728R'
		request.session['asset2_area1'] = '728R'
		request.session['asset3_area1'] = '728R'
		request.session['asset4_area1'] = '728R'
		return render(request, "redirect_tracking.html")
def chart2_1467b(request):
		request.session['area2'] = '50-1467 Broach/Induction'
		request.session['part_area2'] = '50-1467'
		request.session['rate_area2'] = 1
		request.session['asset1_area2'] = '728R'
		request.session['asset2_area2'] = '728R'
		request.session['asset3_area2'] = '728R'
		request.session['asset4_area2'] = '728R'
		return render(request, "redirect_tracking.html")
def chart1_1467o(request):
		request.session['area1'] = '728 Overflow'
		request.session['part_area1'] = '50-1467'
		request.session['rate_area1'] = 1
		request.session['asset1_area1'] = '728O'
		request.session['asset2_area1'] = '728O'
		request.session['asset3_area1'] = '728O'
		request.session['asset4_area1'] = '728O'
		return render(request, "redirect_tracking.html")
def chart2_1467o(request):
		request.session['area2'] = '728 Overflow'
		request.session['part_area2'] = '50-1467'
		request.session['rate_area2'] = 1
		request.session['asset1_area2'] = '728O'
		request.session['asset2_area2'] = '728O'
		request.session['asset3_area2'] = '728O'
		request.session['asset4_area2'] = '728O'
		return render(request, "redirect_tracking.html")
def chart1_1467br(request):
		request.session['area1'] = '1467 Hardened'
		request.session['part_area1'] = '50-1467'
		request.session['rate_area1'] = 187
		request.session['asset1_area1'] = '728'
		request.session['asset2_area1'] = '728'
		request.session['asset3_area1'] = '728'
		request.session['asset4_area1'] = '728'
		return render(request, "redirect_tracking.html")
def chart2_1467br(request):
		request.session['area2'] = '1467 Hardened'
		request.session['part_area2'] = '50-1467'
		request.session['rate_area2'] = 187
		request.session['asset1_area2'] = '728'
		request.session['asset2_area2'] = '728'
		request.session['asset3_area2'] = '728'
		request.session['asset4_area2'] = '728'
		return render(request, "redirect_tracking.html")
def chart1_3050(request):
		request.session['area1'] = '50-3050 Inspection'
		request.session['part_area1'] = '50-3050'
		request.session['rate_area1'] = 15
		request.session['asset1_area1'] = '769'
		request.session['asset2_area1'] = '769'
		request.session['asset3_area1'] = '769'
		request.session['asset4_area1'] = '769'
		return render(request, "redirect_tracking.html")
def chart2_3050(request):
		request.session['area2'] = '50-3050 Inspection'
		request.session['part_area2'] = '50-3050'
		request.session['rate_area2'] = 15
		request.session['asset1_area2'] = '769'
		request.session['asset2_area2'] = '769'
		request.session['asset3_area2'] = '769'
		request.session['asset4_area2'] = '769'
		return render(request, "redirect_tracking.html")
def chart1_3050b(request):
		request.session['area1'] = '50-3050 Broach/Induction'
		request.session['part_area1'] = '50-3050'
		request.session['rate_area1'] = 189
		request.session['asset1_area1'] = '770'
		request.session['asset2_area1'] = '770'
		request.session['asset3_area1'] = '770'
		request.session['asset4_area1'] = '770'
		return render(request, "redirect_tracking.html")
def chart2_3050b(request):
		request.session['area2'] = '50-3050 Broach/Induction'
		request.session['part_area2'] = '50-3050'
		request.session['rate_area2'] = 189
		request.session['asset1_area2'] = '770'
		request.session['asset2_area2'] = '770'
		request.session['asset3_area2'] = '770'
		request.session['asset4_area2'] = '770'
		return render(request, "redirect_tracking.html")
def chart1_5710(request):
		request.session['area1'] = '50-5710 Inspection'
		request.session['part_area1'] = '50-5710'
		request.session['rate_area1'] = 58
		request.session['asset1_area1'] = '769'
		request.session['asset2_area1'] = '769'
		request.session['asset3_area1'] = '769'
		request.session['asset4_area1'] = '769'
		return render(request, "redirect_tracking.html")
def chart2_5710(request):
		request.session['area2'] = '50-5710 Inspection'
		request.session['part_area2'] = '50-5710'
		request.session['rate_area2'] = 58
		request.session['asset1_area2'] = '769'
		request.session['asset2_area2'] = '769'
		request.session['asset3_area2'] = '769'
		request.session['asset4_area2'] = '769'
		return render(request, "redirect_tracking.html")
def chart1_5710b(request):
		request.session['area1'] = '50-5710 Broach/Induction'
		request.session['part_area1'] = '50-5710'
		request.session['rate_area1'] = 189
		request.session['asset1_area1'] = '770'
		request.session['asset2_area1'] = '770'
		request.session['asset3_area1'] = '770'
		request.session['asset4_area1'] = '770'
		return render(request, "redirect_tracking.html")
def chart2_5710b(request):
		request.session['area2'] = '50-5710 Broach/Induction'
		request.session['part_area2'] = '50-5710'
		request.session['rate_area2'] = 189
		request.session['asset1_area2'] = '770'
		request.session['asset2_area2'] = '770'
		request.session['asset3_area2'] = '770'
		request.session['asset4_area2'] = '770'
		return render(request, "redirect_tracking.html")
def chart1_0455(request):
		request.session['area1'] = '50-0455 Inspection'
		request.session['part_area1'] = '50-0455'
		request.session['rate_area1'] = 100
		request.session['asset1_area1'] = '1816'
		request.session['asset2_area1'] = '1816'
		request.session['asset3_area1'] = '1816'
		request.session['asset4_area1'] = '1816'
		return render(request, "redirect_tracking.html")
def chart2_0455(request):
		request.session['area2'] = '50-0455 Inspection'
		request.session['part_area2'] = '50-0455'
		request.session['rate_area2'] = 100
		request.session['asset1_area2'] = '1816'
		request.session['asset2_area2'] = '1816'
		request.session['asset3_area2'] = '1816'
		request.session['asset4_area2'] = '1816'
		return render(request, "redirect_tracking.html")
def chart1_0455_OP30(request):
		request.session['area1'] = '50-0455 OP30'
		request.session['part_area1'] = '50-0455'
		request.session['rate_area1'] = 117
		request.session['asset1_area1'] = '1543'
		request.session['asset2_area1'] = '776'
		request.session['asset3_area1'] = '1529'
		request.session['asset4_area1'] = '1824'
		return render(request, "redirect_tracking.html")
def chart2_0455_OP30(request):
		request.session['area2'] = '50-0455 OP30'
		request.session['part_area2'] = '50-0455'
		request.session['rate_area2'] = 117
		request.session['asset1_area2'] = '1543'
		request.session['asset2_area2'] = '776'
		request.session['asset3_area2'] = '1529'
		request.session['asset4_area2'] = '1824'
		return render(request, "redirect_tracking.html")
def chart1_0455_OP40(request):
		request.session['area1'] = '50-0455 OP40'
		request.session['part_area1'] = '50-0455'
		request.session['rate_area1'] = 117
		request.session['asset1_area1'] = '1804'
		request.session['asset2_area1'] = '1804'
		request.session['asset3_area1'] = '1805'
		request.session['asset4_area1'] = '1805'
		return render(request, "redirect_tracking.html")
def chart2_0455_OP40(request):
		request.session['area2'] = '50-0455 OP40'
		request.session['part_area2'] = '50-0455'
		request.session['rate_area2'] = 117
		request.session['asset1_area2'] = '1805'
		request.session['asset2_area2'] = '1805'
		request.session['asset3_area2'] = '1804'
		request.session['asset4_area2'] = '1804'
		return render(request, "redirect_tracking.html")
def chart1_0455_OP50(request):
		request.session['area1'] = '50-0455 OP50'
		request.session['part_area1'] = '50-0455'
		request.session['rate_area1'] = 117
		request.session['asset1_area1'] = '1806'
		request.session['asset2_area1'] = '1806'
		request.session['asset3_area1'] = '1806'
		request.session['asset4_area1'] = '1806'
		return render(request, "redirect_tracking.html")
def chart2_0455_OP50(request):
		request.session['area2'] = '50-0455 OP50'
		request.session['part_area2'] = '50-0455'
		request.session['rate_area2'] = 117
		request.session['asset1_area2'] = '1806'
		request.session['asset2_area2'] = '1806'
		request.session['asset3_area2'] = '1806'
		request.session['asset4_area2'] = '1806'
		return render(request, "redirect_tracking.html")
def chart1_9341(request):
		request.session['area1'] = '50-9341 Inspection'
		request.session['part_area1'] = '50-9341'
		request.session['rate_area1'] = 367
		request.session['asset1_area1'] = '1533'
		request.session['asset2_area1'] = '1533'
		request.session['asset3_area1'] = '1533'
		request.session['asset4_area1'] = '1533'
		return render(request, "redirect_tracking.html")
def chart2_9341(request):
		request.session['area2'] = '50-9341 Inspection'
		request.session['part_area2'] = '50-9341'
		request.session['rate_area2'] = 367
		request.session['asset1_area2'] = '1533'
		request.session['asset2_area2'] = '1533'
		request.session['asset3_area2'] = '1533'
		request.session['asset4_area2'] = '1533'
		return render(request, "redirect_tracking.html")
def chart1_9341_OP30(request):
		request.session['area1'] = '50-9341 OP30'
		request.session['part_area1'] = '50-9341'
		request.session['rate_area1'] = 367
		request.session['asset1_area1'] = '1502'
		request.session['asset2_area1'] = '1507'
		request.session['asset3_area1'] = '1539'
		request.session['asset4_area1'] = '1540'
		return render(request, "redirect_tracking.html")
def chart2_9341_OP30(request):
		request.session['area2'] = '50-9341 OP30'
		request.session['part_area2'] = '50-9341'
		request.session['rate_area2'] = 367
		request.session['asset1_area2'] = '1502'
		request.session['asset2_area2'] = '1507'
		request.session['asset3_area2'] = '1539'
		request.session['asset4_area2'] = '1540'
		return render(request, "redirect_tracking.html")

def chart1_1502(request):
		request.session['area1'] = '50-9341 1502'
		request.session['part_area1'] = '50-9341'
		request.session['rate_area1'] = 92
		request.session['asset1_area1'] = '1502'
		request.session['asset2_area1'] = '1502'
		request.session['asset3_area1'] = '1502'
		request.session['asset4_area1'] = '1502'
		return render(request, "redirect_tracking.html")
def chart2_1502(request):
		request.session['area2'] = '50-9341 1502'
		request.session['part_area2'] = '50-9341'
		request.session['rate_area2'] = 92
		request.session['asset1_area2'] = '1502'
		request.session['asset2_area2'] = '1502'
		request.session['asset3_area2'] = '1502'
		request.session['asset4_area2'] = '1502'
		return render(request, "redirect_tracking.html")

def chart1_1507(request):
		request.session['area1'] = '50-9341 1507'
		request.session['part_area1'] = '50-9341'
		request.session['rate_area1'] = 92
		request.session['asset1_area1'] = '1507'
		request.session['asset2_area1'] = '1507'
		request.session['asset3_area1'] = '1507'
		request.session['asset4_area1'] = '1507'
		return render(request, "redirect_tracking.html")
def chart2_1507(request):
		request.session['area2'] = '50-9341 1507'
		request.session['part_area2'] = '50-9341'
		request.session['rate_area2'] = 92
		request.session['asset1_area2'] = '1507'
		request.session['asset2_area2'] = '1507'
		request.session['asset3_area2'] = '1507'
		request.session['asset4_area2'] = '1507'
		return render(request, "redirect_tracking.html")

def chart1_1539(request):
		request.session['area1'] = '50-9341 1540'
		request.session['part_area1'] = '50-9341'
		request.session['rate_area1'] = 92
		request.session['asset1_area1'] = '1540'
		request.session['asset2_area1'] = '1540'
		request.session['asset3_area1'] = '1540'
		request.session['asset4_area1'] = '1540'
		return render(request, "redirect_tracking.html")
def chart2_1539(request):
		request.session['area2'] = '50-9341 1539'
		request.session['part_area2'] = '50-9341'
		request.session['rate_area2'] = 92
		request.session['asset1_area2'] = '1539'
		request.session['asset2_area2'] = '1539'
		request.session['asset3_area2'] = '1539'
		request.session['asset4_area2'] = '1539'
		return render(request, "redirect_tracking.html")


def chart1_9341_OP80(request):
		request.session['area1'] = '50-9341 OP80 1510'
		request.session['part_area1'] = '50-9341'
		request.session['rate_area1'] = 200
		request.session['asset1_area1'] = '1510'
		request.session['asset2_area1'] = '1510'
		request.session['asset3_area1'] = '1510'
		request.session['asset4_area1'] = '1510'
		return render(request, "redirect_tracking.html")
def chart2_9341_OP80(request):
		request.session['area2'] = '50-9341 OP80 1527'
		request.session['part_area2'] = '50-9341'
		request.session['rate_area2'] = 200
		request.session['asset1_area2'] = '1527'
		request.session['asset2_area2'] = '1527'
		request.session['asset3_area2'] = '1527'
		request.session['asset4_area2'] = '1527'
		return render(request, "redirect_tracking.html")
def chart1_9341_OP110(request):
		request.session['area1'] = '50-9341 OP110 1511'
		request.session['part_area1'] = '50-9341'
		request.session['rate_area1'] = 200
		request.session['asset1_area1'] = '1511'
		request.session['asset2_area1'] = '1511'
		request.session['asset3_area1'] = '1511'
		request.session['asset4_area1'] = '1511'
		return render(request, "redirect_tracking.html")
def chart2_9341_OP110(request):
		request.session['area2'] = '50-9341 OP110 1528'
		request.session['part_area2'] = '50-9341'
		request.session['rate_area2'] = 200
		request.session['asset1_area2'] = '1528'
		request.session['asset2_area2'] = '1528'
		request.session['asset3_area2'] = '1528'
		request.session['asset4_area2'] = '1528'
		return render(request, "redirect_tracking.html")
def chart1_5214_OP30(request):
		request.session['area1'] = '50-5214 OP30'
		request.session['part_area1'] = '50-5214'
		request.session['rate_area1'] = 76
		request.session['asset1_area1'] = '1710'
		request.session['asset2_area1'] = '1710'
		request.session['asset3_area1'] = '1710'
		request.session['asset4_area1'] = '1710'
		return render(request, "redirect_tracking.html")
def chart2_5214_OP30(request):
		request.session['area2'] = '50-5214 OP30'
		request.session['part_area2'] = '50-5214'
		request.session['rate_area2'] = 76
		request.session['asset1_area2'] = '1710'
		request.session['asset2_area2'] = '1710'
		request.session['asset3_area2'] = '1710'
		request.session['asset4_area2'] = '1710'
		return render(request, "redirect_tracking.html")
def chart1_3214_OP30(request):
		request.session['area1'] = '50-3214 OP30'
		request.session['part_area1'] = '50-3214'
		request.session['rate_area1'] = 76
		request.session['asset1_area1'] = '1710'
		request.session['asset2_area1'] = '1710'
		request.session['asset3_area1'] = '1710'
		request.session['asset4_area1'] = '1710'
		return render(request, "redirect_tracking.html")
def chart2_3214_OP30(request):
		request.session['area2'] = '50-3214 OP30'
		request.session['part_area2'] = '50-3214'
		request.session['rate_area2'] = 76
		request.session['asset1_area2'] = '1710'
		request.session['asset2_area2'] = '1710'
		request.session['asset3_area2'] = '1710'
		request.session['asset4_area2'] = '1710'
		return render(request, "redirect_tracking.html")
def chart1_8670_OP80(request):
		request.session['area1'] = '50-8670 OP80'
		request.session['part_area1'] = '50-8670'
		request.session['rate_area1'] = 38
		request.session['asset1_area1'] = '1719'
		request.session['asset2_area1'] = '1719'
		request.session['asset3_area1'] = '1719'
		request.session['asset4_area1'] = '1719'
		return render(request, "redirect_tracking.html")
def chart2_8670_OP80(request):
		request.session['area2'] = '50-8670 OP80'
		request.session['part_area2'] = '50-8670'
		request.session['rate_area2'] = 38
		request.session['asset1_area2'] = '1719'
		request.session['asset2_area2'] = '1719'
		request.session['asset3_area2'] = '1719'
		request.session['asset4_area2'] = '1719'
		return render(request, "redirect_tracking.html")
def chart1_5404_OP80(request):
		request.session['area1'] = '50-5404 OP80'
		request.session['part_area1'] = '50-5404'
		request.session['rate_area1'] = 39
		request.session['asset1_area1'] = '1719'
		request.session['asset2_area1'] = '1719'
		request.session['asset3_area1'] = '1719'
		request.session['asset4_area1'] = '1719'
		return render(request, "redirect_tracking.html")
def chart2_5404_OP80(request):
		request.session['area2'] = '50-5404 OP80'
		request.session['part_area2'] = '50-5404'
		request.session['rate_area2'] = 39
		request.session['asset1_area2'] = '1719'
		request.session['asset2_area2'] = '1719'
		request.session['asset3_area2'] = '1719'
		request.session['asset4_area2'] = '1719'
		return render(request, "redirect_tracking.html")
def chart1_5401_OP80(request):
		request.session['area1'] = '50-5401 OP80'
		request.session['part_area1'] = 'AB1V Input'
		request.session['rate_area1'] = 39
		request.session['asset1_area1'] = '1706'
		request.session['asset2_area1'] = '1706'
		request.session['asset3_area1'] = '1706'
		request.session['asset4_area1'] = '1706'
		return render(request, "redirect_tracking.html")
def chart2_5401_OP80(request):
		request.session['area2'] = '50-5401 OP80'
		request.session['part_area2'] = 'AB1V Input'
		request.session['rate_area2'] = 39
		request.session['asset1_area2'] = '1706'
		request.session['asset2_area2'] = '1706'
		request.session['asset3_area2'] = '1706'
		request.session['asset4_area2'] = '1706'
		return render(request, "redirect_tracking.html")
def mgmt(request):
	return render(request, "mgmt.html")

def mgmt_production_counts(request):
	tcur=int(time.time())
	try:
		last_time = request.session["mgmt_last_time"]
		if (tcur-last_time) > 3600:
			mgmt_24hr_production(request)
			request.session["mgmt_last_time"] = tcur
	except:
		mgmt_24hr_production(request)
		request.session["mgmt_last_time"] = tcur


	if request.POST:
		try:
			summary_asset = request.session["summary_asset"]
			group_asset = request.session["group_asset"]
		except:
			summary_asset = []
			group_asset = []
		asset1 = request.POST.get("asset")
		group1 = request.POST.get("group")
		button_1 = request.POST.get("button1")

		if button_1 == "add_machine":
			summary_asset.append(asset1)
			group_asset.append(group1)

			request.session['summary_asset'] = summary_asset
			request.session['group_asset'] = group_asset
			summary_data = zip(summary_asset,group_asset)

			mgmt_production_sort(summary_data,request)	# Run the sort algorithm

			# # Sort list and assign -1 or 1 alternating for groups 
			# summary_data.sort(key=getKey3)
			# a1 = []
			# a2 = []
			# a3 = []
			# ab = -1
			# b = 0
			# for i in summary_data:
			#	a = i[1]
			#	if b != a:
			#		ab = ab * -1
			#		b = a
			#	a1.append(i[0]) # Asset number
			#	a2.append(i[1]) # Group number
			#	a3.append(ab)	# marker   1 or -1 for formating
			# aa = zip(a1,a2,a3) # aa is the sorted list with -1 or 1 for grouping
			# request.session['summary_data'] = aa

			# Add some stuff here to display or sort or etc then redirect
			return render(request, "redirect_mgmt_production_counts.html")

		elif button_1 == "calculate":
			mgmt_production_summary(request)
			return render(request, "redirect_mgmt_production_counts.html")

		elif button_1 == "clear":
			del request.session['summary_data']
			del request.session['group_asset']
			del request.session['summary_asset']

			return render(request, "redirect_mgmt_production_counts.html")

		else:
			x1=(button_1.split('|'))
			y1 = (x1[0])
			y2 = (x1[1])
			summary_data = zip(summary_asset,group_asset)
			temp_summary = []
			temp_group = []
			for i in summary_data:
				if i[0] == y2 and i[1] == y1:
					dummy = 0
				else:
					temp_summary.append(i[0])
					temp_group.append(i[1])
			request.session['summary_asset'] = temp_summary
			request.session['group_asset'] = temp_group
			summary_data = zip(temp_summary,temp_group)

		
			mgmt_production_sort(summary_data,request)	# Run the sort algorithm
			# mgmt_production_summary(request)

		return render(request, "redirect_mgmt.html")

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'mgmt_production_counts.html',{'args':args})
	return render(request, "mgmt.html",{'TCUR':tcur})
	return render(request, "mgmt_start.html",{'TCUR':tcur})

def switch_plan_week(var1,var2,var3,request):
	v1 = request.session['Total_10R']
	v2 = v1[12][1]
	v3 = zip(*v1)
	v4=list(v3)
	a=list(v4[0])
	a1=list(v4[1])
	a2=list(v4[2])
	a3=list(v4[3])
	a4=list(v4[4])
	a5=list(v4[5])
	a6=list(v4[6])
	a7=list(v4[7])
	a8=list(v4[8])
	a9=list(v4[9])
	a10=list(v4[10])
	a11=list(v4[11])
	min_sw = list(v4[12])
	b=[]
	for i in min_sw:
		if i == var1: 
			b.append(var1*-1)
		elif i == var2:
			b.append(var3)
		else:
			b.append(i)
	overall = zip(a,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,b)
	request.session['Total_10R'] = overall
	return overall

def mgmt_goals(request):
	db, cur = db_set(request)   
	p='50-0455'
	sql = "SELECT * FROM tkb_production_goals WHERE part = '%s'" % (p)
	cur.execute(sql)
	tmp = cur.fetchall()
	add_factor_0455 = int(tmp[0][3])
	goal_0455 = int(tmp[0][2])
	p='50-9341'
	sql = "SELECT * FROM tkb_production_goals WHERE part = '%s'" % (p)
	cur.execute(sql)
	tmp = cur.fetchall()
	add_factor_9341 = int(tmp[0][3])
	goal_9341= int(tmp[0][2])
	p='50-1467'
	sql = "SELECT * FROM tkb_production_goals WHERE part = '%s'" % (p)
	cur.execute(sql)
	tmp = cur.fetchall()
	add_factor_1467 = int(tmp[0][3])
	goal_1467= int(tmp[0][2])
	p='50-3050'
	sql = "SELECT * FROM tkb_production_goals WHERE part = '%s'" % (p)
	cur.execute(sql)
	tmp = cur.fetchall()
	add_factor_3050 = int(tmp[0][3])
	goal_3050 = int(tmp[0][2])

	part = ['50-0455','50-9341','50-1467','50-3050']
	goals=[]
	addfac=[]
	goals.append(goal_0455)
	goals.append(goal_9341)
	goals.append(goal_1467)
	goals.append(goal_3050)
	addfac.append(add_factor_0455)
	addfac.append(add_factor_9341)
	addfac.append(add_factor_1467)
	addfac.append(add_factor_3050)

	totals=zip(part,goals,addfac)
	request.session['total_goals'] = totals

	if request.POST:
		g1=[]
		pl1=[]
		pr1=[]
		for i in totals:
			goal2=str(i[0]) + '_goal'
			plan2=str(i[0]) + '_plan'
			g=request.POST.get(goal2)
			p=request.POST.get(plan2)
			pr1.append(i[0])
			g1.append(g)
			pl1.append(p)
		totals=zip(pr1,g1,pl1)

		for i in totals:
			cql = ('update tkb_production_goals SET goal = "%s",weekend="%s" WHERE part ="%s"' % (i[1],i[2],i[0]))
			cur.execute(cql)
			db.commit()

		return render(request, "redirect_mgmt_track_week.html")

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'mgmt_goal_entry.html',{'args':args})


def plus_0455(request):
	switch_plan_week(-2,21,22,request)
	return render(request, "redirect_mgmt_track_week.html")

def minus_0455(request):
	switch_plan_week(2,22,21,request)
	return render(request, "redirect_mgmt_track_week.html")

def plus_9341(request):
	switch_plan_week(-1,11,12,request)
	return render(request, "redirect_mgmt_track_week.html")

def minus_9341(request):
	switch_plan_week(1,12,11,request)
	return render(request, "redirect_mgmt_track_week.html")
def plus_3050(request):
	return render(request, "redirect_mgmt_track_week.html")
def minus_3050(request):
	return render(request, "redirect_mgmt_track_week.html")
def plus_1467(request):
	return render(request, "redirect_mgmt_track_week.html")
def minus_1467(request):
	return render(request, "redirect_mgmt_track_week.html")


# Monitor Production vs Target on the Big 4
# Use Live Track and Entries
def mgmt_track_week(request):
	machines1 = ['1504','1506','1519','1520','1502','1507','1501','1515','1508','1532','1509','1514','1510','1503','1511','1518','1521','1522','1523','1539','1540','1524','1525','1538','1541','1531','1527','1530','1528','1513','1533','1543','1529','776','1824','1804','1805','1806','1816','650R','650L','769','769']
	part1=  ['50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-1467','50-1467','50-1467','50-3050']
	rate = [8,8,8,8,4,4,4,4,3,3,2,2,2,2,2,8,8,8,8,4,4,4,4,3,2,2,2,2,2,1,1,4,4,4,4,2,2,1,1,3,3,3,1]
	operation1 = [10,10,10,10,30,30,40,40,50,50,60,70,80,100,110,10,10,10,10,30,30,40,40,50,60,70,80,100,110,90,120,30,30,30,30,40,40,50,120,130,130,130,140]
	min_sw = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,11,-2,-2,-2,-2,-2,-2,-2,21,31,31,31,41]
	ooo=[10,30,40,50,60,70,80,90,100,110,120,10,30,40,50,100,120,130,140]
	opp=['50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-9341','50-0455','50-0455','50-0455','50-0455','50-0455','50-0455','50-1467','50-3050']
	prt = '50-9341'

	# Check if min_sw has values yet
	try:
		v1 = request.session['Total_10R']
		v2 = v1[12][1]
		v3 = zip(*v1)
		v4=list(v3)
		min_sw = list(v4[12])
		operation1 = list(v4[0])
		machines1 = list(v4[1])
		rate = list(v4[4])
		part1 = list(v4[11])
		check1=1
	except:
		check1=0

	opo=zip(ooo,opp)
	# Add for weekend total and Goal for Week 
	db, cur = db_set(request)   
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_production_goals(Id INT PRIMARY KEY AUTO_INCREMENT,part CHAR(80),goal int(80), weekend int(80))""")
	try:
		p='50-0455'
		sql = "SELECT * FROM tkb_production_goals WHERE part = '%s'" % (p)
		cur.execute(sql)
		tmp = cur.fetchall()
		add_factor_0455 = int(tmp[0][3])
		goal_0455 = int(tmp[0][2])
		p='50-9341'
		sql = "SELECT * FROM tkb_production_goals WHERE part = '%s'" % (p)
		cur.execute(sql)
		tmp = cur.fetchall()
		add_factor_9341 = int(tmp[0][3])
		goal_9341= int(tmp[0][2])
		p='50-1467'
		sql = "SELECT * FROM tkb_production_goals WHERE part = '%s'" % (p)
		cur.execute(sql)
		tmp = cur.fetchall()
		add_factor_1467 = int(tmp[0][3])
		goal_1467= int(tmp[0][2])
		p='50-3050'
		sql = "SELECT * FROM tkb_production_goals WHERE part = '%s'" % (p)
		cur.execute(sql)
		tmp = cur.fetchall()
		add_factor_3050 = int(tmp[0][3])
		goal_3050 = int(tmp[0][2])

	except:
		add_factor_9341 = 6000
		goal_9341=39144
		add_factor_0455 = 2500
		goal_0455=14210
		add_factor_1467 = 8400
		goal_1467=29370
		add_factor_3050 = 900
		goal_3050=2750
		p='50-0455'
		cur.execute('''INSERT INTO tkb_production_goals(part,goal,weekend) VALUES(%s,%s,%s)''', (p,goal_0455,add_factor_0455))		
		db.commit()
		p='50-9341'
		cur.execute('''INSERT INTO tkb_production_goals(part,goal,weekend) VALUES(%s,%s,%s)''', (p,goal_9341,add_factor_9341))		
		db.commit()
		p='50-1467'
		cur.execute('''INSERT INTO tkb_production_goals(part,goal,weekend) VALUES(%s,%s,%s)''', (p,goal_1467,add_factor_1467))		
		db.commit()
		p='50-3050'
		cur.execute('''INSERT INTO tkb_production_goals(part,goal,weekend) VALUES(%s,%s,%s)''', (p,goal_3050,add_factor_3050))		
		db.commit()
	# ***************************

	job = zip(operation1,machines1,rate,part1,min_sw)

	# Add the Add Factor and Goals to the job List for each part
	af=[]
	goal1=[]
	for i in job:
		part=i[3][3:7]
		exec('af.append(add_factor_'+part+')')
		exec('goal1.append(goal_'+part+')')
	job = zip(operation1,machines1,rate,part1,af,goal1,min_sw)


	t=int(time.time())
	tm = time.localtime(t)
	a1 = tm[6] * 86400
	a2 = tm[3] * 60 * 60
	a3 = tm[4] * 60
	a4 = tm[5]
	week_start = t - a1 - a2 - a3 - a4
	week_end = week_start + 432000





	request.session['start_time_week'] = week_start

	m=[]
	c=[]
	p=[]
	o=[]
	oop=[]
	prt4=[]
	ms=[]

	for i in job:
		part=i[3][3:7]
		exec('af=add_factor_'+part) # Calculate Add Factor
		aql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%s' and Machine = '%s' and Part = '%s'" % (week_start,i[1],i[3])
		cur.execute(aql)
		tmp = cur.fetchall()
		try:
			count1 = int(tmp[0][0])
		except:
			count1 = 1
		if t > week_end:
			week_end = t
			week_remaining = 172800-(week_start + 604800 - t)
			wr_factor = week_remaining / float(172800)
			af = af * wr_factor
	

		pred = ((count1/float(t-week_start))*(week_end-t) + (af/float(i[2]))) + count1
		m.append(i[1])
		c.append(count1)
		p.append(pred)
		o.append(i[0])
		oop.append(i[2])
		prt4.append(i[3])
		ms.append(i[6])
		

	totals=zip(o,m,c,p,oop,prt4,ms)
	totals.sort()
	op=totals[0][0]
	pt=totals[0][5]
	ctr=0
	ptr=0
	ct=[]
	pt=[]
	ptr=0
	point=0
	oo=[]
	pp=[]
	cc=[]
	mm=[]
	ooop=[]
	op_c =[]
	op_cp=[]
	# Calculates predictions and totals by grouping operation and part
	for i in opo:
		count2=0
		count2_p=0
		for ii in totals:
			if ii[0] == i[0] and ii[5] == i[1]:
				count2=count2+ii[2]
				count2_p=count2_p+ii[3]
		op_c.append(count2)
		op_cp.append(count2_p)
	uu=zip(ooo,op_c,op_cp,opp)

	xx=0

	# xx_ptr=0
	sum_op=[]
	pred_op=[]
	prt4=[]
	ms=[]
	totals=sorted(totals,key=lambda x:(x[5],x[0]))
	for i in totals:
		if i[0]!=xx:
			temp1=0
			temp2=0
			for j in uu:
				if j[0]==i[0] and j[3]==i[5]:
					temp1=int(j[1])
					temp2=int(j[2])







			# temp1=int((uu[xx_ptr][1]))
			# temp2=int((uu[xx_ptr][2]))

			sum_op.append(temp1)
			pred_op.append(temp2)
			# xx_ptr=xx_ptr+1
			xx=i[0]
		else:
			sum_op.append(-1)
			pred_op.append(-1)
		oo.append(i[0])
		mm.append(i[1])
		cc.append(i[2])
		pp.append(i[3])
		ooop.append(i[4])
		prt4.append(i[5])
		ms.append(i[6])

	# Below section adds -1 or 1 to control color change on chart
	overall=zip(oo,mm,cc,pp,ooop,sum_op,pred_op,prt4,ms)

	overall2=sorted(overall,key=lambda x:(x[7],x[0],x[1]))

	# rrrr=4/0
	o=[]
	m=[]
	c=[]
	p=[]
	op=[]
	tot=[]
	pred=[]
	sw=[]
	pm=[]
	pms=[]
	gl=[]
	prt4=[]
	ms=[]
	min_switch4=[]
	switch=1
	old=0
	pl_mi=0

	prt6=''
	for i in overall:
		if prt6=='':prt6=i[7]
		part = i[7][3:7]
		exec('goal1 = (goal_'+part+')')
		if old!=i[0]:
			old=i[0]
			switch=switch*-1
		o.append(i[0])
		m.append(i[1])
		c.append(int_str_comma(i[2]))
		p.append(i[3])
		op.append(i[4])
		ms.append(i[8])
		if i[5]==-1:
			tot.append(i[5])
		else:
			tot.append(int_str_comma(i[5]))

		pred.append(int_str_comma(i[6]))
		sw.append(switch)
		p6=int(i[6])
		pl_mi=p6-goal1
		pl_mis=int_str_comma(abs(pl_mi))

		if pl_mi<0:
			pl_mis='- '+pl_mis
		else:
			pl_mis='+ '+pl_mis

		pm.append(pl_mi)
		pms.append(pl_mis)
		gl.append(int_str_comma(goal1))
		prt4.append(i[7])
		if prt6 != i[7]:
			min_switch = 1
		else:
			min_switch = 0
		prt6=i[7]
		min_switch4.append(min_switch)

	overall=zip(o,m,c,p,op,tot,pred,sw,pm,gl,pms,prt4,ms)

	request.session['Total_10R']= overall
	return render(request,'mgmt_track_week.html')
	return render(request,'mgmt_track_week_b.html')

def int_str_comma(var1):
	x=str(var1)
	y=len(x)
	z=x
	if y>3:
		front1=x[:(y-3)]
		end1=x[-3:]
		z=front1+','+end1
	return z

def mgmt_production_sort(summary_data,request):
	summary_data.sort(key=getKey3)
	a1 = []
	a2 = []
	a3 = []
	ab = -1
	b = 0
	for i in summary_data:
		a = i[1]
		if b != a:
			ab = ab * -1
			b = a
		a1.append(i[0]) # Asset number
		a2.append(i[1]) # Group number
		a3.append(ab)	# marker   1 or -1 for formating
	aa = zip(a1,a2,a3) # aa is the sorted list with -1 or 1 for grouping
	request.session['summary_data'] = aa
	return

def mgmt_production_summary(request):
	aa = request.session['summary_data']
	tcur=int(time.time())
	tcur_prev = tcur - 86400
	
	tm = time.localtime(tcur)
	hh = tm[3]
	mm = tm[4]
	ss = tm[5]
	wd = tm[6]
	u = tcur - (hh*3600) - (mm*60) - (ss) - (wd*86400)	# Week Start
	p = u + 604800	#End of Week
	up = u - 604800	  # Previous Week


	now1 = int((tcur - u + (60*60))/float((8*60*60))) # number of shifts completed 
	if now1 < 1 :
		now1 = 1

	pred_multiplier = 15 / float(now1)



	tm2 = time.localtime(tcur_prev)
	tu = time.localtime(u)
	tup = time.localtime(up)

	mu = str(tu[1])
	mup = str(tup[1])
	mm = str(tm2[1])
	m = str(tm[1])	
	d = str(tm[2])
	dd = str(tm2[2])
	du = str(tu[2])
	dup = str(tup[2])
	hr = int(tm[3])

	m = ('0' + m) if len(m) == 1 else m
	d = ('0' + d) if len(d) == 1 else d
	mm = ('0' + mm) if len(mm) == 1 else mm
	dd = ('0' + dd) if len(dd) == 1 else dd
	mu = ('0' + mu) if len(mu) == 1 else mu
	du = ('0' + du) if len(du) == 1 else du
	mup = ('0' + mup) if len(mup) == 1 else mup
	dup= ('0' + dup) if len(dup) == 1 else dup

	date1 = str(tm[0]) + '-' + m + '-' + d		 # date for Midnight shift of the 24hr mark
	date2 = str(tm2[0]) + '-' + mm + '-' + dd	 # date for Afternoon and Day shift on the 24hr mark
	date3 = str(tu[0]) + '-' + mu + '-' + du	   # date for start of week
	date4 = str(tup[0]) + '-' + mup + '-' + dup		  # date for start of last week

	if hr>= 23 :
		sh1 = ['Aft','Day','Mid']
		sh2 = ['3pm-11pm','7am-3pm','11pm-7am']
		sh3 = [0,0,0]
		sh4 = [1,2,3]
	elif hr>= 15 and hr < 23:
		sh1 = ['Day','Mid','Aft']
		sh2 = ['7am-3pm','11pm-7am','3pm-11pm']
		sh3 = [0,0,1]
		sh4 = [1,2,3]
	elif hr >= 7 and hr < 15:
		sh1 = ['Mid','Aft','Day']
		sh2 = ['11pm-7am','3pm-11pm','7am-3pm']
		sh3 = [0,1,1]
		sh4 = [1,2,3]
	else:
		sh1 = ['Aft','Day','Mid']
		sh2 = ['3pm-11pm','7am-3pm','11pm-7am']
		sh3 = [1,1,1]
		sh4 = [1,2,3]


	ssh = zip(sh1,sh2,sh3,sh4)

	request.session['shift_title1'] = sh1[0]
	request.session['shift_title2'] = sh1[1]
	request.session['shift_title3'] = sh1[2]

	# u_sh_start = tcur - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])	   # Starting unix of shift


	db, cur = db_set(request)
	mid_shift = '11pm-7am'
	aft_shift = '3pm-11pm'
	day_shift = '7am-3pm'

	e1 = []
	e2 = []
	e3 = []
	e4 = []
	f1 = []
	f2 = []
	try:
		assets,groups,formats = zip(*aa)
	except:
		assets,groups,formats,y,y,y,y,y,y,y,y,y = zip(*aa)

	for i in aa:
		# Calculate Week to date total
		try:
			aql = "SELECT SUM(actual_produced) FROM sc_production1 WHERE pdate >= '%s' and asset_num = '%s'" % (date3,i[0])
			cur.execute(aql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			sum1 = int(tmp3[0])
		except:
			sum1 = 0
		f1.append(sum1)
		# Calculate Last Week total
		try:
			aql = "SELECT SUM(actual_produced) FROM sc_production1 WHERE pdate >= '%s' and pdate < '%s' and asset_num = '%s'" % (date4,date3,i[0])
			cur.execute(aql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			sum1 = int(tmp3[0])
		except:
			sum1 = 0
		f2.append(sum1)

		tot1 = 0
		for ii in ssh:
			ptcur = tcur - ii[2] * 86400
			ptm = time.localtime(ptcur)
			pm = str(ptm[1])	
			pd = str(ptm[2])
			pm = ('0' + pm) if len(pm) == 1 else pm
			pd = ('0' + pd) if len(pd) == 1 else pd
			date1 = str(ptm[0]) + '-' + pm + '-' + pd	   # date to lookup

			try:
				aql = "SELECT SUM(actual_produced) FROM sc_production1 WHERE pdate = '%s' and asset_num = '%s' and shift = '%s'" % (date1,i[0],ii[1])
				cur.execute(aql)
				tmp2 = cur.fetchall()
				tmp3 = tmp2[0]
				sum1 = int(tmp3[0])
			except:
				sum1 = 0
			if ii[3] == 1:
				e1.append(sum1)
				ee1 = ii[0]
			elif ii[3] == 2:
				e2.append(sum1)
				ee2 = ii[0]
			elif ii[3] == 3:
				e3.append(sum1)
				ee3 = ii[0]
			tot1 = tot1 + sum1 

		e4.append(tot1) # total for all 3 shifts on this asset


	aa = zip(assets,groups,formats,e1,e2,e3,e4,f1,f2)

	# This section will group totals with the group and assign row span number or 0
	gg=0 
	ctr2 = []
	tot2 = []
	tot4 = []
	tot6 = []
	tot8 = []
	for i in aa:
		g=i[1]
		if g!=gg:
			ctr = 0
			tot = 0
			tot3 = 0
			tot7 = 0
			for ii in aa:
				if ii[1] == g:
					tot = tot + ii[6]
					tot3 = tot3 + ii[7]
					tot7 = tot7 + ii[8]
					ctr = ctr + 1
		else:
			ctr = 0
			tot = 0
			tot3 = 0
			tot7 = 0
		ctr2.append(ctr)
		tot2.append(tot)
		tot4.append(tot3)
		tot5 = int(tot3 * pred_multiplier)
		tot6.append(tot5)
		tot8.append(tot7)
		gg = g

	aa = zip(assets,groups,formats,e1,e2,e3,e4,ctr2,tot2,tot4,tot6,tot8)
	request.session['summary_data'] = aa
	db.close()
	# rr=4/0
	return


def getKey3(item):
	return int(item[1])

def mgmt_initialize_cat_table(request):
	part1 = [('50-3627','GF6'),('50-3632','GF6'),('50-1713','GF6'),('50-1731','GF6'),('50-9341','10R80'),('50-0455','10R60')]
	part1 = part1 + [('50-5214','10R140'),('50-3214','10R140'),('50-4865','GFx'),('50-9641','GFx')]
	part1 = part1 + [('50-5401','AB1V'),('50-5404','AB1V'),('50-8670','AB1V'),('50-6729','6L Output')]
	part1 = part1 + [('50-4900','6L Output'),('50-6686','6L Output'),('50-2421','6L Input'),('50-4916','6L Input')]
	part1 = part1 + [('50-2407','6L Input'),('50-4748','ZF'),('50-3050','Magna'),('50-1467','Magna')]
	db, cursor = db_set(request)
	try:
		cursor.execute("CREATE TABLE tkb_part_cat(Id INT PRIMARY KEY AUTO_INCREMENT,partno CHAR(50), category CHAR(50))")
		db.commit()
		for i in part1:
			cursor.execute('''INSERT INTO tkb_part_cat(partno,category) VALUES(%s,%s)''', (i[0],i[1]))
			db.commit()
	except:
		dummy = 1
	db.close()
	return

def mgmt_24hr_production(request):

	p =['50-1467','50-1467','50-1467','50-1467','50-3050','50-3050','50-3050','50-3050','50-5710','50-5710','50-5710','50-5710','50-9341','50-9341','50-9341','50-9341','50-0455','50-0455','50-0455','50-0455','50-5401','50-5401','50-5401','50-5401','50-5404','50-5404','50-5404','50-5404','50-8670','50-8670','50-8670','50-8670']
	a1=['650L','770','','','769','770','','','769','770','','','1533','','','','1816','','','','','','','','','','','','','','','']
	a2=['650R','728','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
	a3=['769','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
	a4=['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
	order1 = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]
	title1 = ['1467 Finished','1467 Broached','','','3050 Finished','3050 Broached','','','5710 Finished','5710 Broached','','','9341 Finished','','','','0455 Finished','','','','','','','','','','','','','','','']

	cnt=[]
	part2 = []
	title2 = []
	order2 = []
	ddata = []

	data1 = zip(p,a1,a2,a3,a4,order1,title1)

	t=int(time.time())
	tm = time.localtime(t)
	request.session["time"] = t

	a1 = tm[6] * 86400
	a2 = tm[3] * 60 * 60
	a3 = tm[4] * 60
	a4 = tm[5]
	week_start1 = t - a1 - a2 - a3 - a4

	u1 = t - tm[3]*60*60-tm[4]*60-tm[5]-61200	 # Starting 7am previous day
	u2 = u1 + 86400
	week_start2 = week_start1 - 604800



	st_time = [u1,week_start1,week_start2]
	fi_time = [u2,t,week_start1]
	data_name = ["data3","data2","data1"]
	data_title = ['24Hr Production 7am-7am','Production this week','Production Last Week']
	time1 = zip(st_time,fi_time,data_name,data_title)

	db, cur = db_set(request)
	for ii in time1:
		a1 = ii[0]
		a2 = ii[1]
		dataz = ii[2]
		cnt=[]
		part2=[]
		order2=[]
		title2=[]
		for i in data1:
			prt = i[0]
			asset1 = i[1]
			asset2 = i[2]
			asset3 = i[3]
			asset4 = i[4]
			
			if asset1 == 'B':
				pp = prt[-4:]
				aql = "SELECT COUNT(*) FROM barcode WHERE scrap >= '%d' and scrap <= '%d' and right(asset_num,4) = '%s'" % (a1,a2,pp)
				cur.execute(aql)
				tmp2 = cur.fetchall()
				tmp3 = tmp2[0]
				countz = tmp3[0]
			else:
				if prt == '50-5401':
					pprt = 'AB1V Input'
				else:
					pprt = prt
				
				# if ii[2] == 'data2' and asset1=='1511':
				# 	ewew=3/0

				aql = "SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and (Machine = '%s' or Machine = '%s' or Machine = '%s' or Machine = '%s')" % (a1,a2,pprt,asset1,asset2,asset3,asset4)

				cur.execute(aql)
				tmp2 = cur.fetchall()
				tmp3 = tmp2[0]

				# if ii[2] == 'data2' and asset1=='1502':
				# 	ewew=3/0

				countz = tmp3[0]

			county = number_comma(countz)
			cnt.append(county)
			part2.append(prt)
			order2.append(i[5])
			title2.append(i[6])
		data3 = zip(part2,cnt,order2,title2)
		request.session[dataz] = data3

		title1 = dataz + 'title'
		request.session[title1] = ii[3]



	db.close()


	# increment the 3 making it data1 data2 data3 in the for loop above
	# also use an array to figure start finish times example
	# [u1,week_start1,week_start2]
	# [u2,t,week_start1]

	return

def mgmt_test1(request):
	request.session["bounce"] = 0
	return render(request, "mgmt_test1.html")

def number_comma(x):
	x = str(x)
	y = ''
	if len(x) > 3:
		a = len(x)
		y = x[:(a-3)]+","+x[-3:]
	else:
		y = str(x)
	return y
	
# Reset the password so it logs out
def mgmt_logout(request):
	request.session["mgmt_login_password"] = ""
	request.session["mgmt_login_password_check"] = 0
	return render(request, "mgmt.html")

def mgmt_login_form(request):	
	if 'button1' in request.POST:
		login_name = request.POST.get("login_name")
		login_password = request.POST.get("login_password")

		if len(login_name) < 5:
			login_password = 'wrong'

		if login_password == 'bort':
			request.session["mgmt_login_password_check"] = 1
			request.session["mgmt_login_name"] = login_name
			request.session["mgmt_login_password"] = login_password
		else:
			request.session["mgmt_login_password_check"] = 0

	
		return mgmt(request)
		
	elif 'button2' in request.POST:
		
		return render(request,'login/reroute_lost_password.html')

	else:
		form = login_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_name"] = ""
	request.session["login_password"] = ""
	return render(request,'mgmt_login_form.html', args)	

def mgmt_production_hourly(request):
	table_headers = ["ID","Cell","Operator","Date","Shift","Hour","Target","Actual","Shift Target","Shift Actual","DT Code","DT Mins","DT Reason","Created"]
	table_variables = ["id","p_cell","initial","p_date","p_shift","p_hour","hourly_target","hourly_actual","shift_target","shift_actual","downtime_code","downtime_mins","downtime_reason","created_at"]

	mgmt_temp = "SELECT "
	for i in table_variables:
		mgmt_temp = mgmt_temp + i + ","
	mgmt_temp = mgmt_temp[:-1] + " FROM sc_prod_hour"
	request.session["mgmt_table_name"] = 'sc_prod_hour'
	request.session["mgmt_table_title"] = 'Hourly Production'
	request.session["mgmt_table_call"] = mgmt_temp
	request.session["mgmt_edit"] = "mgmt_production_hourly_edit"
	request.session["table_headers"] = table_headers
	request.session["table_variables"] = table_variables
	request.session["mgmt_production_call"] = 'mgmt_production_hourly'
	request.session['starting_id'] = '99999999'
	request.session['direction_id'] = 1
	request.session['ctr'] = 0

	return mgmt_display(request)

def mgmt_production(request):
	table_headers = ["ID","Asset","Job","Part","Amount","DTime","Clock","Date","Shift","Runtime","Target"]
	table_variables = ["id","asset_num","machine","partno","actual_produced","down_time","comments","pdate","shift","shift_hours_length","target"]

	mgmt_temp = "SELECT "
	for i in table_variables:
		mgmt_temp = mgmt_temp + i + ","
	mgmt_temp = mgmt_temp[:-1] + " FROM sc_production1"
	request.session["mgmt_table_name"] = 'sc_production1'
	request.session["mgmt_table_title"] = 'Production Entries'
	request.session["mgmt_table_call"] = mgmt_temp
	request.session["mgmt_edit"] = "mgmt_display_edit"
	request.session["table_headers"] = table_headers
	request.session["table_variables"] = table_variables
	request.session["mgmt_production_call"] = 'mgmt_production'
	request.session['starting_id'] = '99999999'
	request.session['direction_id'] = 1
	request.session['ctr'] = 0

	return mgmt_display(request)

def mgmt_cycletime(request):
	table_headers = ["ID","Asset","Part","Cycletime","Job"]
	table_variables = ["Id","asset","part","cycletime","machine"]

	mgmt_temp = "SELECT "
	for i in table_variables:
		mgmt_temp = mgmt_temp + i + ","
	mgmt_temp = mgmt_temp[:-1] + " FROM tkb_cycletime"
	request.session["mgmt_table_name"] = 'tkb_cycletime'
	request.session["mgmt_table_title"] = 'Cycle Times'
	request.session["mgmt_table_call"] = mgmt_temp
	request.session["mgmt_edit"] = "mgmt_display_edit"
	request.session["table_headers"] = table_headers
	request.session["table_variables"] = table_variables
	request.session["mgmt_production_call"] = 'mgmt_cycletime'
	request.session['starting_id'] = '99999999'
	request.session['direction_id'] = 1
	request.session['ctr'] = 0

	return mgmt_display(request)






def mgmt_production_hourly_edit(request, index):
	tmp_index = index
	#request.session["index"] = index
	db, cur = db_set(request) 
	try:
		sql = "SELECT * FROM sc_prod_hour where id = '%s'" %(tmp_index)
		cur.execute(sql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
	except:
		tmp="No"	


# ***********************************************************************************************************************************
	request.session["mgmt_hourly_cell"] = tmp2[1]
	request.session["mgmt_hourly_initials"] = tmp2[2]
	request.session["mgmt_hourly_shift"] = tmp2[5]
	ddate = tmp2[4]
	ddd = vacation_set_current6(ddate)
	request.session["mgmt_hourly_date"] = vacation_set_current6(ddate)
	request.session["mgmt_hourly_hour"] = tmp2[6]
	request.session["mgmt_hourly_actual"] = tmp2[8]
	request.session["mgmt_hourly_dtcode"] = tmp2[11]
	request.session["mgmt_hourly_dtmins"] = tmp2[12]
	request.session["mgmt_hourly_dtreason"] = " "
	request.session["mgmt_hourly_dtreason"] = tmp2[13]

	


	try:
		if len(request.session["mgmt_hourly_dtreason"]) < 2:
			request.session["mgmt_hourly_dtreason"] = "-"
	except:
		request.session["mgmt_hourly_dtreason"] = "-"


	if request.POST:
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'mgmt_production_hourly'
				return direction(request)
		except:
			dummy = 1

#		return render(request,'kiosk/kiosk_test2.html',{'tmp':ddd})
		mgmt_hourly_date = request.POST.get("mgmt_hourly_date")
		mgmt_hourly_cell = request.POST.get("mgmt_hourly_cell")
		mgmt_hourly_initials = request.POST.get("mgmt_hourly_initials")
		mgmt_hourly_shift = request.POST.get("mgmt_hourly_shift")
		mgmt_hourly_hour = request.POST.get("mgmt_hourly_hour")
		mgmt_hourly_actual = request.POST.get("mgmt_hourly_actual")
		mgmt_hourly_dtcode = request.POST.get("mgmt_hourly_dtcode")
		mgmt_hourly_dtmins = request.POST.get("mgmt_hourly_dtmins")
		mgmt_hourly_dtreason = request.POST.get("mgmt_hourly_reason")


		try:
			cql = ('update sc_prod_hour SET p_cell = "%s",initial="%s",hourly_actual="%s", p_date="%s", p_shift="%s" WHERE id ="%s"' % (mgmt_hourly_cell,mgmt_hourly_initials,mgmt_hourly_actual,mgmt_hourly_date,mgmt_hourly_shift,tmp_index))
			cur.execute(cql)
			db.commit()
		except:
			dummy = 1
			
		db.close()
		request.session["route_1"] = 'mgmt_production_hourly'
		return direction(request)
		#return render(request,'kiosk/kiosk_test2.html',{'tmp':tmp2})

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form	 

#	db, cur = db_set(request)
#	s1 = "SELECT MAX(id)  FROM sc_prod_hour WHERE p_cell = '%s'" %(p_cell) 
#	cur.execute(s1)
#	tmp = cur.fetchall()
#	tmp2 = tmp[0]
#	tmp3 = tmp2[0]
	tcur=int(time.time())
	return render(request, "production/mgmt_production_hourly_edit.html",{'args':args,'tmp':tmp2,'ddate':ddd,'TCUR':tcur})

# ***********************************************************************************************************************************

def mgmt_users_logins(request):
	request.session["bounce"] = 0
	db, cursor = db_set(request)
	request.session["page_edit"] = "user login"
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_logins(Id INT PRIMARY KEY AUTO_INCREMENT,user_name CHAR(50), password CHAR(50), department CHAR(50),active1 INT(10) default 0)""")
	db.commit()
	sql = "SELECT * FROM tkb_logins order by department ASC, user_name ASC" 
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close()
	return render(request, "production/mgmt_users_logins.html",{'tmp':tmp})

def mgmt_users_logins_edit(request):
	p = request.session["page_edit"]
	index = request.session["current_index"]


	if request.POST:
		user_name = request.POST.get("user_name")
		password = request.POST.get("password")
		department = request.POST.get("department")

		a = request.POST
		b = -4
		try:
			b = int(a.get("one"))
		except:
			b = -4
		db, cursor = db_set(request)
		cur = db.cursor()

		if b == -3:	 # Reroute to the Warning message 
			request.session["bounce"] = 1
			request.session["user_logins1"] = user_name
			request.session["password"] = password
			request.session["department"] = department
			return render(request,'production/redirect_mgmt_users_logins_edit.html')

		if b == -2:	 # Cancel Entry and go back to logins list
			request.session["bounce"] = 0

		return render(request,'production/redirect_mgmt_users_logins.html')

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	a = request.session["user_logins1"]
	b = request.session["bounce"]


	return render(request, "production/mgmt_users_logins_edit.html",{'args':args})


def mgmt_users_logins_update(request):
	index = request.session["current_index"]
	user_name = request.session["user_logins1"]
	password = request.session["password"]
	department = request.session["department"] 

	db, cursor = db_set(request)
	cur = db.cursor()

	mql =( 'update tkb_logins SET user_name="%s" WHERE Id="%s"' % (user_name,index))
	cur.execute(mql)
	db.commit()
	mql =( 'update tkb_logins SET password="%s" WHERE Id="%s"' % (password,index))
	cur.execute(mql)
	db.commit()
	mql =( 'update tkb_logins SET department="%s" WHERE Id="%s"' % (department,index))
	cur.execute(mql)
	db.commit()

	request.session["bounce"] = 0
	db.close()
	return render(request,'production/redirect_mgmt_users_logins.html')

def mgmt_users_logins_add(request):
	p = request.session["page_edit"]

	if request.POST:
		user_name = request.POST.get("user_name")
		password = request.POST.get("password")
		department = request.POST.get("department")

		a = request.POST
		b = -4
		try:
			b = int(a.get("one"))
		except:
			b = -4
		db, cursor = db_set(request)
		cur = db.cursor()

		if b == -3:	 # Reroute to the Warning message 
			request.session["bounce"] = 1
			request.session["user_logins1"] = user_name
			request.session["password"] = password
			request.session["department"] = department
			return render(request,'production/redirect_mgmt_users_logins_add.html')

		if b == -2:	 # Cancel Entry and go back to logins list
			request.session["bounce"] = 0

		return render(request,'production/redirect_mgmt_users_logins.html')

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request, "production/mgmt_users_logins_add.html",{'args':args})

def mgmt_users_logins_add_new(request):
	user_name = request.session["user_logins1"]
	password = request.session["password"]
	department = request.session["department"] 

	db, cursor = db_set(request)
	cur = db.cursor()

	cur.execute('''INSERT INTO tkb_logins(user_name,password,department) VALUES(%s,%s,%s)''', (user_name,password,department))
	db.commit()
	db.close()

	request.session["bounce"] = 0
	return render(request,'production/redirect_mgmt_users_logins.html')

def mgmt_priorities(request):
	db, cursor = db_set(request)
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_priorities(Id INT PRIMARY KEY AUTO_INCREMENT,priority Int(50), part CHAR(50))""")
	db.commit()
	sql = "SELECT * FROM tkb_priorities order by priority ASC" 
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close()
	r = []
	p = []
	n = []
	for i in tmp:
		r.append('ranking_' + str(i[1]))
		p.append(i[2])
		n.append(str(i[1]))
	rp = zip(r,p,n)
	if request.POST:
		x = request.POST.get("thedata")
		old1 = ''
		old2 = ''
		cur = ''
		v1 = ''
		v2 = []
		v3 = []
		sw = 0
		for i in x:
			if i == '&':
				sw = 0
				v2.append(v1)
				v1 = ''
			if sw == 1:
				v1 = v1 + str(i)
			if i == '=':
				sw = 1
		v2.append(v1)
		for i in v2:
			for ii in rp:
				if i == ii[2]:
					v3.append(ii[1])
		db, cursor = db_set(request)
		cursor.execute("""DROP TABLE IF EXISTS tkb_priorities""") 
		db.commit()
		cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_priorities(Id INT PRIMARY KEY AUTO_INCREMENT,priority Int(50), part CHAR(50))""")
		db.commit()
		pr = 1
		for i in v3:
			cursor.execute('''INSERT INTO tkb_priorities(priority,part) VALUES(%s,%s)''', (pr,i))
			db.commit()
			pr = pr + 1
		db.close()
		prioritize(request)
		return render(request,"redirect_priorities.html")
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'priorities.html',{'rp':rp,'args':args})

def prioritize(request):
	db, cur = db_set(request)
	# Only uncomment below if you plan to reinitialize the asset list
	
	# cur.execute("""DROP TABLE IF EXISTS tkb_asset_priority""")
	# cur.execute("""CREATE TABLE IF NOT EXISTS tkb_asset_priority(Id INT PRIMARY KEY AUTO_INCREMENT,asset_num CHAR(80), part CHAR(80), priority int(10))""")
	# sql = "SELECT DISTINCT asset_num FROM sc_production1"
	# cur.execute(sql)
	# tmp=cur.fetchall()
	# asset2 = []
	# for i in tmp:
	#	asset = i[0][:4]
	#	try:
	#		test1 = int(asset)
	#	except:
	#		asset = asset[:3]
	#	try:
	#		test1 = int(asset)
	#		asset2.append(asset)
	#	except:
	#		dummy = 1
	# for i in asset2:
	#	tmp_asset2 = 1
	#	n = 'None'
	#	try:
	#		sql1 = "SELECT partno FROM sc_production1 where left(asset_num,4) = '%s' and partno != '%s' ORDER BY id DESC LIMIT 1" %(i,n)
	#		cur.execute(sql1)
	#		tmp_part = cur.fetchall()
	#		part2 = tmp_part[0][0]
	#		part2 = part2[:7]
	#		cur.execute('''INSERT INTO tkb_asset_priority(asset_num,part) VALUES(%s,%s)''', (i,part2))
	#		db.commit()
	#	except:
	#		dummy = 1
	sql1 = "SELECT * FROM tkb_priorities"
	cur.execute(sql1)
	tmp_pr = cur.fetchall()
	for i in tmp_pr:
		mql =( 'update tkb_asset_priority SET priority="%s" WHERE part="%s"' % (i[1],i[2]))
		cur.execute(mql)
		db.commit()
	a = 999
	# Make all the NULL a 999 value
	cql = ('update tkb_asset_priority set priority = "%s" where priority is NULL' % (a))
	cur.execute(cql)
	db.commit()
	db.close()
	return

def wfp(request):
	db, cur = db_set(request)
	w = 'WFP'
	p = 10000
	x = 'Project'
	y = 5000
	mql =( 'update pr_downtime1 SET priority="%s" WHERE right(problem,3)="%s"' % (p,w))
	cur.execute(mql)
	db.commit()
	mql =( 'update pr_downtime1 SET priority="%s" WHERE right(problem,7)="%s"' % (y,x))
	cur.execute(mql)
	db.commit()
	db.close()
	return

# One system will be running this and it will do all the daily updates.
# Check production entries, update manpower, update matrix
def auto_updater(request):	# This will run every 30 min on the refresh page to see if update occurs
	prioritize(request)	  # This will run the asset priority section
	t=int(time.time())
	tm = time.localtime(t)
	hr1 = str(tm[3])
	min1 = str(tm[4])
	dy1 = str(tm[2])
	mn1 = str(tm[1])
	if len(dy1) == 1:
		dy1 = '0'+dy1
	if len(mn1) == 1:
		mn1 = '0' + mn1
	if len(hr1)==1:
		hr1 = '0'+hr1
	if len(min1) == 1: # Add a 0 if it's less than 10 min so it's the correct length
		min1 = '0'+min1
	cur_date  = str(tm[0])+"-"+mn1+"-"+dy1 # Sets the current date
	
	cur_time = hr1 + min1
	update_time = cur_date + " " + hr1 + ":" + min1
	try:
		db, cur = db_set(request)  
		# cur.execute("""DROP TABLE IF EXISTS tkb_updater""")
		cur.execute("""CREATE TABLE IF NOT EXISTS tkb_updater(Id INT PRIMARY KEY AUTO_INCREMENT,cur_date CHAR(80),set_time CHAR(80), program Char(80), var1 Char(80))""")
		sql= '''SELECT * FROM tkb_updater'''
		cur.execute(sql)
		tmp = cur.fetchall()
		db.close()
		for i in tmp:
			date2 = i[1]
			id2 = i[0]
			set_time = i[2]
			if date2 != cur_date:
				if int(cur_time) > int(set_time):
					db, cur = db_set(request)
					mql =( 'update tkb_updater SET cur_date = "%s" WHERE Id ="%s"' % (cur_date,id2))
					cur.execute(mql)
					db.commit()
					sql = "SELECT program,var1 FROM tkb_updater where Id = '%s'"%(id2)
					cur.execute(sql)
					tmp2 = cur.fetchall()
					program1 = tmp2[0][0]
					variable1 = tmp2[0][1]
					request.session['tkb_program'] = program1
					request.session['variable1'] = variable1
					request.session['tkb_update_time'] = update_time
					request.session['tkb_update_date'] = cur_date
					db.close()
					request.session['pecm'] = 0
					return render(request,'redirect_program.html')
	except:
		dummy = 1
	return render(request,'tkb_updater.html')

def cell_track_9341_history_on(request):
	request.session['track_history'] = 1
	return render(request,'redirect_cell_track_9341.html')
def cell_track_9341_history_off(request):
	request.session['track_history'] = ''
	return render(request,'redirect_cell_track_9341.html')


def cell_track_9341(request):
	shift_start, shift_time, shift_left, shift_end = stamp_shift_start(request)	 # Get the Time Stamp info
	machines1 = ['1504','1506','1519','1520','1502','1507','1501','1515','1508','1532','1509','1514','1510','1503','1511','1518','1521','1522','1523','1539','1540','1524','1525','1538','1541','1531','1527','1530','1528','1513','1533']
	rate = [8,8,8,8,4,4,4,4,3,3,2,2,2,2,2,8,8,8,8,4,4,4,4,3,2,2,2,2,2,1,1]
	line1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0]
	operation1 = [10,10,10,10,30,30,40,40,50,50,60,70,80,100,110,10,10,10,10,30,30,40,40,50,60,70,80,100,110,90,120]
	prt = '50-9341'
	machine_rate = zip(machines1,rate,operation1)
	machine_color =[]
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_wip_track where part = '%s'" % (prt) 
	cur.execute(sql)
	wip = cur.fetchall()
	wip_stamp = int(wip[0][1])

	# [1] -- Machine    [4] -- Timestamp  [2] -- Part   [5] -- Count ..usually 1
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%d' and Part = '%s'" % (wip_stamp,prt)
	cur.execute(sql)
	wip_data = cur.fetchall()
	wip_prod = [0 for x in range(140)]	

	for i in machine_rate:
		list1 = filter(lambda x:x[1]==i[0],wip_data)  # Filter list and pull out machine to make list1
		count1=len(list1)  # Total all in list1
		wip_prod[i[2]] = wip_prod[i[2]] + count1  # Add total to that operation variable
	op5=[]
	wip5=[]
	prd5=[]
	for i in wip:
		op5.append(i[3])
		wip5.append(int(i[4]))
		x=int(i[3])
		prd5.append(wip_prod[x])
	op5.append('120')
	wip5.append(0)
	prd5.append(wip_prod[120])
	wip_zip=zip(op5,wip5,prd5)  # Generates totals beside old WIP
	ptr = 1
	new_wip=[]
	for i in wip_zip:
		try:
			w1=i[1]
			i1=i[2]
			i2=wip_zip[ptr][2]
			w1=w1+(i1-i2)
		except:
			w1=0
		if w1 < 0 : w1 = 0
		ptr = ptr + 1
		new_wip.append(w1)
	wip_zip=zip(op5,wip5,prd5,new_wip)

	# Filter a List
	color8=[]
	rate8=[]
	machine8=[]
	pred8 = []
	av55=[]
	cnt55=[]
	sh55=[]
	shl55=[]
	op8=[]
	rt8=[]
	request.session['shift_start'] = shift_start
	for i in machine_rate:
		machine2 = i[0]
		rate2 = 3200 / float(i[1])
		rate2 = (rate2 / float(28800)) * 300
		tt = int(time.time())
		start1 = tt - shift_time
		t= tt-300
		try:
			sql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and Part = '%s' and Machine = '%s'" % (t,prt,machine2)
			cur.execute(sql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			cnt = int(tmp3[0])
		except:
			cnt = 0
		try:
			sql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and Part = '%s' and Machine = '%s'" % (start1,prt,machine2)
			cur.execute(sql)
			tmp22 = cur.fetchall()
			tmp33 = tmp22[0]
			cnt33 = int(tmp33[0])
		except:
			cnt33 = 0

		if cnt is None: cnt = 0


		rate3 = cnt / float(rate2)
		rate3 = int(rate3 * 100) # This will be the percentage we use to determine colour

		# Pediction
		try:
			avg8 = cnt33 / float(shift_time)
		except:
			shift_time = 100
			avg8 = cnt33 / float(shift_time)
			
		avg9 = avg8 * shift_left
		pred1 = int(cnt33 + avg9)

		op8.append(i[2])
		rt8.append(i[1])
		av55.append(avg8)
		cnt55.append(cnt33)
		sh55.append(shift_time)
		shl55.append(shift_left)
		pred8.append(pred1)

		if rate3>=100:
			cc='#009700'
		elif rate3>=90:
			cc='#4FC34F'
		elif rate3>=80:
			cc='#A4F6A4'
		elif rate3>=70:
			cc='#C3C300'
		elif rate3>=50:
			cc='#DADA3F'
		elif rate3>=25:
			cc='#F6F687'
		elif rate3>=10:
			cc='#F7BA84'
		elif rate3>0:
			cc='#EC7371'
		else:
			cc='#FF0400'
		color8.append(cc)
		rate8.append(rate3)
		machine8.append(machine2)

	total8=zip(machine8,rate8,color8,pred8,op8,rt8)
	total99=0
	last_op=10
	op99=[]
	opt99=[]

	op_total = [0 for x in range(200)]	

	for i in total8:
		op_total[i[4]]=op_total[i[4]] + i[3]
	db.close()
	jobs1 = zip(machines1,line1,operation1)

	
	# Date entry for History
	if request.POST:
		request.session["track_date"] = request.POST.get("date_st")
		request.session["track_shift"] = request.POST.get("shift")
		return render(request,'redirect_cell_track_9341_history.html')	
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	total8_0455,op_total_0455, wip_zip_0455 = cell_track_0455(request)

	return render(request,'cell_track_9341.html',{'codes':total8,'op':op_total,'wip':wip_zip,'codes_60':total8_0455,'op_60':op_total_0455,'wip_60':wip_zip_0455,'args':args})	


# Same tracking for 0455
def cell_track_0455(request):
	shift_start, shift_time, shift_left, shift_end = stamp_shift_start(request)	 # Get the Time Stamp info
	machines1 = ['1800','1801','1802','1529','1543','776','1824','1804','1805','1806','1808','1810','1815','1812','1816']
	rate = [2,2,2,4,4,4,4,2,2,1,1,1,1,1,1]
	line1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	operation1 = [10,10,10,30,30,30,30,40,40,50,60,70,80,100,120]
	prt = '50-0455'
	machine_rate = zip(machines1,rate,operation1)
	machine_color =[]
	db, cur = db_set(request)


	sql = "SELECT * FROM tkb_wip_track where part = '%s'" % (prt) 
	cur.execute(sql)
	wip = cur.fetchall()
	wip_stamp = int(wip[0][1])

	# [1] -- Machine    [4] -- Timestamp  [2] -- Part   [5] -- Count ..usually 1
	sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%d' and Part = '%s'" % (wip_stamp,prt)
	cur.execute(sql)
	wip_data = cur.fetchall()
	wip_prod = [0 for x in range(140)]	

	for i in machine_rate:
		list1 = filter(lambda x:x[1]==i[0],wip_data)  # Filter list and pull out machine to make list1
		count1=len(list1)  # Total all in list1
		wip_prod[i[2]] = wip_prod[i[2]] + count1  # Add total to that operation variable
	op5=[]
	wip5=[]
	prd5=[]
	for i in wip:
		op5.append(i[3])
		wip5.append(int(i[4]))
		x=int(i[3])
		prd5.append(wip_prod[x])
	op5.append('120')
	wip5.append(0)
	prd5.append(wip_prod[120])
	wip_zip=zip(op5,wip5,prd5)  # Generates totals beside old WIP
	ptr = 1
	new_wip=[]
	for i in wip_zip:
		try:
			w1=i[1]
			i1=i[2]
			i2=wip_zip[ptr][2]
			w1=w1+(i1-i2)
		except:
			w1=0
		if w1 < 0 : w1 = 0
		ptr = ptr + 1
		new_wip.append(w1)

	wip_zip=zip(op5,wip5,prd5,new_wip)


	# Filter a List
	color8=[]
	rate8=[]
	machine8=[]
	pred8 = []
	av55=[]
	cnt55=[]
	sh55=[]
	shl55=[]
	op8=[]
	rt8=[]
	request.session['shift_start'] = shift_start
	for i in machine_rate:
		machine2 = i[0]
		rate2 = 900 / float(i[1])
		rate2 = (rate2 / float(28800)) * 300
		tt = int(time.time())
		start1 = tt - shift_time
		t= tt-300
		try:
			sql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and Part = '%s' and Machine = '%s'" % (t,prt,machine2)
			cur.execute(sql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			cnt = int(tmp3[0])
		except:
			cnt = 0
		try:
			sql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and Part = '%s' and Machine = '%s'" % (start1,prt,machine2)
			cur.execute(sql)
			tmp22 = cur.fetchall()
			tmp33 = tmp22[0]
			cnt33 = int(tmp33[0])
		except:
			cnt33 = 0
		if cnt is None: cnt = 0
		rate3 = cnt / float(rate2)
		rate3 = int(rate3 * 100) # This will be the percentage we use to determine colour
		# Pediction
		try:
			avg8 = cnt33 / float(shift_time)
		except:
			shift_time = 100
			avg8 = cnt33 / float(shift_time)
			
		avg9 = avg8 * shift_left
		pred1 = int(cnt33 + avg9)

		op8.append(i[2])
		rt8.append(i[1])
		av55.append(avg8)
		cnt55.append(cnt33)
		sh55.append(shift_time)
		shl55.append(shift_left)
		pred8.append(pred1)

		if rate3>=100:
			cc='#009700'
		elif rate3>=90:
			cc='#4FC34F'
		elif rate3>=80:
			cc='#A4F6A4'
		elif rate3>=70:
			cc='#C3C300'
		elif rate3>=50:
			cc='#DADA3F'
		elif rate3>=25:
			cc='#F6F687'
		elif rate3>=10:
			cc='#F7BA84'
		elif rate3>0:
			cc='#EC7371'
		else:
			cc='#FF0400'

		if machine2=='1800' or machine2=='1801' or machine2 =='1802': cc='#C8C8C8'
		color8.append(cc)
		rate8.append(rate3)
		machine8.append(machine2)

	total8=zip(machine8,rate8,color8,pred8,op8,rt8)
	total99=0
	last_op=10
	op99=[]
	opt99=[]

	op_total = [0 for x in range(200)]	

	for i in total8:
		op_total[i[4]]=op_total[i[4]] + i[3]
	db.close()
	jobs1 = zip(machines1,line1,operation1)

	return total8, op_total, wip_zip

def cell_track_9341_mobile(request):

	
	shift_start, shift_time, shift_left, shift_end = stamp_shift_start(request)	 # Get the Time Stamp info
	machines1 = ['1504','1506','1519','1520','1502','1507','1501','1515','1508','1532','1509','1514','1510','1503','1511','1518','1521','1522','1523','1539','1540','1524','1525','1538','1541','1531','1527','1530','1528','1513','1533']
	rate = [8,8,8,8,4,4,4,4,3,3,2,2,2,2,2,8,8,8,8,4,4,4,4,3,2,2,2,2,2,1,1]
	line1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0]
	operation1 = [10,10,10,10,30,30,40,40,50,50,60,70,80,100,110,10,10,10,10,30,30,40,40,50,60,70,80,100,110,90,120]
	prt = '50-9341'
	machine_rate = zip(machines1,rate,operation1)
	machine_color =[]
	db, cur = db_set(request)
	color8=[]
	rate8=[]
	machine8=[]

	for i in machine_rate:
		machine2 = i[0]
		rate2 = 3200 / float(i[1])
		rate2 = (rate2 / float(28800)) * 300
		t=int(time.time()) - 300

		try:
			sql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and Part = '%s' and Machine = '%s'" % (t,prt,machine2)
			cur.execute(sql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			cnt = int(tmp3[0])
		except:
			cnt = 0
		if cnt is None: cnt = 0

		rate3 = cnt / float(rate2)
		rate3 = int(rate3 * 100) # This will be the percentage we use to determine colour
		
		# Below is the Color Codes
		#009700 100%
		#4FC34F 90%
		#A4F6A4 80%
		#C3C300 70%
		#DADA3F 50%
		#F6F687 25%
		#EC7371 0%

		if rate3>=100:
			cc='#009700'
		elif rate3>=90:
			cc='#4FC34F'
		elif rate3>=80:
			cc='#A4F6A4'
		elif rate3>=70:
			cc='#C3C300'
		elif rate3>=50:
			cc='#DADA3F'
		elif rate3>=25:
			cc='#F6F687'
		elif rate3>=10:
			cc='#F7BA84'
		elif rate3>0:
			cc='#EC7371'
		else:
			cc='#FF0400'
			#cc='#EC7371'	Change to red when ready to go
		color8.append(cc)
		rate8.append(rate3)
		machine8.append(machine2)

	total8=zip(machine8,rate8,color8)


	db.close()
	jobs1 = zip(machines1,line1,operation1)



	return render(request,'cell_track_9341_mobile.html',{'codes':total8})

def cell_track_9341_history(request):

	track_date = str(request.session['track_date'])
	track_shift = str(request.session['track_shift'])

	track_stamp = pdate_stamp(track_date)
	if track_shift=='Mid':
		track_stamp = track_stamp - 7200
	elif track_shift=='Day':
		track_stamp = track_stamp + 21600
	elif track_shift=='Aft':
		track_stamp=track_stamp + 50400
	track_stamp_end = track_stamp + 28800



	shift_start, shift_time, shift_left, shift_end = stamp_shift_start(request)	 # Get the Time Stamp info
	machines1 = ['1504','1506','1519','1520','1502','1507','1501','1515','1508','1532','1509','1514','1510','1503','1511','1518','1521','1522','1523','1539','1540','1524','1525','1538','1541','1531','1527','1530','1528','1513','1533']
	rate = [8,8,8,8,4,4,4,4,3,3,2,2,2,2,2,8,8,8,8,4,4,4,4,3,2,2,2,2,2,1,1]
	line1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0]
	operation1 = [10,10,10,10,30,30,40,40,50,50,60,70,80,100,110,10,10,10,10,30,30,40,40,50,60,70,80,100,110,90,120]
	prt = '50-9341'
	machine_rate = zip(machines1,rate,operation1)
	machine_color =[]
	db, cur = db_set(request)
	color8=[]
	rate8=[]
	machine8=[]
	pred8 = []
	av55=[]
	cnt55=[]
	sh55=[]
	shl55=[]
	op8=[]
	for i in machine_rate:
		machine2 = i[0]
		rate2 = 3200 / float(i[1])

		try:
			sql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and TimeStamp <= '%d' and Part = '%s' and Machine = '%s'" % (track_stamp,track_stamp_end,prt,machine2)
			cur.execute(sql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			cnt = int(tmp3[0])
		except:
			cnt = 0


		# try:
		# 	sql = "SELECT SUM(Count) FROM GFxPRoduction WHERE TimeStamp >= '%d' and Part = '%s' and Machine = '%s'" % (start1,prt,machine2)
		# 	cur.execute(sql)
		# 	tmp22 = cur.fetchall()
		# 	tmp33 = tmp22[0]
		# 	cnt33 = int(tmp33[0])
		# except:
		# 	cnt33 = 0


		if cnt is None: cnt = 0

		rate3 = cnt / float(rate2)
		rate3 = int(rate3 * 100) # This will be the percentage we use to determine colour

		# Pediction
		# avg8 = cnt33 / float(shift_time)
		# avg9 = avg8 * shift_left
		pred1 = int(cnt)

		op8.append(i[2])
		# av55.append(avg8)
		# cnt55.append(cnt33)
		# sh55.append(shift_time)
		# shl55.append(shift_left)

		pred8.append(pred1)
	
		# Below is the Color Codes
		#009700 100%
		#4FC34F 90%
		#A4F6A4 80%
		#C3C300 70%
		#DADA3F 50%
		#F6F687 25%
		#EC7371 0%

		if rate3>=100:
			cc='#009700'
		elif rate3>=90:
			cc='#4FC34F'
		elif rate3>=80:
			cc='#A4F6A4'
		elif rate3>=70:
			cc='#C3C300'
		elif rate3>=50:
			cc='#DADA3F'
		elif rate3>=25:
			cc='#F6F687'
		elif rate3>=10:
			cc='#F7BA84'
		elif rate3>0:
			cc='#EC7371'
		else:
			cc='#FF0400'
			#cc='#EC7371'	Change to red when ready to go
		color8.append(cc)
		rate8.append(rate3)
		machine8.append(machine2)


	total8=zip(machine8,rate8,color8,pred8,op8)

	total99=0
	last_op=10
	op99=[]
	opt99=[]

	op_total = [0 for x in range(200)]	


	for i in total8:

		op_total[i[4]]=op_total[i[4]] + i[3]



	db.close()
	jobs1 = zip(machines1,line1,operation1)

	# Date entry for History
	if request.POST:
		request.session["track_date"] = request.POST.get("date_st")
		request.session["track_shift"] = request.POST.get("shift")
		return render(request,'redirect_cell_track_9341_history.html')	
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form


	return render(request,'cell_track_9341.html',{'codes':total8,'op':op_total,'args':args})	

# This will update the WIP_TRACK to current wip and reset time to current time.
def wip_update(request):
	machines1 = ['1504','1506','1519','1520','1502','1507','1501','1515','1508','1532','1509','1514','1510','1503','1511','1518','1521','1522','1523','1539','1540','1524','1525','1538','1541','1531','1527','1530','1528','1513','1533']
	rate1 = [8,8,8,8,4,4,4,4,3,3,2,2,2,2,2,8,8,8,8,4,4,4,4,3,2,2,2,2,2,1,1]
	line1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0]
	operation1 = [10,10,10,10,30,30,40,40,50,50,60,70,80,100,110,10,10,10,10,30,30,40,40,50,60,70,80,100,110,90,120]
	prt1 = ['50-9341','50-0455']

	machines2 = ['1800','1801','1802','1529','1543','776','1824','1804','1805','1806','1808','1810','1815','1812','1816']
	rate2 = [2,2,2,4,4,4,4,2,2,1,1,1,1,1,1]
	line2 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	operation2 = [10,10,10,30,30,30,30,40,40,50,60,70,80,100,120]

	prt3 = []
	for x in machines1:
		prt3.append('50-9341')
	for x in machines2:
		prt3.append('50-0455')

	machines1 = machines1 + machines2
	rate1 = rate1 + rate2
	line1 = line1 + line2
	operation1 = operation1 + operation2
	machine_rate = zip(machines1,rate1,operation1,prt3)


	db, cur = db_set(request)
	for j in prt1:
		sql = "SELECT * FROM tkb_wip_track where part = '%s'" % (j) 
		cur.execute(sql)
		wip = cur.fetchall()
		wip_stamp = int(wip[0][1])

		# [1] -- Machine    [4] -- Timestamp  [2] -- Part   [5] -- Count ..usually 1
		sql = "SELECT * FROM GFxPRoduction WHERE TimeStamp >= '%d' and Part = '%s'" % (wip_stamp,j)
		cur.execute(sql)
		wip_data = cur.fetchall()
		wip_prod = [0 for x in range(140)]	

		for i in machine_rate:
			list1 = filter(lambda x:x[1]==i[0],wip_data)  # Filter list and pull out machine to make list1
			count1=len(list1)  # Total all in list1
			wip_prod[i[2]] = wip_prod[i[2]] + count1  # Add total to that operation variable
		op5=[]
		wip5=[]
		prd5=[]


		for i in wip:
			if j == i[2]:
				op5.append(i[3])
				wip5.append(int(i[4]))
				x=int(i[3])
				prd5.append(wip_prod[x])
		op5.append('120')
		wip5.append(0)
		prd5.append(wip_prod[120])
		wip_zip=zip(op5,wip5,prd5)  # Generates totals beside old WIP


		ptr = 1
		new_wip=[]
		for i in wip_zip:
			try:
				w1=i[1]
				i1=i[2]
				i2=wip_zip[ptr][2]
				w1=w1+(i1-i2)
			except:
				w1=0
			if w1 < 0 : w1 = 0
			ptr = ptr + 1
			new_wip.append(w1)
		wip_zip=zip(op5,wip5,prd5,new_wip)

		t=int(time.time())

		for a in wip_zip:
			mql =( 'update tkb_wip_track SET timestamp="%s",wip="%s"  WHERE (part="%s" and operation = "%s")' % (t,a[3],j,a[0]))
			cur.execute(mql)
			db.commit()



	db.close()
	return render(request,'test7.html')	