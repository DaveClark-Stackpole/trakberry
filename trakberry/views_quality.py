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


def pie_chart(request):
	p = 'CNC Tech'
	db, cur = db_set(request) 
	sql = "SELECT COUNT(*) FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2=tmp[0][0]
	sql = "SELECT date1 FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp_date=tmp[0][0]

	sql = "SELECT Count(*) FROM quality_epv_assets where Person='%s'" % (p)
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

	# tt=5/0

	sql = "SELECT * FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	request.session['epv_left'] = tmp
	request.session['epv_reqd'] = incomplete
	request.session['epv_comp'] = completed


	return render(request, "pie.html")

def sup_pie_chart(request):
	p = 'CNC Tech'
	db, cur = db_set(request) 
	sql = "SELECT COUNT(*) FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2=tmp[0][0]
	sql = "SELECT date1 FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp_date=tmp[0][0]

	sql = "SELECT Count(*) FROM quality_epv_assets where Person='%s'" % (p)
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

	# tt=5/0

	sql = "SELECT * FROM quality_epv_week"
	cur.execute(sql)
	tmp = cur.fetchall()
	request.session['epv_left'] = tmp
	request.session['epv_reqd'] = incomplete
	request.session['epv_comp'] = completed


	return render(request, "sup_pie.html")