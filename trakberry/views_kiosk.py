from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm,tech_loginForm
from trakberry.views import done
from views2 import main_login_form
from views3 import shift_area
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
from trakberry.mod1 import hyphon_fix
from trakberry.views_testing import machine_list_display
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2, vacation_set_current5
from views_vacation import vacation_set_current77,vacation_set_current4,vacation_set_current9, vacation_set_current5
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
import decimal
from smtplib import SMTP
from django.core.context_processors import csrf
from views_routes import direction
from time import mktime
from datetime import datetime, date
from views_db import db_open, db_set, net1
from views_mod1 import kiosk_lastpart_find, kiosk_email_initial
from datetime import datetime
import datetime

# *********************************************************************************************************
# MAIN KIOSK PAGE
# *********************************************************************************************************
# Kiosk Main Page.   Display buttons and route to action when they're pressed
def kiosk(request):
	request.session["route_1"] = 'kiosk_menu' # enable when ready to run
	return direction(request)


	# comment out below line to run local otherwise setting local switch to 0 keeps it on the network
	request.session["local_toggle"] = "/trakberry"
	request.session["kiosk_menu_screen"] = 1
	request.session["cycletime1"] = 0
	request.session["cycletime2"] = 0
	request.session["cycletime3"] = 0
	request.session["cycletime4"] = 0
	request.session["cycletime5"] = 0
	request.session["cycletime6"] = 0

	db, cur = db_set(request)
	sql = "SELECT left(Asset,4) FROM vw_asset_eam_lp"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp
	db.close()
	request.session["tmp"] = tmp
	
	# Utilize variable route_1 and assign it a value to kick to another module.
	# that module needs to have a pattern defined in url.py because direction(request)
	# will route externally to it looking for the pattern.
	if request.POST:
		button_1 = request.POST
		button_pressed =int(button_1.get("kiosk_button1"))
		if button_pressed == -1:
			#request.session["route_1"] = 'kiosk' # disable when ready to run
			request.session["route_1"] = 'kiosk_job_assign' # enable when ready to run
			
			return direction(request)
			
		if button_pressed == -2:
			#request.session["route_1"] = 'kiosk'   #disable when ready to run
			request.session["route_1"] = 'kiosk_production' # enable when ready to run
			return direction(request)
			
		if button_pressed == -3:
			request.session["route_1"] = 'hrly_display' # enable when ready to run

			return direction(request)
		if button_pressed == -4:
			request.session["route_1"] = 'kiosk_help_button' # enable when ready to run
			return direction(request)


			return kiosk_scrap(request)
			
		# If no button pressed...Probably should never get here
		return kiosk_none6(request)


	else:
		form = kiosk_dispForm1()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,"kiosk/kiosk.html",{'args':args})

# *********************************************************************************************************
# Secondary Pages generated from Main Page Button Presses
# *********************************************************************************************************
# Kiosk Secondary page initiated by JOB button press on main page

def down_10r(request):
	machines1 = ['1504','1506','1519','1520','1518','1521','1522','1523','1502','1507','1539','1540','1546','1501','1515','1524','1525','1547','1508','1532','1538','1548','1509','1541','1549','1514','1531','594','1510','1527','1550','1513','1552','1503','1530','751','1511','1528','1554','1533']
	operation1 = [10,10,10,10,10,10,10,10,30,30,30,30,30,40,40,40,40,40,50,50,50,50,60,60,60,70,70,70,80,80,80,90,90,100,100,100,110,110,110,120]
	new1 = [0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1]
	machine_rate = zip(operation1,machines1,new1)
	machines1 = ['1800','1801','1802','1529','776','1543','1824','1804','1805','1806','1808','1810','1815','1542','1812','1813','1816']
	operation1 = [10,10,10,30,30,30,30,40,40,50,60,70,80,90,100,100,110,120]
	new1 = [0,0,0,1,0,0,0,1,0,1,1,1,1,1,1,1,1,1]
	machine_rate2 = zip(operation1,machines1,new1)
	return render(request,"kiosk/down_10r.html",{'machines1':machine_rate,'machines2':machine_rate2})

def tech_down_10r_mobileset(request):  # Set session variable so view will display IPad version
	request.session['tech_down_mobileset'] = 1
	return render(request,"redirect_tech_down_10r.html")

def tech_down_10r_displayset(request):  # Set session variable so view will display IPad version
	request.session['tech_down_mobileset'] = 0
	return render(request,"redirect_tech_down_10r.html")


def tech_10r_login(request):
	db, cursor = db_set(request)
	sql = "SELECT tech FROM tkb_techs ORDER BY tech ASC" 
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close()
	if request.POST:
		tec = request.POST.get("user")
		request.session['tech_down_10r_login'] = 1
		request.session["login_tech10r"] = tec
		
		return render(request,'redirect_tech_down_10r.html')
	else:
		form = tech_loginForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'login_10r_tech.html',{'args':args,'tech':tmp})


def tech_10r_logout(request):
	request.session['tech_down_10r_login'] = 0
	return render(request,'redirect_tech_down_10r.html')


def tech_down_10r(request):
	machines1 = ['1504','1506','1519','1520','1518','1521','1522','1523','1502','1507','1539','1540','1546','1501','1515','1524','1525','1547','1508','1532','1538','1548','1509','1541','1549','1514','1531','594','1510','1527','1550','1513','1552','1503','1530','751','1511','1528','1554','1533']
	operation1 = [10,10,10,10,10,10,10,10,30,30,30,30,30,40,40,40,40,40,50,50,50,50,60,60,60,70,70,70,80,80,80,90,90,100,100,100,110,110,110,120]
	new1 = [0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1]
	color1 = ['#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33']
	machine_rate = zip(operation1,machines1,new1,color1)

	machine_rate = zip(operation1,machines1,new1)
	machines1 = ['1800','1801','1802','1529','776','1543','1824','1804','1805','1806','1808','1810','1815','1542','1812','1813','1816']
	operation1 = [10,10,10,30,30,30,30,40,40,50,60,70,80,90,100,100,110,120]
	new1 = [0,0,0,1,0,0,0,1,0,1,1,1,1,1,1,1,1,1]
	color1 = ['#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33','#49FF33']
	machine_rate2 = zip(operation1,machines1,new1,color1)

	tech1='10r_tech'
	db, cur = db_set(request)
	#sql = "SELECT * FROM pr_downtime1 where LEFT(whoisonit,8)= '%s' and completedtime IS NULL" % (tech1)
	sql = "SELECT * FROM pr_downtime1 where completedtime IS NULL"
	cur.execute(sql)
	tmp2 = cur.fetchall()
	db.close()

	op1 =[]
	m1 = []
	n1 =[]
	c1 =[]
	id1 = []
	ss1 = []
	for ii in machine_rate:
		c2 = 'G'
		idd = '0'
		sss = ''
		for i in tmp2:

			if i[0] == ii[1]:
				if i[5] == 'Yes_Down':
					c2 = 'R'
				if i[5] == 'No':
					c2 = 'Y'
				if i[4] != tech1:
					c2 = 'GR'
					sss = i[4]
				idd = i[11]
		op1.append(ii[0])
		m1.append(ii[1])
		n1.append(ii[2])
		c1.append(c2)
		id1.append(idd)
		ss1.append(sss)

	machine_rate = zip(op1,m1,n1,c1,id1,ss1)
	op1 =[]
	m1 = []
	n1 =[]
	c1 =[]
	id1 =[]
	ss1 = []
	for ii in machine_rate2:
		c2 = 'G'
		idd = '0'
		ss = ''
		for i in tmp2:
			if i[0] == ii[1]:
				if i[5] == 'Yes_Down':
					c2 = 'R'
				if i[5] == 'No':
					c2 = 'Y'
				if i[4] != tech1:
					c2 = 'GR'
					sss = i[4]
				idd = i[11]
		op1.append(ii[0])
		m1.append(ii[1])
		n1.append(ii[2])
		c1.append(c2)
		id1.append(idd)
		ss1.append(sss)

	machine_rate2 = zip(op1,m1,n1,c1,id1,ss1)


	if request.session['tech_down_mobileset'] == 1:
		return render(request,"tech_down_10r_mobile.html",{'machines1':machine_rate,'machines2':machine_rate2})
	else:
		return render(request,"tech_down_10r.html",{'machines1':machine_rate,'machines2':machine_rate2})
	

def redirect_down_10r_fix(request):
	index = request.session['variable1']
	return down_10r_fix(request,index)

def down_10r_fix(request,index):
	id1 = index

	db, cur = db_set(request)
	sql = "SELECT * FROM pr_downtime1 where idnumber = '%s'" % (id1)
	cur.execute(sql)
	tmp2 = cur.fetchall()
	db.close()

	
	asset = tmp2[0][0]
	down1 = tmp2[0][5]
	reason1 = tmp2[0][1]
	who1 = tmp2[0][4]
	request.session['tech_asset'] = asset
	request.session['tech_down'] = down1
	request.session['tech_reason'] = reason1 
	request.session['tech_who'] = who1 
	request.session['tech_index'] = str(id1)

	#down1 = request.session['down_10r_asset_down']

	if request.POST:
		machinenum = asset
		problem = request.POST.get("reason")
		solution = request.POST.get("solution")

		var1 = request.POST.get("enter")  # was the Pass off button pressed or just enter
		if var1 == ' Pass Off ':
			a = 1
		else:
			a = 2

		if len(solution) < 10:
			request.session['variable1'] = index
			return render(request,"redirect_down_10r_fix.html")

		priority = 30000
		try:
			whoisonit = request.session['login_tech10r']
		except:
			whoisonit = 'tech_10r'

		# take comment into tx and ensure no "" exist.	If they do change them to ''
		tx = problem
		tx = ' ' + tx
		tps = list(tx)

		# Genius appostrophe fix
		problem = hyphon_fix(tx)
		tx = solution
		solution = hyphon_fix(tx)

		problem = problem + " Tech:" + solution
		c=1
		t = vacation_temp()
		w = 'Millwright'
		db, cur = db_set(request)


		if a == 1:
			tql =( 'update pr_downtime1 SET whoisonit="%s" WHERE idnumber="%s"' % (w,id1))
			cur.execute(tql)
			db.commit()
			tql =( 'update pr_downtime1 SET problem="%s" WHERE idnumber="%s"' % (problem,id1))
			cur.execute(tql)
			db.commit()
		else:
			tql =( 'update pr_downtime1 SET completedtime="%s" WHERE idnumber="%s"' % (t,id1))
			cur.execute(tql)
			db.commit()
		tql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (solution,id1))
		cur.execute(tql)
		db.commit()
		db.close()

		return render(request,'redirect_tech_down_10r.html')
	
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form


	return render(request, "down_10r_fix.html",{'args':args})


def down_10r_fix_assign(request):
	try:
		who1 = request.session['login_tech10r']
	except:
		who1 = '10r_tech'
	#who1 = request.session['tech_who'] 
	id1 = request.session['tech_index']
	db, cur = db_set(request)
	tql =( 'update pr_downtime1 SET whoisonit="%s" WHERE idnumber="%s"' % (who1,id1))
	cur.execute(tql)
	db.commit()
	db.close()
	return down_10r_fix(request,id1)


	



def down_10r_entry(request,index):
	request.session['down_10r_asset'] = index
	request.session['down_10r_asset_down'] = 'Yes_Down'
	return render(request,"kiosk/down_10r_entry1.html")

def down_10r_asset_check(request):
	request.session['down_10r_asset_down'] = 'No'
	return down_10r_entry2(request)

def down_10r_entry2(request):
	asset = request.session['down_10r_asset']
	down1 = request.session['down_10r_asset_down']


	if request.POST:
		machinenum = asset
		problem = request.POST.get("reason")

		priority = 30000
		whoisonit = '10r_tech'
		
		# take comment into tx and ensure no "" exist.	If they do change them to ''
		tx = problem
		tx = ' ' + tx
		tps = list(tx)

		# Genius appostrophe fix
		problem = hyphon_fix(tx)

		t = vacation_temp()

		db, cur = db_set(request)

		asset3 = machinenum[:4]
		asset2 = machinenum[:3]
		try:
			int(asset3)
			asset4 = asset3
		except:
			asset4 = asset2
		asset5 = machinenum
		try:
			bql = "SELECT priority FROM tkb_asset_priority where asset_num = '%s'" % (asset4)
			cur.execute(bql)
			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
		except:
			tmp3 = 999
		try:
			priority = tmp3[0]
		except:
			priority = 999

		if len(problem)<2:
			problem='No reason given'
		cur.execute('''INSERT INTO pr_downtime1(machinenum,problem,priority,whoisonit,called4helptime,down,changeovertime) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (asset5,problem,priority,whoisonit,t,down1,t))
		db.commit()

		db.close()
		return render(request,'redirect_kiosk.html')
		
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request, "down_10r_entry2.html",{'args':args})



def kiosk_job(request):
	if request.POST:
		button_1 = request.POST
		button_pressed = int(button_1.get("kiosk_button1"))
		if button_pressed == -1:
			request.session["route_1"] = 'kiosk_job_assign'
			return direction(request)
		if button_pressed == -2:
			request.session["route_1"] = 'kiosk_job_leave'
			return direction(request)
		return kiosk_done4(request)
	else:
		form = kiosk_dispForm1()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "kiosk/kiosk_job.html",{'args':args})


def kiosk_production(request):

	job = ['' for x in range(6)]
	TimeOut = -1
	request.session["machine1"] = "1"
	request.session["machine2"] = "2"
	request.session["machine3"] = "3"
	request.session["machine4"] = "4"
	request.session["machine5"] = "5"
	request.session["machine6"] = "6"
	
	dummy2 = 1
	
	if dummy2 == 1:
#	if request.POST:
		kiosk_clock = request.session["current_clock"]
#		kiosk_clock = request.POST.get("clock")
		request.session["clock"] = ""
		request.session["variable1"] = ""
		request.session["variable2"] = ""
		request.session["variable3"] = ""
		request.session["variable4"] = ""
		request.session["variable5"] = ""
		request.session["variable6"] = ""




		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button2"))
			if kiosk_button1 == -2:
				if request.session["kiosk_main_screen"] == 1:
					request.session["route_1"] = 'kiosk'
				else:
					request.session["route_1"] = 'kiosk_menu'
				return direction(request)
		except:
			dummy = 1
			
			
		db, cur = db_set(request)

		sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
		cur.execute(sql)
		tmp2 = cur.fetchall()
		tmp1 = tmp2[0]
		ppp = tmp1[4]

		try:
			sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
			cur.execute(sql)
			tmp2 = cur.fetchall()
			tmp1 = tmp2[0]

			# Call kiosk_lastpart_find (in views_mod1 to get last part for all 6 parts  ***COOL CODE)
			# if no lastpart found then default to  "" for part 
			prt1 = kiosk_lastpart_find (tmp1[4])
			prt2 = kiosk_lastpart_find (tmp1[5])
			prt3 = kiosk_lastpart_find (tmp1[6])
			prt4 = kiosk_lastpart_find (tmp1[7])
			prt5 = kiosk_lastpart_find (tmp1[8])
			prt6 = kiosk_lastpart_find (tmp1[9])

			# ***************************************************************************************

			try:
				pn_len = 3
				request.session["variable1"] = int(tmp1[4])
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(tmp1[4],prt1)
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part1"] = prt1
				request.session["machine1"] = tmpp[5]
				try:
					request.session["cycletime1"] = str(tmpp[4])
				except:
					request.session["cycletime1"] = 0

			except:
				request.session["part1"] = "None"
				request.session["machine1"] = "XX"
				if len(tmp1[4])<2:
					request.session["variable1"] = 99
			try:
				request.session["variable2"] = int(tmp1[5])
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(tmp1[5],prt2)
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part2"] = prt2
				request.session["machine2"] = tmpp[5]
				try:
					request.session["cycletime2"] = str(tmpp[4])
				except:
					request.session["cycletime2"] = 0
			except:
				request.session["part2"] = "None"
				request.session["machine2"] = "XX"
				if len(tmp1[5]) < 2:
					request.session["variable2"] = 99

			try:
				request.session["variable3"] = int(tmp1[6])
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(tmp1[6],prt3)
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part3"] = prt3
				request.session["machine3"] = tmpp[5]
				try:
					request.session["cycletime3"] = str(tmpp[4])
				except:
					request.session["cycletime3"] = 0
			except:
				request.session["part3"] = "None"
				request.session["machine3"] = "XX"
				if len(tmp1[6]) < 2:
					request.session["variable3"] = 99

			try:
				request.session["variable4"] = int(tmp1[7])
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(tmp1[7],prt4)
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part4"] = prt4
				request.session["machine4"] = tmpp[5]
				try:
					request.session["cycletime4"] = str(tmpp[4])
				except:
					request.session["cycletime4"] = 0
			except:
				request.session["part4"] = "None"
				request.session["machine4"] = "XX"
				if len(tmp1[7]) < 2:
					request.session["variable4"] = 99

			try:
				request.session["variable5"] = int(tmp1[8])
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(tmp1[8],prt5)
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part5"] = prt5
				request.session["machine5"] = tmpp[5]
				try:
					request.session["cycletime5"] = str(tmpp[4])
				except:
					request.session["cycletime5"] = 0
			except:
				request.session["part5"] = "None"
				request.session["machine5"] = "XX"
				if len(tmp1[8]) < 2:
					request.session["variable5"] = 99

			try:
				request.session["variable6"] = int(tmp1[9])
				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(tmp1[9],prt6)
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				request.session["part6"] = prt6
				request.session["machine6"] = tmpp[5]
				try:
					request.session["cycletime6"] = str(tmpp[4])
				except:
					request.session["cycletime6"] = 0
			except:
				request.session["part6"] = "None"
				request.session["machine6"] = "XX"
				if len(tmp1[9]) < 2:
					request.session["variable6"] = 99

			db.close()

			request.session["clock"] = kiosk_clock
			request.session["route_1"] = 'kiosk_production_entry'

			return direction(request)
	
	
		except:	
			#Problem is above
			request.session["route_1"] = 'kiosk_menu'
			return direction(request)
	
	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "kiosk/kiosk_production.html",{'args':args})

def manual_production_entry6(request):
	return render(request, "kiosk/kiosk_test.html")

def manual_production_entry3(request):
	
	current_first, shift  = vacation_set_current5()
	#request.session["current_first"] = current_first
	
	
	kiosk_job = ['' for x in range(0)]
	kiosk_part = ['' for x in range(0)]
	kiosk_prod = ['' for x in range(0)]
	kiosk_hrs = ['' for x in range(0)]
	kiosk_dwn = ['' for x in range(0)]
	kiosk_clock = ['' for x in range(0)] 
	
	if request.POST:
		
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'kiosk'
				return direction(request)
		except:
			dummy = 1
			
		x_job = "job"
		x_part = "part"
		x_prod = "prod"
		x_hrs = "hrs"
		x_dwn = "dwn"
		
		kiosk_date = request.POST.get("date_en")
		kiosk_shift = request.POST.get("shift")
		
		for i in range(1,7): # Read in all the data entered for production into appropriate variables
		#try:
			x_job = x_job + str(i)
			x_part = x_part + str(i)
			x_prod = x_prod + str(i)
			x_hrs = x_hrs + str(i)
			x_dwn = x_dwn + str(i)
			kiosk_job.append(request.POST.get(x_job))
			kiosk_part.append(request.POST.get(x_part))
			kiosk_prod.append(request.POST.get(x_prod))
			kiosk_hrs.append(request.POST.get(x_hrs))
			kiosk_dwn.append(request.POST.get(x_dwn))
			
			x_job = "job"
			x_part = "part"
			x_prod = "prod"
			x_hrs = "hrs"
			x_dwn = "dwn"
			
		shift_time = "None"
		#except:
		#	dummy = 1
		if kiosk_shift=="Aft":
			shift_time="3pm-11pm"
		if kiosk_shift=="Day":
			shift_time="7am-3pm"
		if kiosk_shift=="Mid":
			shift_time="11pm-7am"
			
		#pprod = int(kiosk_prod[1])
		#pprod2 = int(kiosk_prod[0])
		
		# Empty variables
		xy = "_"
		zy = 0
		sheet_id = 'kiosk'
		db, cur = db_set(request)
		
		for i in range(0,6):
			job = kiosk_job[i]
			part = kiosk_part[i]
			prod = kiosk_prod[i]
			hrs = kiosk_hrs[i]
			dwn = kiosk_dwn[i]
			clock_number = request.session["clock"]
			
			try:
				dummy = len(job)
				cur.execute('''INSERT INTO sc_production1(asset_num,partno,actual_produced,shift_hours_length,down_time,comments,shift,pdate,machine,scrap,More_than_2_percent,total,target,planned_downtime_min_forshift,sheet_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (job,part,prod,hrs,dwn,clock_number,shift_time,kiosk_date,xy,zy,zy,zy,zy,zy,zy))
				db.commit()
			except:
				dummy = 1
		
		TimeStamp = int(time.time())
		TimeOut = - 1
		cql = ('update tkb_kiosk SET TimeStamp_Out = "%s" WHERE Clock ="%s" and TimeStamp_Out = "%s"' % (TimeStamp,clock_number,TimeOut))
		cur.execute(cql)
		db.commit()
	
		db.close()
		

		
		# Below is to test variables
		#return render(request, "kiosk/kiosk_test2.html",{'job':kiosk_job,'part':pprod2,'prod':pprod,'hrs':kiosk_hrs,'dwn':kiosk_dwn}) 
		
		request.session["route_1"] = 'manual_production_entry'
		return direction(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	return render(request, "kiosk/manual_production_entry.html",{'args':args,'TCUR':tcur,'Curr':current_first, 'Shift':shift})
	
def manual_production_entry(request):
	pn_len = 3
	db, cur = db_set(request)
	current_first, shift  = vacation_set_current5()

	aql = "SELECT MAX(id)  FROM sc_production1" 
	cur.execute(aql)
	tmp3 = cur.fetchall()
	tmp4 = tmp3[0]
	tmp5 = tmp4[0]
	
	bql = "Select shift From sc_production1 WHERE id = '%d'" %(tmp5)
	cur.execute(bql)
	tmp3 = cur.fetchall()
	tmp4 = tmp3[0]
	kshift = tmp4[0]
	
	try:
		dql = "Select pdate From sc_production1 WHERE id = '%d'" %(tmp5)
		cur.execute(dql)
		tmp3 = cur.fetchall()
		tmp4 = tmp3[0]
		dt = tmp4[0]
		ddt = str(dt)
		current_first = ddt
	except:
		dummy = 1 
	
	if kshift=="3pm-11pm":
		shift="Aft"
	if kshift=="7am-3pm":
		shift="Day"
	if kshift=="11pm-7am":
		shift="Mid"
			
	if request.POST:
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'manual_production_entry'
				return direction(request)
		except:
			clock = request.POST.get("clock")
			ddate = request.POST.get("date_en")
			shift = request.POST.get("shift")
			job = request.POST.get("job")
			
			request.session["clock"] = clock
			request.session["date"] = ddate
			request.session["shift"] = shift
			request.session["job"]= job
			pn_len = 3

			db, cur = db_set(request)

#			New Code to find the current operation using cycletime table (It works and use when ready)
#			try:
#				sql = "SELECT * FROM tkb_cycletime WHERE asset = '%s'" %(job)
#				cur.execute(sql)
#				tmp = cur.fetchall()
#				tmpp = tmp[0]
#				request.session["machine"] = tmpp[5]
#			except:
#				request.session["machine"] = "XX"
#			if len(request.session["machine"])<2:
#				request.session["machine"] = "XX"

#			Below is the old code to find the current operation using latest entry
			try:
				aql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' " % (job)

#				aql = "SELECT * FROM sc_production1 WHERE asset_num = '%s' and LENGTH(partno)> '%d' ORDER BY %s %s" %(job,pn_len,'id','DESC')
				cur.execute(aql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				request.session["machine"] = tmp4[5]
				
			except:
				request.session["machine"] = "XX"
				


			try:
				aql = "SELECT * FROM sc_production1 WHERE asset_num = '%s' and LENGTH(partno)> '%d' ORDER BY %s %s" %(job,pn_len,'id','DESC')

				
				cur.execute(aql)
				tmp3 = cur.fetchall()
				tmp4 = tmp3[0]
				request.session["part"] = tmp4[3]
				
			except:
				request.session["part"] = "XX"
			db.close()
#			request.session["machine"] ='GF7 Stop All'
		#	return render(request,"kiosk/kiosk_test2.html")
			request.session["route_1"] = 'manual_production_entry2'
			return direction(request)
	else:
		form = kiosk_dispForm4()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	return render(request, "kiosk/manual_production_entry.html",{'args':args,'TCUR':tcur,'Curr':current_first, 'Shift':shift})
	
def manual_production_entry2(request):
	if request.POST:
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'manual_production_entry'
				return direction(request)
		except:
			part = request.POST.get("part")
			prod = request.POST.get("prod")
			hrs = request.POST.get("hrs")
			dwn = request.POST.get("down")
			mch = request.session['machine']
			
			clock_number = request.session["clock"]
			kiosk_date = request.session["date"] 
			kiosk_shift = request.session["shift"] 
			job = request.session["job"]
			
			if kiosk_shift=="Aft":
				shift_time="3pm-11pm"
			if kiosk_shift=="Day":
				shift_time="7am-3pm"
			if kiosk_shift=="Mid":
				shift_time="11pm-7am"
			
			
			db, cur = db_set(request)
		
			try:
				xy = "_"
				zy = 0
				
				dummy = len(job)
				try:
					kiosk_id = request.session["kiosk_id"]
				except:
					kiosk_id = "Unknown Kiosk"
				cur.execute('''INSERT INTO sc_production1(asset_num,partno,actual_produced,shift_hours_length,down_time,comments,shift,pdate,machine,scrap,More_than_2_percent,total,target,planned_downtime_min_forshift,sheet_id,kiosk_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (job,part,prod,hrs,dwn,clock_number,shift_time,kiosk_date,mch,zy,zy,zy,zy,zy,xy,kiosk_id))
				db.commit()
			except:
				dummy = 1
				
				
			db.close()
			request.session["route_1"] = 'manual_production_entry'
			return direction(request)
	else:
		form = kiosk_dispForm4()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	return render(request, "kiosk/manual_production_entry2.html",{'args':args})


def kiosk_production_entry(request):
	
	current_first, shift  = vacation_set_current5()
	msg1 = "Fail"
	#request.session["current_first"] = current_first
	try:
		checkA = request.session["oa_check"] 
	except:
		request.session["oa_problem"] = ""
		request.session["oa_check"] = ""
		a1 = "oa_part"
		a2 = "oa_machine"
		a3 = "oa_variable"
		for a in range(1,7):
			b1 = a1 + str(a)
			b2 = a2 + str(a)
			b3 = a3 + str(a)
			request.session[b1] = ""
			request.session[b2] = ""
			request.session[b3] = ""
	
	kiosk_job = ['' for x in range(0)]
	oa_prob = ['' for x in range(0)]
	kiosk_part = ['' for x in range(0)]
	kiosk_prod = ['' for x in range(0)]
	kiosk_hrs = ['' for x in range(0)]
	kiosk_dwn = ['' for x in range(0)]
	kiosk_machine = ['' for x in range(0)]
	kiosk_ppm = ['' for x in range(0)]
	kiosk_target = ['' for x in range(0)]
	kiosk_low_production = [0 for x in range(0)]
	kiosk_tpm = ['' for x in range(0)]

	tpm_complete = 0

	if request.POST:
		kiosk_clock = request.POST.get("clock")
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				TimeStamp = int(time.time())
				TimeOut = - 1
				
				try:
					db, cur = db_set(request)
					cql = ('update tkb_kiosk SET TimeStamp_Out = "%s" WHERE Clock ="%s" and TimeStamp_Out = "%s"' % (TimeStamp,kiosk_clock,TimeOut))
					cur.execute(cql)
					db.commit()
					db.close()
				except:
					dummy = 1
				if request.session["kiosk_menu_screen"] == 1:
					request.session["route_1"] = 'kiosk'
				else:
					request.session["route_1"] = 'kiosk_menu'

				return direction(request)
		except:
			dummy = 1
			
		x_job = "job"
		x_part = "part"
		x_prod = "prod"
		x_hrs = "hrs"
		x_dwn = "dwn"
		x_ppm = "ppm"
		x_tpm = "tpm"

		test1 = []
		test2 = []

		kiosk_date = request.POST.get("date_en")
		kiosk_shift = request.POST.get("shift")
		
		tpm_verify = 1
		for i in range(1,7): # Read in all the data entered for production into appropriate variables
		#try:
			x_job = x_job + str(i)
			x_part = x_part + str(i)
			x_prod = x_prod + str(i)
			x_hrs = x_hrs + str(i)
			x_dwn = x_dwn + str(i)
			x_ppm =x_ppm + str(i)
			x_tpm = x_tpm + str(i)
			session1 = 'tpm' + str(i)
			tpm4 = request.session[session1]

			kiosk_job.append(request.POST.get(x_job))
			kiosk_part.append(request.POST.get(x_part))
			k_tpm = request.POST.get(x_tpm)
			kiosk_tpm.append(k_tpm) 

			if tpm4 > 0: # Means there is a TPM required
				if k_tpm:   # Means it was completed
					tpm_complete = 1
				else:       # It wasn't completed
					tpm_complete = 0
			else:
				tpm_complete = -1  # There is no TPM required

			tpm_verify = tpm_verify * tpm_complete  # If there's a 0 tpm_complete it means not done and will make tpm_verify always 0
			# if k_tpm != True and tpm4 == 1:
			# 	tpm_complete = 0
			# elif k_tpm:
			# 	tpm_complete = 1
			# elif tpm4 == 0:
			# 	tpm_complete = -1
			# test2.append(tpm_complete)


			temp_prod = request.POST.get(x_prod)
			if temp_prod == None or temp_prod == "":
				temp_prod = 0
			kiosk_prod.append(temp_prod)
			kiosk_hrs.append(request.POST.get(x_hrs))
			kiosk_dwn.append(request.POST.get(x_dwn))
			kiosk_ppm.append(request.POST.get(x_ppm))
			
			x_job = "job"
			x_part = "part"
			x_prod = "prod"
			x_hrs = "hrs"
			x_dwn = "dwn"
			x_ppm = "ppm"
			x_tpm = "tpm"



		shift_time = "None"
		#except:
		#	dummy = 1
		if kiosk_shift=="Aft":
			shift_time="3pm-11pm"
		if kiosk_shift=="Day":
			shift_time="7am-3pm"
		if kiosk_shift=="Mid":
			shift_time="11pm-7am"
			
		#pprod = int(kiosk_prod[1])
		#pprod2 = int(kiosk_prod[0])
		
		# Empty variables
		xy = "_"
		zy = 0
		oa_check = 0
		part_check = 0
		write_answer = 0
		try:
			sheet_id = request.session["kiosk_type"]
		except:
			sheet_id = 'kiosk'

		# db, cur = kiosk_email_initial(request) # This Check will ensure the new columns are in and if not will add them
		db, cur = db_set(request)

		

		
		for i in range(0,6):
			job = kiosk_job[i]
			part = kiosk_part[i]
			prod = kiosk_prod[i]
			hrs = kiosk_hrs[i]
			dwn = kiosk_dwn[i]
			ppm = kiosk_ppm[i]
			tpm = kiosk_tpm[i]
			low_production_variable = 0
			target1 = 0
			machine = ""
			clock_number = request.session["clock"]
			if i == 0 :
				m = request.session["machine1"]
				ct = request.session["cycletime1"]
			elif i ==1:
				m = request.session["machine2"]
				ct = request.session["cycletime2"]
			elif i ==2:
				m = request.session["machine3"]
				ct = request.session["cycletime3"]
			elif i ==3:
				m = request.session["machine4"]
				ct = request.session["cycletime4"]
			elif i ==4:
				m = request.session["machine5"]
				ct = request.session["cycletime5"]
			elif i ==5:
				m = request.session["machine6"]
				ct = request.session["cycletime6"]
			
			# Use try except to determine if there's a job for this loop
			try:
				if len(job) > 2:
					write_variable = 1
				else:
					write_variable = 0
			except:
				write_variable = 0
			if write_variable == 1:
				try:
					# db, cur = db_set(request)
					uql = "SELECT * FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(job,part)
					cur.execute(uql)
					ymp = cur.fetchall()
					ymp2 = ymp[0]
					ct = ymp2[4]
					# db.close()
				except:
					dummy = 7

				try:
					ppm = float(ppm)
					ct = (60 / ppm)
				except:
					dummy = 1
				h = float(hrs)

				#  to make sure someone didn't put a null amount in for downtime.  If so then make it 0
				try:
					test1 = int(dwn)
				except:
					dwn = 0
				# End of Fix
				
				hh = (h * 60 * 60) - (int(dwn) * 60)
				try:
					ct = float(ct)
					target1 = ((h * 60 * 60) / (ct))
					target2 = (hh / (ct))
				except:
					target1 = int(int(prod) / .85)
					target2 = target1
				test_prod = prod
				# Place the OA Check Code here **********************
				
				if target2 > 0:
					OA = int((int(test_prod) / float(target2)) * 100)
				else:
					OA = 0
				# return render(request,'kiosk/kiosk_test.html', {'OA':OA,'test_prod':test_prod,'target1':target1})	
				kiosk_target.append(int(target1))
				kiosk_machine.append(m)
				
				if OA < 70:
					# return render(request,'kiosk/kiosk_test.html', {'OA':OA})	
					oa_check = 1
					# oa_problem = request.session["oa_problem"]
					oa_problem =  "(" + str(job) + "):" + str(test_prod) + ' for ' + str(hrs) + 'hrs and ' + str(kiosk_dwn[(i)]) + ' down should be ' + str(int(target2*.7)) 
					oa_prob.append(oa_problem)
					low_production_variable = 2
                    
					
					# request.session["oa_problem"] = oa_problem
						# test = str.replace(test, '\n', '\r\n')

				if len(part) < 2 or part == 'None':
					if job not in ['802','500','801']:
						part_check = 1
						part_check_job = job
			
								
			else:
				dummy = 1
				kiosk_target.append(None)
				kiosk_machine.append("")

			kiosk_low_production.append(low_production_variable) # It will be either 0 or 2 at this point
		
		request.session["oa_problem"] = oa_prob
		# Set bounce level
		# yyy = request.session["srgg"]	
		request.session["bounce"] = 0
		bounce = 0

		# if oa_check == 1: 
		# 	# bounce = 1
		# 	bounce = 0 #  bypass error display for now
		# 	write_answer = 1
		# 	request.session["error_title"] = "Low Production"
		# 	request.session["error_message"] = "Make sure that count, hrs run and downtime are correct!"
		# 	request.session["oa_problem2"] = request.session["oa_problem"]
		
		if part_check == 1:
			bounce = 2
			request.session["error_title"] = " Warning !"
			request.session["error_message"] = "Must Have a Part for every Job !"
			request.session["oa_problem2"] = "Machine " + part_check_job + " has no part listed for it."
			request.session["oa_problem"] = ""

		if tpm_verify == 0:
			bounce = 3
			request.session["error_title"] = " Warning !"
			request.session["error_message"] = "All required TPMs must be completed"

		# if request.session["check1"] == 1:  # bypass the presses
		# 	bounce = 0
		# 	write_answer = 1

		# if part_check!=1 and oa_check != 1:
		# 	bounce = 0
		# 	write_answer = 1
		
		# if bounce == 1 and request.session["oa_check"] == "Fail":
		# 	request.session["oa_check"] = ""
		# 	write_answer = 1
		# 	bounce = 0
		if bounce > 0:
			request.session["bounce"] = bounce
			prod_var = 'oa_prod'
			part_var = 'part'
			for j in range(0,6):
				psess = prod_var + str(j+1)
				prsess = part_var + str(j+1)
				request.session[psess] = kiosk_prod[j]
				request.session[prsess] = kiosk_part[j]

			# if bounce == 2:
			# 	request.session["oa_check"] = ""
			# else:
			# 	request.session["oa_check"] = "Fail"
			# request.session["OA_Curr"] = kiosk_date
			# request.session["OA_Shift"] = kiosk_shift
			# a1 = "oa_dwn"
			# a2 = "oa_prod"
			# a3 = "oa_hrs"
			# a4 = "part"
			# for a in range(1,7):
			# 	b1 = a1 + str(a)
			# 	b2 = a2 + str(a)
			# 	b3 = a3 + str(a)
			# 	b4 = a4 + str(a)
			# 	request.session[b1] = kiosk_dwn[(a-1)]
			# 	request.session[b2] = kiosk_prod[(a-1)]
			# 	request.session[b3] = kiosk_hrs[(a-1)]
			# 	request.session[b4] = kiosk_part[(a-1)]
			# yyy = request.session["srgg"]
			request.session["route_1"] = 'kiosk_production_entry'
			return direction(request)
		else:
			request.session["bounce"] = 0
			write_answer = 1

		# if oa_check != 1:
		# 	write_answer = 1
		# else:
		# 	if request.session["oa_check"] == "Fail":
		# 		request.session["oa_check"] = ""
		# 		write_answer = 1
		# 	else:
		# 		request.session["oa_check"] = "Fail"
		# 		request.session["OA_Curr"] = kiosk_date
		# 		request.session["OA_Shift"] = kiosk_shift
		# 		a1 = "oa_dwn"
		# 		a2 = "oa_prod"
		# 		a3 = "oa_hrs"
		# 		for a in range(1,7):
		# 			b1 = a1 + str(a)
		# 			b2 = a2 + str(a)
		# 			b3 = a3 + str(a)
		# 			request.session[b1] = kiosk_dwn[(a-1)]
		# 			request.session[b2] = kiosk_prod[(a-1)]
		# 			request.session[b3] = kiosk_hrs[(a-1)]
		# 		request.session["route_1"] = 'kiosk_production_entry'
		# 		return direction(request)
		

		request.session['kiosk_all_jobs'] = kiosk_job
		request.session['kiosk_all_parts'] = kiosk_part

		varn = [[],[],[],[],[],[]]
		# for x in range(0,20):
		# 	varn[x] = []


		if write_answer == 1:
			for i in range(0,6):
				job = kiosk_job[i]
				tpm = kiosk_tpm[i]
				low_production = kiosk_low_production[i]
				try:
					dummy = len(job)
					write_variable = 1
				except:
					write_variable = 0
				if write_variable == 1:
					part = kiosk_part[i]
					prod = kiosk_prod[i]
					hrs = kiosk_hrs[i]
					dwn = kiosk_dwn[i]
					ppm = kiosk_ppm[i]
					m = kiosk_machine[i]
					target1 = kiosk_target[i]
					if sheet_id == 'manual':  # Set the variable to determine if we had to enter manually so we can email 
						manual_sent = 0
					else:
						manual_sent = 1
					try:
						kiosk_id = request.session["kiosk_id"]
					except:
						kiosk_id = "Unknown Kiosk"
					# y = y / 0
					if job[:1] == '3':
						job = job + request.session['furnace']

					# Determine if tpm is 1-complete 0-not complete or N/A - not needed
					tpm2 = 'No'
					if tpm: tpm2 = 'Yes'
					sql = "SELECT COUNT(Asset) FROM quality_tpm_assets WHERE Asset = '%s'" %(job+".0")
					cur.execute(sql)
					tmp2 = cur.fetchall()
					if int(tmp2[0][0]) == 0:
						tpm2 = 'N/A'

					varn[i].extend((job,part,prod,hrs,dwn,clock_number,shift_time,kiosk_date,m,zy,zy,zy,target1,zy,sheet_id,zy,low_production,manual_sent,kiosk_id,tpm2))


					# cur.execute('''INSERT INTO sc_production1(asset_num,partno,actual_produced,shift_hours_length,down_time,comments,shift,pdate,machine,scrap,More_than_2_percent,total,target,planned_downtime_min_forshift,sheet_id,Updated,low_production,manual_sent,kiosk_id,tpm) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (job,part,prod,hrs,dwn,clock_number,shift_time,kiosk_date,m,zy,zy,zy,target1,zy,sheet_id,zy,low_production,manual_sent,kiosk_id,tpm2))
					# db.commit()

			TimeStamp = int(time.time())
			TimeOut = - 1
			cql = ('update tkb_kiosk SET TimeStamp_Out = "%s" WHERE Clock ="%s" and TimeStamp_Out = "%s"' % (TimeStamp,clock_number,TimeOut))
			cur.execute(cql)
			db.commit()
			db.close()

		
		# ******************************************
		# Put the EPV Verification ReRoute in here *
		# ******************************************
		request.session['varn'] = varn
		request.session["route_1"] = 'kiosk_epv_verification'
		return direction(request)

	#	Below will route to Kiosk Main if it's a joint ipad or kiosk if it's a lone one
		if request.session["kiosk_menu_screen"] == 1:
			request.session["route_1"] = 'kiosk_menu'
		else:
			request.session["route_1"] = 'kiosk_menu'
		return direction(request)
	#
	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	db, cur = db_set(request)
	sql = "SELECT DISTINCT parts_no FROM sc_prod_parts ORDER BY %s %s" %('parts_no','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	db.close()
	# Error Check to see if this is the 2nd time through with a warning on OA 
	# try:
	# 	checkA = request.session["oa_check"] 
	# except:
	# 	request.session["oa_check"] = ""
	# 	kiosk_defaults(request)

	# if request.session["bounce"] > 0:
	# 	current_first = request.session["OA_Curr"]
	# 	shift = request.session["OA_Shift"]

	# else:
	kiosk_defaults(request)


	# # #  End Point   ************************************
	# debug_start = (request.session["debug_start"])
	
	# debug_end = (time.time())

	

	# request.session["debug_end"] = debug_end
	# debug_time = debug_end - debug_start
	# request.session["debug_time"] = debug_time
	# return render(request,'kiosk/kiosk_test2.html')
	# # *******************************************************

	#return render(request, "kiosk/kiosk_test5.html")
	try:
		oa_prob = request.session["oa_problem"]
	except:
		oa_prob = ""
	# Check if it's a CSD2 press .  If so go to kiosk_production_entryP where we use ppm otherwise kiosk_production_entry
	if request.session["check1"] == 1:
		return render(request, "kiosk/kiosk_production_entryP.html",{'args':args,'TCUR':tcur,'Curr':current_first, 'Shift':shift,'Parts':tmp,'Msg1':msg1,'oa_problem':oa_prob})

	return render(request, "kiosk/kiosk_production_entry.html",{'args':args,'TCUR':tcur,'Curr':current_first, 'Shift':shift,'Parts':tmp,'Msg1':msg1,'oa_problem':oa_prob})
	
# Check kiosk entries to see if EPV required.
def kiosk_epv_verification(request):
	kiosk_job = request.session['kiosk_all_jobs']
	kiosk_part = request.session['kiosk_all_parts']
	varn = request.session['varn']

	shift1 = str(varn[0][6])
	date1 = str(varn[0][7])
	who1 = 'Operator'
	db, cur = db_set(request)
	a = []
	jj=[]
	ctr = 1

	for i in range (0,6):
		try:
			job = kiosk_job[i] + '.0'
			job = str(varn[i][0] + '.0')
			part = kiosk_part[i]
			sql = "SELECT * FROM quality_epv_assets where (Person = '%s' and (Asset = '%s' or (Actual = '%s' and Part1 = '%s' ) or (Actual = '%s' and Part2 = '%s' ) or (Actual = '%s' and Part3 = '%s' )  or (Actual = '%s' and Part4 = '%s' )))" %(who1,job,job,part,job,part,job,part,job,part)
			cur.execute(sql)
			tmp = cur.fetchall()
			for ii in tmp:
				chk = ii[1]
				aql = "SELECT COUNT(*) FROM quality_epv_checks where (date1 = '%s' and shift1 = '%s' and check1 = '%s')" %(date1,shift1,chk)
				cur.execute(aql)
				amp = cur.fetchall()
				bmp = amp[0]
				chk_count = bmp[0]
				if int(chk_count) == 0:
					jj = list(ii)
					h = 'id' + str(ctr)
					hh = 'comment' + str(ctr)
					jj.append(h)
					jj.append(hh)
					tmp2 = list(jj)
					a.append(tmp2)
					ctr = ctr + 1
		except:
			dummy = 0
	request.session['epv_checks'] = a
	n_epv_checks = len(a)
	request.session['b'] = n_epv_checks
	if n_epv_checks > 0:
		# Redirect to EPV Verification page using session variable epv_checks
		request.session["route_1"] = 'kiosk_epv_entry'
		return direction(request)
		# return render(request,'test21.html')
	else:
		request.session["route_1"] = 'kiosk_production_write'
		return direction(request)

def kiosk_epv_entry(request):
	varn = request.session['varn']
	shift = str(varn[0][6])
	date1 = str(varn[0][7])
	clock_num = str(varn[0][5])
	if request.POST:
		request.session['bounce6'] = 0
		x = request.POST['kiosk_epv_button']
		if x == 'Cancel':
			request.session["route_1"] = 'kiosk_production_entry'
			return direction(request)
		complete1 = 1
		c = []
		tt=[]
		for i in request.session['epv_checks']:
			# epv_ver = request.POST.get(i[14])
			epv_ver = request.POST.get("acs")
			tt.append(epv_ver)
			epv_comment = request.POST.get(i[15])
			c.append(epv_comment)
			if epv_ver:
				complete1 = complete1 * 1
			else:
				complete1 = complete1 * 0

		# if complete1 == 0:
		if not epv_ver:
			request.session['bounce6'] = 1
			request.session['route_1'] = 'kiosk_epv_entry'
			request.session["error_title"] = " Warning !"
			request.session["error_message"] = "Not All EPVs were checked off !"
		else:
			# Write EPV / Date and Shift
			ctr = 0
			db, cur = db_set(request)
			cur.execute("""CREATE TABLE IF NOT EXISTS quality_epv_checks(Id INT PRIMARY KEY AUTO_INCREMENT,date1 CHAR(80),shift1 CHAR(80), check1 Char(80), description1 Char(80), asset1 Char(80), master1 Char(80), comment Char(255), clock_num Char(80))""")
			for i in request.session['epv_checks']:
				cur.execute('''INSERT INTO quality_epv_checks(date1,shift1,check1,description1,asset1,master1,comment,clock_num) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''', (date1,shift,i[1],i[8],i[3],i[5],c[ctr],clock_num))
				db.commit()
				ctr = ctr + 1
			db.close()
			request.session['route_1'] = 'kiosk_production_write'
		return direction(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request, "kiosk/kiosk_epv_entry.html",{'args':args})

# Write kiosk entries using varn
def kiosk_production_write(request):
	# Change Asset
	old_assets=['349s','344s','341s','342s','343s']  # Old Non Relavent
	new_assets=['1516','344','341','342','343'] # Want changed to
	varn = request.session['varn']
	db, cur = db_set(request)
	for i in varn:
		try:
			asset8 = str(i[0])
			dummy = i[1]
			if asset8 in old_assets:
				ctr = 0
				for x in old_assets:
					if x==asset8:
						asset8 = new_assets[ctr]
						break
					ctr = ctr + 1
			cur.execute('''INSERT INTO sc_production1(asset_num,partno,actual_produced,shift_hours_length,down_time,comments,shift,pdate,machine,scrap,More_than_2_percent,total,target,planned_downtime_min_forshift,sheet_id,Updated,low_production,manual_sent,kiosk_id,tpm) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (asset8,i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19]))
			db.commit()
		except:
			dummy = 1
	db.close()
	request.session["route_1"] = 'kiosk_menu'
	return direction(request)


def kiosk_defaults(request):
	request.session["oa_check"] = ""
	request.session["oa_problem"] = ""
	a1 = "oa_dwn"
	a2 = "oa_prod"
	a3 = "oa_hrs"
	for a in range(1,7):
		b1 = a1 + str(a)
		b2 = a2 + str(a)
		b3 = a3 + str(a)
		request.session[b1] = 0
		request.session[b2] = None
		request.session[b3] = 8
	return



def flex_test(request):
	return render(request, "kiosk/flex_test.html")
	


# *********************************************************************************************************
# Third Tier Pages generated from Secondary Page Button Presses
# *********************************************************************************************************
# Kiosk Third Tier page initiated by Job | Assign button press on Secondary Page
def kiosk_job_assign(request):

	request.session["ppm_check"] = 0
	request.session["check1"] = 0
	request.session["press1"] = 0
	request.session["press2"] = 0
	request.session["press3"] = 0
	request.session["press4"] = 0
	request.session["press5"] = 0
	request.session["press6"] = 0
	db, cur = db_set(request)

	# ********************************************************************
	# This will be added and run seperately sometime.
	# Add the column in sc_production1 if it doesn't exist
	try:
		na1 = 'N/A'
		cur.execute('Alter Table sc_production1 ADD tpm CHAR(80) Default NULL ')
		# cur.execute('Alter Table sc_production1 DROP tpm')
		db.commit()
		cql = ('update sc_production1 SET tpm = "%s" WHERE tpm IS NULL' % (na1))
		cur.execute(cql)
		db.commit()
	except:
		dummy = 1
	# *********************************************************************

	if request.POST:
		kiosk_clock = request.POST.get("clock")
		kiosk_job1 = request.POST.get("job1")
		kiosk_job2 = request.POST.get("job2")
		kiosk_job3 = request.POST.get("job3")
		kiosk_job4 = request.POST.get("job4")
		kiosk_job5 = request.POST.get("job5")
		kiosk_job6 = request.POST.get("job6")

		


	
		#check to see if it's a CSD2 Press entry and add PPM field for entry if it is.  Only look at 2 first characters as 27 is necessary
		if kiosk_job1[:2] == '27':
			request.session["check1"] = 1
			request.session["press1"] = 1
		if kiosk_job2[:2] == '27':
			request.session["check1"] = 1
			request.session["press2"] = 1
		if kiosk_job3[:2] == '27':
			request.session["check1"] = 1
			request.session["press3"] = 1
		if kiosk_job4[:2] == '27':
			request.session["check1"] = 1
			request.session["press4"] = 1
		if kiosk_job5[:2] == '27':
			request.session["check1"] = 1
			request.session["press5"] = 1
		if kiosk_job6[:2] == '27':
			request.session["check1"] = 1
			request.session["press6"] = 1	


		if kiosk_job1[:2] == '90':
			request.session["check1"] = 3
			request.session["insp1"] = 3
		if kiosk_job2[:2] == '90':
			request.session["check1"] = 3
			request.session["insp2"] = 3
		if kiosk_job3[:2] == '90':
			request.session["check1"] = 3
			request.session["insp3"] = 3
		if kiosk_job4[:2] == '90':
			request.session["check1"] = 3
			request.session["insp4"] = 3
		if kiosk_job5[:2] == '90':
			request.session["check1"] = 3
			request.session["insp5"] = 3
		if kiosk_job6[:2] == '90':
			request.session["check1"] = 3
			request.session["insp6"] = 3				


		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				request.session["route_1"] = 'kiosk_job_assign'
				return direction(request)
		except:
			dummy = 1
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button2"))
			if kiosk_button1 == -2:
				
				if request.session["kiosk_menu_screen"] == 1:
					request.session["route_1"] = 'kiosk'
					
				else:
					request.session["route_1"] = 'kiosk_menu'
				return direction(request)
		except:
			dummy = 1

		# Finished and reroute

		# Check if clock number is already assigned or not a valid clock number
		if kiosk_clock == "":
			request.session["route_1"] = 'kiosk_error_badclocknumber'
			return direction(request)
		#Assigned already Check
		ch = 0
		
		
		# Commented out the check to see if someone is in kiosk and not signed out
#		try:
#			TimeOut = -1
#			sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
#			cur.execute(sql)
#			tmp2 = cur.fetchall()
#			tmp1 = tmp2[0]
#			ch = 1
#		except:
#			ch = 0
#		if ch == 1:
#			request.session["route_1"] = 'kiosk_error_assigned_clocknumber'
#			return direction(request)
#       End of section to check if someone is in kiosk and not signed out.

	

			
		# Check if any entry was one with a non numerical value.  If so reroute back to reset kiosk job assign
		job_empty = 0
		
		J = ['343' for x in range(6)]
		
		
	#	try:
		if kiosk_job1 !="":
			job_empty = 1
			request.session["kiosk_job1"] = (kiosk_job1)
			J[0] = kiosk_job1
		if kiosk_job2 !="":
			job_empty = 1
			request.session["kiosk_job2"] = (kiosk_job2)
			J[1] = kiosk_job2
		if kiosk_job3 !="":
			job_empty = 1
			request.session["kiosk_job3"] = (kiosk_job3)
			J[2] = kiosk_job3
		if kiosk_job4 !="":
			job_empty = 1
			request.session["kiosk_job4"] = (kiosk_job4)
			J[3] = kiosk_job4
		if kiosk_job5 !="":
			job_empty = 1
			request.session["kiosk_job5"] = (kiosk_job5)
			J[4] = kiosk_job5
		if kiosk_job6 !="":
			job_empty = 1
			request.session["kiosk_job6"] = (kiosk_job6)
			J[5] = kiosk_job6
			
			# Assign the request variables so they're stored upon transfer to other module
		request.session["kiosk_clock"] = kiosk_clock
		request.session["kiosk_job1"] = kiosk_job1
		request.session["kiosk_job2"] = kiosk_job2
		request.session["kiosk_job3"] = kiosk_job3
		request.session["kiosk_job4"] = kiosk_job4
		request.session["kiosk_job5"] = kiosk_job5
		request.session["kiosk_job6"] = kiosk_job6
		request.session["furnace"] = 'none'
			
		job_chk = 0
		try:
			dummy = 1
#				TimeOut = -1
			for i in range(0,5):
				request.session["kiosk_error"] = J[i]
#				sql = "SELECT * FROM vw_asset_eam_lp WHERE left(Asset,4) = '%s'" %(J[i])
#				cur.execute(sql)
#				tmp2 = cur.fetchall()
#				tmp1 = tmp2[0]
#				ch = 1
#			except:
#				ch = 0

	
			
			
		except:
			request.session["route_1"] = 'kiosk_error_badjobnumber'
			return direction(request)
#			request.session["route_1"] = 'kiosk_error_badjobnumber'
#			return direction(request)
		if job_empty == 0:
			request.session["route_1"] = 'kiosk_error_badjobnumber'
			return direction(request)
		# ***************************************************************************************************

		if kiosk_job1[:1] == '3':
			request.session["route_1"] = 'kiosk_job_furnace'
			return direction(request)
		if kiosk_job2[:1] == '3':
			request.session["route_1"] = 'kiosk_job_furnace'
			return direction(request)
		if kiosk_job3[:1] == '3':
			request.session["route_1"] = 'kiosk_job_furnace'
			return direction(request)
		if kiosk_job4[:1] == '3':
			request.session["route_1"] = 'kiosk_job_furnace'
			return direction(request)
		if kiosk_job5[:1] == '3':
			request.session["route_1"] = 'kiosk_job_furnace'
			return direction(request)
		if kiosk_job6[:1] == '3':
			request.session["route_1"] = 'kiosk_job_furnace'
			return direction(request)
		return kiosk_job_assign_enter(request)

	else:
		form = kiosk_dispForm3()
		
	


	#sql = "SELECT left(Asset,4) FROM vw_asset_eam_lp"
	sql = "SELECT asset FROM tkb_cycletime"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp
	db.close()
	request.session["tmp"] = tmp


#	sql = "SELECT left(Asset,4) FROM vw_asset_eam_lp"
#	cur.execute(sql)
#	tmp = cur.fetchall()
#	tmp2 = tmp
	
	tmp = request.session["tmp"]
	
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	return render(request, "kiosk/kiosk_job_assign.html",{'tmp':tmp,'args':args})

def kiosk_job_furnace(request):
	if request.POST:
		kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
		if kiosk_button1 == -1:
			furnace = ''
		elif kiosk_button1 == -2:
			furnace = 's'
		else:
			furnace = 'u'
		request.session["furnace"] = furnace
		return kiosk_job_assign_enter(request)
	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request, "kiosk/kiosk_job_furnace.html",{'args':args})

def kiosk_error_badjobnumber(request):
	request.session["route_1"] = 'kiosk_job_assign'
	return render(request, "kiosk/kiosk_error_badjobnumber.html")
def kiosk_error_badclocknumber(request):
	request.session["route_1"] = 'kiosk_job_assign'
	return render(request, "kiosk/kiosk_error_badclocknumber.html")
def kiosk_error_assigned_clocknumber(request):
	request.session["route_1"] = 'kiosk_job_assign'
	return render(request, "kiosk/kiosk_error_assigned_clocknumber.html")

def kiosk_job_assign_enter(request):
	
	request.session["debug_start"] = time.time()

	db, cur = db_set(request)
	
	# Make the table if it's never been created
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_kiosk(Id INT PRIMARY KEY AUTO_INCREMENT,Clock INT(30), TimeStamp_In Int(20), TimeStamp_Out Int(20), Job1 CHAR(30), Job2 CHAR(30) , Job3 CHAR(30) , Job4 CHAR(30) , Job5 CHAR(30) , Job6 CHAR(30) )""")
	# Use below line as a break point to check things out
	#return render(request, "kiosk/kiosk_test.html")
	kiosk_clock = request.session["kiosk_clock"]
	kiosk_job1 = request.session["kiosk_job1"]
	kiosk_job2 = request.session["kiosk_job2"]
	kiosk_job3 = request.session["kiosk_job3"]
	kiosk_job4 = request.session["kiosk_job4"]
	kiosk_job5 = request.session["kiosk_job5"]
	kiosk_job6 = request.session["kiosk_job6"]
	TimeOut = -1

	# Set whether TPM Check needs to be done in seesion variable tpm'n'
	furnace_check = 0
	try:
		if request.session['furnace'] in ('u','s'):
			furnace_check = 1
	except:
		furnace_check = 0

	sql = "SELECT COUNT(Asset) FROM quality_tpm_assets WHERE Asset = '%s'" %(kiosk_job1+".0")
	cur.execute(sql)
	tmp2 = cur.fetchall()
	request.session['tpm1'] = int(tmp2[0][0])
	sql = "SELECT COUNT(Asset) FROM quality_tpm_assets WHERE Asset = '%s'" %(kiosk_job2+".0")
	cur.execute(sql)
	tmp2 = cur.fetchall()
	request.session['tpm2'] = int(tmp2[0][0])
	sql = "SELECT COUNT(Asset) FROM quality_tpm_assets WHERE Asset = '%s'" %(kiosk_job3+".0")
	cur.execute(sql)
	tmp2 = cur.fetchall()
	request.session['tpm3'] = int(tmp2[0][0])
	sql = "SELECT COUNT(Asset) FROM quality_tpm_assets WHERE Asset = '%s'" %(kiosk_job4+".0")
	cur.execute(sql)
	tmp2 = cur.fetchall()
	request.session['tpm4'] = int(tmp2[0][0])
	sql = "SELECT COUNT(Asset) FROM quality_tpm_assets WHERE Asset = '%s'" %(kiosk_job5+".0")
	cur.execute(sql)
	tmp2 = cur.fetchall()
	request.session['tpm5'] = int(tmp2[0][0])
	sql = "SELECT COUNT(Asset) FROM quality_tpm_assets WHERE Asset = '%s'" %(kiosk_job6+".0")
	cur.execute(sql)
	tmp2 = cur.fetchall()
	request.session['tpm6'] = int(tmp2[0][0])
	# Adjust if it was furnace unload or supply
	if (kiosk_job1[:1] == '3' and furnace_check == 1) : request.session['tpm1'] = 0 
	if (kiosk_job2[:1] == '3' and furnace_check == 1) : request.session['tpm2'] = 0 
	if (kiosk_job3[:1] == '3' and furnace_check == 1) : request.session['tpm3'] = 0 
	if (kiosk_job4[:1] == '3' and furnace_check == 1) : request.session['tpm4'] = 0 
	if (kiosk_job5[:1] == '3' and furnace_check == 1) : request.session['tpm5'] = 0 
	if (kiosk_job6[:1] == '3' and furnace_check == 1) : request.session['tpm6'] = 0 


	TimeStamp = int(time.time())
	cur.execute('''INSERT INTO tkb_kiosk(Clock,Job1,Job2,Job3,Job4,Job5,Job6,TimeStamp_In,TimeStamp_Out) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (kiosk_clock,kiosk_job1,kiosk_job2,kiosk_job3,kiosk_job4,kiosk_job5,kiosk_job6,TimeStamp,TimeOut))
	db.commit()
	db.close()
	
	request.session["current_clock"] = kiosk_clock
	request.session["bounce"] = 0
	request.session["route_1"] = 'kiosk_production' # enable when ready to run

	return direction(request)
			
			
#	request.session["route_1"] = 'kiosk'
#	return direction(request)

def kiosk_job_leave(request):

	if request.POST:
		kiosk_clock = request.POST.get("clock")
		
		# Assign the request variables so they're stored upon transfer to other module
		request.session["kiosk_clock"] = kiosk_clock
		return kiosk_job_leave_enter(request)
	else:
		form = kiosk_dispForm3()

	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request, "kiosk/kiosk_job_leave.html",{'args':args})

def kiosk_job_leave_enter(request):
	db, cur = db_set(request)
	# Make the table if it's never been created
	
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_kiosk(Id INT PRIMARY KEY AUTO_INCREMENT,Clock INT(30), TimeStamp_In Int(20), TimeStamp_Out Int(20), Job1 CHAR(30), Job2 CHAR(30) , Job3 CHAR(30) , Job4 CHAR(30) , Job5 CHAR(30) , Job6 CHAR(30) )""")
	
	kiosk_clock = request.session["kiosk_clock"]
	
	TimeOut = -1
	#sql = "SELECT * FROM tkb_kiosk WHERE Clock = '%s' and TimeStamp_Out = '%s'" %(kiosk_clock,TimeOut)
	#cur.execute(sql)
	#tmp2 = cur.fetchall()
	#tmp1 = tmp2[0]

	#return render(request, "kiosk/kiosk_test.html",{'tmp':tmp})
	
	TimeStamp = int(time.time())
	cql = ('update tkb_kiosk SET TimeStamp_Out = "%s" WHERE Clock ="%s" and TimeStamp_Out = "%s"' % (TimeStamp,kiosk_clock,TimeOut))
	cur.execute(cql)
	db.commit()
	db.close()
	
	
	request.session["route_1"] = 'kiosk'
	return direction(request)

def tenr_fix2(request):
	db, cur = db_set(request)
	id1 = 418767
	part1 = '50-9341'
	asset = '1502'
	
	
	
	hql = "SELECT MAX(Id) FROM sc_production1 where partno = '%s'" %(part1)
	cur.execute(hql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	tmp3 = tmp2[0]
	
	
	request.session["testvariable1"] = tmp3
	request.session["testvariable2"] = id1
	
	sql = "SELECT * FROM sc_production1 WHERE Id >= '%d' and Id<= '%d' and partno = '%s'" %(id1,tmp3,part1)
	cur.execute(sql)
	tmp2 = cur.fetchall()
	tmp1 = tmp2[0]
	
	for i in tmp2:
		asset1 = i[1]
		runtime1 = i[12]
		id1 = i[0]

		try:
			sql = "SELECT cycletime FROM tkb_cycletime WHERE asset = '%s' and part = '%s'" %(asset1,part1)
			cur.execute(sql)
			tmp = cur.fetchall()
			tmpp = tmp[0]
			ct = tmpp[0]
			
			target1 = (runtime1 * 60 * 60) / ct
			
			cql = ('update sc_production1 SET target = "%s" WHERE Id ="%s"' % (target1,id1))
			cur.execute(cql)
			db.commit()
			

		except:
			dummy = 2

	return render(request, "done_update.html")
	
def tenr_fix3(request):
	# new
	prt = ['50-5128','50-5145','50-5132']

	db, cur = db_set(request)
	id1 = 437584
	
	for j in range (0,3):
		id1 = 437584
		part1 = prt[j]
		asset = '788'
#		if j == 2 :
#			return render(request, "done_update.html",{'temp1':part1})
		hql = "SELECT MAX(Id) FROM sc_production1 where partno = '%s'" %(part1)
		cur.execute(hql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		tmp3 = tmp2[0]

		sql = "SELECT * FROM sc_production1 WHERE Id >= '%d' and Id<= '%d' and partno = '%s'" %(id1,tmp3,part1)
		cur.execute(sql)
		tmp2 = cur.fetchall()
		tmp1 = tmp2[0]

		for i in tmp2:
			asset1 = i[1]
			id1 = i[0]

			try:
				sql = "SELECT machine FROM tkb_cycletime WHERE asset = '%s'" %(asset1)
				cur.execute(sql)
				tmp = cur.fetchall()
				tmpp = tmp[0]
				ct = tmpp[0]
				cql = ('update sc_production1 SET machine = "%s" WHERE Id ="%s"' % (ct,id1))
				cur.execute(cql)
				db.commit()
			except:
				dummy = 2

	return render(request, "done_update.html")
	
def tenr_fix(request):
	db, cur = db_set(request)
	id1 = 438347
	p1 = '50-9341'
	sh1 = '01-10R'
	
	
	
	cql = ('update sc_production1 SET sheet_id = "%s" WHERE partno ="%s" and id > "%s"' % (sh1,p1,id1))
	cur.execute(cql)
	db.commit()
	
	
	#trg1 = 0
	#m1 = 'OP30'
	#cql = ('update sc_production1 SET target = "%s" WHERE partno ="%s" and id > "%s" and machine = "%s"' % (trg1,p1,id1,m1))
	#cur.execute(cql)
	#db.commit()
	
	

	return render(request, "done_update.html")


def manpower_layout(request):

	db, cur = db_set(request)
	TimeOut = -1
	id_limit = 211738
	part = '50-9341'
	sql = "SELECT DISTINCT asset_num,machine FROM sc_production1 WHERE partno = '%s' and id > '%s' ORDER BY %s %s " %(part,id_limit,'machine','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()
	
	TimeOut = -1
	mql = "SELECT Clock,Job1,Job2,Job3,Job4,Job5,Job6 FROM tkb_kiosk WHERE TimeStamp_Out = '%s'" %(TimeOut)
	cur.execute(mql)
	tmp2 = cur.fetchall()
	
	J = [[] for x in range(len(tmp))]
	ctr = 0
	for i in tmp:
		J[ctr].append(i[0])
		a = '---'
		
		for ii in tmp2:
			if ii[1] == i[0]:
				J[ctr].append(ii[0])
			else:
				J[ctr].append(a)
		ctr = ctr + 1
	
	return render(request, "kiosk/kiosk_test.html",{'tmp':J})
	
	
def manual_entry(request):	

	if request.POST:
        			
		asset_num = request.POST.get("asset_num")
		machine = request.POST.get("machine")
		priority = request.POST.get("priority")
		whoisonit = request.session["whoisonit"]
		partno = "50-6175"
		target = 215
		
		
		
		
		# call external function to produce datetime.datetime.now()
		createdtime = vacation_temp()
		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		cur.execute('''INSERT INTO sc_production1(asset_num,machine,partno,pdate,shift,shift_hours_length,target,createdtime,updatedtime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (asset_num,machine,partno,pdate,shift,shift_hours_length,target,createdtime,createdtime))
		db.commit()
		db.close()
		
		return done(request)
		
	else:
		#request.session["machinenum"] = "692"
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'manual_entry.html', {'args':args})
	
def entry_recent(request):
	db, cursor = db_set(request)  		
	sql = "SELECT * FROM sc_production ORDER BY id DESC limit 50" 
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close
	machine="Recent Machine Breakdowns"
	request.session["machine_search"] = machine
	request.session["tech_display"] = 1
	return render(request,"entry_recent_display.html",{'machine':tmp})
	

def manual_cycletime_table(request):
	
	db, cur = db_set(request)
	
	# Make the table if it's never been created
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_cycletime(Id INT PRIMARY KEY AUTO_INCREMENT,asset CHAR(30), timest Int(20), cycletime Int(20))""")


	db.commit()
	db.close()
	
	return render(request, "kiosk/kiosk_test.html")

def kiosk_sub_menu(request):
	if request.POST:
		button1 = request.POST
		bp1 = int(button1.get("kiosk_button1"))
		
		if bp1 == -1:
			pcell = 'TRI'
			hourly_title = 'Hourly Trilobe'
		if bp1 == -2:
			pcell = '10ROP30'
			hourly_title = 'Hourly 10ROP30'
		if bp1 == -3:
			pcell = '10R'
			hourly_title = 'Hourly 10R'
		if bp1 == -4:
			pcell = '9HP'
			hourly_title = 'Hourly 9HP'
		if bp1 == -5:
			pcell = '6LOutput'
			hourly_title = 'Hourly 6L Output'
		if bp1 == -6:
			pcell = 'GF9'
			hourly_title = 'Hourly GF9'
		if bp1 == -7:
			pcell = 'AB1V-INPUT'
			hourly_title = 'Hourly AB1V-Input'
		if bp1 == -8:
			pcell = 'AB1V-REACTION'
			hourly_title = 'Hourly AB1V-Reaction'
		if bp1 == -9:
			pcell = 'AB1V-OVERDRIVE'
			hourly_title = 'Hourly AB1V-Overdrive'


		request.session["pcell"] = pcell
		request.session["hourly_title"] = hourly_title



		request.session["route_1"] = 'kiosk_hourly_entry'
		return direction(request)

		


		
	else:
		form = kiosk_dispForm1()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,"kiosk/kiosk_sub_menu.html",{'args':args})
	
		
def kiosk_menu(request):
	db, cursor = db_set(request) # This just sets the local link and DB 
	db.close()
	request.session["kiosk_menu_screen"] = 2
	request.session["cycletime1"] = 0
	request.session["cycletime2"] = 0
	request.session["cycletime3"] = 0
	request.session["cycletime4"] = 0
	request.session["cycletime5"] = 0
	request.session["cycletime6"] = 0
	request.session["furnace"] = ''
	try:
		test1 = request.session["whiteboard_message"] 
	except:
		request.session["whiteboard_message"] = ""

	if request.POST:
		button_1 = request.POST
		button_pressed =int(button_1.get("kiosk_button1"))
		if button_pressed == -1:  # This is the button for the white board
			try:
				y = request.session["dddd"]
				#request.session["pcell"]
			except:
				# Reroute to the submenu to pick the different cells
				# request.session["route_1"] = 'kiosk_menu'
				request.session["route_1"] = 'kiosk_sub_menu'
				return direction(request)

			#request.session["route_1"] = 'kiosk' # disable when ready to run
			request.session["route_2"] = 2
			request.session["route_3"] = 1
			request.session["route_1"] = 3 # enable when ready to run
			return direction(request)
			
		if button_pressed == -2:  # This is the button for the Production Entry
			request.session["route_3"] = 2
			#request.session["route_1"] = 'kiosk'   #disable when ready to run
			request.session["route_2"] = 2
			kiosk_defaults(request)
			request.session["route_1"] = 'kiosk_job_assign' # enable when ready to run
			# request.session["route_1"] = 'kiosk_name' # enable when ready to run
			return direction(request)

		if button_pressed == -3:
			return render(request, "kiosk/route_1.html")


		if button_pressed == -4:
			return render(request, "kiosk/route_2.html")
			

	else:
		form = kiosk_dispForm1()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	request.session["TCUR"] = int(time.time())
	return render(request,"kiosk/kiosk_menu.html",{'args':args})


def ab1v_manpower(request):

	db, cur = db_set(request)  
	
	cur.execute("""DROP TABLE IF EXISTS tkb_ab1v""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_ab1v(Id INT PRIMARY KEY AUTO_INCREMENT,asset_num CHAR(30), machine CHAR(30), partno CHAR(30), actual_produced Int(20), comments CHAR(30), pdate date, shift CHAR(30)) """)

	id1 = 438221
	pd = '2019-04-00'
	part1 = '50-5145'
	part2 = '50-5132'
	part3 = '50-5128'
	machine1 = 'Cremer Furnace'
	sql = "SELECT * FROM sc_production1 WHERE partno = '%s' or partno = '%s' or partno = '%s'" %(part1,part2,part3)
	cur.execute(sql)
	tmp2 = cur.fetchall()

	for tmp1 in tmp2:
		cur.execute('''INSERT INTO tkb_ab1v(asset_num,machine,partno,actual_produced,comments,pdate,shift) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (tmp1[1],tmp1[2],tmp1[3],tmp1[4],tmp1[9],tmp1[10],tmp1[11]))
		db.commit()
		cday = tmp1[10]

	sql = "SELECT * FROM tkb_ab1v WHERE pdate > '%s' and machine != '%s' ORDER BY %s %s " %(pd,machine1,'pdate','ASC')
	cur.execute(sql)
	tmp2 = cur.fetchall()
	
	cur.execute("""DROP TABLE IF EXISTS tkb_ab1v""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_ab1v(Id INT PRIMARY KEY AUTO_INCREMENT,asset_num CHAR(30), machine CHAR(30), partno CHAR(30), actual_produced Int(20), comments CHAR(30), pdate date, shift CHAR(30)) """)


	for tmp1 in tmp2:
		day1 = tmp1[6]
		if tmp1[2] == "OP_Insp":
			total1 = tmp1[4]
		elif tmp1[2][:4] == 'OP10' :
			total1 = tmp1[4]
		
		else:
			total1 = 0
		if tmp1[2] == 'OP100':
			total1 = 0
		comments = tmp1[4]

		cur.execute('''INSERT INTO tkb_ab1v(asset_num,machine,partno,actual_produced,comments,pdate,shift) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (tmp1[1],tmp1[2],tmp1[3],total1,comments,tmp1[6],tmp1[7]))
		db.commit()

	db.close()
	return render(request, "done_update.html")

def kiosk_hourly_entry(request):
	request.session["hourly_drop"] = 'Hourly Trilobe'
	current_first, shift  = vacation_set_current5()
#	request.session["pcell"] = '10ROP30'

	if request.POST:
		kiosk_hourly_clock = request.POST.get("clock")
		try:
			kiosk_button1 = int(request.POST.get("kiosk_assign_button1"))
			if kiosk_button1 == -1:
				if request.session["kiosk_menu_screen"] == 1:
					request.session["route_1"] = 'kiosk'
				else:
					request.session["route_1"] = 'kiosk_menu'
				return direction(request)
		except:
			dummy = 1

		request.session["kiosk_hrs"] = 1

		kiosk_hourly_pcell = request.session["pcell"]

		#if request.session["pcell"] == "AB1V-INPUT":
	#		kiosk_hourly_pcell = request.POST.get("pcell")

		kiosk_hourly_date = request.POST.get("date_en")
		kiosk_hourly_shift = request.POST.get("shift")
		kiosk_hourly_clock = request.POST.get("clock")
		kiosk_hourly_hour = request.POST.get("hrs")
		kiosk_hourly_qty = request.POST.get("qty")
		kiosk_hourly_dtcode = request.POST.get("dtcode")
		kiosk_hourly_dtmin = request.POST.get("dtmin")
		kiosk_hourly_dtreason = request.POST.get("dtreason")

		# Easter Egg:  If you enter -2 for parts made (qty) then it takes Downtime Reason (dtreason) 
		# as the new kiosk_id then reverts back to main Kiosk Screen
		if int(kiosk_hourly_qty) == -2:
			request.session["kiosk_id"] = kiosk_hourly_dtreason
			request.session["route_1"] = 'kiosk_menu'
			return direction(request)


		
		# Store the data in request variables so we can reroute
		request.session["kiosk_hourly_pcell"] = kiosk_hourly_pcell
		request.session["kiosk_hourly_clock"] = kiosk_hourly_clock
		request.session["kiosk_hourly_date"] = kiosk_hourly_date
		request.session["kiosk_hourly_shift"] = kiosk_hourly_shift
		request.session["kiosk_hourly_hour"] = kiosk_hourly_hour
		request.session["kiosk_hourly_qty"] = kiosk_hourly_qty
		request.session["kiosk_hourly_dtcode"] = kiosk_hourly_dtcode
		request.session["kiosk_hourly_dtmin"] = kiosk_hourly_dtmin
		request.session["kiosk_hourly_dtreasonq"] = kiosk_hourly_dtreason

		kiosk_hourly_target = 1
		shift_target = 1
		shift_actual = 1
		shift_time = "None"
		sheet_id = 'kiosk'

		db, cur = db_set(request)
		stopp = "None"
		hr_var = int(kiosk_hourly_hour) # Set current hour looking at
		# try: # Check if there's an entry for this one already
		# 	hr_check = hr_var
		# 	sql = "SELECT * FROM sc_prod_hour WHERE p_cell = '%s' and p_date = '%s' and p_shift = '%s' and p_hour = '%s'" %(kiosk_hourly_pcell,kiosk_hourly_date,kiosk_hourly_shift,hr_check)
  		# 	cur.execute(sql)
  		# 	tmp2 = cur.fetchall()
		# 	tmp3 = tmp2[0]
		# 	stopp = "Duplicate"
		# except:
		# 	dummy = 1

		try: # Check if there's earlier entries
			hr_check = hr_var -1
			sql = "SELECT * FROM sc_prod_hour WHERE p_cell = '%s' and p_date = '%s' and p_shift = '%s' and p_hour = '%s'" %(kiosk_hourly_pcell,kiosk_hourly_date,kiosk_hourly_shift,hr_check)
  			cur.execute(sql)
  			tmp2 = cur.fetchall()
			tmp3 = tmp2[0]
			stopp = "Earlier 1"
		except:
			dummy = 1

		# y = request.session["dkdd"]
		request.session["whiteboard_message"] = ""
		try:
			cur.execute('''INSERT INTO sc_prod_hour(p_cell,initial,p_date,p_shift,p_hour,hourly_actual,downtime_code,downtime_mins,downtime_reason) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (kiosk_hourly_pcell,kiosk_hourly_clock,kiosk_hourly_date,kiosk_hourly_shift,kiosk_hourly_hour,kiosk_hourly_qty,kiosk_hourly_dtcode,kiosk_hourly_dtmin,kiosk_hourly_dtreason))
			db.commit()
		except:
			dummy = 1
			request.session["whiteboard_message"] = "duplicate"
		db.close()

	
	#	Below will route to Kiosk Main if it's a joint ipad or kiosk if it's a lone one
		if request.session["kiosk_menu_screen"] == 1:
			request.session["route_1"] = 'kiosk'
		else:
			request.session["route_1"] = 'kiosk_menu'
		return direction(request)

	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  
	
	tcur=int(time.time())

	p_cell = request.session["pcell"]

	db, cur = db_set(request)
	s1 = "SELECT MAX(id)  FROM sc_prod_hour WHERE p_cell = '%s'" %(p_cell) 
	cur.execute(s1)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	tmp3 = tmp2[0]

	s2 = "SELECT * From sc_prod_hour WHERE id = '%s'" %(tmp3) 
	cur.execute(s2)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	tmp3 = tmp2[2]


	request.session["clock"] = tmp3

	# Below will set hrs , shift and date to current one using 30min past hour as flip point
	hrs, shift2, current_first = vacation_set_current77()

	# hrs = int(tmp2[6])
	# hrs = hrs + 1
	# hrs = ah


	# if hrs > 8:
	# 	if request.session["hourly_title"] == 'Hourly Trilobe':
	# 		if hrs > 12:
	# 			hrs = 1
	# 	else:
	# 		hrs = 1

	request.session["hrs"] = str(hrs)
	kiosk_hourly_shift = tmp2[5]
	#h = request.session["bugbug"]

	request.session["shift"] = tmp2[5]
	request.session["shift"] = shift2
#	if kiosk_hourly_shift=="4D":
#		request.session["shift"] = "Day"
#	elif kiosk_hourly_shift == "3N":
#		request.session["shift"] = "Mid"
#	elif kiosk_hourly_shift == "2CD":
#		request.session["shift"] = "Day"
#	elif kiosk_hourly_shift == "5A":
#		request.session["shift"] = "Aft"
	db.close()


	return render(request, "kiosk/kiosk_hourly_entry.html",{'args':args,'TCUR':tcur,'Curr':current_first})

def tenr1(request):
	request.session["pcell"] = '10ROP30'
	request.session["hourly_title"] = 'Hourly 10ROP30'
	request.session["mgmt_login_password"] = 'bort'
	request.session["mgmt_login_name"] = 'Dave'
	return render(request, "done_update2.html")
def trilobe(request):
	request.session["pcell"] = 'TRI'
	request.session["hourly_title"] = 'Hourly Trilobe'
	request.session["kiosk_label"] = 'B'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")
def tenr2(request):
	request.session["pcell"] = '10R'
	request.session["hourly_title"] = 'Hourly 10R'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")

def kiosk_initial_6L_Output(request):
	request.session["pcell"] = '6LOutput'
	request.session["hourly_title"] = 'Hourly 6L Output'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")	
def kiosk_initial_9HP(request):
	request.session["pcell"] = '9HP'
	request.session["hourly_title"] = 'Hourly 9HP'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")	
def kiosk_initial_6L_IN(request):
	request.session["pcell"] = '6L_IN'
	request.session["hourly_title"] = 'Hourly 6L Input'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")	
def kiosk_initial_GF9(request):
	request.session["pcell"] = 'GF9'
	request.session["hourly_title"] = 'Hourly GF9'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")	
def kiosk_initial_AB1V(request):
	request.session["pcell"] = 'AB1V-INPUT'
	request.session["hourly_title"] = 'Hourly AB1V'
	request.session["mgmt_login_password"] = 'boob'
	request.session["mgmt_login_name"] = 'Dean'
	return render(request, "done_update2.html")	

def error_hourly_duplicate(request):
	return render(request, "error_hourly_duplicate.html")	

def kiosk_fix55(request):
	ts = 1562849834
	ty = -1
	db, cur = db_set(request)
	cql = ('update tkb_kiosk SET TimeStamp_Out = "%s" WHERE TimeStamp_Out ="%s"' % (ts,ty))
	cur.execute(cql)
	db.commit()
	return render(request, "error_hourly_duplicate.html")	

def kiosk_manual(request):
	request.session["kiosk_type"] = "manual"
	request.session["route_1"] = 'kiosk_menu'
	return direction(request)
def kiosk_kiosk(request):
	request.session["kiosk_type"] = "kiosk"
	request.session["route_1"] = 'kiosk_menu'
	return direction(request)


def kiosk_fix44(request):
	db, cur = db_set(request)
	ml = 4
	id1 = 475199

	s1 = "SELECT * From sc_production1 WHERE length(partno) < '%s' and id > '%d'" %(ml,id1)
	# s1 = "SELECT MAX(id)  FROM sc_prod_hour WHERE p_cell = '%s'" %(p_cell) 
	cur.execute(s1)
	tmp = cur.fetchall()
	

	for i in tmp:
		machine1 = i[1]
		id2 = i[0]
		prt1 = kiosk_lastpart_find (machine1)
		cql = ('update sc_production1 SET partno = "%s" WHERE id ="%d"' % (prt1,id2))
		cur.execute(cql)
		db.commit()
	db.close()



	# request.session["tmp6"] = tmp
	# tmp3 = tmp2[0]

	# s2 = "SELECT * From sc_prod_hour WHERE id = '%s'" %(tmp3) 
	# cur.execute(s2)
	# tmp = cur.fetchall()
	# tmp2 = tmp[0]
	# tmp3 = tmp2[2]
	# uu = request.session["ddss"]


	return render(request, "kiosk/kiosk_test5.html",{'tmp1':tmp})	


def kiosk_help(request):
	db, cursor = db_set(request)  
	closed1 = 0
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_help(Id INT PRIMARY KEY AUTO_INCREMENT,employee CHAR(50), kiosk_id CHAR(50), supervisor CHAR(50), help_message CHAR(100), help_date datetime, closed INT(10) default 0)""")
	db.commit()
	sql = "SELECT * FROM tkb_help WHERE closed = '%d' ORDER BY help_date ASC" %(closed1)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = list(tmp)
	db.close()
	return tmp

def kiosk_help_close(request):    # Close out kiosk help message
	kiosk_help_index = int(request.session['bounce_help_index'])
	kiosk_closed = 1
	db, cursor = db_set(request)  
	cql = ('update tkb_help SET closed = "%s" WHERE Id ="%d"' % (kiosk_closed, kiosk_help_index))
	cursor.execute(cql)
	db.commit()
	db.close()
	request.session['bounce_help'] = 0
	return render(request, "redirect_supervisor.html")

def kiosk_help_form(request):
	# Hard Code Supervisors for now.   Will use a DB List eventually
	supervisors = ['Karl Edwards','Andrew Smith','Scott McMahon','Gary Harvey','Pete Murphy','Raid Biram', 'Scott Brownlee','Ken Frey','Mike Clarke']
	request.session['supervisor_list'] = supervisors
	length_fail = 0
	tmp = kiosk_help(request)  # Retieve unclosed files and initialize table for kiosk_help
	if request.POST:
		help_employee = request.POST.get("help_employee")
		help_supervisor = request.POST.get("help_supervisor")
		help_message = request.POST.get("help_message")

		if len(help_supervisor) < 3 :length_fail = 1
		if len(help_employee) < 1 :length_fail = 1

		if length_fail == 1 : return render(request, "redirect_kiosk_help.html")
		try:
			help_kiosk_id = request.session["kiosk_id"]
		except:
			help_kiosk_id = 'unknown'
		t = vacation_temp()
		db, cursor = db_set(request) 
		cursor.execute('''INSERT INTO tkb_help(employee,supervisor,help_date,kiosk_id,help_message) VALUES(%s,%s,%s,%s,%s)''', (help_employee,help_supervisor,t,help_kiosk_id,help_message))
		db.commit()
		db.close()

		return render(request, "redirect_kiosk.html")
		# return kiosk_help_send(request)

	else:
		form = kiosk_dispForm3()

	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request, "kiosk_help_form.html",{'args':args})

def kiosk_forklift(request):
	db, cursor = db_set(request)  
	closed1 = 0
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_forklift(Id INT PRIMARY KEY AUTO_INCREMENT,employee CHAR(50), kiosk_id CHAR(50), area CHAR(50), message CHAR(100), call_time datetime, received_time datetime, closed TINYINT(10) default NULL,driver CHAR(100))""")
	db.commit()
	sql = "SELECT * FROM tkb_forklift WHERE closed = '%d' ORDER BY call_time ASC" %(closed1)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = list(tmp)
	db.close()
	return tmp

def kiosk_forklift_form(request):
	length_fail = 0
	tmp = kiosk_forklift(request)  # Retieve unclosed files and initialize table for kiosk_help
	if request.POST:
		forklift_employee = request.POST.get("forklift_employee")
		forklift_area = request.POST.get("forklift_area")
		forklift_message = request.POST.get("forklift_message")

		if len(forklift_employee) < 3 :length_fail = 1
		if len(forklift_area) < 3 :length_fail = 1

		if length_fail == 1 : return render(request, "redirect_kiosk_help.html")
		try:
			forklift_kiosk_id = request.session["kiosk_id"]
		except:
			forklift_kiosk_id = 'unknown'
		t = vacation_temp()
		db, cursor = db_set(request) 
		cursor.execute('''INSERT INTO tkb_forklift(employee,kiosk_id,area,message,call_time) VALUES(%s,%s,%s,%s,%s)''', (forklift_employee,forklift_kiosk_id,forklift_area,forklift_message,t))
		db.commit()
		db.close()

		return render(request, "redirect_kiosk.html")
		# return kiosk_help_send(request)

	else:
		form = kiosk_dispForm3()

	args = {}
	args.update(csrf(request))
	args['form'] = form  
	return render(request, "kiosk_forklift_form.html",{'args':args})

def set_test1(request):
	d = 0
	try:
		d = 1
		dummy = request.session["route_a6"] 
	except:
		d = 2
		request.session["route_a6"] = 1


	x = int(request.session["route_a6"])
	x = x + 1
	y = (x % 3) + 1
	request.session["route_a6"] = y

	# re = request.session["jjek"]

	return render(request,"done_update2.html")

# This will be the Scrap Entry section in the Kiosk
def kiosk_scrap(request):
	db, cursor = db_set(request)
	# cursor.execute("""DROP TABLE IF EXISTS tkb_scrap""")   # only uncomment this line if you need to re generate the table structure or start new
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_scrap(Id INT PRIMARY KEY AUTO_INCREMENT,scrap_part CHAR(50),scrap_operation CHAR(50), scrap_category CHAR(50), scrap_amount INT(20), scrap_line CHAR(50), total_cost CHAR(50), date CHAR(50))""")
	db.commit()
	db.close()

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
	return render(request,'kiosk_scrap.html')

def kiosk_scrap_reset(request):
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
	return kiosk_scrap_entry(request)

def kiosk_scrap_finalize(request):
	request.session["scrap_entry"] = 4
	request.session["scrap_part"] = "Part Num:"
	request.session["scrap_operation"] = "Operation:"
	request.session["scrap_category"] = "Category:"
	request.session["scrap_part"] = "Part No:"
	request.session["scrap_amount"] = 0
	request.session["scrap1"] =""
	request.session["scrap2"] ='''disabled="true"'''
	request.session["scrap3"] ='''disabled="true"'''
	request.session["scrap4"] ='''disabled="true"'''
	return kiosk_scrap_entry(request)



	# # This will assign all the values of machines into session variable machine_temp
	# if request.session["scrap_entry"] == 0:
	# 	active = '1.0'
	# 	sql = "SELECT Part FROM scrap_part_line WHERE Active = '%s'" %(active)
	# 	cursor.execute(sql)
	# 	tmp = cursor.fetchall()
	# 	request.session["scrap_part_selection"] = tmp

	# # if request.session["scrap_entry"] == 1:
	# # 	sql1 = "SELECT line FROM scrap_part_line"
	# # 	cursor.execute(sql1)
	# # 	tmp1 = cursor.fetchall()
	# # 	tmp3 = tmp1
	# # 	request.session["machine_operation"] = tmp3


	# # sql2 = "SELECT category FROM scrap_line_operation_category"
	# # cursor.execute(sql2)
	# # tmp4 = cursor.fetchall()
	# # tmp5 = tmp4
	# # request.session["machine_category"] = tmp5 
	# db.close()	
	# # ******************************************************************************


	
	
	# # Use Asset Number  (Machine Number)
	# # Use Job Description (example Sintering, Secondary, Finishing, Compacting)
	# # Use Scrap Description (will use a drop down for this and will be retrieved from Table eventually.  Dropped, Damaged, Oversize, Undersize)
	# # Use Scrap Quantity (amount)

	# # s1 = "SELECT * From sc_production1 WHERE length(partno) < '%s' and id > '%d'" %(ml,id1)

	# # sql = select job_description from scrap_categories where asset_num =  ' %s' %(asset)
	# # cursor.execute(sql)
	# # tmp = cursor.fetchall()
	# # tmp2 = tmp
	# # request.session["description_temp"] = tmp
 
 	# if request.POST:
	# 	scrap_part = request.POST.get("scrap_part")
	# 	scrap_operation = request.POST.get("scrap_operation")
	# 	scrap_category = request.POST.get("scrap_category")
	# 	scrap_amount = request.POST.get("scrap_amount")

	# 	# if asset != request.session["asset"]:
	# 	# 	request.session["scrap_entry"] = 0
	# 	# if job != request.session["job"]:
	# 	# 	request.session["scrap_entry"] = 1
	# 	# if scrap != request.session["scrap"]:
	# 	# 	request.session["scrap_entry"] = 2

	# 	try: 
	# 		if request.session["scrap_entry"] == 0:
	# 			request.session["scrap_part"] = scrap_part
	# 			request.session["scrap_entry"] = 1
	# 			request.session["scrap1"] ='''disabled="true"'''
	# 			request.session["scrap2"] =''
	# 			request.session["scrap3"] ='''disabled="true"'''
	# 			request.session["scrap4"] ='''disabled="true"'''
	# 			request.session["scrap"] = "Scrap Description:"
	# 			request.session["amount"] = "Asset Num:"
	# 			db, cursor = db_set(request)
	# 			sql = "SELECT Line FROM scrap_part_line WHERE Part = '%s'" %(scrap_part)
	# 			cursor.execute(sql)
	# 			tmp = cursor.fetchall()
	# 			scrap_part_line = tmp[0][0]
	# 			request.session["scrap_part_line"] = scrap_part_line

	# 			sql = "SELECT DISTINCT Operation FROM scrap_line_operation_category WHERE Line = '%s'" %(scrap_part_line)
	# 			cursor.execute(sql)
	# 			tmp = cursor.fetchall()
	# 			request.session["scrap_operation_selection"] = tmp
	# 			db.close()
	# 			return render(request, "redirect_kiosk_scrap_entry.html")

	# 		if request.session["scrap_entry"] == 1:
	# 			request.session["scrap_operation"] = scrap_operation
	# 			request.session["scrap_entry"] = 2
	# 			request.session["scrap1"] ='''disabled="true"'''
	# 			request.session["scrap2"] ='''disabled="true"'''
	# 			request.session["scrap3"] =''
	# 			request.session["scrap4"] ='''disabled="true"'''
	# 			line = request.session["scrap_part_line"]
	# 			db, cursor = db_set(request)
	# 			sql = "SELECT Category FROM scrap_line_operation_category WHERE Line = '%s' and Operation ='%s'" %(line,scrap_operation)
	# 			cursor.execute(sql)
	# 			tmp = cursor.fetchall()
	# 			request.session["scrap_category_selection"] = tmp
	# 			return render(request, "redirect_kiosk_scrap_entry.html")

	# 		if request.session["scrap_entry"] == 2:
	# 			request.session["scrap_category"] = scrap_category
	# 			request.session["scrap_entry"] = 3
	# 			request.session["scrap1"] ='''disabled="true"'''
	# 			request.session["scrap2"] ='''disabled="true"'''
	# 			request.session["scrap3"] ='''disabled="true"'''
	# 			request.session["scrap4"] =''
	# 			return render(request, "redirect_kiosk_scrap_entry.html")
			
	# 		# will execute bottom section if all other scrap_entry passes are missed.   ie scrap_entry = 3
	# 		request.session["scrap_amount"] = scrap_amount
	# 		category = request.session["scrap_category"]
	# 		operation = request.session["scrap_operation"]
	# 		part = request.session["scrap_part"]
	# 		amount = scrap_amount
	# 		line = request.session["scrap_part_line"]


	# 		# sql= "SELECT Dept FROM scrap_operation_dept WHERE Operation = '%s'" % (scrap_operation)
	# 		# cursor.execute(sql)
	# 		# tmp = cursor.fetchall()
	# 		# scrap_operation_dept = tmp[0][0]
	# 		# request.session["scrap_operation_dept"] = scrap_operation_dept
	# 		# sql = "SELECT Cost FROM scrap_part_dept_cost WHERE Part = '%s' and Dept = '%s'" %(part,scrap_operation_dept)
	# 		# cursor.execute(sql)
	# 		# cost = cursor.fetchall()
	# 		# request.session["scrap_cost"] = cost
	# 		# ####what goes in here#######
	# 		# cost = cost*amount

	# 		# redid the above attempt.   scrap_operation wasn't assigned.  Need operation
	# 		# cost will need to be retrieved from cursor.fetchall() [0][0].
	# 		# need to assign cost and amount as float variables before multiplying to get total_cost

	# 		db, cursor = db_set(request)
	# 		sql2 = "SELECT Dept FROM scrap_operation_dept WHERE Operation = '%s'" % (operation)
	# 		cursor.execute(sql2)
	# 		tmp = cursor.fetchall()
	# 		department = tmp[0][0]

	# 		sql3 = "SELECT Cost FROM scrap_part_dept_cost WHERE Part = '%s' and Dept = '%s'" % (part,department)
	# 		cursor.execute(sql3)
	# 		tmp = cursor.fetchall()
	# 		try:
	# 			cost = tmp[0][0]
	# 		except: 
	# 			cost = 0

	# 		total_cost = float(cost) * float(amount)

	# 		# date = datetime.datetime.now()
	# 		date = vacation_set_current9()


		
	# 		cursor.execute('''INSERT INTO tkb_scrap(scrap_part,scrap_operation,scrap_category,scrap_amount,scrap_line,total_cost,date) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (part,operation,category,amount,line,total_cost,date))
	# 		db.commit()
	# 		db.close()
			

	# 		# return render(request,"done_update2.html")
	# 		return render(request, "redirect_kiosk_scrap.html")
	# 	except:
	# 		# e = 4/0
	# 		return render(request, "redirect_kiosk_scrap.html")

	# else:
	# 	form = sup_downForm()
	# args = {}
	# args.update(csrf(request))
	# args['form'] = form

	# # return render(request,'kiosk_scrap_entry.html',{'args':args})	
	# return render(request,'kiosk_mult_entries.html')
	# # return kiosk_scrap_entry(request)

def kiosk_scrap_entry(request):




	current_first, shift  = vacation_set_current5()

	db, cursor = db_set(request)
	try:
		dummy = request.session["scrap_entry"]
	except:
		request.session["scrap_entry"] = 1


	# This will assign all the values of machines into session variable machine_temp
	if request.session["scrap_entry"] == 0:
		active = '1.0'
		sql = "SELECT Part FROM scrap_part_line WHERE Active = '%s' ORDER BY Part ASC" %(active)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		request.session["scrap_part_selection"] = tmp

	# if request.session["scrap_entry"] == 1:
	# 	sql1 = "SELECT line FROM scrap_part_line"
	# 	cursor.execute(sql1)
	# 	tmp1 = cursor.fetchall()
	# 	tmp3 = tmp1
	# 	request.session["machine_operation"] = tmp3


	# sql2 = "SELECT category FROM scrap_line_operation_category"
	# cursor.execute(sql2)
	# tmp4 = cursor.fetchall()
	# tmp5 = tmp4
	# request.session["machine_category"] = tmp5 
	db.close()	
	# ******************************************************************************


	
	
	# Use Asset Number  (Machine Number)
	# Use Job Description (example Sintering, Secondary, Finishing, Compacting)
	# Use Scrap Description (will use a drop down for this and will be retrieved from Table eventually.  Dropped, Damaged, Oversize, Undersize)
	# Use Scrap Quantity (amount)

	# s1 = "SELECT * From sc_production1 WHERE length(partno) < '%s' and id > '%d'" %(ml,id1)

	# sql = select job_description from scrap_categories where asset_num =  ' %s' %(asset)
	# cursor.execute(sql)
	# tmp = cursor.fetchall()
	# tmp2 = tmp
	# request.session["description_temp"] = tmp


	


 	if request.POST:
		
		finish_switch=0
		scrap_part = request.POST.get("scrap_part")
		scrap_operation = request.POST.get("scrap_operation")
		scrap_category = request.POST.get("scrap_category")
		scrap_amount = request.POST.get("scrap_amount")
		finish_switch = 0
		scrap_operation=str(scrap_operation)

		try:
			finish_switch = request.POST.get("one")
		except:
			finish_switch = 0
		sse=request.session["scrap_entry"]

		# if asset != request.session["asset"]:
		# 	request.session["scrap_entry"] = 0
		# if job != request.session["job"]:
		# 	request.session["scrap_entry"] = 1
		# if scrap != request.session["scrap"]:
		# 	request.session["scrap_entry"] = 2

#		try: 
		if finish_switch == '1':
			

			request.session["scrap_amount"] = scrap_amount
			if scrap_amount > 0:
				category = request.session["scrap_category"]
				operation = request.session["scrap_operation"]
				part = request.session["scrap_part"]
				amount = scrap_amount
				line = request.session["scrap_part_line"]
				db, cursor = db_set(request)
				sql2 = "SELECT Dept FROM scrap_operation_dept WHERE Operation = '%s'" % (operation)
				cursor.execute(sql2)
				tmp = cursor.fetchall()
				department = tmp[0][0]

				sql3 = "SELECT Cost FROM scrap_part_dept_cost WHERE Part = '%s' and Dept = '%s'" % (part,department)
				cursor.execute(sql3)
				tmp = cursor.fetchall()
				try:
					cost = tmp[0][0]
				except:
					cost = 0
				total_cost = float(cost) * float(amount)
				date = vacation_set_current9()
				cursor.execute('''INSERT INTO tkb_scrap(scrap_part,scrap_operation,scrap_category,scrap_amount,scrap_line,total_cost,date) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (part,operation,category,amount,line,total_cost,date))
				db.commit()
				db.close()
			return render(request, "redirect_kiosk_scrap.html")

		if request.session["scrap_entry"] == 0 and scrap_part[:6] == 'Powder':
			request.session["scrap_entry"] = 2
			request.session["scrap_part"] = scrap_part
			request.session["scrap_operation"] = 'Powder'
			scrap_category = 'Powder'

		if request.session["scrap_entry"] == 0:
			request.session["scrap_part"] = scrap_part
			request.session["scrap_entry"] = 1
			request.session["scrap1"] ='''disabled="true"'''
			request.session["scrap2"] =''
			request.session["scrap3"] ='''disabled="true"'''
			request.session["scrap4"] ='''disabled="true"'''
			request.session["scrap"] = "Scrap Description:"
			request.session["amount"] = "Asset Num:"
			db, cursor = db_set(request)
				

			sql = "SELECT Line FROM scrap_part_line WHERE Part = '%s'" %(scrap_part)
			cursor.execute(sql)
			tmp = cursor.fetchall()
			
			scrap_part_line = tmp[0][0]
			request.session["scrap_part_line"] = scrap_part_line

			sql = "SELECT DISTINCT Operation FROM scrap_line_operation_category WHERE Line = '%s'" %(scrap_part_line)
			cursor.execute(sql)
			tmp = cursor.fetchall()
			request.session["scrap_operation_selection"] = tmp
			db.close()

			return render(request, "redirect_kiosk_scrap_entry.html")

		if request.session["scrap_entry"] == 1:

			request.session["scrap_operation"] = scrap_operation
			request.session["scrap_entry"] = 2
			request.session["scrap1"] ='''disabled="true"'''
			request.session["scrap2"] ='''disabled="true"'''
			request.session["scrap3"] =''
			request.session["scrap4"] ='''disabled="true"'''
			line = str(request.session["scrap_part_line"])

			db, cursor = db_set(request)
			ttt='5'
			request.session['loop1'] = 1
			sql = "SELECT Category FROM scrap_line_operation_category WHERE Line = '%s' and Operation ='%s' and LENGTH(Category) > '%s' ORDER BY Category ASC" %(line,scrap_operation,ttt)
			cursor.execute(sql)
			tmp = cursor.fetchall()

			request.session["scrap_category_selection"] = tmp


	

			return render(request, "redirect_kiosk_scrap_entry.html")

		if request.session["scrap_entry"] == 2:
			request.session["scrap_category"] = scrap_category
			request.session["scrap_entry"] = 3
			request.session["scrap1"] ='''disabled="true"'''
			request.session["scrap2"] ='''disabled="true"'''
			request.session["scrap3"] ='''disabled="true"'''
			request.session["scrap4"] =''
			return render(request, "redirect_kiosk_scrap_entry.html")

		if request.session["scrap_entry"] == 3:
			request.session["scrap_amount"] = scrap_amount
			request.session["scrap_entry"] = 2
			request.session["scrap1"] ='''disabled="true"'''
			request.session["scrap2"] ='''disabled="true"'''
			request.session["scrap3"] =''
			request.session["scrap4"] ='''disabled="true"'''
			category = request.session["scrap_category"]
			operation = request.session["scrap_operation"]
			part = request.session["scrap_part"]
			amount = scrap_amount
			line = request.session["scrap_part_line"]
			db, cursor = db_set(request)
			sql2 = "SELECT Dept FROM scrap_operation_dept WHERE Operation = '%s'" % (operation)
			cursor.execute(sql2)
			tmp = cursor.fetchall()
			department = tmp[0][0]

			sql3 = "SELECT Cost FROM scrap_part_dept_cost WHERE Part = '%s' and Dept = '%s'" % (part,department)
			cursor.execute(sql3)
			tmp = cursor.fetchall()
			try:
				cost = tmp[0][0]
			except:
				cost = 0
			total_cost = float(cost) * float(amount)
			date = vacation_set_current9()
			cursor.execute('''INSERT INTO tkb_scrap(scrap_part,scrap_operation,scrap_category,scrap_amount,scrap_line,total_cost,date) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (part,operation,category,amount,line,total_cost,date))
			db.commit()
			db.close()

			return render(request, "redirect_kiosk_scrap_entry.html")

		if request.session["scrap_entry"] == 4:
			request.session["scrap_amount"] = scrap_amount
			category = request.session["scrap_category"]
			operation = request.session["scrap_operation"]
			part = request.session["scrap_part"]
			amount = scrap_amount
			line = request.session["scrap_part_line"]
			db, cursor = db_set(request)
			sql2 = "SELECT Dept FROM scrap_operation_dept WHERE Operation = '%s'" % (operation)
			cursor.execute(sql2)
			tmp = cursor.fetchall()
			department = tmp[0][0]

			sql3 = "SELECT Cost FROM scrap_part_dept_cost WHERE Part = '%s' and Dept = '%s'" % (part,department)
			cursor.execute(sql3)
			tmp = cursor.fetchall()
			try:
				cost = tmp[0][0]
			except:
				cost = 0
			total_cost = float(cost) * float(amount)
			date = vacation_set_current9()
			cursor.execute('''INSERT INTO tkb_scrap(scrap_part,scrap_operation,scrap_category,scrap_amount,scrap_line,total_cost,date) VALUES(%s,%s,%s,%s,%s,%s,%s)''', (part,operation,category,amount,line,total_cost,date))
			db.commit()
			db.close()
			return render(request, "redirect_kiosk_scrap.html")
			
		return render(request, "redirect_kiosk_scrap.html")
#		except:
			
#			return render(request, "redirect_kiosk_scrap.html")

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'kiosk_scrap_entry.html',{'args':args})

def shift_select(shift):
	shift4 = ''
	if shift == 'Plant 1 Days' or shift == 'Plant 3 Days' or shift == 'Plant 4 Day':
		shift4 = '7am-3pm'
	if shift == 'Plant 1 Mid' or shift == 'Plant 3 Mid' or shift == 'Plant 4 Mid':
		shift4 = '11pm-7am'
	if shift == 'Plant 1 Aft' or shift == 'Plant 3 Aft' or shift == 'Plant 4 Aft':
		shift4 = '3pm-11pm'
	return shift4


def production_entry_check(request):
	date1, shift2 = vacation_set_current5()

	# Comment below line when running from server update program
	# request.session['tkb_update_date'] = '2021-01-15' # Put this in temporarily to force check

	date1 = request.session['tkb_update_date']  # Date is date from update program
	shift = request.session['variable1']  # The shift is retrieved from updater table

	# dw between 0 and 4 for weekday if not reroute back to auto_updater
	dt = datetime.datetime.strptime(date1, '%Y-%m-%d')
	dt2 = time.mktime(dt.timetuple())
	dt3 = time.localtime(dt2)
	dw = dt3[6]
	if dw > 4:
		return render(request,"redirect_auto_updater.html")  # This will actually go back to updater on final product

	# shift = 'Plant 1 Days'
	# shift = request.session["variable1"]
	
	request.session['date_prod'] = date1
	request.session['shift_prod'] = shift
	status3 = 'Pending'
	status4 = 'No Entry'
	status5 = 'Good'

	# shift = request.session["production_shift"]
	shift4 = shift_select(shift)

	# production_duplicate_fix(request,date1)

	db, cur = db_set(request)

	# Delete Assets we don't use or track from allocation
	asset9 = ['1542','859','1514','1531','1541','1509','594','650','215','274']
	for b in asset9:
		dql = ('DELETE FROM sc_production1 WHERE asset_num = "%s"' %(b))
		cur.execute(dql)
		db.commit()

	# cur.execute("""DROP TABLE IF EXISTS tkb_scheduled""")
	# cur.execute("""CREATE TABLE IF NOT EXISTS tkb_scheduled(Id INT PRIMARY KEY AUTO_INCREMENT,timestamp CHAR(80), dummy int(10))""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_scheduled(Id INT PRIMARY KEY AUTO_INCREMENT,Id1 Char(80),Date1 Char(80), Employee CHAR(80), Clock CHAR(80), Asset CHAR(80), Job CHAR(80), Part CHAR(80), Shift Char(80), Hrs Char(80),Status Char(80),Shift_Mod Char(80))""")
	# This will have to be tweaked for continental of who is working.
	# maybe some type of calander calculator 


	# The below section should recheck the pending people to see if they've updated
	sql="SELECT * FROM tkb_scheduled where (Status='%s' and Shift= '%s')" % (status3,shift)
	cur.execute(sql)
	tmp_all = cur.fetchall()
	for i in tmp_all:
		clock7 = i[4]
		date7 = i[2]
		sql_count= "SELECT COUNT(*) FROM sc_production1 where comments = '%s' and pdate ='%s'" % (clock7,date7)
		cur.execute(sql_count)
		tmp7= cur.fetchall()
		count7 = int(tmp7[0][0])
		if count7 > 0 :
			cql = ('update tkb_scheduled SET Status = "%s" WHERE (Clock="%s" and Date1 = "%s")' % (status5,clock7,date7))
			cur.execute(cql)
			db.commit()
		else:
			cql = ('update tkb_scheduled SET Status = "%s" WHERE (Clock="%s" and Date1 = "%s")' % (status4,clock7,date7))
			cur.execute(cql)
			db.commit()

	# Right now it just makes them No Entry again
	cql = ('update tkb_scheduled SET Status = "%s" WHERE (Status="%s" and Shift = "%s")' % (status4,status3,shift))
	cur.execute(cql)
	db.commit()

	sql = "SELECT * FROM tkb_manpower where Shift = '%s'" %(shift)
	cur.execute(sql)
	tmp_all = cur.fetchall()  # List of all current employees on the shift

# Determine which Continental Shift to use and assign to shift_mod3
	cshift4 = 'none'
	break4 = 0
	for i in tmp_all:
		clock4 = i[3][:-2]
		if i[2] != i[4]:
			try:
				sql_cont = "SELECT * FROM sc_production1 where pdate = '%s' and comments = '%s'" % (date1,clock4)
				cur.execute(sql_cont)
				tmp_all_4 = cur.fetchall()
				tmp_all_42 = tmp_all_4[0]
				cshift4 = i[4]
				break4 = 1
			except:
				dummy = 1
		if break4 == 1:
			break

	sql = "SELECT * FROM tkb_manpower where Shift_Mod = '%s' or Shift_Mod = '%s'" %(shift,cshift4)
	cur.execute(sql)
	tmp = cur.fetchall()  # List of all current employees on the shift including proper Continental

	name1 =[]
	clock1 =[]
	job1 = []
	part1 = []
	hrs1 = []
	name_good = []
	clock_good = []
	job_good = []
	part_good = []
	hrs_good = []
	count_good = []
	asset_good = []
	part_qty = []

	flow1 = 'go'
	for i in tmp:
		r=0
		hrs_verify = 8
		if i[2] != i[4]:
			hrs_verify = 8  # Change this to 12 once we figure out Continental 

		cur.execute("""DROP TABLE IF EXISTS tkb_scheduled_temp""")
		cur.execute("""CREATE TABLE IF NOT EXISTS tkb_scheduled_temp(Id INT PRIMARY KEY AUTO_INCREMENT,Id1 CHAR(80), Employee CHAR(80),Clock CHAR(80), Asset Char(80), Job Char(80), Part Char(80), Hrs Int(10), Qty Int(10),Shift_Mod Char(80))""")
		db.commit()
		nm = i[1]
		shift_mod = i[4]
		job7 = []
		qty7 = []
		hrs7 = []
		try:
			clock_num = int(i[3][:-2])
		except:
			clock_num = 0
		# Check all sc_production for the clock and the date .   Assign to tmp_sc
		sql = "SELECT * FROM sc_production1 where comments = '%s' and pdate ='%s'" % (clock_num,date1)
		cur.execute(sql)
		tmp_sc=cur.fetchall()
		# Assign count to number of finds of above filter
		sql_count= "SELECT COUNT(*) FROM sc_production1 where comments = '%s' and pdate ='%s'" % (clock_num,date1)
		cur.execute(sql_count)
		tmp_count = cur.fetchall()
		count = int(tmp_count[0][0])
		
		# Do below if found data for the clock on that day in sc_production
		if count > 0:
			for x in tmp_sc:
				asset = x[1] + '.0'
				part = x[3]
				hrs = x[12]
				qty = x[4]
				id1 = x[0]
				try:
					sql2 = "SELECT Job,Sig1 From tkb_allocation where (Asset1 = '%s' or Asset2 = '%s' or Asset3 = '%s' or Asset4 = '%s' or Asset5 = '%s' or Asset6 = '%s')" % (asset,asset,asset,asset,asset,asset)
					cur.execute(sql2)
					tmp3 = cur.fetchall()
					sig = int(tmp3[0][1][:-2])
					if sig == 1:
						sql2a = "SELECT Job From tkb_allocation where (Asset1 = '%s' or Asset2 = '%s' or Asset3 = '%s' or Asset4 = '%s' or Asset5 = '%s' or Asset6 = '%s') and (Part1 = '%s' or Part2 = '%s' or Part3 = '%s' or Part4 = '%s')" % (asset,asset,asset,asset,asset,asset,part,part,part,part)
						cur.execute(sql2a)
						tmp3 = cur.fetchall()
					job = tmp3[0][0]
				except:
					if x[1] == '500':
						job = 'Cleaning'
					elif asset == '800':
						job = 'Covid Cleaner'
					elif x[1] == '656':
						job = 'Op20 Offline (683/684/752/656/657)'
					else:
						job = 'not a job'
	
				name_good.append(nm)
				clock_good.append(clock_num)
				job_good.append(job)
				part_good.append(part)
				hrs_good.append(hrs)
				asset_good.append(asset)
				part_qty.append(qty)

				job7.append(job)
				hrs7.append(hrs)

				cur.execute('''INSERT INTO tkb_scheduled_temp(Id1,Employee,Clock,Asset,Job,Part,Hrs,Qty,Shift_Mod) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (id1,nm,clock_num,asset,job,part,hrs,qty,shift_mod))
				db.commit()

				# cur.execute('''INSERT INTO tkb_scheduled(Date1,Employee,Clock,Asset,Job,Part,Shift,Hrs) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''', (date1,nm,clock_num,asset,job,part,shift,hrs))
				# db.commit()
			total7=zip(job7,hrs7)
			
		# Do below if no data found for clock on that day in sc_production
		else:
			asset = 'no entry'
			part = '------'
			hrs4 = 0
			hrs = 0
			qty = 0
			part = ""
			job = ""
			name1.append(nm)
			clock1.append(clock_num)
			job1.append('no entry made')
			part1.append('no part')
			cur.execute('''INSERT INTO tkb_scheduled_temp(Employee,Clock,Asset,Job,Part,Hrs,Qty,Shift_Mod) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''', (nm,clock_num,asset,job,part,hrs,qty,shift_mod))
			db.commit()
			flow1 = 'stop'

		# Perform task on tkb_scheduled_temp
		# 1)delete duplicates
		# 2)group jobs and hours
		# 3)determine if Continental or 8hrs
		# 4)if less than 8 or 12 then mark as incomplete
		# if clock_num == 5876:
		# 	d=4/0

		# Delete Duplicates
		sql = "SELECT * FROM tkb_scheduled_temp ORDER BY %s %s" %('id','DESC')
		cur.execute(sql)
		tmp=cur.fetchall()
		for x in tmp:
			id1 = x[0]
			dql = ('DELETE FROM tkb_scheduled_temp WHERE Id < "%d" and Asset = "%s" and Part = "%s" and Qty ="%s" and Hrs = "%s"' %(x[0],x[4],x[6],x[8],x[7]))
			cur.execute(dql)
			db.commit()

		sql = "SELECT * FROM sc_production1 WHERE pdate = '%s' and comments = '%s' ORDER BY %s %s" %(date1,clock_num,'id','DESC')
		cur.execute(sql)
		tmp=cur.fetchall()
		for x in tmp:
			id1 = x[0]
			dql = ('DELETE FROM sc_production1 WHERE id < "%d" and asset_num = "%s" and partno = "%s" and actual_produced ="%s" and comments = "%s" and shift_hours_length = "%s"' %(x[0],x[1],x[3],x[4],x[9],x[12]))
			cur.execute(dql)
			db.commit()
		# ***********************************************************


		job1 = []
		hrs1 = []
		asset1 = []
		part1 = []
		ida = []
		shift_mod1 =[]
		hrs_total = 0

		sql = "SELECT * FROM tkb_scheduled_temp ORDER BY Job DESC, Hrs DESC" 
		cur.execute(sql)
		tmp=cur.fetchall()
		job_current = ''
		hrs_current = 0
		no_entry = 0

		for x in tmp:
			if asset == 'no entry':
				job1.append('no entry')
				hrs1.append('no entry')
				asset1.append('no entry')
				part1.append('no part')
				ida.append(0)
				shift_mod1.append(shift)
			elif job_current != x[5]:  # This determines if another job of same name for that person so ignores
				job1.append(x[5])
				hrs1.append(int(x[7]))
				asset1.append(x[4])
				part1.append(x[6])
				ida.append(x[1])
				shift_mod1.append(x[9])
				hrs_total = hrs_total + int(x[7])
				job_current = x[5]

		if hrs_total >= 8 and hrs_total <=12:
		# if hrs_total == hrs_verify:
			if job == 'not a job':
				no_entry = 1
			else:
				complete1 = 'Good'
		else:
			if asset == 'no entry':
				complete1 = 'No Entry'
			else:
				complete1 = 'Hrs Wrong'
			if job == 'not a job':
				no_entry = 1

		data3 = zip(job1,hrs1,asset1,part1,ida,shift_mod1)

		njob1 = 0
		for x in data3:
			if x[0] == 'not a job':
				njob1 = 1
		if njob1 ==1:
			complete1 = 'Bad Entry'
		
		for x in data3:
			cur.execute('''INSERT INTO tkb_scheduled(Id1,Date1,Employee,Clock,Job,Hrs,Shift,Asset,Part,Status,Shift_Mod) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (x[4],date1,nm,clock_num,x[0],x[1],shift,x[2],x[3],complete1,x[5]))
			db.commit()

	data1 = zip(name_good,clock_good,job_good,part_good,hrs_good,asset_good,part_qty)
	data2 = zip(name1,clock1,job1,part1)   # Data containing all those on the shift that didn't enter anything on the day
	request.session["shift_manpower"] = data2
	db.close()

	if request.session['pecm'] == 1:
		return render(request,"redirect_master.html")
	# Email the link to Supervisor in question.
	production_fix_email(request)

	return render(request,"redirect_auto_updater.html")
	return render(request,"redirect_master.html")  # This will actually go back to updater on final product
	return render(request,"redirect_production_entry_fix.html")
	return render(request,"test71.html",{'data1':data1,'data2':data2})

def production_fix_email(request):
	try:
		shift = request.session['variable1']
	except:
		shift = ''
	if len(shift) > 0 :
		b = "\r\n"
		# Determine who to send email to 
		toaddrs = ["dclark@stackpole.com"]
		if shift == 'Plant 1 Days':
			toaddrs = ["sbrownlee@stackpole.com","dclark@stackpole.com"]
		elif shift == 'Plant 1 Mid':
			toaddrs = ["jreid@stackpole.com","dclark@stackpole.com"]
		elif shift == 'Plant 1 Aft':
			toaddrs = ["kfrey@stackpole.com","dhawthorn@stackpole.com","dclark@stackpole.com"]
		elif shift == 'Plant 3 Days':
			toaddrs = ["kedwards@stackpole.com","gpackham@stackpole.com","dclark@stackpole.com"]
		elif shift == 'Plant 3 Aft':
			toaddrs = ["ashoemaker@stackpole.com","gpackham@stackpole.com","dclark@stackpole.com"]
		elif shift == 'Plant 3 Mid':
			toaddrs = ["gharvey@stackpole.com","gpackham@stackpole.com","dclark@stackpole.com"]
		elif shift == 'Plant 4 Day':
			toaddrs = ["asmith@stackpole.com","pmurphy@stackpole.com","dmilne@stackpole.com","dclark@stackpole.com"]
		elif shift == 'Plant 4 Mid':
			toaddrs = ["rbiram@stackpole.com","pstreet@stackpole.com","dmilne@stackpole.com","dclark@stackpole.com"]
		elif shift == 'Plant 4 Aft':
			toaddrs = ["rbiram@stackpole.com","pstreet@stackpole.com","asmith@stackpole.com","pmurphy@stackpole.com","dmilne@stackpole.com","dclark@stackpole.com"]

		fromaddr = 'stackpole@stackpole.com'
		frname = 'Dave'
		server = SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login('StackpolePMDS@gmail.com', 'stacktest6060')
		message_subject = 'Production Entry Verification Needed'
		message3 = "Click the link below to resolve the improper production entries." 
		message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
		var2 = request.session['variable1']
		var3 = (var2.replace(' ','*'))
		# message2 = "http://localhost:8080/production_entry_fix_shift/get/" + var3
		message2 = "http://pmdsdata.stackpole.ca:8986/trakberry/production_entry_fix_shift/get/" + var3

		message = message + "\r\n\r\n" + message3 + "\r\n\r\n" + "\r\n\r\n" + message2

		server.sendmail(fromaddr, toaddrs, message)
		server.quit()
	return

def production_entry_fix_shift(request,index):

	shift2 = (index.replace('*',' '))
	# request.session['variable1'] = shift2
	request.session['shift_prod'] = shift2
	return render(request,"redirect_production_entry_fix.html")

def production_duplicate_fix(request,date1):
	db, cur = db_set(request)
	sql = "SELECT * FROM sc_production1 WHERE pdate = '%s' ORDER BY %s %s" %(date1,'id','DESC')
	cur.execute(sql)
	tmp=cur.fetchall()
	for x in tmp:
		id1 = x[0]
		dql = ('DELETE FROM sc_production1 WHERE id < "%d" and asset_num = "%s" and partno = "%s" and actual_produced ="%s" and comments = "%s" and shift_hours_length = "%s"' %(x[0],x[1],x[3],x[4],x[9],x[12]))
		cur.execute(dql)
		db.commit()
	return

def production_entry_cleanup(request):
	db, cur = db_set(request)

	st='No Entry'
	dql = ('DELETE FROM tkb_scheduled WHERE status = "%s"' % (st))
	cur.execute(dql)
	db.commit()

	st='not a job'
	dql = ('DELETE FROM tkb_scheduled WHERE Job = "%s"' % (st))
	cur.execute(dql)
	db.commit()

	st='Good'
	cql = ('update tkb_scheduled SET Status = "%s"' % (st))
	cur.execute(cql)
	db.commit()
	

	return render(request,"redirect_master2.html")




def production_entry_fix(request):
	# date1, shift2 = vacation_set_current5()
	# date1 = request.session['tkb_update_date']  # Date is date from update program
	shift = request.session['shift_prod']  # The shift is retrieved from updater table
	# request.session['shift_prod'] = shift
	# date1 = request.session['date_prod'] 
	# shift = request.session['shift_prod']
	# date1='2021-01-06'
	# shift = 'Plant 1 Days'

	status1 = 'Good'
	status2 = 'Pending'
	status3 = 'No Entry'

	db, cur = db_set(request)

	# sql =( 'update scheduled SET Status="%s" WHERE (Shift="%s" and Status="%s"' % (t,tfull,index))
	# cur.execute(sql)
	# db.commit()
	# db.close()
	b = 0
	dql = ('DELETE FROM tkb_scheduled WHERE Clock = "%s"' %(b))
	cur.execute(dql)
	db.commit()



	sql = "SELECT * FROM tkb_scheduled WHERE Shift = '%s' and Status != '%s' and Status != '%s' ORDER BY %s %s, %s %s, %s %s" %(shift,status1,status2,'Date1','DESC','Status','DESC','Employee','ASC')
	cur.execute(sql)
	tmp=cur.fetchall()
	area = shift_area(shift)
	# sql = "SELECT Job FROM tkb_allocation WHERE Area = '%s'" %(area)
	sql = "SELECT Job FROM tkb_allocation" 
	cur.execute(sql)
	tmp_job=cur.fetchall()
	request.session['Jobs7'] = tmp_job

	if request.POST:
		new_job = request.POST.get('job7')
		delete_answer = request.POST.get('delete1')
		status_answer = request.POST.get('pending1')
		fix_answer = request.POST.get('fix1')
		fix_job = request.POST.get('fix_job1')
		fix_hrs_ok = request.POST.get('fix_hrs1')

		if status_answer > 0:
			cur.execute("""CREATE TABLE IF NOT EXISTS tkb_scheduled_missed(Id INT PRIMARY KEY AUTO_INCREMENT,Date CHAR(80), Employee CHAR(80),Clock CHAR(80), Shift Char(80))""")
			db.commit()
			fql = "SELECT * FROM tkb_scheduled WHERE Id = '%s'" % (status_answer)
			cur.execute(fql)
			fql2 = cur.fetchall()
			date9 = fql2[0][2]
			employee9 = fql2[0][3]
			clock9 = fql2[0][4]
			shift9 = fql2[0][8]
			cur.execute('''INSERT INTO tkb_scheduled_missed(Date,Employee,Clock,Shift) VALUES(%s,%s,%s,%s)''', (date9,employee9,clock9,shift9))
			db.commit()
			status2 = 'Pending'
			cql = ('update tkb_scheduled SET Status = "%s" WHERE Id ="%s"' % (status2,status_answer))
			cur.execute(cql)
			db.commit()
		elif delete_answer > 0:
			cur.execute("""CREATE TABLE IF NOT EXISTS tkb_scheduled_off(Id INT PRIMARY KEY AUTO_INCREMENT,Date CHAR(80), Employee CHAR(80),Clock CHAR(80), Shift Char(80))""")
			db.commit()
			fql = "SELECT * FROM tkb_scheduled WHERE Id = '%s'" % (delete_answer)
			cur.execute(fql)
			fql2 = cur.fetchall()
			date9 = fql2[0][2]
			employee9 = fql2[0][3]
			clock9 = fql2[0][4]
			shift9 = fql2[0][8]
			cur.execute('''INSERT INTO tkb_scheduled_off(Date,Employee,Clock,Shift) VALUES(%s,%s,%s,%s)''', (date9,employee9,clock9,shift9))
			db.commit()
			dql = ('DELETE FROM tkb_scheduled WHERE Id = "%s"' %(delete_answer))
			cur.execute(dql)
			db.commit()
		elif fix_answer > 0:
			fql = "SELECT * FROM tkb_scheduled WHERE Id = '%s'" % (fix_answer)
			cur.execute(fql)
			fql2 = cur.fetchall()
			shift1 = fql2[0][8]
			shift2 = fql2[0][11]
			shift1 = shift1.strip()
			shift2 = shift2.strip()

			#Determine if it's Continental or not
			hr7 = 8
			if shift1 != shift2:
				hr7 = 12

			fql = "SELECT Clock FROM tkb_scheduled WHERE Id = '%s'" % (fix_answer)
			cur.execute(fql)
			fql2 = cur.fetchall()
			clock_fix = fql2[0][0]  # Assign clock number of the person

			fql = "SELECT Date1 FROM tkb_scheduled WHERE Id = '%s'" % (fix_answer)
			cur.execute(fql)
			fql2 = cur.fetchall()
			date2 = fql2[0][0]  # Assign date  of the person

			sql_count= "SELECT COUNT(*) FROM tkb_scheduled where Clock = '%s' and Date1 ='%s'" % (clock_fix,date2)
			cur.execute(sql_count)
			tmp_count = cur.fetchall()
			count_fix = int(tmp_count[0][0])  # Number of entries by this person

			new_hrs = int(hr7 / float(count_fix))
			cql = ('update tkb_scheduled SET Hrs = "%s" WHERE (Clock="%s" and Date1 = "%s")' % (new_hrs,clock_fix,date2))
			cur.execute(cql)
			db.commit()
			cql = ('update tkb_scheduled SET Status = "%s" WHERE (Clock="%s" and Date1 = "%s")' % (status1,clock_fix,date2))
			cur.execute(cql)
			db.commit()

		elif fix_hrs_ok >0:
			request.session['hrs_skip'] = 'yes'
			fql = "SELECT Clock FROM tkb_scheduled WHERE Id = '%s'" % (fix_hrs_ok)
			cur.execute(fql)
			fql2 = cur.fetchall()
			clock_fix = fql2[0][0]  # Assign clock number of the person
			fql = "SELECT Date1 FROM tkb_scheduled WHERE Id = '%s'" % (fix_hrs_ok)
			cur.execute(fql)
			fql2 = cur.fetchall()
			date2 = fql2[0][0]  # Assign date  of the person


			cql = ('update tkb_scheduled SET Status = "%s" WHERE (Clock="%s" and Date1 = "%s")' % (status1,clock_fix,date2))
			cur.execute(cql)
			db.commit()

		elif fix_job > 0 and new_job != None:
			# update the Job to correct one
			cql = ('update tkb_scheduled SET Job = "%s" WHERE (Id="%s")' % (new_job,fix_job))
			cur.execute(cql)
			db.commit()

			fql = "SELECT Employee,Clock,Date1 FROM tkb_scheduled WHERE Id = '%s'" % (fix_job)
			cur.execute(fql)
			fql2 = cur.fetchall()
			clock_num = fql2[0][1]  # Assign clock number of the person
			nm = fql2[0][0]
			date2 = fql2[0][2]
			request.session['clock_num'] = clock_num
			request.session['nm'] = nm

			production_entry_check2(request,date2)

		return render(request,"redirect_production_entry_fix.html")
	else:
		form = kiosk_dispForm4()
	args = {}
	args.update(csrf(request))
	args['form'] = form


	return render(request,"product_entry.html",{'data':tmp,'args':args})

def production_entry_check2(request,date1):
	# date1 = request.session['date_prod'] 
	shift = request.session['shift_prod'] 
	clock_num = request.session['clock_num']
	status1 = 'Good'
	nm = request.session['nm']
	db, cur = db_set(request)
	job1 = []
	hrs1 = []
	asset1 = []
	part1 = []
	ida = []
	shift_mod1 =[]
	hrs_total = 0
	try:
		hrs_skip = request.session['hrs_skip']
	except:
		hrs_skip = 'no'

	# Put the clock num from schedu into temp
	sql = "SELECT * FROM tkb_scheduled WHERE Date1 = '%s' and Shift = '%s' and Clock = '%s' ORDER BY Employee DESC, Job DESC, Hrs DESC" %(date1,shift,clock_num)
	cur.execute(sql)
	tmp=cur.fetchall()
	job_current = ''
	hrs_current = 0
	no_entry = 0

	# Remove the clock num temporarily from Scheduled
	dql = ('DELETE FROM tkb_scheduled WHERE Date1 = "%s" and Shift = "%s" and Clock = "%s"' %(date1,shift,clock_num))
	cur.execute(dql)
	db.commit()

	# work with the shifts entries to check
	for x in tmp:
		if job_current != x[6]:  # This determines if another job of same name for that person so ignores
			job1.append(x[6])
			hrs1.append(int(x[9]))
			asset1.append(x[5])
			part1.append(x[7])
			ida.append(x[1])
			shift_mod1.append(x[11])
			hrs_total = hrs_total + int(x[9])
			job_current = x[6]

	if hrs_skip == 'no':
		if hrs_total >= 8 and hrs_total <=12:
			complete1 = 'Good'
		else:
			complete1 = 'Hrs Wrong'
	else:
		complete1 = 'Good'

	data3 = zip(job1,hrs1,asset1,part1,ida,shift_mod1)

	for x in data3:
		cur.execute('''INSERT INTO tkb_scheduled(Id1,Date1,Employee,Clock,Job,Hrs,Shift,Asset,Part,Status,Shift_Mod) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (x[4],date1,nm,clock_num,x[0],x[1],shift,x[2],x[3],complete1,x[5]))
		db.commit()

	sql_count= "SELECT COUNT(*) FROM tkb_scheduled where Clock = '%s' and Date1 ='%s'" % (clock_num,date1)
	cur.execute(sql_count)
	tmp_count = cur.fetchall()
	count_fix = int(tmp_count[0][0])  # Number of entries by this person

	new_hrs = int(8 / float(count_fix))
	cql = ('update tkb_scheduled SET Hrs = "%s" WHERE (Clock="%s" and Date1 = "%s")' % (new_hrs,clock_num,date1))
	cur.execute(cql)
	db.commit()
	cql = ('update tkb_scheduled SET Status = "%s" WHERE (Clock="%s" and Date1 = "%s")' % (status1,clock_num,date1))
	cur.execute(cql)
	db.commit()
	db.close()
	return

def production_entry_check_manual(request):

	if request.POST:
		kiosk_date = request.POST.get("date_en")
		kiosk_shift = request.POST.get("shift")
		request.session['tkb_update_date'] = kiosk_date
		request.session['variable1'] = kiosk_shift

		sh = kiosk_shift[-3:]
		if sh=='aft':
			shift1 = '3pm-11pm'
		elif sh=='day':
			shift1 = '7am-3pm'
		elif sh=='mid':
			shift1 = '11pm-7am'
		else:
			shift1 = '7am-3pm'


		db, cur = db_set(request)
		sql_count= "SELECT COUNT(*) FROM tkb_scheduled where Shift = '%s' and Date1 ='%s'" % (kiosk_shift,kiosk_date)
		cur.execute(sql_count)
		tmp_count = cur.fetchall()
		count_entries = int(tmp_count[0][0])  # Number of entries in scheduled

		sql_count= "SELECT COUNT(*) FROM sc_production1 where shift = '%s' and pdate ='%s'" % (shift1,kiosk_date)
		cur.execute(sql_count)
		tmp_count = cur.fetchall()
		count_kiosk = int(tmp_count[0][0])  # Number of entries in kiosk

		db.close()
		
		if count_kiosk > 0 and count_entries == 0:
			request.session['pecm'] = 1
			return render(request, "redirect_production_entry_check.html")
		else:
			return render(request, "redirect_master.html")
	else:
		form = kiosk_dispForm3()
	args = {}
	args.update(csrf(request))
	args['form'] = form  

	return render(request, "production_check_form.html",{'args':args})

def test_1_10R(request):

	db, cur = db_set(request)
	cur.execute("Alter Table quality_tpm_assets ADD Part Char(30)")



	db.commit()
	db.close()
	return render(request, "test_1_10R.html")