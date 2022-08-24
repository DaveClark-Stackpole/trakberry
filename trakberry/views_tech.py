from socket import AF_APPLETALK
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import tech_closeForm, tech_loginForm, tech_searchForm, tech_message_Form
from trakberry.forms import sup_downForm
from views_db import db_open, db_set,net1
from views_mod1 import find_current_date
from views_email import e_test
from views_supervisor import supervisor_tech_call
import MySQLdb
import time
import datetime
import calendar
from views_routes import direction
import smtplib

from smtplib import SMTP
from django.template.loader import render_to_string  #To render html content to string
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2,vacation_set_current55


#import datetime as dt 
from django.core.context_processors import csrf


# Returns date for week start in format  YYYY-MM-DD
def week_start_finder(request):
	t=int(time.time())
	tm = time.localtime(t)
	a1 = tm[6] * 86400
	a2 = tm[3] * 60 * 60
	a3 = tm[4] * 60
	a4 = tm[5]
	week_start1 = t - a1 - a2 - a3 - a4 + 1
	tm = time.localtime(week_start1)
	ma = ''
	da = ''
	if tm[1] < 10: ma = '0'
	if tm[2] < 10: da = '0'
	y1 = str(tm[0])
	m1 = str(tm[1])
	d1 = str(tm[2])
	date1 = y1 + '-' + (ma + m1) + '-' + (da + d1)
	return date1


# This will add week_start, check_id columns then populate epv_checks with the ones not populated.
# Testing phase to start though
def epv_checks_update(request):
	clock = '99999'
	ws_len = 3
	db, cursor = db_set(request)  
	loop1 = 1
	# Add Columns if not added
	try:
		sql ="SELECT Asset_Id FROM quality_epv_checks"
		cursor.execute(sql)
		tmp4 = cursor.fetchall()
	except:
		cursor.execute("Alter Table quality_epv_checks ADD Asset_Id Int(30)")
		db.commit()
		cursor.execute("Alter Table quality_epv_checks ADD Week_Start Char(30)")
		db.commit()

	while loop1 > 0:
		try:
			sql = "SELECT date1,Id FROM quality_epv_checks where clock_num >'%s' and Week_Start IS NULL" %(clock)
			cursor.execute(sql)
			tmp7 = cursor.fetchall()
			pdate = tmp7[0][0]
		except:
			loop1 = 0
		pstamp = pdate_stamp(pdate)
		pm = time.localtime(pstamp)
		xm = pm[6]
		xm = int(xm) * 86400
		pstamp = pstamp - xm
		pstamp_next = pstamp + 518400
		pdate = stamp_pdate(pstamp) # pdate is Monday of week
		pdate_next = stamp_pdate(pstamp_next) # pdate_next is Sunday of week

		sql = "SELECT Id,date1,shift1,check1,description1,asset1,comment,clock_num FROM quality_epv_checks where date1 >= '%s' and date1 <= '%s' and clock_num >'%s'" %(pdate,pdate_next,clock)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		request.session['epv1'] = tmp
		dd = []
		for i in tmp:
			try:
				sql = "SELECT Id FROM quality_epv_assets where Asset = '%s' and QC1 = '%s'" % (i[5],i[3])
				cursor.execute(sql)
				tmp2 = cursor.fetchall()
				tmp3 = int(tmp2[0][0])
				sql =( 'update quality_epv_checks SET Asset_Id = "%s" WHERE Id = "%s"' % (tmp3,i[0]))
				cursor.execute(sql)
				db.commit()
				sql =( 'update quality_epv_checks SET Week_Start = "%s" WHERE Id = "%s"' % (pdate,i[0]))
				cursor.execute(sql)
				db.commit()
			except:
				dql = ('DELETE FROM quality_epv_checks WHERE Id="%s"' % (i[0]))
				cursor.execute(dql)
				db.commit()
	db.close()
	return render(request,"epv_check_update_complete.html")




def week_prev_forw(request):
	date1 = week_start_finder(request)
	try:
		d = request.session['date_current_epv']
	except:
		request.session['date_current_epv'] = date1
		

	return date1

def date_finder(request):
	week_start1 =int(time.time())
	tm = time.localtime(week_start1)
	ma = ''
	da = ''
	if tm[1] < 10: ma = '0'
	if tm[2] < 10: da = '0'
	y1 = str(tm[0])
	m1 = str(tm[1])
	d1 = str(tm[2])
	date1 = y1 + '-' + (ma + m1) + '-' + (da + d1)
	return date1

def tech_manpower(request):

	db, cursor = db_set(request) 
	sql = "SELECT * FROM tkb_techs ORDER BY tech ASC" 
	cursor.execute(sql)
	tmp = cursor.fetchall()
	# tmp2 = tmp[0]

	db.close()
	return tmp

def out(request):
	#request.session["test"] = 78
	return render(request, "out.html")

# Module to Check if we need to send downtime report out
# via email.   This goes out through the Tech App refreshing	

def hour_check():
	# obtain current date from different module to avoid datetime style conflict

	h = 2
	m = 2
	ch = 0
	send_email = 0
	t=int(time.time())
	tm = time.localtime(t)
	min = tm[4]
	hour = tm[3]
	current_date = find_current_date()
	#if min > m:
	if hour >= h and min > m:
		ch = 1

	db, cursor = db_set(request)  
	try:
		sql = "SELECT checking FROM tkb_email_conf where date='%s'" %(current_date)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		checking = tmp2[0]
	except:
		checking = 0
		cursor.execute('''INSERT INTO tkb_email_conf(date) VALUES(%s)''', (current_date))
		db.commit()
		tmp2 = 0

	if ch == 1 and checking == 0:
		checking = 1
		pql =( 'update tkb_email_conf SET checking="%s" WHERE date="%s"' % (checking,current_date))
		cursor.execute(pql)
		db.commit()
		tql = "SELECT sent FROM tkb_email_conf where date='%s'" %(current_date)
		cursor.execute(tql)
		tmp = cursor.fetchall()
		tmp2 = tmp[0]
		sent = tmp2[0]
		if sent == 0:
			sent = 1
			rql =( 'update tkb_email_conf SET sent="%s" WHERE date="%s"' % (sent,current_date))
			cursor.execute(rql)
			db.commit()
			send_email = 1				
	db.close()	
	return send_email
	
def reset_call_route(request):
	request.session["call_route"] = 'supervisor'
	return render(request, "out.html")

def tech_email_test(request):
	send_email = hour_check()
	if send_email == 1:
		return render(request, "email_downtime.html")
		
	return render(request, "email_downtime_cycle.html")

def time_write():
	# t = int(time.time())
	# db,cur = db_open()
	# i = 101
	# mach = 555
	# part = 'time_update'
	# x = 1
	# a = '1'
	# cur.execute('''insert into tkb_prodtrak(pi_id,part_number,machine,part_timestamp,autotime,last_time_diff) VALUES(%s,%s,%s,%s,%s,%s)''',(i,part,part,t,mach,mach))
	# db.commit()
	# db.close()
	return
	
	
	
def tech(request):
	net1(request)
	# Below section is check to ensure a Tech is logged in before loading this main page
	try:
		if request.session["login_tech"] =='none':
			return render(request,"redirect_tech_logout.html",)
	except:
		return render(request,"redirect_tech_logout.html",)





	#Do the Hour Check to see if email needs sending

	#return email_hour_check(request)
#	send_email = hour_check()
#	if send_email == 1:
#		return e_test(request)	
#		return render(request, "email_downtime.html")

	# Check if it's local running or not and if not then force the path as /trakberry
	# Run switch_net to set it back to network or switch_local for local use
	# try:
	# 	if request.session["local_switch"] == 1:
	# 		request.session["local_toggle"] = ""
	# 	else:
	# 		request.session["local_toggle"] = "/trakberry"
	# except:
	# 	request.session["local_toggle"] = "/trakberry"
	# ******************************************************************************
	
	
	
# New Time Check to send 
	t1 = int(time.time())
	try:
		t2 = request.session["time2"]
	except:
		t2 = t1
		request.session["time2"] = t1
		
	if (t1 - t2) > 300:
		request.session["time2"] = t1
		time_write()  # Write current time to DB tkb_prodtrak

	try:
		request.session["login_tech"] 

#		Below is Dead Code

#		t_name = request.session["login_tech"] 
#		jj = email_hour_check(t_name)
		#return render(request,'done_test5.html',{'jj':jj})
	except:
		request.session["login_tech"] = "none"
	try:
		request.session["tech_ctr"] 
	except:
		request.session["tech_ctr"] = 0
  
	request.session["refresh_tech"] = 0
  # initialize current time and set 'u' to shift start time
	t=int(time.time())
	tm = time.localtime(t)
	c = []
	date = []
	prob = []
	job = []
	priority = []
	id = []
	machine = []
	count = []
	tmp2=[]
	smp2=[]
	mach_cnt = []
	tch = []
	# Update CNC TEch PM Lists
	# tech_pm_update(request)
	# *******************************

	# Will update Weekly Tech EPV List once if it doesn't exist 
	clock2 = 'Operator'
	clock3 = 'Once per shift'
	clock4 = 'Gauge Tech'
	clock_len = '9999'
	db, cursor = db_set(request)   
	# cursor.execute("""CREATE TABLE IF NOT EXISTS quality_epv_checks(Id INT PRIMARY KEY AUTO_INCREMENT,date1 CHAR(80),shift1 CHAR(80), check1 Char(80), description1 Char(80), asset1 Char(80), master1 Char(80), comment Char(255), clock_num Char(80))""")
	# cursor.execute("""CREATE TABLE IF NOT EXISTS quality_epv_week(Id INT PRIMARY KEY AUTO_INCREMENT,date1 CHAR(80),QC1 Char(255), OP1 Char(255), Check1 Char(255), Desc1 Char(255), Method1 Char(255), Asset Char(80), Person Char(100))""")
	date_start = week_start_finder(request)
	xql = "SELECT * FROM quality_epv_checks where (clock_num > '%s')" %(clock_len)
	cursor.execute(xql)
	xmp = cursor.fetchall()

	aql = "SELECT COUNT(*) FROM quality_epv_checks where (date1 = '%s' and clock_num > '%s')" %(date_start,clock_len)
	cursor.execute(aql)
	amp = cursor.fetchall()
	bmp = amp[0]
	count2 = bmp[0]
	aql = "SELECT COUNT(*) FROM quality_epv_week where (date1 = '%s')" %(date_start)
	cursor.execute(aql)
	amp = cursor.fetchall()
	bmp = amp[0]
	count3 = bmp[0]

	# count2= 0
	# count3=0
	if count2 == 0 and count3 == 0 :

		# We should write the remaining EPVs into a missed EPV list for reference
		cursor.execute("TRUNCATE TABLE quality_epv_week")  # This will clear out remaining EPVs
		db.commit()


		week_dump = 1
		sql = "SELECT QC1,OP1,Check1,Desc1,Method1,Asset,Person FROM quality_epv_assets where Person <> '%s' and Person <> '%s' and Person <> '%s' " % (clock2,clock3,clock4)
		cursor.execute(sql)
		tmp = cursor.fetchall()
		for i in tmp:
			try:
				cursor.execute('''INSERT INTO quality_epv_week(date1,QC1,OP1,Check1,Desc1,Method1,Asset,Person) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''', (date_start,i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
				db.commit()
			except:
				cursor.execute("Alter Table quality_epv_week ADD Person Char(30)")
				db.commit()
				cursor.execute('''INSERT INTO quality_epv_week(date1,QC1,OP1,Check1,Desc1,Method1,Asset,Person) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''', (date_start,i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
				db.commit()

	
	# Retrieve information from Database and put 2 columns in array {list}
	# then send array to Template machinery.html
	c = ["tech","Jim Barker"]
	j = "tech"
	jj = "Tech"
	a1 = "Dave McLaren"
	a2 = "Muoi Le"
	a3 = "Jim Barker"
	a4 = "Scott Smith"
	a5 = "Toby Kuepfer"
	a6 = "Terry Kennedy"
	a7 = "Paul Wilson"
	a8 = "James Kuepfer"
	a9 = "Ervin Kuepfer"
	a10 = "Jonathan Brunk"
	a11 = "Mayank Gehlot"
	a13 = "Surjit Toora"
	a12 = "Karissa St.Pierre"
	a14 = "Jered Pankratz"
	a15 = "Jimanie Tulloch"
	a16 = "Rob Wood"
	a17 = "Jeremy Bourque"
	a18 = "Scott Warner"
	

	
	d1 = '2015-05-01'
	d2 = '2015-07-01'
	sqlT = "SELECT * FROM pr_downtime1 where closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s' OR closed IS NULL AND whoisonit = '%s'" %(j,jj,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18)

	cursor.execute(sqlT)
	tmp = cursor.fetchall()
	
	ctr = 0
	for x in tmp:
		tmp2 = (tmp[ctr])
		temp_pr = tmp2[3]
		if temp_pr == "A":
			tp = 1
		elif temp_pr =="c":
			tp = 3
		elif temp_pr =="b" :
			tp = 2
		elif temp_pr =="B" :
			tp = 2
		elif temp_pr =="C" :
			tp = 3
		elif temp_pr =="D"	:
			tp = 4
		elif temp_pr =="E":
			tp = 5
		else:
			tp = 5

		
		job.append(tmp2[0])
		prob.append(tmp2[1])
		priority.append(int(tmp2[3]))
		id.append(tmp2[11])
		tmp3 = tmp2[4]
		if tmp3 == "tech":
			tmp3 = "TAKE CALL"
		if tmp3 == "Tech":
			tmp3 = "TAKE CALL"	
		tch.append(tmp3)
		ctr = ctr + 1
		
	for i in range(0, ctr-1):
		for ii in range(i+1, ctr):
			if int(priority[ii]) < int(priority[i]):
				jjob = job[i]
				job[i] = job[ii]
				job[ii] = jjob
				pprob = prob[i]
				prob[i] = prob[ii]
				prob[ii] = pprob
				pprior = priority[i]
				priority[i] = priority[ii]
				priority[ii] = pprior
				iid = id[i]
				id[i] = id[ii]
				id[ii]= iid
				ttch = tch[i]
				tch[i] = tch[ii]
				tch[ii] = ttch
	if request.session["tech_ctr"] == ctr:
		request.session["tech_alarm"] = "/media/clock2.wav"
	else:
		request.session["tech_alarm"] = "/media/clock.wav"
		request.session["tech_ctr"] = ctr
	list = zip(job,prob,id,tch,priority)
	
	db.close()
	n = "none"
	if request.session["login_tech"] == "Jim Barker":
		request.session["login_image"] = "/static/media/tech_jim.jpg"
		request.session["login_back"] = "/static/media/back_jim.jpg"
	elif request.session["login_tech"] == "Dave Clark":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/tech_training.jpg"
	elif request.session["login_tech"] == "Scott Smith":
		request.session["login_image"] = "/static/media/tech_scott.jpg"
		request.session["login_back"] = "/static/media/back_scott.jpg"
	elif request.session["login_tech"] == "Dave McLaren":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"
	elif request.session["login_tech"] == "Jonathan Brunk":
		request.session["login_image"] = "/static/media/tech_woodrow.jpg"
		request.session["login_back"] = "/static/media/back_woodrow.jpg"
	elif request.session["login_tech"] == "Ervin Kuepfer":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"			
	elif request.session["login_tech"] == "Muoi Le":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"
	elif request.session["login_tech"] == "Scott Warner":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"
	elif request.session["login_tech"] == "Jeremy Bourque":
		request.session["login_image"] = "/static/media/tech_nigel.jpg"
		request.session["login_back"] = "/static/media/back_nigel.jpg"		
	elif request.session["login_tech"] == "Mayank Gehlot":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"
	elif request.session["login_tech"] == "James Kuepfer":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"	
	elif request.session["login_tech"] == "Chris Coakley":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"
	elif request.session["login_tech"] == "Rob Wood":
		request.session["login_image"] = "/static/media/tech_training.jpg"
		request.session["login_back"] = "/static/media/back_tech_training.jpg"
			
	elif request.session["login_tech"] == "Terry Kennedy":
		request.session["login_image"] = "/static/media/tech_terry.jpg"
		request.session["login_back"] = "/static/media/back_terry.jpg"		
	elif request.session["login_tech"] == "Dan Deighton":
		request.session["login_image"] = "/static/media/tech_vaters.jpg"
		request.session["login_back"] = "/static/media/back_vaters.jpg"	
	else:
		request.session["login_image"] = "/static/media/tech_rick.jpg"
		request.session["login_back"] = "/static/media/back_rick.jpg"
		
  # call up 'display.html' template and transfer appropriate variables.  
  
  # *********************************************************************************************************
  # ******     Messaging portion of the Tech App  ***********************************************************
  # *********************************************************************************************************
	N = request.session["login_tech"]
	R = 0
	db, cur = db_set(request) 
	try:
		sql = "SELECT * FROM tkb_message WHERE Receiver_Name = '%s' and Complete = '%s'" %(N,R)	
		cur.execute(sql)
		tmp44 = cur.fetchall()
		tmp4 = tmp44[0]

		request.session["sender_name"] = tmp4[2]
		request.session["sender_name_last"] = tmp4[2]
		request.session["message_id"] = tmp4[0]

		aql = "SELECT COUNT(*) FROM tkb_message WHERE Receiver_Name = '%s' and Complete = '%s'" %(N,R)
		cur.execute(aql)
		tmp2 = cur.fetchall()
		tmp3 = tmp2[0]
		cnt = tmp3[0]
	except:
		cnt = 0
		tmp4 = ''
		request.session["sender_name"] = ''
		request.session["message_id"] = 0

	Z = 1
	if cnt > 0 :
		cnt = 1
		request.session["refresh_tech"] = 3
	# ********************************************************************************************************
	try:
		request.session['tech_epv_second']
	except:
		request.session['tech_epv_second'] = 0
	try:
		request.session['tech_pm_second']
	except:
		request.session['tech_pm_second'] = 0

	tcur=int(time.time())
	sql = "SELECT DISTINCT QC1,OP1,Check1,Person FROM quality_epv_week ORDER BY %s %s" % ('QC1','ASC')
	cur.execute(sql)
	tmp2 = cur.fetchall()
	request.session['tech_epv_list'] = tmp2

	tech_log1 = request.session['login_tech']
	sql = "SELECT DISTINCT Equipment FROM PM_CNC_Tech_due where Assigned = '%s'" % (tech_log1)  
	cur.execute(sql)
	tmp5 = cur.fetchall()
	request.session['tech_pm_list'] = tmp5


	# Below will link Asset numers to Q numbers
	sql2 = "SELECT QC1, OP1, Check1, Asset, Person FROM quality_epv_week"
	cur.execute(sql2)
	tmp3 = cur.fetchall()

	a = []
	b=[]
	for i in tmp2:
		if i[3] == tech_log1:
			c=''
			for ii in tmp3:
				if i[0] == ii[0]:
					c = c + ii[3][:-2] + '/'
			a.append(i[0])
			a.append(i[1])
			a.append(i[2])
			a.append(c)
			b.append(a)
			a=[]

	request.session['tech_epv_list'] = b

	return render(request,"tech.html",{'L':list,'cnt':cnt,'M':tmp4,'N':n,'Z':Z,'TCUR':tcur})


# Run this after updating EPV_Assest for the CNC Tech Names
def tech_epv_person_update(request):
	clock2 = 'Operator'
	clock3 = 'Once per shift'
	clock4 = 'Gauge Tech'
	db, cursor = db_set(request)   
	try:
		sql="Select Person From quality_epv_week"
		cursor.execute(sql)
		tmp = cursor.fetchall()
	except:
		cursor.execute("Alter Table quality_epv_week ADD Person Char(90)")
		db.commit()
	sql = "SELECT QC1,OP1,Check1,Desc1,Method1,Asset,Person FROM quality_epv_assets where Person <> '%s' and Person <> '%s' and Person <> '%s' " % (clock2,clock3,clock4)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	for i in tmp:
		cursor.execute("UPDATE quality_epv_week SET Person = '%s' WHERE QC1 = '%s'"% (i[6],i[0]))
		db.commit()
	return render(request,"done_test2.html")

def tech_epv_assign(request):
	clock2 = 'Operator'
	clock3 = 'Once per shift'
	clock4 = 'Gauge Tech'
	db, cursor = db_set(request)   
	try:
		sql="Select Person From quality_epv_week"
		cursor.execute(sql)
		tmp = cursor.fetchall()
	except:
		cursor.execute("Alter Table quality_epv_week ADD Person Char(90)")
		db.commit()

	s2ql = "SELECT tech FROM tkb_techs ORDER BY %s %s" % ('tech','ASC')
	cursor.execute(s2ql)
	tmp3 = cursor.fetchall()
	request.session["CNC_Tech_Names"] = tmp3

	sql = "SELECT DISTINCT QC1,Person FROM quality_epv_assets where Person <> '%s' and Person <> '%s' and Person <> '%s'  ORDER BY %s %s" % (clock2,clock3,clock4,'QC1','ASC')
	cursor.execute(sql)
	tmp = cursor.fetchall()
	a=[]
	d=[]
	b=0
	for i in tmp:
		b=b+1
		a.append(b)
		try:
			s3="SELECT Asset From quality_epv_assets where QC1 = '%s'" % (i[0])
			cursor.execute(s3)
			tmp2=cursor.fetchall()
			tmp22=tmp2[0][0]
		except:
			tmp22=''
		d.append(tmp22)

	c=zip(a,tmp,d)
	request.session["CNC_Tech_Person"] = c

	if request.POST:
		b=0
		a=[]
		aa=[]
		for i in c:
			b=b+1
			bb=str(b)
			tech1 = str(request.POST.get(bb))
			a.append(tech1)
			aa.append(i[1][0])
		bb=zip(aa,a)


		for i in bb:
			sql =( 'update quality_epv_assets SET Person="%s" WHERE QC1="%s"' % (i[1],i[0]))
			cursor.execute(sql)
			db.commit()
	
		return render(request, "redirect_sup_pie_chart.html")

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_epv_assign.html',{'args':args})

def tech_epv_week_assign(request):
	clock2 = 'Operator'
	clock3 = 'Once per shift'
	clock4 = 'Gauge Tech'
	db, cursor = db_set(request)   
	try:
		sql="Select Person From quality_epv_week"
		cursor.execute(sql)
		tmp = cursor.fetchall()
	except:
		cursor.execute("Alter Table quality_epv_week ADD Person Char(90)")
		db.commit()

	s2ql = "SELECT tech FROM tkb_techs ORDER BY %s %s" % ('tech','ASC')
	cursor.execute(s2ql)
	tmp3 = cursor.fetchall()
	request.session["CNC_Tech_Names"] = tmp3

	sql = "SELECT DISTINCT QC1,Person FROM quality_epv_week ORDER BY %s %s" % ('QC1','ASC')
	cursor.execute(sql)
	tmp = cursor.fetchall()
	a=[]
	d=[]
	b=0
	for i in tmp:
		b=b+1
		a.append(b)
		try:
			s3="SELECT Asset From quality_epv_assets where QC1 = '%s'" % (i[0])
			cursor.execute(s3)
			tmp2=cursor.fetchall()
			tmp22=tmp2[0][0]
		except:
			tmp22=''
		d.append(tmp22)

	c=zip(a,tmp,d)
	request.session["CNC_Tech_Person"] = c

	if request.POST:
		b=0
		a=[]
		aa=[]
		for i in c:
			b=b+1
			bb=str(b)
			tech1 = str(request.POST.get(bb))
			a.append(tech1)
			aa.append(i[1][0])
		bb=zip(aa,a)


		for i in bb:
			sql =( 'update quality_epv_week SET Person="%s" WHERE QC1="%s"' % (i[1],i[0]))
			cursor.execute(sql)
			db.commit()
	
		return render(request, "redirect_sup_pie_chart.html")

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_epv_week_assign.html',{'args':args})

def epv_past_fix(request):
	# Find Monday timestamp of time t
	t=int(time.time())
	pm=time.localtime(t)
	xm=pm[6]
	xm=int(xm)*86400
	t=t-xm
	pdate =''

	db,cur = db_set(request)
	# Use Monday timestamp and convert to pdate
	while pdate !='2021-10-25':
		pdate = stamp_pdate(t)

		print 'Monday:',pdate
		t=t-604800
	return


def tech_epv_complete(request, index):
	date1 = date_finder(request)
	db, cur = db_set(request) 
	sql = "SELECT * FROM quality_epv_week WHERE Id = '%s'" % (index)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2=tmp[0]
	qc1 = tmp2[2]
	op1 = tmp2[3]
	check1 = tmp2[4]
	desc1 = tmp2[5]
	meth1 = tmp2[6]
	asset1 = tmp2[7]

	# Retrieve the Id from asset list
	sql2="SELECT Id FROM quality_epv_assets where QC1='%s' and Asset='%s'"%(qc1,asset1)
	cur.execute(sql2)
	tmp4 = cur.fetchall()
	tmp44 = int(tmp4[0][0])
	# Retrieve PDate of Monday of current week
	t=int(time.time())
	pm=time.localtime(t)
	xm=pm[6]
	xm=int(xm)*86400
	t=t-xm
	pdate44 = stamp_pdate(t)

	tech = request.session['login_tech']
	cur.execute('''INSERT INTO quality_epv_checks(date1,check1,description1,asset1,master1,clock_num,Asset_Id,Week_Start) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''', (date1,qc1,desc1,asset1,meth1,tech,tmp44,pdate44))
	db.commit()
	dql = ('DELETE FROM quality_epv_week WHERE Id="%s"' % (index))
	cur.execute(dql)
	db.commit()
	index = request.session['tech_epv_qc'] 
	sql = "SELECT * FROM quality_epv_week WHERE QC1 = '%s'" % (index)
	cur.execute(sql)
	tmp = cur.fetchall()

	# Fix all past EPVs
	a=[]
	b=[]
	ctr = 0

# Determine dates missed previously and add them in as done
	dates1 = []
	while pdate44 > '2021-04-30':
		t=t-604800
		pdate44=stamp_pdate(t)
		dates1.append(pdate44)
	sql3="SELECT * FROM quality_epv_checks WHERE Asset_Id='%s'"%(tmp44)
	cur.execute(sql3)
	tmp3=cur.fetchall()
	dates2 =[]
	dates_missed=[]
	for i in tmp3:
		dates2.append(i[11])
	for i in dates1:
		if i not in dates2:
			dates_missed.append(i)  # This will be the dates missed variable

	for i in dates_missed:
		cur.execute('''INSERT INTO quality_epv_checks(date1,check1,description1,asset1,master1,clock_num,Asset_Id,Week_Start) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''', (i,qc1,desc1,asset1,meth1,tech,tmp44,i))
		db.commit()


	db.close()
	request.session['tech_epv_list2'] = tmp


	return render(request,"redirect_tech.html")

def tech_pm_complete(request, index):
	t = int(time.time())
	# date1 = date_finder(request)
	db, cur = db_set(request) 

	# This will take an old check done and move it somewhere so we can enter new check
	sql="SELECT MAX(Id) FROM PM_CNC_Tech_checks"
	cur.execute(sql)
	tmp=cur.fetchall()
	id_ctr=int(tmp[0][0])
	id_ctr = id_ctr + 1
	rql =( 'update PM_CNC_Tech_checks SET Id="%s" WHERE Id="%s"' % (id_ctr,index))
	cur.execute(rql)
	db.commit()

	cur.execute('''INSERT PM_CNC_Tech_checks Select * From PM_CNC_Tech_due where Id = "%s"''' % (index))
	db.commit()
	rql =( 'update PM_CNC_Tech_checks SET Last_Checked="%s" WHERE Id="%s"' % (t,index))
	cur.execute(rql)
	db.commit()
	rql =( 'update PM_CNC_Tech SET Last_Checked="%s" WHERE Id="%s"' % (t,index))
	cur.execute(rql)
	db.commit()
	dql = ('DELETE FROM PM_CNC_Tech_due WHERE Id="%s"' % (index))
	cur.execute(dql)
	db.commit()
	index = request.session['tech_pm_qc'] 
	sql = "SELECT * FROM PM_CNC_Tech_due WHERE Equipment = '%s'" % (index)
	cur.execute(sql)
	tmp = cur.fetchall()
	request.session['tech_pm_list2'] = tmp
	db.close()
	return render(request,"redirect_tech.html")


def tech_pm_complete_asset(request,index):

	index = str(index)
	db, cur = db_set(request) 
	
	cur.execute("""DROP TABLE IF EXISTS PM_CNC_Tech_Temp""")
	cur.execute("""CREATE TABLE IF NOT EXISTS PM_CNC_Tech_Temp LIKE PM_CNC_Tech_checks""")

	sql = "Insert PM_CNC_Tech_Temp Select * From PM_CNC_Tech_due WHERE Equipment='%s'" % (index)
	cur.execute(sql)
	# cur.execute('''INSERT PM_CNC_Tech_Temp Select * From PM_CNC_Tech_due WHERE Equipment = "%s"''') % (index)
	db.commit()
	# cursor.execute("""ALTER TABLE tkb_layered_temp DROP COLUMN Id""")
	# db.commit() 
	sql="SELECT MAX(Id) FROM PM_CNC_Tech_checks"
	cur.execute(sql)
	tmp=cur.fetchall()
	id_ctr=int(tmp[0][0])
	id_ctr = id_ctr + 1

	sql = "SELECT * FROM PM_CNC_Tech_Temp"
	cur.execute(sql)
	tmp = cur.fetchall()

	for i in tmp:
		id1 = i[0]
		rql =( 'update PM_CNC_Tech_Temp SET Id="%s" WHERE Id="%s"' % (id_ctr,id1))
		cur.execute(rql)
		db.commit()
		id_ctr = id_ctr + 1

	iql = "INSERT PM_CNC_Tech_checks Select * From PM_CNC_Tech_Temp"
	cur.execute(iql)
	db.commit()

	dql = ('DELETE FROM PM_CNC_Tech_due WHERE Equipment="%s"' % (index))
	cur.execute(dql)
	db.commit()
	db.close()




	return render(request,"redirect_master.html")


	request.session['tech_pm_asset'] = index
	if request.POST:
		try:
			button1 = int(request.POST.get("button_a"))
			if button1 == -1:
				request.session["route_1"] = 'tech_pm_complete_asset'
				return direction(request)
		except:
			date1 = request.POST.get("date_en")

		db, cur = db_set(request) 

		t = pdate_stamp(date1)
		t=str(t)
		t=t[:-2]
		
		cur.execute('''INSERT PM_CNC_Tech_checks Select * From PM_CNC_Tech_due where Equipment = "%s"''' % (index))
		db.commit()
		rql =( 'update PM_CNC_Tech_checks SET Last_Checked="%s" WHERE Equipment="%s"' % (t,index))
		cur.execute(rql)
		db.commit()
		rql =( 'update PM_CNC_Tech SET Last_Checked="%s" WHERE Equipment="%s"' % (t,index))
		cur.execute(rql)
		db.commit()
		dql = ('DELETE FROM PM_CNC_Tech_due WHERE Equipment="%s"' % (index))
		cur.execute(dql)
		db.commit()
		db.close()
		return render(request,"redirect_tech_PM_master_complete.html")

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_pm_complete_asset.html',{'args':args})


def tech_pm_complete_all(request):
	index = request.session['tech_pm_asset']
	t = request.session['tech_pm_stamp']
	# t = int(time.time())
	db, cur = db_set(request) 
	cur.execute('''INSERT PM_CNC_Tech_checks Select * From PM_CNC_Tech_due where Equipment = "%s"''' % (index))
	db.commit()
	rql =( 'update PM_CNC_Tech_checks SET Last_Checked="%s" WHERE Equipment="%s"' % (t,index))
	cur.execute(rql)
	db.commit()
	rql =( 'update PM_CNC_Tech SET Last_Checked="%s" WHERE Equipment="%s"' % (t,index))
	cur.execute(rql)
	db.commit()
	dql = ('DELETE FROM PM_CNC_Tech_due WHERE Equipment="%s"' % (index))
	cur.execute(dql)
	db.commit()
	db.close()
	return render(request,"redirect_tech_PM_master_complete.html")

def pdate_stamp(pdate):
	string=str(pdate)
	element = datetime.datetime.strptime(string,"%Y-%m-%d")
	tuple = element.timetuple()
	timestamp = time.mktime(tuple)
	return timestamp
#convery timestamp to pdate

def stamp_pdate(stamp):
	tm = time.localtime(stamp)
	ma = ''
	da = ''
	if tm[1] < 10: ma = '0'
	if tm[2] < 10: da = '0'
	y1 = str(tm[0])
	m1 = str(tm[1])
	d1 = str(tm[2])
	pdate = y1 + '-' + (ma + m1) + '-' + (da + d1)
	return pdate


def tech_pm_summary(request):
	t = int(time.time())
	db, cur = db_set(request) 
	sql = "SELECT DISTINCT Equipment FROM PM_CNC_Tech ORDER BY %s %s" % ('Equipment','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()

	a = []
	b = []
	c = []
	tch = []
	od = []
	od_count = 0
	for i in tmp:
		sql = "SELECT MIN(Last_Checked),MIN(Frequency),MIN(Assigned) FROM PM_CNC_Tech WHERE Equipment = '%s'" % (i[0])
		cur.execute(sql)
		tmp3 = cur.fetchall()
		tmp2=tmp3[0][0]
		tmp22=tmp3[0][1]
		tmp33=tmp3[0][2]
		x=int(tmp2)
		y=int(tmp22)
		z=x+y
		a.append(i[0])
		tch.append(tmp33)
		hr = stamp_pdate(int(z))
		yy=int(x)

		if int(z) < int(t):
			over_due = 1
			od_count = od_count + 1
		else:
			over_due = 0

		pd = stamp_pdate(int(x))
		c.append(pd)
		b.append(hr)
		od.append(over_due)
	c = zip(b,a,c,od,tch)
	c.sort()
	request.session['CNC_Tech_Overdue_PM'] = od_count


	# c = zip(a,b,c)


	request.session["PM_Tech_Due"] = c

	# sql = "SELECT DISTINCT Equipment FROM PM_CNC_Tech ORDER BY %s %s" % ('Equipment','ASC')
	# cursor.execute(sql)
	# tmp2 = cursor.fetchall()
	
	# a=[]
	# b=[]
	# for i in tmp2:
		


	return render(request,"tech_pm_summary.html")


def tech_epv(request, index):	
	request.session['tech_epv_second'] = 1
	index = str(index)
	db, cur = db_set(request) 
	sql = "SELECT * FROM quality_epv_week WHERE QC1 = '%s'" % (index)
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()
	request.session['tech_epv_qc'] = index
	request.session['tech_epv_second'] = 1
	request.session['tech_epv_list2'] = tmp
	return render(request,"redirect_tech.html")

def tech_pm(request, index):	
	request.session['tech_pm_second'] = 1
	index = str(index)
	db, cur = db_set(request) 
	sql = "SELECT * FROM PM_CNC_Tech_due WHERE Equipment = '%s'" % (index)
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()




	request.session['tech_pm_list2'] = tmp
	request.session['tech_pm_qc'] = index
	return render(request,"redirect_tech.html")
	
def tech_epv_back(request):
	request.session['tech_epv_second'] = 0
	return render(request,"redirect_tech.html")

def tech_pm_back(request):
	request.session['tech_pm_second'] = 0
	return render(request,"redirect_tech.html")

def tech_message_close(request):
	request.session["refresh_tech"] = 0
	I = request.session["message_id"]
	C = 1
	db, cur = db_set(request)
	sql = ('update tkb_message SET Complete="%s" WHERE idnumber ="%s"' % (C,I))
	cur.execute(sql)
	db.commit()
	return tech(request)

def tech_message_reply1(request):
	request.session["refresh_tech"]=0
	I = request.session["message_id"]
	C = 1
	db, cur = db_set(request)
	sql = ('update tkb_message SET Complete="%s" WHERE idnumber ="%s"' % (C,I))
	cur.execute(sql)
	db.commit()
	return tech_message_reply2(request)
	
	
def job_call(request, index):	
	
	tec = request.session["login_tech"]

	# Select prodrptdb db located in views_db
	db, cur = db_set(request)  
	sql =( 'update pr_downtime1 SET whoisonit="%s" WHERE idnumber="%s"' % (tec,index))
	cur.execute(sql)
	db.commit()
	db.close()

	return tech(request)

def job_close(request, index):	
	

	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)  
		

	sql = "SELECT whoisonit FROM pr_downtime1 where idnumber='%s'" %(index)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = tmp[0]
	
	ssql = "SELECT * FROM pr_downtime1 where idnumber='%s'" %(index)
	cursor.execute(ssql)
	ttmp = cursor.fetchall()
	m2 = ttmp[0]
	m1 = m2[0]
	m3 = m2[1]
	#m2 = ttmp[1]
	
	
	try:
		request.session["tech_comment"]
	except:
		request.session["tech_comment"] = ""

		
	if request.POST:
		
		# take comment into tx and ensure no "" exist.  If they do change them to ''
		
		tx = request.POST.get("comment")
		tx = ' ' + tx
		if (tx.find('"'))>0:
			#request.session["test_comment"] = tx
			#return out(request)
			ty = list(tx)
			ta = tx.find('"')
			tb = tx.rfind('"')
			ty[ta] = "'"
			ty[tb] = "'"
			tc = "".join(ty)
		else:
			tc = tx
		request.session["tech_comment"] = tc
		t = datetime.datetime.now()
		

		# Select prodrptdb db located in views_db
		db, cur = db_set(request)  

		sql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (tc,index))
		cur.execute(sql)
		db.commit()
		db.close()
		
		db, cur = db_set(request)  
		tql =( 'update pr_downtime1 SET completedtime="%s" WHERE idnumber="%s"' % (t,index))
		cur.execute(tql)
		db.commit()
		db.close()

		return tech(request)
		
	else:
		form = tech_closeForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_close.html',{'Machine':m1,'Description':m3,'args': args})
#	return render(request,'tech_message_form.html', {'List':tmp,'A':A,'args':args})	
		
def tech_logout(request):	

	if request.POST:
					
		tec = request.POST.get("user")
		pwd = request.POST.get("pwd")

	
		request.session["login_tech"] = tec
		
		
		
		return tech(request)
		
	else:
		form = tech_loginForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	request.session["login_tech"] = "none"
	return render(request,'tech_login.html', args)	
	
def job_pass(request, index):	
	
	db, cursor = db_set(request)  
	sql = "SELECT whoisonit FROM pr_downtime1 where idnumber='%s'" %(index)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	tmp2 = tmp[0]
	db.close()
	try:
		request.session["tech_comment"]
	except:
		request.session["tech_comment"] = ""

		
	if request.POST:

		tc = request.POST.get("comment")
		request.session["tech_comment"] = tc
		tp = request.POST.get("pass")
		request.session["tech_pass"] = tp
		t = datetime.datetime.now()
		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)

		sql =( 'update pr_downtime1 SET remedy="%s" WHERE idnumber="%s"' % (tc,index))
		cur.execute(sql)
		db.commit()
		db.close()
		
		db, cur = db_set(request)  
		tql =( 'update pr_downtime1 SET whoisonit="%s" WHERE idnumber="%s"' % (tp,index))
		cur.execute(tql)
		db.commit()
		db.close()

		return tech(request)
		
	else:
		form = tech_closeForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_pass.html', args)		

							  
def tech_recent(request):

	
	db, cursor = db_set(request)  		
	sql = "SELECT * FROM pr_downtime1 ORDER BY called4helptime DESC limit 100" 
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close
	machine="Recent Machine Breakdowns"
	request.session["machine_search"] = machine
	request.session["tech_display"] = 1
	return render(request,"tech_search_display.html",{'machine':tmp})
	
def tech_recent2(request):
	db, cursor = db_set(request)  		
	sql = "SELECT * FROM pr_downtime1 ORDER BY called4helptime DESC limit 100" 
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close
	machine="Recent Machine Breakdowns"
	request.session["machine_search"] = machine
	request.session["tech_display"] = 1
	return render(request,"tech_search_display2.html",{'machine':tmp})
	
def tech_map(request):

	return render(request,"tech_map.html")	

def tech_history(request):	

	if request.POST:
					
		machine = request.POST.get("machine")
		request.session["machine_search"] = machine
		db, cur = db_set(request) 
		if len(machine) == 3:
			sql = "SELECT * FROM pr_downtime1 where LEFT(machinenum,3) = '%s' ORDER BY called4helptime DESC limit 20" %(machine)
		else:
			sql = "SELECT * FROM pr_downtime1 where LEFT(machinenum,4) = '%s' ORDER BY called4helptime DESC limit 20" %(machine)
		cur.execute(sql)
		tmp = cur.fetchall()
		db.close
		request.session["tech_display"] = 0
		return render(request,"tech_search_display.html",{'machine':tmp})
		
	else:
		
		form = tech_searchForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_search.html', args)		

def tech_history2(request):	
	if request.POST:     			
		machine = request.POST.get("machine")
		request.session["machine_search"] = machine
		db, cur = db_set(request) 
		if len(machine) == 3:
			sql = "SELECT * FROM pr_downtime1 where LEFT(machinenum,3) = '%s' ORDER BY called4helptime DESC limit 60" %(machine)
		else:
			sql = "SELECT * FROM pr_downtime1 where LEFT(machinenum,4) = '%s' ORDER BY called4helptime DESC limit 60" %(machine)
		cur.execute(sql)
		tmp = cur.fetchall()
		db.close
		a=[]
		aa=[]
		for i in tmp:
			a=[]
			timestamp1 = calendar.timegm(i[2].timetuple())
			timestamp2 = calendar.timegm(i[7].timetuple())
			b=timestamp2 - timestamp1
			for x in i:
				a.append(x)
			a.append(b)
			aa.append(a)


		request.session["tech_display"] = 0
		return render(request,"tech_search_display2.html",{'machine':aa})
		
	else:
		
		form = tech_searchForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_search2.html', args)		

def t1_call(request):
	request.session["call_route"] = 'tech'
	request.session["url_route"] = 'tech.html'


	return supervisor_tech_call(request)
						  

def tech_message(request):	
	Tech_Manpower = []
	Tech_Manpower = tech_manpower(request)

	A = 'Chris Strutton'
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_tech_list"
	cur.execute(sql)
	tmp = cur.fetchall()

	db.close()

	if request.POST:
					
		a = request.session["login_tech"]
		b = request.POST.get("name")
		c = request.POST.get("message")
		
		

		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		cur.execute('''INSERT INTO tkb_message(Sender_Name,Receiver_Name,Info) VALUES(%s,%s,%s)''', (a,b,c))

		db.commit()
		db.close()
		
		return tech(request)
		#return done(request)
		
	else:
		form = tech_message_Form()
	

	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,'tech_message_form.html', {'List':tmp,'A':A,'TList':Tech_Manpower,'args':args})	

def tech_message_reply2(request):	
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_tech_list"
	cur.execute(sql)
	tmp = cur.fetchall()
	db.close()

	if request.POST:
					
		a = request.session["login_tech"]
		b = request.POST.get("name")
		b = request.session["sender_name_last"]
		c = request.POST.get("message")
		
		

		
		# Select prodrptdb db located in views_db
		db, cur = db_set(request)
		cur.execute('''INSERT INTO tkb_message(Sender_Name,Receiver_Name,Info) VALUES(%s,%s,%s)''', (a,b,c))

		db.commit()
		db.close()
		
		return tech(request)
		#return done(request)
		
	else:
		form = tech_message_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	
	return render(request,'tech_message_reply_form.html', {'List':tmp,'args':args})	
	
def modal_test(request):	
	a = 1
	b = 1
	request.session["modal_1"] = a
	return render(request,'modal_test.html',{'b':b})
	
# Dead Code
def email_hour_check(t_name):
	# obtain current date from different module to avoid datetime style conflict
	
	jj = 88
	h = 5
	m = 6
	ch = 0
	send_email = 0
	t=int(time.time())
	tm = time.localtime(t)
	min = tm[4]
	hour = tm[3]
	current_date = find_current_date()
	#hour = 9
	if hour >= h:
		ch = 1

		db, cursor = db_set(request)  
		try:
			sql = "SELECT sent FROM tkb_email_conf where date='%s' and employee='%s'" %(current_date,t_name)
			cursor.execute(sql)
			tmp = cursor.fetchall()
			tmp2 = tmp[0]

			
			db.close()
			#return render(request,'done_test3.html',{'D':current_date,'N':t_name,'tmp':tmp})
			
			try:
				sent = tmp2[0]
			except:
				sent = 0
		except:
			sent = 0
		if sent == 0:
			checking = 1
			cursor.execute('''INSERT INTO tkb_email_conf(date,employee,checking,sent) VALUES(%s,%s,%s,%s)''', (current_date,t_name,checking,checking))
			db.commit()
			db.close()
			jj = tech_report_email(t_name)
			
		else:
			return jj
			

	return jj
	

# Dead Code
def tech_report_email(name):
	# Current tech will be request.session.login_tech
	# Initialize counter for message length
	m_ctr = 0
	subjectA = []
	
	db, cursor = db_set(request)  		
	sql = "SELECT * FROM pr_downtime1 WHERE whoisonit = '%s' ORDER BY called4helptime DESC limit 60" %(name)
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close
	
	
	jj = len(tmp)
	#if tmp=='':
	#return render(request,'done_test5.html',{'jj':jj})
	job_assn = []
	job_date = []
	job_solution = []
	a = []
	b = []
	c = []
	d = []
	
	message_subject = 'Tech Report from :' + name
	# set request.session.email_name as the full email address for link
	email_name = 'dclark@stackpole.com'

	toaddrs = email_name
	fromaddr = 'stackpole@stackpole.com'
	frname = 'Dave'
	server = SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('StackpolePMDS@gmail.com', 'stacktest6060')
	
	
	
	message = "From: %s\r\n" % frname + "To: %s\r\n" % toaddrs + "Subject: %s\r\n" % message_subject + "\r\n" 
	message = message + message_subject + "\r\n\r\n" + "\r\n\r\n"
	for x in tmp:
		# assign job date and time to dt
		dt = x[2]
		dtt = str(x[2])
		
		dt_t = time.mktime(dt.timetuple())
		# assign current date and time to dtemp
		dtemp = vacation_temp()
		dtemp_t = time.mktime(dtemp.timetuple())
		# assign d_diff to difference in unix
		d_dif = dtemp_t - dt_t
		if d_dif < 86400:
			message = message + '[' + dtt[:16]+'] ' + x[0] + ' - ' + x[1] + ' --- ' + x[8] + "\r\n\r\n"
			m_ctr = m_ctr + 1


	
	# retrieve left first character of login_name only
	name_temp1 = name[:1]
	# retrieve last name of login name only 
	name_temp2 = name.split(" ",1)[1]
	

	


	
	#if m_ctr > 0:
	server.sendmail(fromaddr, toaddrs, message)
	server.quit()
	
	mm = m_ctr
	return mm
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<




def tech_pm_update(request):
	db, cursor = db_set(request)  
	sql = "SELECT DISTINCT Equipment,Last_Checked,Frequency FROM PM_CNC_Tech"
	cursor.execute(sql)
	tmp = cursor.fetchall()
	t = int(time.time())
	asset = []
	for i in tmp:
		if (t-int(i[2])) > int(i[1]) :
			# Check if Equipment is due.   If none found (Except) then write to due
			try:
				sql = "SELECT * FROM PM_CNC_Tech_due where Equipment='%s'" % (i[0])
				cursor.execute(sql)
				tmp3 = cursor.fetchall()
				dummy=tmp3[0]
			except:
				cursor.execute('''INSERT PM_CNC_Tech_due Select * From PM_CNC_Tech where Equipment = "%s"''' % (i[0]))
				db.commit()
	db.close()
	return

def tech_PM_assign(request):
	clock2 = 'Operator'
	clock3 = 'Once per shift'
	clock4 = 'Gauge Tech'
	db, cursor = db_set(request)   

	s2ql = "SELECT tech FROM tkb_techs ORDER BY %s %s" % ('tech','ASC')
	cursor.execute(s2ql)
	tmp3 = cursor.fetchall()
	request.session["CNC_Tech_Names"] = tmp3

	sql = "SELECT DISTINCT Equipment,Assigned FROM PM_CNC_Tech ORDER BY %s %s" % ('Equipment','ASC')
	cursor.execute(sql)
	tmp = cursor.fetchall()
	request.session["PM_Tech_Person"] = tmp


	if request.POST:
		b=0
		a=[]
		aa=[]
		for i in tmp:
			tech1 = str(request.POST.get(i[0]))
			a.append(tech1)
			aa.append(i[0])
		bb=zip(aa,a)

		for i in bb:
			sql =( 'update PM_CNC_Tech SET Assigned="%s" WHERE Equipment="%s"' % (i[1],i[0]))
			cursor.execute(sql)
			db.commit()
	
		return render(request, "redirect_master.html")

	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'tech_pm_assign.html',{'args':args})

def tech_PM_master_complete(request):
	db, cursor = db_set(request)
	sql = "SELECT DISTINCT Equipment FROM PM_CNC_Tech_due ORDER BY %s %s" % ('Equipment','ASC')
	cursor.execute(sql)
	tmp = cursor.fetchall()
	request.session["PM_Tech_Due"] = tmp
	return render(request,'tech_pm_master_complete.html')


def tech_name_update(request):
	tech = []
	#Assigned Employee
	tech.append('Jim Barker')
	tech.append('Al Vilandre')
	tech.append('Woodrow Sismar')
	tech.append('Kevin Bisch')
	tech.append('Muoi Le')
	tech.append('Scott Smith')
	tech.append('Toby Kuepfer')
	tech.append('Paul Wilson')
	tech.append('Chris Strutton')
	tech.append('Phuc Bui')


	db, cur = db_set(request)
	for x in tech:
		cur.execute('''INSERT INTO tkb_techs(tech) VALUES(%s)''', (x))
		db.commit()

	db.close()
	
	return render(request,'done_test.html')	


	




