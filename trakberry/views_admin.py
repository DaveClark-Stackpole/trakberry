from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import tech_closeForm, tech_loginForm, tech_searchForm
from views_db import db_open, db_set
from views_supervisor import supervisor_tech_call
import MySQLdb
import time
import datetime
from django.core.context_processors import csrf

def fup(x):
	return x[2]
def frup(x):
	return x[11]	

def gup(x):
	return x[5]
	
def nup(x):
	return x[4]

def tup(x):
	global tst, down_time
	tst.append(str(x[5]))

	
def eup(x):
		global st, nt
		nt.append(str(x[4]))
		st.append(str(x[5]))

def mup(x):
		global dt
		dt.append(str(x[7]))
		
def pup(x):
	global lt
	lt.append(str(x[11]))
	
def retrieve(request):
	
	machine = 574
  	u = 1459479600
  	t = 1459508400
  		
	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)
  
	#sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d'" %(u)
	sql = "SELECT * FROM tkb_prodtrak where part_timestamp >= '%d' and part_timestamp< '%d' and machine = '%d'" %(u,t,machine)
	cursor.execute(sql)
	tmp = cursor.fetchall()

	
	tql = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND part_timestamp > '%d' AND part_timestamp < '%d'" %(machine, u, t)
	cursor.execute(tql)
	xmp = cursor.fetchall()
	tmp2 = xmp[0]
	total = tmp2[0]
		
	
	return render(request,"test3.html",{'tmp':tmp,'total':total})	

def master(request):
	return render(request, "master.html")
	
def master2(request):
	return render(request, "master2.html")

def tech_pm_add(request):
	db, cursor = db_set(request)
	q = '1705'
	p = '1746'
	cursor.execute("""DROP TABLE IF EXISTS pm_cnc_tech3""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS pm_cnc_tech3 LIKE PM_CNC_Tech""")
	sql2 = '''INSERT pm_cnc_tech3 SELECT * From PM_CNC_Tech where Equipment = "%s"'''%(q)
	cursor.execute(sql2)
	db.commit()
	tql = "SELECT MAX(Id) FROM PM_CNC_Tech"
	cursor.execute(tql)
	xmp = cursor.fetchall()
	mx = int(xmp[0][0])
	mx=mx+1
	sql = "SELECT * FROM pm_cnc_tech3"
	cursor.execute(sql)
	tmp = cursor.fetchall()
	for i in tmp:
		ii = i[0]
		cursor.execute("UPDATE pm_cnc_tech3 SET Equipment = '%s' WHERE Id = '%s'"% (p,ii))
		cursor.execute("UPDATE pm_cnc_tech3 SET Id = '%s' WHERE Id = '%s'"% (mx,ii))
		db.commit()
		mx=mx+1
	sql2 = '''INSERT PM_CNC_Tech SELECT * From pm_cnc_tech3'''
	cursor.execute(sql2)
	db.commit()
	db.close()
	return render(request, "master.html")




