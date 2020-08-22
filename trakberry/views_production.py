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
from views_db import db_open, db_set
from mod_tracking import Graph_Data
# from datetime import datetime 
from time import strftime
from datetime import datetime
import time


# *********************************************************************************************************
# MAIN Production View
# This is the main Administrator View to tackle things like cycle times, view production etc.
# *********************************************************************************************************
def track_10r_data(request,t,u):
	m = '1533'
	mrr = (337*(28800))/float(28800)
	db, cursor = db_set(request)
	sql = "SELECT * FROM GFxPRoduction where TimeStamp >= '%d' and TimeStamp< '%d' and machine = '%s'" %(u,t,m)
	cursor.execute(sql)
	tmp = cursor.fetchall()	
	db.close()
	gr_list, brk1, brk2, multiplier  = Graph_Data(t,u,m,tmp,mrr)
	return gr_list

def track_tri_data(request,t,u):
	m = '920'
	mrr = (189*(28800))/float(28800)
	db, cursor = db_set(request)
	sql = "SELECT * FROM GFxPRoduction where TimeStamp >= '%d' and TimeStamp< '%d' and machine = '%s'" %(u,t,m)
	cursor.execute(sql)
	tmp = cursor.fetchall()	
	db.close()
	gr_list, brk1, brk2, multiplier  = Graph_Data(t,u,m,tmp,mrr)
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


	return wday,mnth,day1,shift

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
	u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])    # Starting unix of shift

	shift_time = t-u
	shift_left = 28800 - shift_time
	request.session["shift_time"] = shift_time
	# target = 337 / float(3600) # 10R Target
	target = 189 / float(3600) # Trilobe Target

	target = shift_time * target
	request.session["target"] = int(target)

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

	gr_list = track_tri_data(request,t,u) # Get the Graph Data
	
	return render(request, "track.html",{"tm":u,"dt":tm,'GList':gr_list})



def mgmt(request):
	request.session["bounce"] = 0
	tcur=int(time.time())

	mgmt_24hr_production(request)
	return render(request, "mgmt_start.html",{'TCUR':tcur})

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
	mgmt_initialize_cat_table(request)  # initialize category table if it doesn't exist
	# vt = vacation_temp()
	vt1, vt2 = vacation_set_current2_1()
	sh1 = '11pm-7am'
	sh2 = '7am-3pm'
	sh3 = '3pm-11pm'
	len_partno = []
	cat_part = []

	request.session["current_time"] = str(vt1)
	request.session["previous_time"] = str(vt2)

	db, cur = db_set(request) 
	a1 = '900'
	b1=7


	# sql = "SELECT asset_num, actual_produced, machine, partno, down_time, comments, shift_hours_length, target  FROM sc_production1 where pdate = '%s' and shift = '%s'  and asset_num = '%s'" %(vt1,sh1,a1)

	# sql = "SELECT FORMAT(sum(actual_produced),0),partno FROM sc_production1 where pdate = '%s' and shift = '%s' and asset_num = '%s' GROUP by partno" %(vt1,sh1,a1)
	# cur.execute(sql)
	# tmp_mid = cur.fetchall()
	# tmp_mid2=tmp_mid[0]
	# yy=int(tmp_mid2[0])
	# for i in tmp_mid:
	# 	m.append(int(i[0]))
	# 	m.append(i[1])
	# h = list(m)

	sql1 = "SELECT asset_num, actual_produced, machine, partno, down_time, comments, shift_hours_length, target, shift  FROM sc_production1 where pdate = '%s' and shift = '%s'" %(vt2,sh2)
	cur.execute(sql1)
	tmp_day = cur.fetchall()

	sql2 = "SELECT asset_num, actual_produced, machine, partno, down_time, comments, shift_hours_length, target, shift  FROM sc_production1 where pdate = '%s' and shift = '%s'" %(vt2,sh3)
	cur.execute(sql2)
	tmp_aft = cur.fetchall()
	sql3 = sql1 + ' union all ' +  sql2

	# Select all data last 24hrs in list
	sql4 = "SELECT asset_num, actual_produced, machine, partno, down_time, comments, shift_hours_length, target, shift  FROM sc_production1 where (pdate = '%s' and shift = '%s') or (pdate = '%s' and shift = '%s') or (pdate = '%s' and shift = '%s')" %(vt2,sh3,vt2,sh2,vt1,sh1) 
	cur.execute(sql4)
	tmp_all2 = cur.fetchall()

	sql5 = "SELECT asset_num, actual_produced, machine, partno, down_time, comments, shift_hours_length, target, shift  FROM sc_production1 where (pdate = '%s' and shift = '%s' and asset_num = '%s') or (pdate = '%s' and shift = '%s' and asset_num = '%s') or (pdate = '%s' and shift = '%s' and asset_num = '%s') ORDER BY %s %s" %(vt2,sh3,a1,vt2,sh2,a1,vt1,sh1,a1,'partno','DESC') 
	cur.execute(sql5)
	tmp_all = cur.fetchall()

	sql6 = "SELECT FORMAT(sum(actual_produced),0),partno FROM sc_production1 where length(partno) > '%d' and (pdate = '%s' and shift = '%s' and asset_num = '%s') or (pdate = '%s' and shift = '%s' and asset_num = '%s') or (pdate = '%s' and shift = '%s' and asset_num = '%s') GROUP by partno order by %s %s" %(b1,vt2,sh3,a1,vt2,sh2,a1,vt1,sh1,a1,'partno','DESC') 
	cur.execute(sql6)
	tmp_sum = cur.fetchall()

	sql_cat = "Select * from tkb_part_cat"
	cur.execute(sql_cat)
	tmp_cat = cur.fetchall()

	# This will create a new list using first number as length of partno and rest as a tuple of partno and sum of 24hr parts 
	# produced.   Make sure to refer to [1] in list as partno and [0][1] or [0][0] as other two variables
	for x in tmp_sum:
		len_partno.append(len(x[1]))
		cat1 = 'unknown'

		for y in tmp_cat:
			if x[1] == y[1]:
				cat1 = y[2]
		cat_part.append(cat1)
	part_totals_24hr = zip(tmp_sum,len_partno,cat_part)
	sort1 = sorted(part_totals_24hr, key=lambda vr: vr[2])


	request.session["24hr_production_mid"] = sort1
	request.session["24hr_production_day"] = sort1
	request.session["24hr_production_aft"] = tmp_aft

	db.close()
	return

def mgmt_test1(request):
	request.session["bounce"] = 0
	return render(request, "mgmt_test1.html")



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

		if b == -3:  # Reroute to the Warning message 
			request.session["bounce"] = 1
			request.session["user_logins1"] = user_name
			request.session["password"] = password
			request.session["department"] = department
			return render(request,'production/redirect_mgmt_users_logins_edit.html')

		if b == -2:  # Cancel Entry and go back to logins list
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

		if b == -3:  # Reroute to the Warning message 
			request.session["bounce"] = 1
			request.session["user_logins1"] = user_name
			request.session["password"] = password
			request.session["department"] = department
			return render(request,'production/redirect_mgmt_users_logins_add.html')

		if b == -2:  # Cancel Entry and go back to logins list
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