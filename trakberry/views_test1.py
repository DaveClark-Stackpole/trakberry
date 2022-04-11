from django.shortcuts import render_to_response
#from math import trunc
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render
from trakberry.forms import login_Form
from django.http import HttpResponse
from views_db import db_open, db_set
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from smtplib import SMTP
import MySQLdb
import time
import datetime

def kiosk_name(request):
	if request.POST:
		kiosk_id = request.POST.get("kiosk_id")
		request.session["kiosk_id"] = kiosk_id
		return render(request,'done_test8.html')
	else:
		form = login_Form()
	args = {}
	args.update(csrf(request))
	args['form'] = login_Form
	return render(request,'kiosk_id.html', args)	

def update_column(request):
	db, cur = db_set(request)
	old_value = "OP30"
	new_value = "PP30"
	part1 = "50-9341"
	cql = ('update sc_production1 SET machine = "%s" WHERE machine ="%s"  and partno = "%s"' % (old_value,new_value,part1))
	cur.execute(cql)
	db.commit()
	db.close()
	return render(request,'done_test8.html')


def pdate_stamp(pdate):
	string=str(pdate)
	element = datetime.datetime.strptime(string,"%Y-%m-%d")
	tuple = element.timetuple()
	timestamp = time.mktime(tuple)
	return timestamp

def stamp_pdate(stamp):
	stamp=stamp+86400
	tm = time.localtime(stamp)
	ma = ''
	da = ''
	if tm[1] < 10: ma = '0'
	if tm[2] < 10: da = '0'
	y1 = str(tm[0])
	m1 = str(tm[1])
	d1 = str(tm[2])
	pdate = y1 + '-' + (ma + m1) + '-' + (da + d1)
	hr1 = str(tm[3])

	return pdate, hr1

def balancer_1508(request):
	db, cur = db_set(request)
	stamp1 = 1647835201  # March 21 12am
	m = '1508'
	cur.execute("""CREATE TABLE IF NOT EXISTS temp_balancer(Id INT PRIMARY KEY AUTO_INCREMENT,pdate CHAR(80), hour CHAR(80), count INT(20))""")
	db.commit()
	sql = "SELECT * FROM GFxPRoduction where TimeStamp >= '%d' and Machine = '%s'" %(stamp1,m)
	cur.execute(sql)
	tmp = cur.fetchall()	
	ctr = 0
	# pdate = []
	pdate2, hr2 = stamp_pdate(tmp[0][4])
	for i in tmp:
		pdate1, hr1 = stamp_pdate(i[4])
		if pdate1 == pdate2 and hr1 == hr2:
			ctr = ctr + 1
		else:
			cur.execute('''INSERT INTO temp_balancer(pdate,hour,count) VALUES(%s,%s,%s)''', (pdate2,hr2,ctr))
			db.commit()
			# pd = pdate2 + '(' + hr2 + ') -' + str(ctr)
			ctr = 0
			pdate2 = pdate1
			hr2 = hr1
			# pdate.append(pd)
			
	# request.session['pdate8'] = pdate

	return render(request,'done_test8.html')




