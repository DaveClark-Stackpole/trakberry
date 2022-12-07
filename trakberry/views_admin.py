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



def manpower_calculation(request):
	pdate='2022-10-01'
	db, cursor = db_set(request)
	cursor.execute("""DROP TABLE IF EXISTS budget_manpower""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS budget_manpower(asset_num CHAR(50), partno CHAR(50))""")
	db.commit()
	sql2 = '''INSERT budget_manpower SELECT DISTINCT(asset_num),partno FROM sc_production1 where pdate > "%s" GROUP BY asset_num,partno'''%(pdate)
	cursor.execute(sql2)
	db.commit()

	# Eliminate Unknown Assets
	asset_min = '1501'
	dql = ('DELETE FROM budget_manpower WHERE asset_num < "%s"' % (asset_min))
	cursor.execute(dql)
	db.commit()
	# Eliminate Non Press with -B or -A
	asset_min = '2'
	len1 = 7
	dql = ('DELETE FROM budget_manpower WHERE left(asset_num,1) <> "%s" and length(partno)>"%d"' % (asset_min,len1))
	cursor.execute(dql)
	db.commit()
	# Eliminate Less than 7 characters
	len1 = 7
	dql = ('DELETE FROM budget_manpower WHERE length(partno) < "%d"' % (len1))
	cursor.execute(dql)
	db.commit()
	# Eliminate Press non Component 
	asset_min = '2'
	len1 = 9
	dql = ('DELETE FROM budget_manpower WHERE left(asset_num,1) = "%s" and length(partno)<"%d"' % (asset_min,len1))
	cursor.execute(dql)
	db.commit()
	# Eliminate 35- if not starts with 2,3,4 
	asset1 = '2'
	asset2 = '3'
	asset3 = '4'
	asset4 = '1516'
	op1 = '1'
	op2 = '2'

	pn1 = '35'
	dql = ('DELETE FROM budget_manpower WHERE left(partno,2) = "%s" and (left(asset_num,1)<> "%s" AND left(asset_num,1)<> "%s" AND left(asset_num,1)<>"%s")' % (pn1,asset1,asset2,asset3))
	cursor.execute(dql)
	db.commit()
	# Add Colun for Median
	cursor.execute("""ALTER TABLE budget_manpower ADD rate INT(40) NOT NULL DEFAULT 0 AFTER partno""")
	db.commit() 

	cursor.execute("""ALTER TABLE budget_manpower ADD OP CHAR(40) NOT NULL DEFAULT 0 AFTER partno""")
	db.commit() 

	cursor.execute("UPDATE budget_manpower SET OP = '%s' WHERE LEFT(asset_num,1) = '%s'"% (op1,asset1))
	db.commit()
	cursor.execute("UPDATE budget_manpower SET OP = '%s' WHERE LEFT(asset_num,1) = '%s'"% (op2,asset2))
	db.commit()
	cursor.execute("UPDATE budget_manpower SET OP = '%s' WHERE LEFT(asset_num,1) = '%s'"% (op2,asset4))
	db.commit()

	sql = "SELECT * FROM budget_manpower"
	cursor.execute(sql)
	tmp = cursor.fetchall()


	sql = "SELECT asset_num,partno,actual_produced,shift_hours_length FROM sc_production1 where pdate>'%s'" % (pdate)
	cursor.execute(sql)
	tmp2=cursor.fetchall()


	for i in tmp:
		asset1 = i[0]
		part1 = i[1]


		a3 = filter(lambda c:c[0]==asset1 and c[1]==part1,tmp2)  

		a5 = filter(lambda c:c[0]==asset1 and c[1]==part1 and c[2]>0,tmp2)  

		a6 = filter(lambda c:c[0]==asset1 and c[1]==part1 and c[2]==0,tmp2) 


		# try:
		# 	a4 = filter(lambda c:c[0]==asset1 and c[1]==part1 and c[2]>0 and c[3]==8,tmp2)  
		# 	a4=sorted(a4,key=lambda x:x[2])
		# 	count_a4 = len(a4) / float(2)
		# 	count_a4=int(count_a4)
		# 	median1 = a4[count_a4][2]
		# 	rate1 = median1 / float(8)
		# except:
		# 	median1=0
		# 	rate1=0

		# try:
		a4 = filter(lambda c:c[0]==asset1 and c[1]==part1 and c[2]>0 and c[3]>0,tmp2)  



		ee=3/0

		a4=sorted(a4,key=lambda x:x[2])
		count_a4 = len(a4) / float(2)
		count_a4=int(count_a4)
		median1 = a4[count_a4][2]
		rate1 = median1 / float(8)
		# except:
		# 	median1=0
		# 	rate1=0


		# hrs_zero = sum(map(lambda x: int(x[3]), a6))
		# hrs_non = sum(map(lambda x: int(x[3]), a5))
		# cnt_total = sum(map(lambda x: int(x[2]), a5))
		# cnt_rate = rate1 * hrs_non

		# hrs = hrs_zero + hrs_non
		# cnt = cnt_rate


		# cnt = sum(map(lambda x: int(x[2]), a3))
		# hrs = sum(map(lambda x: int(x[3]), a3))


		# q=23/0


		# sql = "SELECT actual_produced,pdate,shift,shift_hours_length FROM sc_production1 where pdate>'%s' and asset_num='%s' and partno='%s'" % (pdate,asset1,part1)
		# cursor.execute(sql)
		# tmp2=cursor.fetchall()
		# tmp2_sorted = sorted(tmp2,key=lambda x:(x[1],x[2]))

		# sql = "SELECT sum(actual_produced),sum(shift_hours_length) FROM sc_production1 where pdate>'%s' and asset_num='%s' and partno='%s'" % (pdate,asset1,part1)
		# cursor.execute(sql)
		# tmp2=cursor.fetchall()

		# cnt = int(tmp2[0][0])
		# hrs = int(tmp2[0][1])
		# rate = cnt/float(hrs) * 40

		

		cursor.execute("UPDATE budget_manpower SET rate = '%s' WHERE asset_num = '%s' and partno='%s'"% (rate1,asset1,part1))
		db.commit()







	return render(request,"test58.html")	 



	
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




