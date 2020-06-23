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
	sql_scrap = "SELECT FORMAT(sum(scrap_amount),0),scrap_part,FORMAT(sum(total_cost),2) FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) group by scrap_part ORDER BY sum(total_cost) DESC"
	# sql_scrap = "SELECT * FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day);"
	cur.execute(sql_scrap)
	request.session["tmp_scrap"] = cur.fetchall()
	return render(request, "scrap_mgmt24.html")

def scrap_edit_selection(request):
	ptr = request.session["scrap_ptr"]
	db, cur = db_set(request)

	if ptr == 0:
		sql_max_ptr = "SELECT max(Id) FROM tkb_scrap"
		cur.execute(sql_max_ptr)
		ptr = cur.fetchall()
		ptr = ptr[0][0] + 1
	
	sql_scrap_entries = "SELECT * FROM tkb_scrap where Id < '%s' order by Id DESC limit 10" % (ptr)
	cur.execute(sql_scrap_entries)
	request.session["tmp_scrap_entries"] = cur.fetchall()

	sql_scrap_entries_last = "SELECT min(Id) FROM (select ID from tkb_scrap where Id < '%s' order by Id DESC limit 10) as selectmin" % (ptr)
	cur.execute(sql_scrap_entries_last)
	last = cur.fetchall()
	last = last[0][0]
	request.session["scrap_ptr"] = last

	sql_scrap_entries_first = "SELECT max(Id) FROM (select ID from tkb_scrap where Id < '%s' order by Id DESC limit 10) as selectmin" % (ptr)
	cur.execute(sql_scrap_entries_first)
	first = cur.fetchall()
	first = first[0][0]
	request.session["scrap_ptr_first"] = first
	db.close()
	return

def scrap_entries_next(request):
	scrap_edit_selection(request)
	return render(request, "scrap_entries.html")

def scrap_entries(request):
	request.session["scrap_partno_filter"] = ""
	request.session["scrap_date_filter"] = ""
	request.session["scrap_line_filter"] = ""
	request.session["scrap_operation_filter"] = ""
	request.session["scrap_category_filter"] = ""
	request.session["scrap_ptr"] = 0


	scrap_edit_selection(request)
	# request.session["scrap_ptr"] = 6

	# ptr = request.session["scrap_ptr"]
	# db, cur = db_set(request)
	# sql_scrap_entries = "SELECT * FROM tkb_scrap where Id < '%s' order by Id DESC limit 3" % (ptr)
	# cur.execute(sql_scrap_entries)
	# request.session["tmp_scrap_entries"] = cur.fetchall()
	# se = request.session["tmp_scrap_entries"]


	# sql_scrap_entries_first = "SELECT max(Id) FROM (select Id from tkb_scrap order by Id DESC limit 3) as selectmax"
	# cur.execute(sql_scrap_entries_first)
	# first = cur.fetchall()
	# first = first[0][0]
	# sql_scrap_entries_last = "SELECT min(Id) FROM (select ID from tkb_scrap where Id < '%s' order by Id DESC limit 3) as selectmin" % (ptr)
	# cur.execute(sql_scrap_entries_last)
	# last = cur.fetchall()
	# last = last[0][0]

	return render(request, "scrap_entries.html")

def scrap_display_operation(request,index):
	request.session["scrap_24hrs_part"]=index
	db, cur = db_set(request)
	sql_scrap1 = "SELECT FORMAT(sum(scrap_amount),0),scrap_operation, scrap_part,FORMAT(sum(total_cost),2) FROM tkb_scrap  WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) AND scrap_part = '%s' group by scrap_operation ORDER BY sum(total_cost) DESC" % (index)
	cur.execute(sql_scrap1)
	request.session["tmp_scrap"] = cur.fetchall()
	tt = request.session["tmp_scrap"]
	return render(request, "scrap_mgmt_operation.html")

def scrap_display_category(request,index):
	index_check = index[-1:]
	index_len = len(index) - 1
	if index_check == '/': # bit of a bug when Sinter is used it adds a / to name
		index = index[:index_len]
	request.session["scrap_24hrs_operation"] = index
	index_part = request.session["scrap_24hrs_part"]

	db, cur = db_set(request)
	index.replace(" ","")
	sql_scrap2 = "SELECT FORMAT(sum(scrap_amount),0),scrap_category, scrap_operation,FORMAT(sum(total_cost),2) FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) AND scrap_operation = '%s' AND scrap_part = '%s' group by scrap_category ORDER BY sum(total_cost) DESC" % (index,index_part)
	cur.execute(sql_scrap2)
	request.session["tmp_scrap2"] = cur.fetchall()
	return render(request, "scrap_mgmt_category.html")	

def scrap_display_category_shift(request,index):
	request.session["scrap_24hrs_category"] = index
	index_part = request.session["scrap_24hrs_part"]
	index_operation = request.session["scrap_24hrs_operation"]
	index_category = index
	db, cur = db_set(request)
	index.replace(" ","")
	#DATE_FORMAT(date, "%M %d %Y") 
	sql_scrap2 = "SELECT scrap_amount,scrap_category, scrap_operation,FORMAT(total_cost,2),date FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) AND scrap_operation = '%s' AND scrap_category = '%s' AND scrap_part = '%s' ORDER BY scrap_amount DESC" % (index_operation,index_category,index_part)
	cur.execute(sql_scrap2)
	request.session["tmp_scrap2"] = cur.fetchall()
	tmp_scrap2 = request.session["tmp_scrap2"]
	return render(request, "scrap_mgmt_category_shift.html")	
