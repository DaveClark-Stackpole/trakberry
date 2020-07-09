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
#import datetime as dt
from django.core.context_processors import csrf
import math


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


def scrap_display_24hr(request):
	request.session["scrap_display_type"] = "24hr" 
	return render(request, "redirect_scrap_display.html")

def scrap_display(request):
	db, cur = db_set(request)
	if request.session["scrap_display_type"] == "24hr":
		sql_scrap = "SELECT FORMAT(sum(scrap_amount),0),scrap_part,FORMAT(sum(total_cost),2) FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) group by scrap_part ORDER BY sum(total_cost) DESC"
	else:
		date1 = request.session["scrap_display_date1"]
		date2 = request.session["scrap_display_date2"]
		sql_scrap = "SELECT FORMAT(sum(scrap_amount),0),scrap_part,FORMAT(sum(total_cost),2) FROM tkb_scrap WHERE date BETWEEN '%s' AND '%s' group by scrap_part ORDER BY sum(total_cost) DESC" % (date1,date2)
	# sql_scrap = "SELECT * FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day);"
	cur.execute(sql_scrap)
	request.session["tmp_scrap"] = cur.fetchall()
	return render(request, "scrap_mgmt24.html")

def scrap_edit_selection(request):
	ptr = request.session["scrap_ptr"]
	ptr_first = request.session["scrap_ptr_first"]
	ptr_direction = request.session["scrap_entries_direction"]
	# ptr_direction = "up"
	# ptr_first = 2

	db, cur = db_set(request)

	if ptr == 0:
		sql_max_ptr = "SELECT max(Id) FROM tkb_scrap"
		cur.execute(sql_max_ptr)
		ptr = cur.fetchall()
		ptr = ptr[0][0] + 1
	
	if ptr_direction == "down":
		# request.session["scrap_ptr_first"] = ptr
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


		# t=5/0
	else:
		
		sql_scrap_entries_first = "SELECT max(Id) FROM (select ID from tkb_scrap where Id > '%s' order by Id ASC limit 10) as selectmin" % (ptr_first)
		cur.execute(sql_scrap_entries_first)
		first = cur.fetchall()
		first = first[0][0]
		request.session["scrap_ptr_first"] = first 

		sql_scrap_entries = "SELECT * FROM tkb_scrap where Id <= '%s' order by Id DESC limit 10" % (first)
		cur.execute(sql_scrap_entries)
		request.session["tmp_scrap_entries"] = cur.fetchall()

		sql_scrap_entries_last = "SELECT min(Id) FROM (select ID from tkb_scrap where Id > '%s' order by Id ASC limit 10) as selectmin" % (ptr_first)
		cur.execute(sql_scrap_entries_last)
		last = cur.fetchall()
		last = last[0][0]
		request.session["scrap_ptr"] = last

	
		

		

	db.close()
	return

# def scrap_edit_prev_selection2(request):
# 	ptr = request.session["scrap_ptr"]
# 	db, cur = db_set(request)

# 	if ptr == 0:
# 		sql_max_ptr = "SELECT max(Id) FROM tkb_scrap"
# 		cur.execute(sql_max_ptr)
# 		ptr = cur.fetchall()
# 		ptr = ptr[0][0] + 1
	
# 	sql_scrap_entries = "SELECT * FROM tkb_scrap where Id < '%s' order by Id DESC limit 10" % (ptr)
# 	cur.execute(sql_scrap_entries)
# 	request.session["tmp_scrap_entries"] = cur.fetchall()

# 	sql_scrap_entries_last = "SELECT min(Id) FROM (select ID from tkb_scrap where Id < '%s' order by Id DESC limit 10) as selectmin" % (ptr)
# 	cur.execute(sql_scrap_entries_last)
# 	last = cur.fetchall()
# 	last = last[0][0]
# 	request.session["scrap_ptr"] = last

# 	sql_scrap_entries_first = "SELECT max(Id) FROM (select ID from tkb_scrap where Id < '%s' order by Id DESC limit 10) as selectmin" % (ptr)
# 	cur.execute(sql_scrap_entries_first)
# 	first = cur.fetchall()
# 	first = first[0][0]
# 	request.session["scrap_ptr_first"] = first
# 	db.close()
# 	return



def scrap_entries_next(request):
	request.session["scrap_entries_direction"] = "down"
	scrap_edit_selection(request)
	request.session["scrap_prev"] += 1
	request.session["scrap_next"] -= 1
	return render(request, "scrap_entries.html")

def scrap_entries_prev(request):
	request.session["scrap_entries_direction"] = "up"
	scrap_edit_selection(request)
	request.session["scrap_prev"] -= 1
	request.session["scrap_next"] += 1
	return render(request, "scrap_entries.html")

def scrap_entries(request):
	request.session["scrap_entries_direction"] = "down"
	request.session["scrap_partno_filter"] = ""
	request.session["scrap_date_filter"] = ""
	request.session["scrap_line_filter"] = ""
	request.session["scrap_operation_filter"] = ""
	request.session["scrap_category_filter"] = ""
	request.session["scrap_ptr"] = 0
	request.session["scrap_ptr_first"] = 0
	
	db, cur = db_set(request)
	row_count = "SELECT COUNT(*) FROM tkb_scrap" ## checking number of rows we have
	execu = cur.execute(row_count) #executing
	maximize = cur.fetchall() ## fetch
	maximize = maximize[0][0]	## converting to integer
	db.close()

	num_entries =  maximize / float(10) 
	x = math.ceil(num_entries)

	
	
	request.session["scrap_prev"] = 0
	request.session["scrap_next"] = x-1




 

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
	if request.session["scrap_display_type"] == "24hr":
		sql_scrap1 = "SELECT FORMAT(sum(scrap_amount),0),scrap_operation, scrap_part,FORMAT(sum(total_cost),2) FROM tkb_scrap  WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) AND scrap_part = '%s' group by scrap_operation ORDER BY sum(total_cost) DESC" % (index)
	else:
		date1 = request.session["scrap_display_date1"]
		date2 = request.session["scrap_display_date2"]
		sql_scrap1 = "SELECT FORMAT(sum(scrap_amount),0),scrap_operation, scrap_part,FORMAT(sum(total_cost),2) FROM tkb_scrap  WHERE date BETWEEN '%s' AND '%s' AND scrap_part = '%s' group by scrap_operation ORDER BY sum(total_cost) DESC" % (date1,date2,index)
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
	if request.session["scrap_display_type"] == "24hr":
		sql_scrap2 = "SELECT FORMAT(sum(scrap_amount),0),scrap_category, scrap_operation,FORMAT(sum(total_cost),2) FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) AND scrap_operation = '%s' AND scrap_part = '%s' group by scrap_category ORDER BY sum(total_cost) DESC" % (index,index_part)
	else:
		date1 = request.session["scrap_display_date1"]
		date2 = request.session["scrap_display_date2"]
		sql_scrap2 = "SELECT FORMAT(sum(scrap_amount),0),scrap_category, scrap_operation,FORMAT(sum(total_cost),2) FROM tkb_scrap WHERE date BETWEEN '%s' AND '%s'  AND scrap_operation = '%s' AND scrap_part = '%s' group by scrap_category ORDER BY sum(total_cost) DESC" % (date1,date2,index,index_part)
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
	if request.session["scrap_display_type"] == "24hr":
		sql_scrap2 = "SELECT scrap_amount,scrap_category, scrap_operation,FORMAT(total_cost,2),date FROM tkb_scrap WHERE date BETWEEN date_sub(now(), interval 1 day) AND date_add(now(), interval 1 day) AND scrap_operation = '%s' AND scrap_category = '%s' AND scrap_part = '%s' ORDER BY scrap_amount DESC" % (index_operation,index_category,index_part)
	else:
		date1 = request.session["scrap_display_date1"]
		date2 = request.session["scrap_display_date2"]
		sql_scrap2 = "SELECT scrap_amount,scrap_category, scrap_operation,FORMAT(total_cost,2),date FROM tkb_scrap WHERE date BETWEEN '%s' AND '%s' AND scrap_operation = '%s' AND scrap_category = '%s' AND scrap_part = '%s' ORDER BY scrap_amount DESC" % (date1, date2, index_operation,index_category,index_part)		
	cur.execute(sql_scrap2)
	request.session["tmp_scrap2"] = cur.fetchall()
	tmp_scrap2 = request.session["tmp_scrap2"]
	return render(request, "scrap_mgmt_category_shift.html")	

def scrap_entries_update(request,index):
	db, cur = db_set(request)
	index.replace(" ","")
	sql = "SELECT * FROM tkb_scrap where Id = '%s'" % (index) 
	cur.execute(sql)
	request.session["tmp_scrap3"] = cur.fetchall()
	db.close()
	tmp_scrap3 = request.session["tmp_scrap3"]
	if request.POST:
		scrap_part = request.POST.get("scrap_part")
		scrap_operation = request.POST.get("scrap_operation")
		scrap_category = request.POST.get("scrap_category")
		scrap_amount = request.POST.get("scrap_amount")
		scrap_line = request.POST.get("scrap_line")
		total_cost = request.POST.get("total_cost")
		date = request.POST.get("date")
		db, cur = db_set(request)
		# Calculate new cost but if error (changed operation) keep cost same
		try:
			sql2 = "SELECT Dept FROM scrap_operation_dept WHERE Operation = '%s'" % (scrap_operation)
			cur.execute(sql2)
			tmp = cur.fetchall()
			department = tmp[0][0]
			sql3 = "SELECT Cost FROM scrap_part_dept_cost WHERE Part = '%s' and Dept = '%s'" % (scrap_part,department)
			cur.execute(sql3)
			tmp = cur.fetchall()
			cost = tmp[0][0]
			total_cost = float(cost) * float(scrap_amount)
		except:
			dummy = 1
		cql = ('update tkb_scrap SET scrap_part = "%s",scrap_operation="%s",scrap_amount="%s", scrap_line="%s", total_cost="%s", date="%s" WHERE id ="%s"' % (scrap_part, scrap_operation, scrap_amount, scrap_line, total_cost, date, index))
		cur.execute(cql)
		db.commit()
		db.close()
		return render(request, "scrap_mgmt.html")
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'scrap_display_edit_entries.html',{'args':args})

def scrap_display_date_pick(request):
	# t = datetime.datetime.now()
	date = vacation_set_current9()
	request.session["date1_default"] =  date
	# request.session["date2_default"] = t
	if request.POST:
		request.session["scrap_display_date1"] = request.POST.get("scrap_display_date1")
		request.session["scrap_display_date2"] = request.POST.get("scrap_display_date2")
		request.session["scrap_display_type"] = "date_selection"
		return render(request, "redirect_scrap_display.html")

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'scrap_display_date_pick_form.html',{'args':args})


def operation_department(request):
	request.session["operation_entries_direction"] = "down"
	request.session["operation_filter"] = ""
	request.session["operation_dept_filter"] = ""
	request.session["oper_dept_ptr"] = 0
	request.session["oper_dept_ptr_first"] = 0
	
	db, cur = db_set(request)
	row_count = "SELECT COUNT(*) FROM scrap_operation_dept" ## checking number of rows we have
	execu = cur.execute(row_count) #executing
	maximize = cur.fetchall() ## fetch
	maximize = maximize[0][0]	## converting to integer
	db.close()

	num_entries =  maximize / float(10) 
	x = math.ceil(num_entries)
	

	
	
	request.session["oper_prev"] = 0
	request.session["oper_next"] = x-1




 

	oper_dept_edit_selection(request)

	return render(request, "scrap_operation_dept.html")		

def oper_dept_edit_selection(request):
	ptr = request.session["oper_dept_ptr"]
	ptr_first = request.session["oper_dept_ptr_first"]
	ptr_direction = request.session["operation_entries_direction"]
	# ptr_direction = "up"
	# ptr_first = 2

	db, cur = db_set(request)

	if ptr == 0:
		sql_max_ptr = "SELECT max(Id) FROM scrap_operation_dept"
		cur.execute(sql_max_ptr)
		ptr = cur.fetchall()
		ptr = ptr[0][0] + 1
	
	if ptr_direction == "down":
		# request.session["scrap_ptr_first"] = ptr
		sql_scrap_entries = "SELECT * FROM scrap_operation_dept where Id < '%s' order by Id DESC limit 10" % (ptr)
		cur.execute(sql_scrap_entries)
		request.session["tmp_oper_dept_entries"] = cur.fetchall()

		sql_scrap_entries_last = "SELECT min(Id) FROM (select ID from scrap_operation_dept where Id < '%s' order by Id DESC limit 10) as selectmin" % (ptr)
		cur.execute(sql_scrap_entries_last)
		last = cur.fetchall()
		last = last[0][0]
		request.session["oper_dept_ptr"] = last

		sql_scrap_entries_first = "SELECT max(Id) FROM (select ID from scrap_operation_dept where Id < '%s' order by Id DESC limit 10) as selectmin" % (ptr)
		cur.execute(sql_scrap_entries_first)
		first = cur.fetchall()
		first = first[0][0]
		request.session["oper_dept_ptr_first"] = first


		# t=5/0
	else:
		
		sql_scrap_entries_first = "SELECT max(Id) FROM (select ID from scrap_operation_dept where Id > '%s' order by Id ASC limit 10) as selectmin" % (ptr_first)
		cur.execute(sql_scrap_entries_first)
		first = cur.fetchall()
		first = first[0][0]
		request.session["oper_dept_ptr_first"] = first 

		sql_scrap_entries = "SELECT * FROM scrap_operation_dept where Id <= '%s' order by Id DESC limit 10" % (first)
		cur.execute(sql_scrap_entries)
		request.session["tmp_oper_dept_entries"] = cur.fetchall()

		sql_scrap_entries_last = "SELECT min(Id) FROM (select ID from scrap_operation_dept where Id > '%s' order by Id ASC limit 10) as selectmin" % (ptr_first)
		cur.execute(sql_scrap_entries_last)
		last = cur.fetchall()
		last = last[0][0]
		request.session["oper_dept_ptr"] = last

	
		

		

	db.close()
	return

def operation_entries_next(request):
	request.session["oper_dept_entries_direction"] = "down"
	oper_dept_edit_selection(request)
	request.session["oper_prev"] += 1
	request.session["oper_next"] -= 1
	return render(request, "scrap_operation_dept.html")

def operation_entries_prev(request):
	request.session["oper_dept_entries_direction"] = "up"
	oper_dept_edit_selection(request)
	request.session["oper_prev"] -= 1
	request.session["oper_next"] += 1
	return render(request, "scrap_operation_dept.html")



def operation_entries_update(request,index):
	db, cur = db_set(request)
	index.replace(" ","")
	sql = "SELECT * FROM scrap_operation_dept where Id = '%s'" % (index) 
	cur.execute(sql)
	request.session["tmp_scrap4"] = cur.fetchall()
	db.close()
	tmp_scrap4 = request.session["tmp_scrap4"]
	if request.POST:
		operation = request.POST.get("Operation")
		department = request.POST.get("Dept")
		db, cur = db_set(request)

		cql = ('update scrap_operation_dept SET Operation = "%s",Dept="%s" WHERE id ="%s"' % (operation, department, index))
		cur.execute(cql)
		db.commit()
		db.close()
		return render(request, "scrap_mgmt.html")
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'scrap_display_edit_operation_entries.html',{'args':args})

 
def kiosk_initiate(request):
	request.session["scrap_entry"] = 0
	request.session["scrap_part"] = "Part Num:"
	request.session["scrap_operation"] = "Operation:"
	request.session["scrap_category"] = "Category:"
	request.session["scrap_part"] = "Part No:"
	request.session["scrap_amount"] = 0
	request.session["scrap1"] =""
	request.session["scrap2"] ='''disabled="true"'''
	request.session["scrap3"] ='''disabled="true"'''
	request.session["scrap4"] ='''disabled="true"'''
	return render(request,'scrap_edits.html')

# def category_update(request,index):
# 	db, cur = db_set(request)
# 	index.replace(" ","")
# 	sql = "SELECT * FROM scrap_line_operation_category where Id = '%s'" % (index) 
# 	cur.execute(sql)
# 	request.session["tmp_scrap6"] = cur.fetchall()
# 	db.close()
# 	tmp_scrap4 = request.session["tmp_scrap6"]
# 	if request.POST:
# 		scrap_part = request.POST.get("scrap_part")
# 		scrap_operation = request.POST.get("scrap_operation")
# 		db, cur = db_set(request)

# 		cql = ('update scrap_operation_dept SET scrap_part = "%s",scrap_operation="%s" WHERE id ="%s"' % (scrap_part, scrap_operation, index))
# 		cur.execute(cql)
# 		db.commit()
# 		db.close()
# 		return render(request, "scrap_mgmt.html")
# 	else:
# 		form = sup_downForm()
# 	args = {}
# 	args.update(csrf(request))
# 	args['form'] = form
# 	return render(request,'scrap_display_edit_operation_entries.html',{'args':args})

def kiosk_add_category(request):


	# e = 4/0
	db, cursor = db_set(request)
	# index.replace(" ","")

	# sql_11 = "SELECT * FROM scrap_line_operation_category where Id = '%s'" % (index) 
	# cursor.execute(sql_11)
 	# request.session["tmp_scrap6"] = cursor.fetchall()

 	# tmp_scrap4 = request.session["tmp_scrap6"]
	# This will assign all the values of machines into session variable machine_temp
	if request.session["scrap_entry"] == 0:
		active = '1.0'
		sql = "SELECT Part FROM scrap_part_line WHERE Active = '%s'" %(active)
		##sql = "update scrap_part_line SET Part ='%s' WHERE Active = '%s'" %(active)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		request.session["scrap_part_selection"] = tmp
	db.close()	

 	if request.POST:
		

		scrap_category = request.POST.get("scrap_category")

		
		
		if request.session["scrap_entry"] == 0:
			request.session["scrap_part"] = request.POST.get("scrap_part")
			scrap_part = request.session["scrap_part"] 
			request.session["scrap_entry"] = 1
			#print(request.session["scrap_entry"])
			
			request.session["scrap1"] ='''disabled="true"'''
			request.session["scrap2"] =''
			request.session["scrap3"] ='''disabled="true"'''
			request.session["scrap4"] ='''disabled="true"'''
			#request.session["scrap"] = "Scrap Description:"
			#request.session["amount"] = "Asset Num:"
			db, cursor = db_set(request)
			sql = "SELECT Line FROM scrap_part_line WHERE Part = '%s'" %(scrap_part)
			cursor.execute(sql)
			tmp = cursor.fetchall()
			scrap_part_line = tmp[0][0]
  			request.session["scrap_part_line"] = scrap_part_line
 			#r=4/0
  			sql = "SELECT DISTINCT Operation FROM scrap_line_operation_category WHERE Line = '%s'" %(scrap_part_line)
 			cursor.execute(sql)
  			tmp = cursor.fetchall()
  			request.session["scrap_operation_selection"] = tmp
 			db.close()
	
 		
 			return render(request, "redirect_edit_category.html")
 			
 		if request.session["scrap_entry"] == 1:
 			request.session["scrap_operation"] = request.POST.get("scrap_operation")
 			request.session["scrap_entry"] = 2
  			request.session["scrap1"] ='''disabled="true"'''
 			request.session["scrap2"] ='''disabled="true"'''
 			request.session["scrap3"] =''
 			# request.session["scrap4"] ='''disabled="true"'''
 			line = request.session["scrap_part_line"]

			# tmp_scrap4 = request.session["tmp_scrap6"]
 			# db, cursor = db_set(request)
 			# index.replace(" ","")
 			# sql = "SELECT * FROM scrap_line_operation_category where Id = '%s'" % (index) 
 			# cursor.execute(sql)
 			# request.session["tmp_scrap6"] = cursor.fetchall()
 			# db.close()
 			# tmp_scrap6 = request.session["tmp_scrap6"]
 			# if request.POST:
			# scrap_category = request.POST.get("scrap_category")
			# 	# scrap_operation =request.POST.get("scrap_operation") 


			# return render(request, "scrap_mgmt.html")
			## i tried adding an index parameter in the function so this works but didn't work  ^^. 
			## i wanted to make it so im taking a similar approach as def operationg_entries_update() but I dont think this is quite there
	
			return render(request, "redirect_edit_category.html") 

		if request.session["scrap_entry"] == 2:
			

			request.session["scrap_category"] = request.POST.get("scrap_category")

			scrap_part = request.session["scrap_part"]
			scrap_operation = request.session["scrap_operation"]
			scrap_category = request.session["scrap_category"]
			line = request.session["scrap_part_line"]
			active = '1.0'
			#r=4/0 
			

			#Put in here that you INSERT into Mysql a new line showing three things above
			db, cursor = db_set(request)
			cursor.execute('''INSERT INTO scrap_line_operation_category(Line,Operation,Category) VALUES(%s,%s,%s)''', (line,scrap_operation,scrap_category))
			cursor.execute('''INSERT INTO scrap_part_line(Part,Line,Active) VALUES(%s,%s,%s)''', (scrap_part,line,active))
			db.commit()
			db.close()

			return render(request, "redirect_scrap_mgmt.html") 

		return render(request, "redirect_scrap_mgmt.html") 

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'edit_category.html',{'args':args})
