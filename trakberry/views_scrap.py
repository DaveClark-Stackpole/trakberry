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
	sql_scrap = "SELECT FORMAT(sum(scrap_amount),0),scrap_part,date FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) group by scrap_part"
	# sql_scrap = "SELECT * FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day);"
	cur.execute(sql_scrap)
	request.session["tmp_scrap"] = cur.fetchall()

	return render(request, "scrap_mgmt24.html")

def scrap_entries(request):
	
	db, cur = db_set(request)
	sql_scrap_entries = "SELECT * FROM tkb_scrap group by scrap_part"
	# sql_scrap = "SELECT * FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day);"
	cur.execute(sql_scrap_entries)
	request.session["tmp_scrap_entries"] = cur.fetchall()

	return render(request, "scrap_entries.html")


def scrap_display_operation(request,index):
	db, cur = db_set(request)


	sql_scrap1 = "SELECT FORMAT(sum(scrap_amount),0),scrap_operation, scrap_part, date FROM tkb_scrap  WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) AND scrap_part = '%s' group by scrap_operation" % (index)

	# *********************  COMMENTS
	# Need to filter out the sql_scrap1 so it's only pulling the correct part number.    
	# like select format .......   by scrap_operation where scrap_part = .......
	# otherwise it just shows total of all operations.
	# ***********************************************
	


	# sql_scrap = "SELECT * FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day);"
	cur.execute(sql_scrap1)
	request.session["tmp_scrap"] = cur.fetchall()
	return render(request, "scrap_mgmt_operation.html")

def scrap_display_category(request,index):	
	db, cur = db_set(request)


	sql_scrap2 = "SELECT FORMAT(sum(scrap_amount),0),scrap_category, scrap_operation, date FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) AND scrap_operation = '%s' group by scrap_category" % (index)

	# *********************  COMMENTS
	# Need to filter out the sql_scrap1 so it's only pulling the correct part number.    
	# like select format .......   by scrap_operation where scrap_part = .......
	# otherwise it just shows total of all operations.
	# ***********************************************
	


	# sql_scrap = "SELECT * FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day);"
	cur.execute(sql_scrap2)
	request.session["tmp_scrap2"] = cur.fetchall()
	return render(request, "scrap_mgmt_category.html")	

# def scrap_display_o(request):

# 	t=7/0

# 	# request.session["table_headers"]  ==>  The name displayed on page 
# 	# request.session["table_variables"] ==> The name in the DB 
# 	p = ['' for y in range(0)]
# 	v = ['' for y in range(0)]
# 	datecheck = ['' for y in range(0)]
# 	a1 = ['' for y in range(0)]

# 	# call in to tmp the row to edit
# 	update_list = ''
# 	ctr = 0
# 	tmp_part = partno
# 	db, cur = db_set(request) 
# 	sq1 = request.session["scrap_table_call"] + "  where id = '%s'" %(tmp_part)
# 	cur.execute(sq1)
# 	tmp = cur.fetchall()
# 	tmp2 = tmp[0]

# ## tried a whole bunch of stuff. couldn't figure what shall go where. referred to multiple kisok,management
# ##  and scrap files too. let me know what you think and how to fix this.
	
	
# 	if request.POST:
# 		db, cur = db_set(request)
# 		sql_scrap1 = "SELECT FORMAT(sum(scrap_amount),0),scrap_operation FROM tkb_scrap group by scrap_operation"
# 		# sql_scrap = "SELECT * FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day);"
# 		cur.execute(sql_scrap1)
# 		request.session["tmp_scrap"] = cur.fetchall()

# 	return render(request, "scrap_mgmt24.html")
