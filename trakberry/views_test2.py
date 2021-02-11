from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import kiosk_dispForm1,kiosk_dispForm2,kiosk_dispForm3,kiosk_dispForm4, sup_downForm
from trakberry.views import done
from views2 import main_login_form
from views3 import shift_area
from views_mod1 import find_current_date
from trakberry.views2 import login_initial
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
from views_db import db_open, db_set
from views_mod1 import kiosk_lastpart_find, kiosk_email_initial
from datetime import datetime
import datetime


def prediction1(request,st,fi,interval1,shst):
	x=[]
	y=[]
	start1 = st
	finish1 = fi
	prediction1 = 1612983600
	machine = '1533'
	db, cur = db_set(request)
	sql = "SELECT TimeStamp,PerpetualCount FROM GFxPRoduction WHERE Machine = '%s' and TimeStamp > '%d' and TimeStamp < '%d' ORDER BY %s %s" %(machine,shst,finish1,'TimeStamp','ASC')
	cur.execute(sql)
	tmp7=cur.fetchall()
	start_count = tmp7[0][1]

	sql = "SELECT TimeStamp,PerpetualCount FROM GFxPRoduction WHERE Machine = '%s' and TimeStamp > '%d' and TimeStamp < '%d' ORDER BY %s %s" %(machine,start1,finish1,'TimeStamp','ASC')
	cur.execute(sql)
	tmp=cur.fetchall()


	# This will only take data in 900 second intervals to speed time
	x_ctr = start1
	x_skip = 0
	for i in tmp:
		x_temp = i[0]
		if x_skip == 0:
			x.append(i[0])
			y.append(i[1])
			x_skip = 1
			x_ctr = x_ctr + interval1
		if i[0] > x_ctr:
			x_skip = 0

	z=zip(x,y)

	m, b= machine1(request,z)
	# prediction = m * prediction1 + b
	# prediction = prediction - start_count

	return m, b, start_count
	# return render(request,"test79.html",{'prediction':prediction,'m':m,'b':b})

def machine1(request,data2):
	db, cur = db_set(request)
	cur.execute("""DROP TABLE IF EXISTS machine_test1""")
	cur.execute("""CREATE TABLE IF NOT EXISTS machine_test1(Id INT PRIMARY KEY AUTO_INCREMENT,Y DEC(18,4), X DEC(18,4),X_Xm DEC(18,4), Y_Ym DEC(18,4), X_Xm2 DEC(18,4), XXm_YYm DEC(18,4))""")
	db.commit()

# Put data in table for X and Y
	for i in data2:
		x5 = i[0]
		y5 = i[1]
		cur.execute('''INSERT INTO machine_test1(X,Y) VALUES(%s,%s)''', (x5,y5))
		db.commit()



	# Derive the Mean for X  (mean_x) and Mean for Y (mean_y)
	sql = "SELECT SUM(X) FROM machine_test1"
	cur.execute(sql)
	tmp=cur.fetchall()
	sumx = float(tmp[0][0])
	sql = "SELECT COUNT(X) FROM machine_test1"
	cur.execute(sql)
	tmp=cur.fetchall()
	cntx = float(tmp[0][0])
	sql = "SELECT SUM(Y) FROM machine_test1"
	cur.execute(sql)
	tmp=cur.fetchall()
	sumy = float(tmp[0][0])
	sql = "SELECT COUNT(Y) FROM machine_test1"
	cur.execute(sql)
	tmp=cur.fetchall()
	cnty = float(tmp[0][0])
	mean_x = sumx / float(cntx)
	mean_y = sumy / float(cnty)


	sql = "SELECT * FROM machine_test1"
	cur.execute(sql)
	tmp=cur.fetchall()

	for i in tmp:
		x_xm = mean_x - float(i[2])
		x_xm2 = x_xm**2
		y_ym = mean_y - float(i[1])
		xy = x_xm * y_ym
		cql = ('update machine_test1 SET X_Xm = "%s" WHERE (Id="%s")' % (x_xm,i[0]))
		cur.execute(cql)
		db.commit()
		cql = ('update machine_test1 SET X_Xm2 = "%s" WHERE (Id="%s")' % (x_xm2,i[0]))
		cur.execute(cql)
		db.commit()
		cql = ('update machine_test1 SET Y_Ym = "%s" WHERE (Id="%s")' % (y_ym,i[0]))
		cur.execute(cql)
		db.commit()
		cql = ('update machine_test1 SET XXm_YYm = "%s" WHERE (Id="%s")' % (xy,i[0]))
		cur.execute(cql)
		db.commit()

	sql = "SELECT SUM(X_Xm2) FROM machine_test1"
	cur.execute(sql)
	tmp=cur.fetchall()
	d = float(tmp[0][0])  # Denominator for Slope

	sql = "SELECT SUM(XXm_YYm) FROM machine_test1"
	cur.execute(sql)
	tmp=cur.fetchall()
	n = float(tmp[0][0])  #Numerator for Slope

	m = n / float(d)  # Calculates Slope
	b = mean_y - (m*mean_x)  # Calculates Y Intersept

	return m,b


