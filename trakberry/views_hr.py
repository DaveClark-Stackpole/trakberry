from multiprocessing import dummy
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,login_Form
from trakberry.forms import maint_closeForm, maint_loginForm, maint_searchForm, tech_loginForm, sup_downForm
from trakberry.views import done
from views2 import main_login_form
from mod1 import hyphon_fix
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
from views_maintenance import login_password_check
import datetime
# from datetime import datetime 
from time import strftime
import time

def hr(request):
	request.session["main_screen_color"] = "#e4ddf4"  # Color of Background in APP
	request.session["main_menu_color"] = "#fffbf0"    # Color of Menu Bar in APP
	request.session["secondary_menu_color"] = "#943d24"    # Color of Menu Bar in APP
	request.session["secondary_text_color"] = "#e4ddf4"    # Color of Menu Bar in APP
	request.session["app"] = "hr"    # Color of Menu Bar in APP

	return render(request, "hr.html")

def hr_login_form(request):
	request.session["login_department"] = request.session['app']
	h = request.session['app']
	users1(request) 
	request.session["hr_login_name"] = ""
	request.session["hr_login_password"] = ""
	request.session["hr_login_password_check"] = 'False'
	request.session["hr_main_switch"] = 0
	if 'button1' in request.POST:
		request.session["login_name"] = request.POST.get("login_name")
		request.session["login_password"] = request.POST.get("login_password")
		request.session["login_password_check"] = ''
		login_password_check(request)
		check = request.session["login_password_check"]


		if check != 'false':
			request.session["hr_login_name"] = request.session["login_name"]
			request.session["hr_login_password"] = request.session["login_password"]
			request.session["hr_login_password_check"] = 'True'
		else:
			request.session["hr_login_password_check"] = 'False'
		ch2 = request.session["hr_login_password_check"]
		
		return render(request,'redirect_hr.html')  # Need to bounce out to an html and redirect back into a module otherwise infinite loop
	elif 'button2' in request.POST:
		request.session["login_name"] = request.POST.get("login_name")
		request.session["password_lost_route1"] = "hr.html"
		return render(request,'login/reroute_lost_password.html')
	else:
		form = tech_loginForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["hr_login_name"] = ""
	request.session["hr_login_password"] = ""
	return render(request,'hr_login_form.html', {'args':args})

def users1(request):
	db, cursor = db_set(request)
	dep = str(request.session['login_department'])
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_logins(Id INT PRIMARY KEY AUTO_INCREMENT,user_name CHAR(50), password CHAR(50), department CHAR(50), active1 INT(10) default 0)""")
	db.commit()
	sql = "SELECT * FROM tkb_logins WHERE department = '%s' ORDER BY user_name ASC" %(dep)  # Select only those in the department  (dep)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = list(tmp)
	db.close()
	request.session["users1"] = tmp
	return 

def hr_down(request):	

	request.session['asset_down'] = 'Yes_Down'

	if request.POST:

		machinenum = request.POST.get("machine")
		problem = request.POST.get("reason")
		priority = request.POST.get("priority")
		priority = 1
		whoisonit = request.session["whoisonit"]
		
		# take comment into tx and ensure no "" exist.  If they do change them to ''
		tx = problem
		tx = ' ' + tx
		tps = list(tx)
	
			
		# Genius appostrophe fix
		problem = hyphon_fix(tx)

		# Add name of person entering job to description
		try:
			nm = request.session['login_name']
		except:
			nm=''
		if len(nm)<2:
			nm = request.session['login_tech']
		problem = problem + ' (entered by '+nm+')'
		# ***********************************************

		
		# call external function to produce datetime.datetime.now()
		t = vacation_temp()
		
		db, cur = db_set(request)

		asset_test = machinenum[:4]

		side1 = '0'
		location1='G'
		side2 = '0'
		try:
			asset3 = machinenum[:4]
			asset2 = machinenum[:3]
			try:
				int(asset3)
				asset4 = asset3
			except:
				asset4 = asset2
			aql = "SELECT * FROM vw_asset_eam_lp where left(Asset,4) = '%s'" %(asset4)
			# aql = "SELECT * FROM vw_asset_eam_lp WHERE Asset LIKE '%s'" % ("%" + asset4 + "%")
			cur.execute(aql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			asset5 = tmp3[1] + " - " + tmp3[3]
			location1 = tmp3[3]
		except:
			asset5 = machinenum

		priority = 0
		down7 = 'Yes_Down'
			
		
# This will determine side of asset and put in breakdown
		location_check = location1[:1]
		if location_check < 'G':
			side1 = '2'
		elif location_check > 'G':
			side1 = '1'
		else:
			side1 = '0'
	

		cur.execute('''INSERT INTO pr_downtime1(machinenum,problem,priority,whoisonit,called4helptime,side,down,changeovertime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''', (asset5,problem,priority,whoisonit,t,side1,down7,t))
		db.commit()
		db.close()

		# prioritize(request)
		return render(request,'redirect_hr.html')
		
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form


	
	# Old Method
	rlist = machine_list_display()
	
	return render(request,'hr_down.html', {'List':rlist,'args':args})
