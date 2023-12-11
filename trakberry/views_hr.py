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
		priority = 0
		whoisonit = 'Millwright'
		
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

def pdate_stamp2(pdate):
	year1 = pdate[:4]
	month1 = pdate[5:7]
	day1 = pdate[-2:]
	x=[]
	x=[0 for i in range(9)] 
	x[0] = int(year1)
	x[1] = int(month1)
	x[2] = int(day1)
	x[3] = 0
	x[4] = 0
	x[5] = 0
	y = time.mktime(x)
	stamp = y +79200 - 86400
	return stamp


def production_OA(request):
	b1 = str(request.session["start_date"])
	b2 = str(request.session["end_date"])
	a1 = pdate_stamp2(b1)+3600
	a2 = pdate_stamp2(b2)+90000
	d7 = a2 - a1
	sched1 = a2-a1  # Time frame
	breaks1 = (sched1 * .0833333)    # Break time in that timeframe


	# Calculate Downtime for Interval group by Asset
	c1 = 'Yes_Down'
	t=int(time.time())
	db, cur = db_set(request)

	m1='1723'
	m4='1533'
	m5='650'
	m6='769'
	m7='1816'
	m8='1617'
	m9='797'

	mm = ['1533','1716L','1716R','1717L']
	cc = [9,62,62,62]
	ss = ['10R80','AB1V Reaction','AB1V Overdrive','AB1V Input']

	mc = zip(mm,cc,ss)
	mm = tuple(mm)

	machine1 = []
	A1 = []
	P1 = []
	Q1 = []
	OA1 = []
	# sql="SELECT Machine, COUNT(*) FROM GFxPRoduction WHERE TimeStamp >='%s' and TimeStamp <= '%s' and Machine IN {} GROUP BY Machine".format(mm) % (a1,a2)
	# cur.execute(sql)
	# tmpX=cur.fetchall()
	for j in mc:
		m=j[0]
		sql="SELECT Machine,TimeStamp FROM GFxPRoduction where  TimeStamp >='%s' and TimeStamp <= '%s' and Machine = '%s'" % (a1,a2,m)
		cur.execute(sql)
		tmpY=cur.fetchall()
		sql="SELECT COUNT(*) FROM GFxPRoduction WHERE TimeStamp >='%s' and TimeStamp <= '%s' and Machine = '%s'" % (a1,a2,m)
		cur.execute(sql)
		tmpX=cur.fetchall()
		sql="SELECT SUM(scrap_amount) FROM tkb_scrap WHERE LEFT(date_current,10) >='%s' and LEFT(date_current,10) <= '%s' and scrap_line = '%s'" % (b1,b2,j[2])
		cur.execute(sql)
		tmpZ=cur.fetchall()

		ctr1 = 0
		prev_time = 0
		dt1 = 0
		min_time = 100000
		for i in tmpY:
			calc1 = int(i[1]) - prev_time
			if calc1 > 900:  # Using 15min to determine downtime
				if ctr1 > 0:
					dt1 = dt1 + (calc1)
			ctr1 = 1
			prev_time = int(i[1])

		# Calculate Availability
		A = 1-((dt1)/(sched1-breaks1))
		

		# Calculate Productivity
		ct = j[1]   # Cycle time
		qty = int(tmpX[0][0])  # Calculate Quantity Run
		P = (ct * qty) / float(sched1 - breaks1 - dt1)

		# Calculate Quality
		try:
			scrap_qty = int(tmpZ[0][0])
		except:
			scrap_qty = 0
		Q = ( qty ) / float(qty + scrap_qty)
		

		OA = A * P * Q
		OA = round((OA*100000)/float(1000),2)
		A = round((A*100000)/float(1000),2)
		P = round((P*100000)/float(1000),2)
		Q = round((Q*100000)/float(1000),2)

		machine1.append(j[2])
		A1.append(A)
		P1.append(P)
		Q1.append(Q)
		OA1.append(OA)



	OA_Summary = zip(machine1,A1,P1,Q1,OA1)

	request.session['oa_summary'] = OA_Summary
		
	

	# rrr=3/0

	
	# sql_prod = "SELECT Part,COUNT(*) AS Total FROM GFxPRoduction WHERE TimeStamp >='%s' AND TimeStamp <='%s' AND (Machine ='%s' OR Machine ='%s' OR Machine ='%s' OR Machine ='%s' OR Machine ='%s' OR Machine ='%s' OR Machine ='%s') GROUP BY Part" % (a1,a2,m1,m4,m5,m6,m7,m8,m9)  
	# cur.execute(sql_prod)
	# tmp_prod=cur.fetchall()

	# sql_test = "SELECT Asset,called4helptime,completedtime,Downtime,problem,remedy FROM OA_Availability WHERE (LEFT(called4helptime,10) >='%s' and LEFT(called4helptime,10) <='%s') OR (completedtime IS NULL) and down='%s'" % (b1,b2,c1)
	# cur.execute(sql_test)
	# tmp_test=cur.fetchall()
	# a1 = []
	# start1 = []
	# end1 = []
	# down1 = []
	# problem1 = []
	# remedy1 = []
	# for i in tmp_test:
	# 	s1 = (time.mktime(i[1].timetuple()))
	# 	try:
	# 		e1 = (time.mktime(i[2].timetuple()))
	# 	except:
	# 		e1 = t
	# 	d1 = int(e1) - int(s1)
	# 	a1.append(i[0])
	# 	start1.append(s1)
	# 	end1.append(e1)
	# 	down1.append(d1)
	# 	problem1.append(i[4])
	# 	remedy1.append(i[5])
	# data1=zip(a1,start1,end1,down1,problem1,remedy1)
	# data2 = zip(a1,down1)
	# data2 = sorted(data2,key=lambda x:x[0])
	# time1 = 0
	# a2 = []
	# d2 = []
	# c2 = []
	# a = ''
	# ch = 0
	# for i in data2:
	# 	if i[0] != a:
	# 		if a != '':
	# 			a2.append(a)
	# 			if time1 > d7:
	# 				time1 = int(d7)
	# 				ch = 1
	# 			d2.append(time1)
	# 			c2.append(ch)
	# 			time1 = i[1]
	# 			a = i[0]
	# 			ch = 0
	# 		else:
	# 			time1 = time1 + i[1]
	# 			a = i[0]
	# 	else:
	# 		time1 = time1 + i[1]
	# res = zip(a2,d2,c2)
	# res = sorted(res,key=lambda x:x[0])   # List of Assets and how long in seconds down
	


	# Wrong address
	return render(request,'oa_summary.html')




	
def productline_dl(request):

	b1 = request.session["start_date"]
	b2 = request.session["end_date"]



	t=int(time.time())
	tm = time.localtime(t)
	shift_start = -2
	if tm[3]<23 and tm[3]>=15:
		shift_start = 14
	elif tm[3]<15 and tm[3]>=7:
		shift_start = 6
	cur_hour = tm[3]
	if cur_hour == 23:
		cur_hour = -1
	u = t - (((cur_hour-shift_start)*60*60)+(tm[4]*60)+tm[5])	 # Starting unix of shift
	db, cur = db_set(request)

	# b1 = '2023-07-01'
	# b2 = '2023-07-03'
	q1='Compacting'
	q2='50-5214'
	q3='50-3214'
	q4='50-6114'
	q5='50-6314'
	q6='50-4314'

	sql_test = "SELECT LEFT(partno,7) AS Part, machine AS Operation,MAX(shift_hours_length) AS Hrs FROM sc_production1 WHERE pdate >='%s' and pdate <='%s' and machine='%s' and (LEFT(partno,7)='%s' OR LEFT(partno,7)='%s' OR LEFT(partno,7)='%s' OR LEFT(partno,7)='%s' OR LEFT(partno,7)='%s') GROUP BY comments,machine,shift,pdate " % (b1,b2,q1,q2,q2,q4,q5,q6)
	cur.execute(sql_test)
	tmp_test=cur.fetchall()
	ctr = 0
	for i in tmp_test:
		ctr = ctr + int(i[2])

	
	
	# Create View in timeframe needed
	sql_prem = "SELECT LEFT(partno,7) AS Part, machine AS Operation,MAX(shift_hours_length) AS Hrs FROM sc_production1 WHERE pdate >='%s' and pdate <='%s' GROUP BY comments,machine,shift,pdate " % (b1,b2)
	cur.execute(sql_prem)
	tmp_prem=cur.fetchall()
	tmp_p = list(tmp_prem)
	tmp_p = sorted(tmp_p,key=lambda x:(x[0],x,[2]))


	part8=[]
	oper8=[]
	coun8=[]

	tt=[]
	a = tmp_p[0][0]
	b = tmp_p[0][1]
	c = int(tmp_p[0][2])
	for i in tmp_p:
		o = i[1]
		if o!='Compacting':
			if o!='Sintering':
				if o!='Machining':
					if o!='Packing':
						o = 'Other'
		ch = 0
		if i[0] == a:
			if o==b:
				ch = 1
		if ch == 0:
			if a != '':
				part8.append(a)
				oper8.append(b)
				coun8.append(c)
			a=i[0]
			b=o
			c=c+int(i[2])
	tst=zip(part8,oper8,coun8)



   # Need to look at LEFT $ for compacts so you don't double count
	part9=[]
	oper9=[]
	coun9=[]
	ctr2 = 0
	a = tmp_p[0][0]
	b = tmp_p[0][1]
	c = int(tmp_p[0][2])
	for i in tmp_p:
		
		if a!= i[0]:
			if b!=i[1]:
				part9.append(a)
				oper9.append(b)
				coun9.append(ctr2)
				a=i[0]
				b=i[1]
				c=int(i[2])
				ctr2=0

		ctr2 = ctr2 + int(i[2])
	ttst = zip(part9,oper9,coun9)



	a1 = pdate_stamp2(b1)
	a2 = pdate_stamp2(b2)+86400


	as1 = '900'
	pt1 = '50-3627'
	parts = ['50-1713','50-1731','50-3632','50-3627']
	pparts = tuple(parts)

	
	machines = ['1750','1724','1725','1533','650L','650R','769','1816','1617','797'] 

	mmachines = tuple(machines)
	sql1="SELECT Part,COUNT(Machine) AS Total FROM GFxPRoduction WHERE TimeStamp >='%s' and TimeStamp <= '%s' and Machine IN  {} GROUP BY Part".format(mmachines) % (a1,a2) 
	sql2="SELECT partno AS Part, SUM(actual_produced) AS Total FROM sc_production1 WHERE pdate >= '%s' AND pdate <= '%s' AND asset_num = '%s' AND partno IN {} GROUP BY partno".format(pparts) % (b1,b2,as1) 
	sql3 ="Select DISTINCT(Line), LEFT(Part,7) From PartLines"
	sql4 ="Select DISTINCT(Line) From PartLines"
	#sql5="SELECT Part,SUM(Hrs) AS Total FROM tkb_scheduled WHERE Date1 >='%s' and Date1 <= '%s' GROUP BY Part" % (b1,b2) 

	#sql5="SELECT Part,SUM(Hrs),Operation AS Hrs FROM view_employee_worked WHERE pdate >='%s' and pdate <= '%s' GROUP BY Part,Operation" % (b1,b2) 





	cur.execute(sql1)
	tmp1=cur.fetchall()
	cur.execute(sql2)
	tmp2=cur.fetchall()
	cur.execute(sql3)
	tmp3=cur.fetchall()
	cur.execute(sql4)
	tmp4=cur.fetchall()
	#cur.execute(sql5)
	#tmp5=cur.fetchall()


	pl = []
	pl_count = []
	hr_count = []
	hr_compact =[]
	hr_sinter = []
	hr_machine = []
	hr_pack = []
	hr_other = []


	# Calculate Production in the interval and put in total1
	for i in tmp4:
		line1 = i[0]
		cnt = 0
		hrs = 0
		hrs_compact = 0
		hrs_sinter = 0
		hrs_machine = 0
		hrs_pack = 0
		prt = []
		for ii in tmp3:
			if ii[0] == line1:
				prt.append(ii[1])	
		for iii in tmp1:
			if iii[0] in prt:
				cnt = cnt + int(iii[1])
		for jjj in tmp2:
			if jjj[0] in prt:
				cnt = cnt + int(jjj[1])
		for k in ttst:
			p4 = k[0][:7]
			if p4 in prt:
				hrs = hrs + int(k[2])
				if k[1] == 'Compacting':
					hrs_compact = hrs_compact + int(k[2])
				elif k[1] ==  'Packing':
					hrs_pack = hrs_pack + int(k[2])
				elif k[1] ==  'Machining':
					hrs_machine = hrs_machine + int(k[2])
				elif k[1] ==  'Sintering':
					hrs_sinter = hrs_sinter + int(k[2])


			
		pl.append(line1)
		pl_count.append(cnt)
		hr_count.append(hrs)
		hrs_other = hrs - (hrs_compact + hrs_pack + hrs_machine + hrs_sinter)
		hr_compact.append(hrs_compact)
		hr_sinter.append(hrs_sinter)
		hr_machine.append(hrs_machine)
		hr_pack.append(hrs_pack)
		hr_other.append(hrs_other)

	total1=zip(pl,pl_count,hr_count,hr_compact,hr_sinter,hr_machine,hr_pack,hr_other)


	line_name = ['10R140','10R60','10R80','AB1V','GF6','GFx','Magna','9HP']
	line_price = [32.97,13.7,12.84,29.07,13.95,11.72,14.1,13.47]
	line_costing = zip(line_name,line_price)

	sales1=[]
	labour1=[]
	labour_per = []
	labour_compact = []
	labour_sinter = []
	labour_machine = []
	labour_pack = []
	labour_other = []

	pl2=[]
	pl_count2=[]
	hr_count2=[]


	for i in total1:
		line1=''
		line1 = i[0]
		for j in line_costing:
			if j[0] == line1:
				pl2.append(i[0])
				pl_count2.append(i[1])
				hr_count2.append(i[2])
				sales1.append(i[1] * j[1])
				labour1.append(i[2] * 23)
				try:
					diff1 =round((((i[2]*23)/(i[1]*j[1]))*100),2)
				except:
					diff1 = 0
				labour_per.append(diff1)
				diff1 = round((i[3] / float(i[2]))*100,2)
				labour_compact.append(diff1)

				

				diff1 = round((i[4] / float(i[2]))*100,2)
				labour_sinter.append(diff1)
				diff1 = round((i[5] / float(i[2]))*100,2)
				labour_machine.append(diff1)
				diff1 = round((i[6] / float(i[2]))*100,2)
				labour_pack.append(diff1)
				diff1 = round((i[7] / float(i[2]))*100,2)
				labour_other.append(diff1)
	


				break
	total2 = zip(pl2,pl_count2,hr_count2,sales1,labour1,labour_per,labour_compact,labour_sinter,labour_machine,labour_pack,labour_other)

	plant_build = 0
	plant_cost = 0
	for i in total2:
		plant_build = plant_build + i[3]
		plant_cost = plant_cost + i[4]
	plant1 = round((plant_cost / plant_build)*100,3)

	# print out total2 columns
	# also plant margin will be plant cost / plant build
	request.session['plant_margin'] = plant1
	request.session['plant_build'] = plant_build
	request.session['plant_cost'] = plant_cost
	request.session['total'] = total2
	db.close()



	
	return render(request,'build_direct.html')


def date_picker_productline(request):
	if request.POST:
		a= request.POST.get("start_date")
		b = request.POST.get("end_date")
		request.session['start_date'] = a
		request.session['end_date'] = b
		return render(request,'redirect_productline_dl.html')  # Need to bounce out to an html and redirect back into a module otherwise infinite loop
	else:
		form = tech_loginForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'productionline_datepicker.html', {'args':args})


def date_picker_production_OA(request):
	if request.POST:
		a= request.POST.get("start_date")
		b = request.POST.get("end_date")
		request.session['start_date'] = a
		request.session['end_date'] = b
		return render(request,'redirect_production_OA.html')  # Need to bounce out to an html and redirect back into a module otherwise infinite loop
	else:
		form = tech_loginForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'production_OA_datepicker.html', {'args':args})









