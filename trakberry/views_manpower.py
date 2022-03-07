from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from trakberry.forms import login_Form, login_password_update_Form, kiosk_dispForm4, sup_downForm
from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os,sys
from django.core.context_processors import csrf
from shutil import copyfile
import MySQLdb
import time
import os
import smtplib
from smtplib import SMTP
import xlrd
#import pandas
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current2,vacation_set_current6, vacation_set_current4
from views_vacation import vacation_set_current5,vacation_set_current9
from views3 import matrix_read,shift_area

def manpower_layout(request):

	db, cur = db_set(request)
	TimeOut = -1
	part = '50-9341'
	sql = "SELECT DISTINCT asset_num FROM sc_production1 WHERE partno = '%s'" %(part)
	cur.execute(sql)
	tmp = cur.fetchall()
	return render(request, "kiosk/kiosk_test.html",{'tmp':tmp})

def matrix_initial_v2(request):
	db, cursor = db_set(request)  
	cursor.execute("""DROP TABLE IF EXISTS tkb_matrix_cache""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix_cache(Id INT PRIMARY KEY AUTO_INCREMENT,Area CHAR(80), Shift CHAR(80), Matrix TEXT(1000000), Job TEXT(1000000))""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_matrix""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Job Char(100), Trained Char(100),Enabled CHAR(10),Clock CHAR(80))""")
	db.commit()
	db.close()

	return

def manpower_initial_v2(request):
	db, cursor = db_set(request)  
	cursor.execute("""DROP TABLE IF EXISTS tkb_manpower2""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_manpower""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_manpower(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Clock CHAR(80), Shift_Mod Char(80))""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_allocation""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_allocation2""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_allocation(Id INT PRIMARY KEY AUTO_INCREMENT,Job CHAR(80), Area CHAR(80),Asset1 CHAR(20),Asset2 CHAR(20),Asset3 CHAR(20),Asset4 CHAR(20),Asset5 CHAR(20),Asset6 CHAR(20),Sig1 Char(10), Part1 CHAR(20), Part2 CHAR(20), Part3 CHAR(20), Part4 CHAR(20))""")
	db.commit()
	db.close()
	return

def manpower_update_v2(request):
		# comment below when running local
	label_link = '/home/file/import1/Inventory/importedxls'
	os.chdir(label_link)
	# ********************************

	sheet = 'inventory.xlsx'
	sheet_name = 'Sheet1'

	book = xlrd.open_workbook(sheet)
	working = book.sheet_by_name(sheet_name)
	tot = 266  # Row on Excel Sheet
	toc = 35   # Col on Excel Sheet
	tdate = tot+1
	jj = 1
	a = []
	b = []
	c = []
	job1 = [[] for xx in range(600)]
	area1 = [[] for yy in range(600)]
	asset1 = [[] for zz in range(600)]
	asset2 = [[] for zz in range(600)]
	asset3 = [[] for zz in range(600)]
	asset4 = [[] for zz in range(600)]
	asset5 = [[] for zz in range(600)]
	asset6 = [[] for zz in range(600)]
	sig1 = [[] for ww in range(600)]
	part1 = [[] for uu in range(600)]
	part2 = [[] for uu in range(600)]
	part3 = [[] for uu in range(600)]
	part4 = [[] for uu in range(600)]

	for fnd in range(1,400):  # Determine what row to start reading manpower from
		fnd_cell = str(working.cell(fnd,0).value)
		if fnd_cell == 'Plant 1 Days':
			start1 = fnd
			break
	
	for i in range((start1+1),(start1+60)):
		for ii in range(0,21):
			if len(str(working.cell(i,ii).value)) > 5:
				zz = ii + 21
				z = str(working.cell(i,zz).value)
				x = str(working.cell(i,ii).value) 
				if x[-1:] == ';':
					xlen = len(x)
					x = x[:(xlen-1)]
				y = str(working.cell(start1,ii).value) 
				a.append(x)
				b.append(y)
				c.append(z)

				jj = jj + 1
	a=tuple(a)
	b=tuple(b)
	c=tuple(c)
	abc=zip(a,b,c)

	# # return render(request,"test71.html",{'matrix':abc})
	for fnd in range(start1,900):  # Determine what row to start reading jobs from
		fnd_cell = str(working.cell(fnd,0).value)
		if fnd_cell == 'Area 1':
			start2 = fnd-1
			break
	kk = 1
	for i in range((start2+1),(start2+180)):
		try:
			if len(str(working.cell(i,0).value)) > 5:
				area_allocation = str(working.cell(i,0).value) 
				job_allocation = str(working.cell(i,1).value) 
				a1 = str(working.cell(i,2).value) 
				a2 = str(working.cell(i,3).value) 
				a3 = str(working.cell(i,4).value)
				a4 = str(working.cell(i,5).value)
				a5 = str(working.cell(i,6).value)
				a6 = str(working.cell(i,7).value)
				sig = str(working.cell(i,8).value)
				p1 = str(working.cell(i,9).value)
				p2 = str(working.cell(i,10).value)
				p3 = str(working.cell(i,11).value)
				p4 = str(working.cell(i,12).value) 

				area1[kk].append(area_allocation)
				job1[kk].append(job_allocation)
				asset1[kk].append(a1)
				asset2[kk].append(a2)
				asset3[kk].append(a3)
				asset4[kk].append(a4)
				asset5[kk].append(a5)
				asset6[kk].append(a6)
				sig1[kk].append(sig)
				part1[kk].append(p1)
				part2[kk].append(p2)
				part3[kk].append(p3)
				part4[kk].append(p4)
				kk = kk + 1
			else:
				break
		except:
			break
	manpower_initial_v2(request)
# # 	# Write new Manpower and Allocation
	db, cur = db_set(request)
	x = 1
	adj_shift = [('A Days P1','Plant 1 Days'),('B Days P1','Plant 1 Days'),('A Days A3','Plant 4 Day'),('B Days A3','Plant 4 Day'),('A Nights P1','Plant 1 Mid'),('B Nights P1','Plant 1 Mid'),('A Nights A3','Plant 4 Mid'),('B Nights A3','Plant 4 Mid')]
	for i in abc:
		y = str(i[0])
		yy = str(i[1])
		yyy = str(i[2])
		cur.execute('''INSERT INTO tkb_manpower(Employee,Shift,Clock,Shift_Mod) VALUES(%s,%s,%s,%s)''', (y,yy,yyy,yy))
		db.commit()
	for i in range(1,kk):
		job3 = str(job1[i][0])
		area3 = str(area1[i][0])
		a1 = str(asset1[i][0])
		a2 = str(asset2[i][0])
		a3 = str(asset3[i][0])
		a4 = str(asset4[i][0])
		a5 = str(asset5[i][0])
		a6 = str(asset6[i][0])
		s3 = str(sig1[i][0])
		p1 =  str(part1[i][0])
		p2 =  str(part2[i][0])
		p3 =  str(part3[i][0])
		p4 =  str(part4[i][0])
		cur.execute('''INSERT INTO tkb_allocation(Job,Area,Asset1,Asset2,Asset3,Asset4,Asset5,Asset6,Sig1,Part1,Part2,Part3,Part4) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (job3,area3,a1,a2,a3,a4,a5,a6,s3,p1,p2,p3,p4))
		db.commit()

# Fix Continental Shifts Mod
	adj_shift = [('A Days P1','Plant 1 Days'),('B Days P1','Plant 1 Days'),('A Days A3','Plant 4 Day'),('B Days A3','Plant 4 Day'),('A Nights P1','Plant 1 Mid'),('B Nights P1','Plant 1 Mid'),('A Nights A3','Plant 4 Mid'),('B Nights A3','Plant 4 Mid')]
	for index in adj_shift:
		t1 = index[1]
		s1 = index[0]
		mql =( 'update tkb_manpower SET Shift = "%s" WHERE Shift_Mod ="%s"' % (t1,s1))
		cur.execute(mql)
		db.commit()


	return render(request,"redirect_auto_updater.html")


def matrix_update_v2(request):
	request.session["trained_email"] = ''
	# The below section fixes any blank asset entries so they don't mess up the matrix update
	# **************************************************************************************
	db, cur = db_set(request)
	t1 = '111'
	s1 = ''
	mql =( 'update sc_production1 SET asset_num = "%s" WHERE asset_num = "%s"' % (t1,s1))
	cur.execute(mql)
	db.commit()
	db.close()
	# **************************************************************************************

	# Dump old matrix into tkb_matrix2 for future coparison
	# ******************************************************************************
	db, cur = db_set(request)
	cur.execute("""DROP TABLE IF EXISTS tkb_matrix_old""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix_old LIKE tkb_matrix""")
	cur.execute('''INSERT tkb_matrix_old Select * From tkb_matrix''')
	db.commit()
	db.close()
	#*******************************************************************************

	matrix_initial_v2(request)  # Empty Cache and Matrix to start fresh.

# Select RollNo,Name,Subject from(select RollNo,Name,Subject from students union all select RollNo,Name,Subject from Student1)as std GROUP BY RollNo,Name,Subject HAVING Count(*) = 1 ORDER BY RollNo;



	asset_test = []
	trained_test = []
	shift = ['Plant 1 Mid','Plant 1 Aft','Plant 1 Days','Plant 3 Mid','Plant 3 Aft','Plant 3 Days','Plant 4 Mid','Plant 4 Aft','Plant 4 Day']
	# shift = ['Plant 1 Mid','Plant 1 Aft']

	
	for i in shift:
		shift1 = i
		area1 = shift_area(i)
		enabled1 = '1'
		db, cur = db_set(request)

		# Comment below to run normal
		# clock_test = '4532.0'  # Use this to test one person
		# sql="SELECT * FROM tkb_manpower where Shift = '%s' and Clock = '%s'" % (shift1,clock_test)

		# Uncomment this line
		sql="SELECT * FROM tkb_manpower where Shift = '%s'" % (shift1)

		cur.execute(sql)
		tmp1=cur.fetchall()

		sql = "SELECT * FROM tkb_allocation where Area = '%s'"%(area1)
		cur.execute(sql)
		tmp2 = cur.fetchall()
		ctr9 = 0
		for i in tmp1:
			try:
				clock = int(i[3][:-2])
			except:
				clock = 0
			name1 = i[1]
			ctr6 = 0
			for ii in tmp2:
				job1 = ii[1]
				asset1 = ii[3][:-2]
				asset2 = ii[4][:-2]
				asset3 = ii[5][:-2]
				asset4 = ii[6][:-2]
				asset5 = ii[7][:-2]
				asset6 = ii[8][:-2]
				ssig = ii[9][:-2]
				sig = int(ssig)
				part1 = ii[10]
				part2 = ii[11]
				part3 = ii[12]
				part4 = ii[13]
				
				if sig == 1:
					sql2= '''SELECT COUNT(*) FROM sc_production1 where comments = "%s" and (asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s") and (partno = "%s" or partno = "%s" or partno = "%s" or partno = "%s")''' % (clock,asset1,asset2,asset3,asset4,asset5,asset6,part1,part2,part3,part4)
					cur.execute(sql2)
					tmp3 = cur.fetchall()
					count1 = tmp3[0][0]
					count1 = int(tmp3[0][0])
				else:
					sql2= '''SELECT COUNT(*) FROM sc_production1 where comments = "%s" and (asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s")''' % (clock,asset1,asset2,asset3,asset4,asset5,asset6)
					cur.execute(sql2)
					tmp3 = cur.fetchall()
					count1 = tmp3[0][0]
					count1 = int(tmp3[0][0])

				ctr9 = ctr9 + 1
				# if ctr9 > 100:
				# 	t=5/0
				# asset_test.append(job1)
				# trained_test.append(count1)
				trained1 = 'Not Trained'
				if int(count1) > 0 and int(count1) < 5:
					trained1 = 'Training <5 days'
				elif int(count1) > 4 and int(count1) < 10:
					trained1 = 'Training >4 days'
				elif int(count1) >9 and int(count1) < 26:
					trained1 = 'Trained'
				elif int(count1) > 25 and int(count1) < 99999:
					trained1 = 'A Trainer'
				if int(count1) > 0 and int(count1) < 99999:
					dummy = 4
					cur.execute('''INSERT INTO tkb_matrix(Employee,Job,Trained,Shift,Clock) VALUES(%s,%s,%s,%s,%s)''', (name1,job1,trained1,shift1,count1))
					db.commit()
		db.close()

	db, cur = db_set(request)
	cur.execute("""DROP TABLE IF EXISTS tkb_matrix_cache""") # Clear all Cache and start fresh
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix_cache(Id INT PRIMARY KEY AUTO_INCREMENT,Area CHAR(80), Shift CHAR(80), Matrix TEXT(1000000), Job TEXT(1000000))""")
	db.close()
	shift ,area = 'Plant 1 Mid','Area 1'
	matrix_read(shift,area,request)
	shift ,area = 'Plant 1 Aft','Area 1'
	matrix_read(shift,area,request)
	shift ,area = 'Plant 1 Days','Area 1'
	matrix_read(shift,area,request)
	shift ,area = 'Plant 3 Days','Area 2'
	matrix_read(shift,area,request)
	shift ,area = 'Plant 3 Mid','Area 2'
	matrix_read(shift,area,request)
	shift ,area = 'Plant 3 Aft','Area 2'
	matrix_read(shift,area,request)
	shift ,area = 'Plant 4 Day','Area 3'
	matrix_read(shift,area,request)
	shift ,area = 'Plant 4 Aft','Area 3'
	matrix_read(shift,area,request)
	shift ,area = 'Plant 4 Mid','Area 3'
	matrix_read(shift,area,request)
	

	# ************************************************************************************************************************
	# This will find any employees from before Matrix update that weren't trained but now are and
	# will put them in a[] and their job in b[] and produce tuple trained_email
	level='Trained'
	db,cur=db_set(request)
	sql = "select * from tkb_matrix where Trained = '%s'"%(level)
	cur.execute(sql)
	tmp7=cur.fetchall()
	a=[]
	b=[]
	for i in tmp7:
		name1 = i[1]
		# small problem with people and the ' in their name
		job1 = i[3]
		level1 = i[4]
		level2='Trained'
		try:
			sql2="select * from tkb_matrix_old where Employee='%s' and Job='%s' and Trained!='%s'"%(name1,job1,level2)
			cur.execute(sql2)
			tmp8=cur.fetchall()
			try:
				# Make sure another job same name doesn't have this person trained
				sql3="select * from tkb_matrix_old where Employee='%s' and Job='%s' and Trained='%s'" %(name1,job1,level2)
				cur.execute(sql3)
				tmp9=cur.fetchall()
				try:
					tmp99=tmp9[0]
				# If it doesn't then do the except if it does then ignore
				except:
					n1 = tmp8[0][1]
					j1=tmp8[0][3]
					a.append(n1)
					b.append(j1)
			except:
				dummy='skip'
		except:
			dummy='skip'
	request.session['trained_email'] = zip(a,b)
# ***************************************************************************************************************************
	trained_email(request)  # Email the list, if any, to Melissa
	return render(request,"redirect_auto_updater.html")

def trained_email(request):
	try:
		trained1 = request.session['trained_email']
	except:
		trained1=''
	if len(trained1) > 0 :
		db,cur=db_set(request)
		date1, shift2 = vacation_set_current5()
		cur.execute("""CREATE TABLE IF NOT EXISTS tkb_trained(Id INT PRIMARY KEY AUTO_INCREMENT,Date CHAR(80), Employee CHAR(80), Job CHAR(80))""")
		db.commit()
		for x in trained1:
			cur.execute('''INSERT INTO tkb_trained(Date,Employee,Job) VALUES(%s,%s,%s)''', (date1,x[0],x[1]))
			db.commit()
		db.close()

		b = "\r\n"
		ctr = 0
		message_subject = 'Training Document Required !'
		message3 = "The following people require training documents for the noted jobs." 
		# toaddrs = ["dclark@stackpole.com","menns@stackpole.com"]
		toaddrs = ["dclark@stackpole.com","AHuehnergard@stackpole.com"]
		#toaddrs = ["rrompen@stackpole.com","rbiram@stackpole.com","rzylstra@stackpole.com","lbaker@stackpole.com","dmilne@stackpole.com","sbrownlee@stackpole.com","pmurphy@stackpole.com","pstreet@stackpole.com","kfrey@stackpole.com","asmith@stackpole.com","smcmahon@stackpole.com","gharvey@stackpole.com","ashoemaker@stackpole.com","jreid@stackpole.com"]
		fromaddr = 'stackpole@stackpole.com'
		frname = 'Dave'
		server = SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login('StackpolePMDS@gmail.com', 'stacktest6060')
		message = "From: %s\r\n" % frname + "To: %s\r\n" % ', '.join(toaddrs) + "Subject: %s\r\n" % message_subject + "\r\n" 
		message = message + "\r\n\r\n" + message3 + "\r\n\r\n" + "\r\n\r\n" 
		for i in trained1:
			employee1 = i[0]
			job1 = i[1]
			b = "\r\n"
			message = message + employee1 + "  [" + job1 + "]" + b + b
		server.sendmail(fromaddr, toaddrs, message)
		server.quit()
	return
	# return render(request,"redirect_master.html")
	# return render(request,"redirect_auto_updater.html")


def training_matrix3(request):
	request.session['matrix_update'] = 0   # This variable is determining if we update all or one person
# Set the shift and Area
	try:
		shift = request.session["matrix_shift"] 
		area = request.session["matrix_area"]
	except:
		request.session["matrix_shift"] = 'Plant 1 Mid'
		request.session["matrix_area"] = 'Area 1'
		shift = 'Plant 1 Mid'
		area = 'Area 1'
		

	try:
		dummy = request.session["bounce_matrix"]
	except:
		request.session["bounce_matrix"] = 0

	# shift ,area = 'Plant 3 Days','Area 2'
	# Read in current data for shift and area and assign to matrix and jobs
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_matrix_cache where Area = '%s' and Shift = '%s'" %(area,shift)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	matrix = tmp2[3]
	jobs = tmp2[4]
	Id1 = tmp2[0]
	matrix = eval(matrix) # Convert string from database read to required tuple
	jobs_current = jobs
	jobs = eval(jobs) # Convert string from database read to required tuple
	db.close()

	if request.POST:
		matrix_shift = request.POST.get('matrix_shift')
		matrix_area = shift_area(matrix_shift)
		request.session["matrix_shift"] = matrix_shift
		request.session["matrix_area"] = matrix_area
		return render(request,"redirect_training_matrix3.html")
	else:
		form = kiosk_dispForm4()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	request.session['data_matrix'] = matrix
	request.session['data_jobs'] = jobs

	return render(request,"training_matrix2.html",{'args':args,'matrix':matrix,'jobs':jobs})

def training_performance(request):

	if request.POST:
		asset_performance = request.POST.get('asset_performance')

		# Do the search for list of those that are good on this asset
		db, cur = db_set(request)
		a= []
		cnt = []


		sql = "SELECT * FROM sc_production1 WHERE asset_num LIKE '%s' ORDER BY actual_produced DESC limit 100" %("%" + asset_performance + "%")
		cur.execute(sql)
		tmp = cur.fetchall()

		for i in tmp:
			clock1 = i[9] + '.0'

			sql = "SELECT Employee FROM tkb_manpower WHERE Clock = '%s'" %(clock1)
			cur.execute(sql)
			tmp2 = cur.fetchall()
			b = 0
			try:
				employee1 = tmp2[0][0]
			except:
				employee1 = ''
				b=1
			check = 0
			for ii in a:
				e1 = ii
				e2 = employee1
				if e1==e2:
					check == 1
			if check == 0:
				if b == 0:
					a.append(employee1)

		request.session['training_performance_employees'] = a

		return render(request,"training_performance.html")

	else:
		form = kiosk_dispForm4()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	return render(request,"training_performance_form.html",{'args':args})

# Update Allocation Breakdown
# Only need to do this when changes occur
def manpower_allocation(request):
	# label_link = '/home/file/import1/Inventory/importedxls'
	# os.chdir(label_link)
	sheet = 'inventory.xls'  # Use this for Dell Comp only
	# sheet = 'inventory.xlsx' # Use this all other places
	sheet_name = 'Sheet1'

	book = xlrd.open_workbook(sheet)
	working = book.sheet_by_name(sheet_name)
	tot = 266  # Row on Excel Sheet
	toc = 35   # Col on Excel Sheet
	tdate = tot+1
	jj = 1
	a = []
	b = []
	c = []

	area7 = []
	job7 = []
	label7 = []

	for fnd in range(1,400):  # Determine what row to start reading manpower from
		fnd_cell = str(working.cell(fnd,0).value)
		if fnd_cell == 'Plant 1 Days':
			start1 = fnd
			break
	for fnd in range(start1,900):  # Determine what row to start reading jobs from
		fnd_cell = str(working.cell(fnd,0).value)
		if fnd_cell == 'Area 1':
			start2 = fnd-1
			break

	# initialize 1-13 for a[]
	for i in range(1,13):
		exec('a' + str(i) + '= []')
		exec('q' + str(i) + '= []')

# Read in the Area, Job, Label and Hours for Allocation
	for i in range((start2+1),(start2+180)):
		try:
			if len(str(working.cell(i,0).value)) > 5 and len(str(working.cell(i,12).value)) > 0:
				area7.append((str(working.cell(i,0).value)))
				job7.append((str(working.cell(i,1).value)))
				label_temp = ((str(working.cell(i,12).value)))
				label_temp=label_temp[:-2]
				label7.append(int(label_temp))
				hrs7 = 0
				ctr = 13
				for ii in range(13,23):
					temp3=str(working.cell(i,ii).value)
					temp3=int(temp3[:-2])
					hrs_multiplier = 8
					if ii > 18:
						hrs_multiplier=12
					hrs7=hrs7+(temp3*hrs_multiplier)
				a3.append(hrs7)

				# Read in the categories
				for ii in range(23,25):
					temp3 = str(working.cell(i,ii).value)
					try:
						temp3=int(temp3[:-2])
					except:
						dummy=0
					exec('q'+str(ii-22)+'.append(temp3)')
		except:
			break
	b=zip(label7,a3,job7)
	qq=zip(q1,q2)  # This is the list of Jobs with the label number for reference
	# c=sorted(b) # Sort the list 
	c=b
	b=c

# Sum hours grouped by labels
	w={}
	for row in c:
		if row[0] not in w:
			w[row[0]]=[]
		w[row[0]].append(row[1])
	u=[]
	j=[]
	k=[]

	r=4/0
# Put together the label, hours and Job
	for i in w:
		try:
			# u.append(i)
			# j.append(sum(w[i]))
			for ii in qq:
				if int(ii[0]) == i:
					u.append(i)
					k.append(ii[1])
					j.append(sum(w[i]))
					break
		except:
			uu=0
	job_allocation =zip(u,j,k)
	job_allocation=sorted(job_allocation)
	job_list=zip(job7,label7)
	request.session['job_allocation'] = job_allocation  # The list of Label , Allocation Hrs, Categories
	request.session['job_list'] = job_list # The list of Jobs, And each Label for those Jobs
	return render(request,"test_allocation1.html")

def manpower_allocation_interval_pick(request):
	t=int(time.time())
	tm = time.localtime(t)
	if tm[1] < 10:
		m = "0" + str(tm[1])
	else:
		m = str(tm[1])
	if tm[2] < 10:
		d = "0" + str(tm[2])
	else:
		d = str(tm[2])
	date7 = str(tm[0]) + "-" + m + "-" + d
	t=int(time.time()) - 86400
	tm = time.localtime(t)
	if tm[1] < 10:
		m = "0" + str(tm[1])
	else:
		m = str(tm[1])
	if tm[2] < 10:
		d = "0" + str(tm[2])
	else:
		d = str(tm[2])
	date6 = str(tm[0]) + "-" + m + "-" + d
	request.session["date1_default"] =  date7
	request.session["date2_default"] =  date6
	if request.POST:
		request.session["date1_allocation"] = request.POST.get("scrap_display_date1")
		request.session["date2_allocation"] = request.POST.get("scrap_display_date2")
		return manpower_allocation_calculation(request)
	else:
		form = sup_downForm()
	args = {}
	args.update(csrf(request))
	args['form'] = form
	return render(request,'manpower_allocation_interval_pick.html',{'args':args})

def manpower_allocation_calculation(request):
	date1 = request.session["date1_allocation"]
	date2 = request.session["date2_allocation"]
	db, cur = db_set(request)
	ne = 'no entry'
	aql = "SELECT Job,Hrs FROM tkb_scheduled WHERE Date1 >= '%s' and Date1 <= '%s' and Hrs <> '%s'" % (date1,date2,ne)
	cur.execute(aql)
	tmp2 = cur.fetchall()
		
	w={}
	for row in tmp2:
		if row[0] not in w:
			w[row[0]]=[]
		v=int(row[1])
		w[row[0]].append(v)

	job_list = request.session["job_list"]
	job_allocation = request.session["job_allocation"]

	
	u=[]
	j=[]
	k=[]
	for i in w:
			u.append(i)
			j.append(sum(w[i]))
			# for ii in job_list:
			# 	if (ii[0]) == i:
			# 		k.append(ii[1])
			# 		break

	# jobz =zip(k,j)
	jobz = zip(u,j)

	# Associate Job with Index number 'k' and reginerate list
	u=[]
	j=[]
	for i in jobz:
		for ii in job_list:
			if i[0] == ii[0]:
				k.append(ii[1])
				u.append(i[0])
				j.append(i[1])
				break
	jobz = zip(k,u,j)
	jobz = sorted(jobz)

	# Group all indexes with their sum of hours
	w={}
	for row in jobz:
		if row[0] not in w:
			w[row[0]]=[]
		w[row[0]].append(row[2])
	
# Sum all the indexes appropriately
	j=[]
	k=[]
	u = []
	pm = []
	for i in w:
		jj = sum(w[i])
		j.append(jj)
		for ii in job_allocation:
			if ii[0]==i:
				u.append(i)
				k.append(ii[2])
				if ii[1] < jj:
					clr7 = '#ff9d96'
				else:
					x1 = ii[1]
					x2 = jj
					x3 = x2 / float(x1)
					x3 = x3 * 100
					if x3 > 79:
						clr7= '#abc8ff'
					else:
						clr7 = '#d1c882'
				pm.append(clr7)

				break
		
	jobz=zip(u,j,k,pm)



	request.session["job_list"] = jobz
	return render(request,"test_allocation2.html")
	return render(request,'manpower_allocation.html')