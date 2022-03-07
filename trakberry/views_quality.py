from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import maint_closeForm, maint_loginForm, maint_searchForm, tech_loginForm, sup_downForm
from views_db import db_open, db_set
from views_mod1 import find_current_date
from views_mod2 import seperate_string, create_new_table,generate_string
from views_email import e_test
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current2, vacation_set_current9
from views_supervisor import supervisor_tech_call
from views_maintenance import login_password_check
from trakberry.views_testing import machine_list_display
from mod1 import hyphon_fix, multi_name_breakdown
import MySQLdb
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
import time
import datetime 
from django.core.context_processors import csrf

def pie_chart_date(tm):
	month_st = tm[1]
	year_st = tm[0]
	day_st = tm[2]
	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
	return current_first

def initial_epv(request):
	dummy=6
	request.session["direction5"] = 0
	return render(request, "redirect_pie_chart.html")

def previous_epv(request):
	direction4 = request.session["direction5"]
	direction4 = int(direction4) - 1
	request.session["direction5"] = direction4
	return render(request,"redirect_pie_chart.html")

def next_epv(request):
	direction4 = request.session["direction5"]
	direction4 = int(direction4) + 1
	if direction4 > 0:
		direction4 = 0
	request.session["direction5"] = direction4
	return render(request,"redirect_pie_chart.html")


def pie_chart(request):
	p = 'CNC Tech'
	pp = '99999'
	c2 = 'Operator'
	c3 = 'Once per shift'
	c4 = 'Gauge Tech'
	db, cur = db_set(request) 
	sql = "SELECT COUNT(*) FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2=tmp[0][0]


	sql = "SELECT date1 FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp_date=tmp[0][0]


	try:
		direction4 = request.session["direction5"]  # -1 is backwards +1 forward
	except:
		direction4 = 0
		request.session["direction5"] = 0


	
	# Take tmp_date and calculate 7 days prior and make it current_first
	ts = time.mktime(datetime.datetime.strptime(tmp_date,"%Y-%m-%d").timetuple())
	ts = ts - 86400 + (604800 * direction4)
	tm = time.localtime(ts)
	date_start = pie_chart_date(tm)


	ts = ts + 691200
	tm = time.localtime(ts)
	date_end = pie_chart_date(tm)

	request.session["EPV_Week"] = date_start
	cnum = '99999'
	# sql7 = "SELECT Count(*) FROM quality_epv_checks where clock_num >'%s' and date1 > '%s' and date1 < '%s' " % (pp,date_start,date_end)
	# sql7 = "SELECT Count(*) FROM quality_epv_checks where shift1 IS NULL and date1 > '%s' and date1 < '%s' " % (date_start,date_end)
	# cur.execute(sql7)
	# tmp7 = cur.fetchall()
	# tmp_cmplt = tmp7[0][0]
	# sql27 = "SELECT check1,description1,asset1 FROM quality_epv_checks where shift1 IS NULL and date1 > '%s' and date1 < '%s' " % (date_start,date_end)
	# cur.execute(sql27)
	# tmp27 = cur.fetchall()

	# Use this to count Completed EPVs in checks because sometimes duplicates get entered for some reason
	sql17 = "SELECT DISTINCT check1,description1,asset1 FROM quality_epv_checks where shift1 IS NULL and date1 > '%s' and date1 < '%s' " % (date_start,date_end)
	cur.execute(sql17)
	tmp17 = cur.fetchall()
	ctr = 0
	for j in tmp17:
		ctr = ctr + 1
	tmp_cmplt = ctr


	sql9 = "SELECT date1,shift1,check1,description1,asset1,master1,clock_num FROM quality_epv_checks where clock_num >'%s' and date1 > '%s' and date1 < '%s' " % (pp,date_start,date_end)
	cur.execute(sql9)
	tmp9 = cur.fetchall()
	request.session['test9'] = tmp9
	# return render(request, "test_2.html")


	
	sql7 = "SELECT Count(*) FROM quality_epv_week"
	cur.execute(sql7)
	tmp7 = cur.fetchall()
	tmp_week = tmp7[0][0]

	sql = "SELECT Count(*) FROM quality_epv_assets where Person <> '%s' and Person <> '%s' and Person <> '%s'" % (c2,c3,c4)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp_reqd=tmp[0][0]

	sql2 = "SELECT * FROM quality_epv_assets where Person <> '%s' and Person <> '%s' and Person <> '%s'" % (c2,c3,c4)
	# sql2 = "Select * from quality_epv_assets where Person>'%s'" % (pp)
	cur.execute(sql2)
	tmp2 = cur.fetchall()

	sql3 = "Select * from quality_epv_checks where clock_num > '%s' and date1 > '%s' and date1 <= '%s' " % (cnum,date_start,date_end)
	cur.execute(sql3)
	tmp3 = cur.fetchall()

	# ctr1 = 0
	# ctr2 = 0
	# for x1 in tmp2:
	# 	ctr1 = ctr1 + 1
	# for x2 in tmp3:
	# 	ctr2 = ctr2 + 1

	a=[]
	for i in tmp2:
		ch = 0
		for ii in tmp3:
			if i[1] == ii[3] and i[8] == ii[5]:
				ch = 1
				break
		if ch == 0:
			a.append(i)

	# tmp_reqd = int(tmp_week) + int(tmp_cmplt)
	completed = int(tmp_cmplt)
	incomplete = int(tmp_reqd) - int(tmp_cmplt)


	# pp = 99999
	# sql = "SELECT Count(*) FROM quality_epv_checks where date1 >= '%s' and clock_num>'%s'" % (tmp_date,pp)
	# cur.execute(sql)
	# tmp = cur.fetchall()

	# tmp_done=tmp[0][0]

	# completed = int(tmp_done)
	# incomplete = int(tmp_reqd) - int(tmp_done)


	

	# completed = int(tmp_reqd) - int(tmp2)
	# incomplete = int(tmp2)

	sql = "SELECT * FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()

	ctr4 = 0
	for i in a:
		ctr4 = ctr4 + 1

	incomplete = ctr4

	request.session['epv_left'] = a
	request.session['epv_reqd'] = incomplete
	request.session['epv_comp'] = completed



	return render(request, "pie.html")

def epv_cleanup(request):
	c2 = 'Operator'
	c3 = 'Once per shift'
	c4 = 'Gauge Tech'
	cnum = '99999'

	tmp_date = '2021-12-08'
	# Take tmp_date and calculate 7 days prior and make it current_first
	ts = time.mktime(datetime.datetime.strptime(tmp_date,"%Y-%m-%d").timetuple())
	ts = ts - 86400 
	tm = time.localtime(ts)
	date_start = pie_chart_date(tm)
	ts = ts + 691200
	tm = time.localtime(ts)
	date_end = pie_chart_date(tm)

	db, cur = db_set(request) 
	# Use this to count Completed EPVs in checks because sometimes duplicates get entered for some reason
	sql17 = "SELECT DISTINCT check1,description1,asset1 FROM quality_epv_checks where shift1 IS NULL and date1 > '%s' and date1 < '%s' " % (date_start,date_end)
	cur.execute(sql17)
	tmp17 = cur.fetchall()
	ctr = 0
	for j in tmp17:
		ctr = ctr + 1
	tmp_cmplt = ctr

	sql2 = "SELECT * FROM quality_epv_assets where Person <> '%s' and Person <> '%s' and Person <> '%s'" % (c2,c3,c4)
	# sql2 = "Select * from quality_epv_assets where Person>'%s'" % (pp)
	cur.execute(sql2)
	tmp2 = cur.fetchall()

	sql3 = "Select * from quality_epv_checks where clock_num > '%s' and date1 > '%s' and date1 <= '%s' " % (cnum,date_start,date_end)
	cur.execute(sql3)
	tmp3 = cur.fetchall()

	a=[]
	for i in tmp2:
		ch = 0
		for ii in tmp3:
			a1 = i[1]
			b1 = ii[3]
			a2 = i[8]
			b2 = ii[5]
			a3 = i[3]
			b3 = ii[4]
			if i[1] == ii[3] and i[8] == ii[5]:
				ch = 1

				break

		if ch == 0:
			a.append(i)


	request.session['epv_toclean'] = a

	return render(request, "pie_clean.html")


def sup_pie_chart(request):
	# p = 'CNC Tech'
	# pp='99999'
	# c2 = 'Operator'
	# c3 = 'Once per shift'
	# c4 = 'Gauge Tech'
	# db, cur = db_set(request) 
	# sql = "SELECT COUNT(*) FROM quality_epv_week"
	# cur.execute(sql)
	# tmp = cur.fetchall()
	# tmp2=tmp[0][0]
	# sql = "SELECT date1 FROM quality_epv_week"
	# cur.execute(sql)
	# tmp = cur.fetchall()
	# tmp_date=tmp[0][0]

	# sql = "SELECT Count(*) FROM quality_epv_assets where Person <> '%s' and Person <> '%s' and Person <> '%s'" % (c2,c3,c4)
	# # sql = "SELECT Count(*) FROM quality_epv_assets where Person>'%s'" % (pp)
	# cur.execute(sql)
	# tmp = cur.fetchall()
	# tmp_reqd=tmp[0][0]

	# # pp = 99999
	# # sql = "SELECT Count(*) FROM quality_epv_checks where date1 >= '%s' and clock_num>'%s'" % (tmp_date,pp)
	# # cur.execute(sql)
	# # tmp = cur.fetchall()

	# # tmp_done=tmp[0][0]

	# # completed = int(tmp_done)
	# # incomplete = int(tmp_reqd) - int(tmp_done)

	# completed = int(tmp_reqd) - int(tmp2)
	# incomplete = int(tmp2)



	# sql = "SELECT * FROM quality_epv_week"
	# cur.execute(sql)
	# tmp = cur.fetchall()
	# request.session['epv_left'] = tmp
	# request.session['epv_reqd'] = incomplete
	# request.session['epv_comp'] = completed
	# END OLD CODE

	p = 'CNC Tech'
	pp = '99999'
	c2 = 'Operator'
	c3 = 'Once per shift'
	c4 = 'Gauge Tech'
	db, cur = db_set(request) 
	sql = "SELECT COUNT(*) FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2=tmp[0][0]


	sql = "SELECT date1 FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp_date=tmp[0][0]


	try:
		direction4 = request.session["direction5"]  # -1 is backwards +1 forward
	except:
		direction4 = 0
		request.session["direction5"] = 0


	
	# Take tmp_date and calculate 7 days prior and make it current_first
	ts = time.mktime(datetime.datetime.strptime(tmp_date,"%Y-%m-%d").timetuple())
	ts = ts - 86400 + (604800 * direction4)
	tm = time.localtime(ts)
	date_start = pie_chart_date(tm)


	ts = ts + 691200
	tm = time.localtime(ts)
	date_end = pie_chart_date(tm)

	request.session["EPV_Week"] = date_start
	cnum = '99999'
	# sql7 = "SELECT Count(*) FROM quality_epv_checks where clock_num >'%s' and date1 > '%s' and date1 < '%s' " % (pp,date_start,date_end)
	# sql7 = "SELECT Count(*) FROM quality_epv_checks where shift1 IS NULL and date1 > '%s' and date1 < '%s' " % (date_start,date_end)
	# cur.execute(sql7)
	# tmp7 = cur.fetchall()
	# tmp_cmplt = tmp7[0][0]
	# sql27 = "SELECT check1,description1,asset1 FROM quality_epv_checks where shift1 IS NULL and date1 > '%s' and date1 < '%s' " % (date_start,date_end)
	# cur.execute(sql27)
	# tmp27 = cur.fetchall()

	# Use this to count Completed EPVs in checks because sometimes duplicates get entered for some reason
	sql17 = "SELECT DISTINCT check1,description1,asset1 FROM quality_epv_checks where shift1 IS NULL and date1 > '%s' and date1 < '%s' " % (date_start,date_end)
	cur.execute(sql17)
	tmp17 = cur.fetchall()
	ctr = 0
	for j in tmp17:
		ctr = ctr + 1
	tmp_cmplt = ctr


	sql9 = "SELECT date1,shift1,check1,description1,asset1,master1,clock_num FROM quality_epv_checks where clock_num >'%s' and date1 > '%s' and date1 < '%s' " % (pp,date_start,date_end)
	cur.execute(sql9)
	tmp9 = cur.fetchall()
	request.session['test9'] = tmp9
	# return render(request, "test_2.html")


	
	sql7 = "SELECT Count(*) FROM quality_epv_week"
	cur.execute(sql7)
	tmp7 = cur.fetchall()
	tmp_week = tmp7[0][0]

	sql = "SELECT Count(*) FROM quality_epv_assets where Person <> '%s' and Person <> '%s' and Person <> '%s'" % (c2,c3,c4)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp_reqd=tmp[0][0]

	sql2 = "SELECT * FROM quality_epv_assets where Person <> '%s' and Person <> '%s' and Person <> '%s'" % (c2,c3,c4)
	# sql2 = "Select * from quality_epv_assets where Person>'%s'" % (pp)
	cur.execute(sql2)
	tmp2 = cur.fetchall()

	sql3 = "Select * from quality_epv_checks where clock_num > '%s' and date1 > '%s' and date1 <= '%s' " % (cnum,date_start,date_end)
	cur.execute(sql3)
	tmp3 = cur.fetchall()

	a=[]
	for i in tmp2:
		ch = 0
		for ii in tmp3:
			if i[1] == ii[3] and i[8] == ii[5]:
				ch = 1
				break
		if ch == 0:
			a.append(i)

	# tmp_reqd = int(tmp_week) + int(tmp_cmplt)
	completed = int(tmp_cmplt)
	incomplete = int(tmp_reqd) - int(tmp_cmplt)


	# pp = 99999
	# sql = "SELECT Count(*) FROM quality_epv_checks where date1 >= '%s' and clock_num>'%s'" % (tmp_date,pp)
	# cur.execute(sql)
	# tmp = cur.fetchall()

	# tmp_done=tmp[0][0]

	# completed = int(tmp_done)
	# incomplete = int(tmp_reqd) - int(tmp_done)


	

	# completed = int(tmp_reqd) - int(tmp2)
	# incomplete = int(tmp2)

	sql = "SELECT * FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()


	request.session['epv_left'] = a
	request.session['epv_reqd'] = incomplete
	request.session['epv_comp'] = completed


	
	return render(request, "sup_pie.html")

def quality_epv_asset_entry(request):

	if request.POST:
		asset = request.POST.get("asset")
		request.session["epv_asset2"] = asset
		asset = asset + ".0"
		
		db, cur = db_set(request)
		sql = "SELECT Id,date1,shift1,check1,description1,asset1,master1,comment,clock_num FROM quality_epv_checks where description1 = '%s' ORDER BY date1 DESC" % (asset)
		cur.execute(sql)
		tmp2 = cur.fetchall()
		request.session["asset_epv"] = tmp2


		return render(request,'quality_epv_asset_list.html')
		
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'quality_epv_asset_entry.html', {'args':args})

def gate_alarm_champion_initial(request,index):
	request.session['gate_alarm_index'] = index
	return gate_alarm_champion(request)

def gate_alarm_champion(request):
	try:
		request.session['gate_id_edit']
	except:
		request.session['gate_id_edit'] = 1
	index = request.session['gate_alarm_index']

	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_gate_alarm where Id = '%s'" % (index)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2=tmp[0]
	part = tmp2[1]
	operation = tmp2[2]
	category = tmp2[3]

	sql = "SELECT * FROM tkb_gate_alarm_log where part = '%s' and operation = '%s' and category = '%s' ORDER BY pdate DESC " % (part,operation,category)
	cur.execute(sql)
	tmp = cur.fetchall()  # List of all gate alarms in the log for the selected one

	request.session['gate_alarm_champion'] = tmp
	request.session['secondary_menu_color'] = '#131C02'
	request.session['secondary_text_color'] = '#F4F7E0'
	request.session['main_screen_color'] = '#DEDEDE'

	if request.POST:
		v=0
		value1 = request.POST.get("entry")

		value1=str(value1)
		value2,value3 = value1[1:],value1[:1]  # value2 is the index 
		value2 = int(value2)
		
		request.session['gate_id_edit'] = int(value2)
		if value3 == 'E':
			v=10
		elif value3 == 'U':
			v=20




		if v>0:
			sql = ('update tkb_gate_alarm_log SET reviewed="%s" WHERE Id ="%s"' % (v,value2))
			cur.execute(sql)
			db.commit()
			dummy=3
			request.session['gate_id_edit'] = int(value2)

		return render(request,'redirect_gate_alarm_champion.html')


	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'gate_alarm_champion.html', {'args':args})
