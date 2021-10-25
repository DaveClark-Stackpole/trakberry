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
	sql7 = "SELECT Count(*) FROM quality_epv_checks where clock_num >'%s' and date1 > '%s' and date1 < '%s' " % (pp,date_start,date_end)
	cur.execute(sql7)
	tmp7 = cur.fetchall()
	tmp_cmplt = tmp7[0][0]
	
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

	return render(request, "pie.html")

def sup_pie_chart(request):
	p = 'CNC Tech'
	pp='99999'
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

	sql = "SELECT Count(*) FROM quality_epv_assets where Person <> '%s' and Person <> '%s' and Person <> '%s'" % (c2,c3,c4)
	# sql = "SELECT Count(*) FROM quality_epv_assets where Person>'%s'" % (pp)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp_reqd=tmp[0][0]

	# pp = 99999
	# sql = "SELECT Count(*) FROM quality_epv_checks where date1 >= '%s' and clock_num>'%s'" % (tmp_date,pp)
	# cur.execute(sql)
	# tmp = cur.fetchall()

	# tmp_done=tmp[0][0]

	# completed = int(tmp_done)
	# incomplete = int(tmp_reqd) - int(tmp_done)

	completed = int(tmp_reqd) - int(tmp2)
	incomplete = int(tmp2)



	sql = "SELECT * FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	request.session['epv_left'] = tmp
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
