from django.shortcuts import render_to_response
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from smtplib import SMTP
import MySQLdb

def net1(request):
	request.session["local_switch"] = 0
	request.session["local_toggle"] = "/trakberry"
	# ###this
	# request.session["local_switch"] = 1
	# request.session["local_toggle"] = ""
	return
# Methods for opening database for all and returning db and cur
def db_open():
	# db = MySQLdb.connect(host="10.4.1.224",user="dg417",passwd="dg",db='prodrptdb')
	# cursor = db.cursor()
	# sql = "SELECT * from testtest" 
	# cursor.execute(sql)
	# tmp2 = cursor.fetchall()
	# return db, cursor+
	# Will try and connect to the PMDS Server first and test it but if it doesn't work will do local
	try:
		db = MySQLdb.connect(host="127.0.0.1",user="dg417",passwd="dg",db='prodrptdb')
		cursor = db.cursor()	# request.session["local_switch"] = 1
	# request.session["local_toggle"] = ""
		sql = "SELECT * from testtest" 
		cursor.execute(sql)
		tmp2 = cursor.fetchall()
		return db, cursor
	except:
		try:
			db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="password",db='prodrptdb')
			cursor = db.cursor()
			sql = "SELECT * from testtest" 
  			cursor.execute(sql)
  			tmp2 = cursor.fetchall()
			return db, cursor
		except:
			db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="benny6868",db='prodrptdb')
			cursor = db.cursor()
			sql = "SELECT * from testtest" 
  			cursor.execute(sql)
  			tmp2 = cursor.fetchall()
			return db, cursor

# This will set the correct database based on a error acknowledgement.	# return db, cursor
# It will aslo initialize local_toggle which is used for the workaround on templates


def db_set2(request):
	db = MySQLdb.connect(host="10.4.1.225",user="prodmon",passwd="pm258",db='prodmon')
	cursor = db.cursor()
	return db, cursor

def db_set_3(request):  # Module to set DB settings to the one that works.  Whether local or Server
	db = MySQLdb.connect(host="10.4.1.245",user="muser",passwd="wsj.231.kql",db="django_pms",port=6601)
	cursor = db.cursor()
	return db, cursor

def db_set(request):  # Module to set DB settings to the one that works.  Whether local or Server
	db = MySQLdb.connect(host="10.4.1.224",user="stuser",passwd="stp383",db='prodrptdb')
	cursor = db.cursor()
	return db, cursor

 # update

	# try:
	# 	db = MySQLdb.connect(host="127.0.0.1",user="dg417",passwd="dg",db='prodrptdb')
	# 	cursor = db.cursor()
	# 	sql = "SELECT * from testtest" 
	# 	cursor.execute(sql)
	# 	tmp2 = cursor.fetchall()
	# 	request.session["local_toggle"]="/trakberry"
	# 	return db, cursor
	# except:
	# 	try:
	# 		db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="password",db='prodrptdb')
	# 		cursor = db.cursor()
	# 		sql = "SELECT * from testtest" 
  	# 		cursor.execute(sql)
  	# 		tmp2 = cursor.fetchall()
	# 		request.session["local_toggle"]=""
	# 		return db, cursor
	# 	except:
	# 		db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="benny6868",db='prodrptdb')
	# 		cursor = db.cursor()
	# 		sql = "SELECT * from testtest" 
  	# 		cursor.execute(sql)
  	# 		tmp2 = cursor.fetchall()
	# 		request.session["local_toggle"]=""
	# 		return db, cursor
	# return

def select_test(request):
	table = 'tkb_jobs'
	col1 = 'Description'
	var1 = 'GF6 Input'
	blank = ''
	tmp2 = db_select(table,col1,var1,blank,blank,blank,blank)
	total = tmp2[0]
	return render(request,"test3.html",{'total':total})
	
		
def db_select(table,col1,var1,col2,var2,col3,var3):
	db, cursor = db_set(request)

#	if col1=='':
	sqlcommand = 'SELECT * FROM '+ table
#	elif col2=='':
#		sqlcommand = '''SELECT * FROM " + table + " where " + col1 + "== '%d'''%(var1)"
#		sqlcommand = "SELECT * FROM tkb_jobs where Description == '%d'" %(var1)

	
	cursor.execute(sqlcommand)
	tmp = cursor.fetchall()
	tmp2 = tmp[0]
	db.close()
	
	return tmp2