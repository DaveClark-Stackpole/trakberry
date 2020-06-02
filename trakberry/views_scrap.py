from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import maint_closeForm, maint_loginForm, maint_searchForm, tech_loginForm, sup_downForm
from views_db import db_open, db_set
from views_mod1 import find_current_date
from views_mod2 import seperate_string, create_new_table,generate_string
from views_email import e_test
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
from views_supervisor import supervisor_tech_call
from views_maintenance import login_password_check
from trakberry.views_testing import machine_list_display
from mod1 import hyphon_fix, multi_name_breakdown
import MySQLdb
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
import time
#import datetime as dt
from django.core.context_processors import csrf


def scrap_mgmt_manpower(request):
	db, cursor = db_set(request)
	dep = request.session['login_department']
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_logins(Id INT PRIMARY KEY AUTO_INCREMENT,user_name CHAR(50), password CHAR(50), department CHAR(50), active1 INT(10) default 0)""")
	db.commit()
	sql = "SELECT * FROM tkb_logins WHERE department = '%s' ORDER BY user_name ASC" %(dep)  # Select only those in the department  (dep)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = list(tmp)
	db.close()
	request.session["scrap_mgmt_manpower"] = tmp
	return 

# Login for Maintenance Manager App
def scrap_mgmt_login_form(request):
	
	request.session["login_department"] = 'Quality Manager'
	scrap_mgmt_manpower(request)
	request.session["scrap_mgmt_login_name"] = ""
	request.session["scrap_mgmt_login_password"] = ""
	request.session["scrap_mgmt_login_password_check"] = 'False'
	request.session["scrap_mgmt_main_switch"] = 0



#	if request.POST:
	if 'button1' in request.POST:

		request.session["login_name"] = request.POST.get("login_name")
		request.session["login_password"] = request.POST.get("login_password")
		request.session["login_password_check"] = ''
		login_password_check(request)
		check = request.session["login_password_check"]
		#request.session["scrap_mgmt_login_password_check"]


		# if len(login_name) < 5:
		# 	login_password = 'wrong'
		if check != 'false':
			request.session["scrap_mgmt_login_name"] = request.session["login_name"]
			request.session["scrap_mgmt_login_password"] = request.session["login_password"]
			request.session["scrap_mgmt_login_password_check"] = 'True'
		else:
			request.session["scrap_mgmt_login_password_check"] = 'False'

		ch2 = request.session["scrap_mgmt_login_password_check"]
		request.session["wildcard1"] = 1

		return render(request,'redirect_scrap_mgmt.html')  # Need to bounce out to an html and redirect back into a module otherwise infinite loop


	elif 'button2' in request.POST:
		request.session["password_lost_route1"] = "scrap_mgmt.html"
		return render(request,'login/reroute_lost_password.html')

	else:
		form = tech_loginForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["scrap_mgmt_login_name"] = ""
	request.session["scrap_mgmt_login_password"] = ""



	return render(request,'scrap_mgmt_login_form.html', {'args':args})

def scrap_mgmt(request):
	request.session["main_screen_color"] = "#849185"  # Color of Background in APP
	request.session["main_menu_color"] = "#d3ded4"    # Color of Menu Bar in APP
	return render(request, "scrap_mgmt.html")

def scrap_display(request):
	db, cur = db_set(request)
	sql_scrap = "SELECT * FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day);"
	cur.execute(sql_scrap)
	request.session["tmp_scrap"] = cur.fetchall()

	return render(request, "scrap_mgmt24.html")

