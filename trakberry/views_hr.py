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
	request.session["app"] = "HR"    # Color of Menu Bar in APP

	return render(request, "hr.html")

def hr_login_form(request):
	
	request.session["login_department"] = 'HR'
	hr_manpower(request) 
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
		request.session["wildcard1"] = 1
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

def hr_manpower(request):
	db, cursor = db_set(request)
	dep = request.session['login_department']
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_logins(Id INT PRIMARY KEY AUTO_INCREMENT,user_name CHAR(50), password CHAR(50), department CHAR(50), active1 INT(10) default 0)""")
	db.commit()
	sql = "SELECT * FROM tkb_logins WHERE department = '%s' ORDER BY user_name ASC" %(dep)  # Select only those in the department  (dep)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = list(tmp)
	db.close()
	request.session["hr_manpower"] = tmp
	return 