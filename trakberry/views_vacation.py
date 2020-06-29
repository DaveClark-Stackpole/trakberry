from django.shortcuts import render_to_response
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime 
from views_db import db_open, db_set

def vacation_1(i):
	td = datetime.datetime.fromtimestamp(int(i)).strftime('%Y-%m-%d %H:%M:%S')
	return td

def back_db(request):
	#db = MySQLdb.connect(host="10.4.1.245",user="dg417",passwd="dg",db='prodrptdb')
	db = MySQLdb.connect(host="127.0.0.1",user="dg417",passwd="dg",db='prodrptdb')
	cursor = db.cursor()	
	sql = "SELECT * FROM pr_parts"
	cursor.execute(sql)
	tmp = cursor.fetchall()
	db.close()
	
	# Uncomment below line to switch to new server PMDS3 and comment above line out
	db2 = MySQLdb.connect(host="10.4.10.160",user="localhost",passwd="dg",db='prodrptdb')
	cur = db2.cursor()
	
	
	#cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_employee(Id INT PRIMARY KEY AUTO_INCREMENT,Part CHAR(30), OP CHAR(30), Machine INT(10))""")
	#cur.execute('''INSERT INTO pr_downtime1(machinenum,problem,priority,whoisonit,called4helptime) VALUES(%s,%s,%s,%s,%s)''', (machinenum,problem,priority,whoisonit,t)
	
	
	
# Methods for opening database for all and returning db and cur
def vacation_temp():
	
	t = datetime.datetime.now()
#	t = dt.datetime.today().strftime("%m/%d/%Y")
#	t = dt.datetime.today().strftime("%Y-%m-%d")
#	Change host , username , password and db to suit 
#	x=t.strftime('%Y-%m-%d')
	return t
def vacation_temp_v2():
	t = datetime.datetime.now() + datetime.timedelta(days=1)
	return t

def vacation_set_current():

	t = vacation_temp()
	month_st = t.month
	year_st = t.year
	one = 1
	current_first = str(year_st) + "-" + str(month_st) + "-" + str(one)
	current_shift = 'All'
	
	return current_first, current_shift

def vacation_set_current2():

	t = vacation_temp()
	month_st = t.month
	#month_st = month_st - 1
	year_st = t.year
	day_st = t.day
	
	#day_st = 10
	
	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
		
	return current_first

# Returns todays date formatted and yesterdays date formatted properly
def vacation_set_current2_1():
	t = vacation_temp()
	month_st = t.month 
	year_st = t.year
	day_st = t.day 

	day_st = 2
	month_st = 12
	year_st = 2019

	day_st2 = day_st - 1
	month_st2 = month_st
	if day_st2 == 0:
		month_st2 = month_st - 1
		# r=8/0
		if month_st2 == 9 or month_st2 == 4 or month_st2 == 6 or month_st2 == 11:
			day_st2 = 30
		elif month_st2 == 2:
			r1 = year_st/float(4)
			r2 = int((year_st/4))
			if r1== r2:
				day_st2 = 29
			else:
				day_st2 = 28
		else:
			day_st2 = 31
	current_first = sc2(year_st,month_st,day_st)
	current_second = sc2(year_st,month_st2,day_st2)
	return current_first,current_second

def sc2(y,m,d):
	if int(m)<10:
		current_first = str(y) + "-" + "0" + str(m) 
	else:
		current_first = str(y) + "-" + str(m) 	
	if int(d)<10:
		current_first = current_first + "-" + "0" + str(d)
	else:
		current_first = current_first + "-" + str(d)
	return current_first

def vacation_set_current77():  # This one sets hour to current one needed for whiteboard 30min past flips
	t = vacation_temp()
	tt = vacation_temp_v2()
	month_st = t.month
	year_st = t.year
	day_st = t.day
	hour_st = t.hour
	min_st = t.minute
	# hour_st = 15
	# min_st = 45

	if int(min_st) > 30:
		hour_st = int(hour_st) + 1
		if hour_st == 24:
			hour_st = 0
			month_st = tt.month
			year_st = tt.year
			day_st = tt.day

	if int(hour_st) ==23:
		hrs = int(hour_st) - 15
		shift = "Aft"
	if int(hour_st) <= 7:
		hrs = int(hour_st) + 1
		shift = "Mid"
	if int(hour_st) >7 and int(hour_st) <=15:
		shift = "Day"
		hrs = int(hour_st) - 7
	if int(hour_st) >15: 
		hrs = int(hour_st) - 15
		shift = "Aft"

	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)

	return hrs, shift, current_first


def vacation_set_current7():  # Use this one to set Kiosk Date properly
	t = vacation_temp()
	month_st = t.month
	year_st = t.year
	day_st = t.day
	day_st = day_st
	hour_st = t.hour
	
	if int(hour_st) >=23 or int(hour_st) <7:
		shift1 = "Mid"
		hour_calc = 22
	if int(hour_st) < 7:
		shift1 = "Mid"
		hour_calc = -2
	if int(hour_st) >=7 and int(hour_st) <15:
		shift1 = "Day"
		hour_calc = 6
	if int(hour_st) >=15 and int(hour_st) <23: 
		shift1 = "Aft"
		hour_calc = 14
	if int(hour_st) >=19 or int(hour_st) <7:
		shift2 = "Cont A Mid"
		shift3 = "Cont B Mid"
	if int(hour_st) >=7 and int(hour_st) <19:
		shift2 = "Cont A Day"
		shift3 = "Cont B Day"

	hour_curr = int(hour_st) - hour_calc
		

	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
	

	return current_first, shift1, shift2, shift3, hour_curr
	
def vacation_set_current6(t):
	month_st = t.month
	year_st = t.year
	day_st = t.day
	day_st = day_st


	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
		
	return current_first



def vacation_set_current5():  # Use this one to set Kiosk Date properly

	t = vacation_temp()


	month_st = t.month
	year_st = t.year
	day_st = t.day
	day_st = day_st
	hour_st = t.hour

	if int(hour_st) >= 3 and int(hour_st) <= 11:
		shift = "Mid"
	if int(hour_st) >11 and int(hour_st) <=19:
		shift = "Day"
	if int(hour_st) > 19 and int(hour_st) <24: 
		shift = "Aft"
	if int(hour_st) <3:
		shift = "Aft"
		day_st = day_st - 1
		

	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
		
	return current_first, shift
	
def vacation_set_current3():

	t = vacation_temp()
	month_st = t.month
	#month_st = month_st - 1
	year_st = t.year
	day_st = t.day
	
	# Force it to start from June 19
	day_st = 19
	month_st = 7
	
	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
		
	return current_first

def vacation_set_current4(t):

	#t = vacation_temp()
	month_st = t.month
	#month_st = month_st - 1
	year_st = t.year
	day_st = t.day
	
	#day_st = 12
	
	if int(month_st)<10:
		current_first = str(year_st) + "-" + "0" + str(month_st) 
	else:
		current_first = str(year_st) + "-" + str(month_st) 	
		
	if int(day_st)<10:
		current_first = current_first + "-" + "0" + str(day_st)
	else:
		current_first = current_first + "-" + str(day_st)
		
	return current_first

def vacation_set_current9():
	t = vacation_temp()
	month_st = t.month
	year_st = t.year
	day_st = t.day
	hour_st = int(t.hour)
	min_st = t.minute
	min_st_st = str(min_st)
	if len(min_st_st) < 2:
		min_st_st = "0" + min_st_st
	weekday_st = t.weekday()
	if month_st < 10 and hour_st < 10:
		current_first = str(year_st) + "-0" + str(month_st) + "-" +str(day_st) + "T0"+str(hour_st) + ":" + min_st_st
	if month_st < 10 and hour_st > 10:
		current_first = str(year_st) + "-0" + str(month_st) + "-" +str(day_st) + "T"+str(hour_st) + ":" + min_st_st
	if month_st > 10 and hour_st < 10:
		current_first = str(year_st) + "-" + str(month_st) + "-" +str(day_st) + "T0"+str(hour_st) + ":" + min_st_st
	elif month_st > 10 and hour_st > 10:
		current_first = str(year_st) + "-" + str(month_st) + "-" +str(day_st) + "T"+str(hour_st) + ":" + min_st_st

	return current_first





def vacation_backup(request):

	# backup Vacation Table
	db, cursor = db_set(request)  
	
	#cursor.execute("""DROP TABLE IF EXISTS vacation_backup""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS barcode LIKE sc_production1""")
	#cursor.execute('''INSERT vacation_backup Select * From vacation''')

	db.commit()
	db.close()
	return render(request,'done_test.html')

def vacation_rebuild(request):

	# backup Vacation Table
	db, cursor = db_set(request)  
	
	#cursor.execute("""DROP TABLE IF EXISTS vacation_backup2""")
	#cursor.execute("""CREATE TABLE IF NOT EXISTS vacation_backup2 LIKE vacation_backup""")
	#cursor.execute('''INSERT vacation_backup2 Select * From vacation_backup''')

	#db.commit()
	db.close()
	return render(request,'done_test.html')
	
def vacation_restore(request):

	# backup Vacation Table
	db, cursor = db_set(request)  
	# Add something
	
	#cursor.execute("""DROP TABLE IF EXISTS vacation""")
	#cursor.execute("""CREATE TABLE IF NOT EXISTS vacation LIKE vacation_backup""")
	#cursor.execute('''INSERT vacation Select * From vacation_backup''')

	#db.commit()
	db.close()
	return render(request,'done_test.html')
	
def vacation_purge(request):

	# distinquish vacation entries that have different months
	db, cursor = db_set(request)  
	
	# cursor.execute("""DROP TABLE IF EXISTS tkb_tech_list""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_maint_list LIKE tkb_tech_list""")
	
	
	#cursor.execute('''INSERT vacation_purge Select * From vacation_backup2 where month_start != month_end ''')

	db.commit()
	db.close()
	return render(request,'done_test.html')


def create_table_1(request):
	db, cursor = db_set(request)
	# cursor.execute("""DROP TABLE IF EXISTS tkb_scrap""")   # only uncomment this line if you need to re generate the table structure or start new
	cursor.execute("""CREATE TABLE IF NOT EXISTS GFxPRoduction(Id INT PRIMARY KEY AUTO_INCREMENT,Machine CHAR(20),Part CHAR(20), PerpetualCount Double(20,2), TimeStamp Double(20,2))""")
	db.commit()
	db.close()
	return render(request,'done_test.html')


def vacation_purge_delete(request):

	# delete all entries with wrap dates
	db, cursor = db_set(request)  
	#dql = ('DELETE FROM vacation WHERE month_start != month_end ' )
	#cursor.execute(dql)
	#db.commit()
	db.close()

	return render(request,'done_test.html')

def message_create(request):

	# create Message Table
	db, cursor = db_set(request)  
	
#	cursor.execute("""DROP TABLE IF EXISTS tkb_inventory_fixed""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_inventory_fixed LIKE tkb_jobs_test""")
	#cursor.execute('''INSERT vacation_backup Select * From vacation''')

	db.commit()
	db.close()
	return render(request,'done_test.html')

def duplicate_1(request):

	# distinquish vacation entries that have different months
	db, cursor = db_set(request)  
	
	cursor.execute("""DROP TABLE IF EXISTS duplicates""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS duplicates LIKE barcode""")

	var1 = "5401"
	var2 = "8670"
	s1 = "0"
	

	# mql = "SELECT * FROM barcode WHERE left(asset_num,length(asset_num)-4) = '%s'" %(bar3)

	mql = "SELECT * FROM barcode WHERE right(asset_num,4) = '%s' or right(asset_num,4) = '%s'" %(var1,var2)
	cursor.execute(mql)
	tmp2 = cursor.fetchall()
	# dd = request.session["kkk"]
	# cursor.execute('''INSERT INTO barcode(asset_num,scrap,skid,part) VALUES(%s,%s,%s,%s)''', (i[1],i[2],i[3],i[3])) 

	for i in tmp2:
		cursor.execute('''INSERT INTO barcode(asset_num,scrap,skid,part) VALUES(%s,%s,%s,%s)''', (i[1],i[2],i[3],i[3]))
		db.commit()

	# db.commit()

    # kk = request.session["bbummy"]

    
    # try:
    #  tmp3=tmp2[0]
    #  tmp4=tmp3[0]
    #  timestamp = tmp3[2]
    #  dd = vacation_1(stamp)
    #  d = vacation_1(timestamp)
    #  request.session["alert_time"] = d
    #  request.session["now_time"] = dd
    #  request.session["diff_time"] = int(stamp - timestamp)
    #  return render(request,"barcode_alert.html")

    # except:
    #   dummy = 1


	
	# #cursor.execute('''INSERT vacation_purge Select * From vacation_backup2 where month_start != month_end ''')

	# db.commit()
	db.close()
	return render(request,'done_test.html')