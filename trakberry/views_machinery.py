from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import sup_downForm, sup_dispForm, sup_closeForm, report_employee_Form, sup_vac_filterForm, sup_message_Form
from trakberry.views import done
from views2 import main_login_form
from views_mod1 import find_current_date
from mod1 import hyphon_fix
from views_production import prioritize, wfp
from trakberry.views2 import login_initial
from trakberry.views_testing import machine_list_display
from mod1 import hyphon_fix, multi_name_breakdown
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
from django.http import QueryDict
import MySQLdb
import json
import time 
import smtplib
from smtplib import SMTP

from time import mktime
from datetime import datetime, date

from views_db import db_open, db_set

from django.core.context_processors import csrf

def downtime_category_enter(request):
	db, cur = db_set(request)
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_downtime_categories(Id INT PRIMARY KEY AUTO_INCREMENT,Category CHAR(80), Keyword CHAR(80))""")
	db.commit()

	sql="SELECT * FROM tkb_downtime_categories ORDER BY %s %s, %s %s" % ('Category','ASC','Keyword','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()
	request.session['downtime_category'] = tmp

	a='2023-06-01'
	b='uncategorized'
	c=''
	wql="SELECT problem,idnumber,machinenum,category FROM pr_downtime1 where completedtime >'%s' and (category ='%s' OR category IS NULL or category='%s') ORDER BY %s %s" % (a,b,c,'completedtime','ASC')
	cur.execute(wql)
	wmp = cur.fetchall()
	swmp = len(wmp)
	request.session['downtime_data'] = wmp
	request.session['downtime_data_count'] = swmp



	if request.POST:
		selection1 = request.POST.get("cat1")
		selection2 = request.POST.get("key1")
		cur.execute('''INSERT INTO tkb_downtime_categories(Category,Keyword) VALUES(%s,%s)''', (selection1,selection2))
		db.commit()
		return render(request,'redirect_downtime_category_enter.html')
	

	else:
		form = sup_closeForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form


	return render(request,'downtime_category_enter.html',{'args':args})


def downtime_category(request):

	# This will execute code
	a='2023-07-04'
	b='uncategorized'
	c=''

	db, cur = db_set(request)

	sql="SELECT problem,idnumber,machinenum,completedtime,category FROM pr_downtime1 where completedtime >'%s' and (category ='%s' OR category IS NULL or category='%s') ORDER BY %s %s" % (a,b,c,'completedtime','ASC')
	cur.execute(sql)
	tmp = cur.fetchall()


	list2 = request.session['downtime_category']
	aa=[]
	ctr = 0
	for i in tmp:
		a=[]
		p='uncategorized'
		xi = i[0].split(" ")
		for j in xi:
			key2 = j.lower()
			cat2 = filter(lambda c:c[2]==key2,list2)
			try:
				p = cat2[0][1]

			except:
				dummy = 1




		id5 = i[1]
		st5 = p
		a.append(id5)
		a.append(st5)

		aa.append(a)
		ctr = ctr + 1


		
	y = len(aa)
	request.session['Length_None'] = y
	for i in aa:
		cql = ('update pr_downtime1 SET category = "%s" WHERE idnumber = "%s"' % (i[1],i[0]))
		cur.execute(cql)
		db.commit()

	db.close()
	return render(request,'redirect_downtime_category_enter.html')



def machinery(request):
  
  # initialize current time and set 'u' to shift start time
	t=int(time.time())
	tm = time.localtime(t)
  
	date = []
	machine = []
	count = []
	tmp2=[]
	smp2=[]
	mach_cnt = []
   
  # Select prodrptdb db 
	# Select prodrptdb db located in views_db
	db, cursor = db_set(request)

	#sqlA = "SELECT SUM(qty) FROM tkb_prodtrak where machine = '%s' AND time >= '%d'" %(machine_list[i], u)
	  # Select the Qty of entries for selected machine table from the current shift only 
	  # and assign it to 'count'
	
	# Retrieve information from Database and put 2 columns in array {list}
	# then send array to Template machinery.html
	d1 = '2015-05-01'
	d2 = '2015-07-01'
	sqlA = "SELECT * FROM pr_downtime1 ORDER BY called4helptime DESC LIMIT 100" 
	
	sqlB = "SELECT machinenum, COUNT(*) FROM pr_downtime1 GROUP BY machinenum ORDER BY COUNT(*) DESC"
	

	
	cursor.execute(sqlA)
	tmp = cursor.fetchall()

	cursor.execute(sqlB)
	smp = cursor.fetchall()
	smp2 = smp[0]
	mach_cnt = smp2[0]
	a=1
	for i in range(0,100):
		
		tmp2 =(tmp[i]) 
		#machine[i]=(tmp2[0])
		
		machine.append(tmp2[0])
		date.append(tmp2[2])
		count.append(a)
	list = zip(machine,date,count)
	
	db.close()
  
  # call up 'display.html' template and transfer appropriate variables.  
	return render(request,"machinery.html",{'L':list,'M':smp})

