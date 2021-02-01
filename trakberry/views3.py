from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from views_db import db_open, db_set
from trakberry.forms import login_Form, login_password_update_Form, kiosk_dispForm4
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


def scrapdate_fix1(request):
	id1 = 13
	len1 = 5
	db, cur = db_set(request)
	sql2 = "SELECT * FROM tkb_scrap where date is NULL"
	cur.execute(sql2)
	tmp = cur.fetchall()
	for x in tmp:
		id1 = x[0]

		sql3 = "SELECT max(Id) from tkb_scrap where Id < '%d' and date IS NOT NULL" % (id1)
		cur.execute(sql3)
		ttmp = cur.fetchall()
		ttmp2 = ttmp[0]
		ttmp3 = ttmp2[0]

		sql4 = "SELECT date from tkb_scrap where Id = '%d' and date IS NOT NULL" % (ttmp3)
		cur.execute(sql4)
		ttmp = cur.fetchall()
		ttmp2 = ttmp[0]
		date_not_null = ttmp2[0]

		mql =( 'update tkb_scrap SET date="%s" WHERE Id="%s"' % (date_not_null,id1))
		cur.execute(mql)
		db.commit()

	sql = "SELECT * FROM tkb_scrap where (date_current) is NULL" 
	cur.execute(sql)
	tmp = cur.fetchall()

	for x in tmp:
		tmp2 = x[0]
		tmp3 = x[7]
		check1 = tmp3[9:10]
		if check1=='T':
			left1 = tmp3[:9]
		else:
			left1 = tmp3[:10]
		right1 = tmp3[-5:]
		clock1 = left1+' ' +right1
		mql =( 'update tkb_scrap SET date_current="%s" WHERE Id="%s"' % (clock1,tmp2))
		cur.execute(mql)
		db.commit()

	db.close()

	return render(request,"master_excel_message2.html")


def request_test(request):
	a,b,c = 5,7,8
	rtest = []
	for i in range(1,10):
		y = i * 3
		rtest.append(str(y))
	request.session['rtest'] = str(a)+str(b)+str(c)
	return render(request,"test71.html")


def excel_dump(request):
	excel_table_create("excel_dump.xlsx",request)
	return render(request,"master_excel_message1.html")

def excel_scrap_dump(request):
	
	excel_table_create("scrap_line_operation_category.xlsx",request)
	excel_table_create("scrap_operation_dept.xlsx",request)
	excel_table_create("scrap_part_dept_cost.xlsx",request)
	excel_table_create("scrap_part_line.xlsx",request)
	return render(request,"master_excel_message1.html")

def excel_table_create(sheet,request):
	# Read in Excel Sheet  .  Top corner is name of table.  Top row is column name and below that is data for each column
	# Read it in as a tuple
	# Create a table with that structure.
	# Write it to Database

	# if different folder otherwise root
	# label_link = 'c:/Programming/Stackpole'
	# sheet = 'excel_dump.xlsx'
	sheet_name = 'Sheet1'


	label_link = '/home/file/import1/Inventory/importedxls'


	# use this if excel sheet is in a different folder
	os.chdir(label_link)
	
	book = xlrd.open_workbook(sheet)
	working = book.sheet_by_name(sheet_name)

	yy = ''

	table_name = str(working.cell(0,0).value)  # retrieved from cell 0,0 on excel sheet (top left corner A1)
	name1 = ''
	ss =[]
	a = 0 #set counter / column start at 0
	while True:
		try:
			name1 = str(working.cell(1,a).value)  # read in cell / column for table
		except:
			break  # if error on reading cell (ie NULL) then end the loop
		if len(name1)<1:  # if cell has 0 length then end loop
			break
		ss.append(name1) # add cell value to list of names for table headers
		a=a+1 # increment so as to read next colunn
	ss_len = len(ss)  # lets us know how many columns there are.  Could use   (a-1) as well 

	db, cur = db_set(request)
	s1 = ("""DROP TABLE IF EXISTS xx1""")
	index = s1.find('xx1')
	s1 = s1[:index] + table_name + s1[index+3:]
	cur.execute(s1)
	db.commit()

	for i in ss:
		yy = yy + ',xx2 CHAR(50)'
		index = yy.find('xx2')
		yy = yy[:index] + i + yy[index+3:]

	s1 = ("""CREATE TABLE IF NOT EXISTS xx1(Id INT PRIMARY KEY AUTO_INCREMENT xyz)""")
	index = s1.find('xx1')
	s1 = s1[:index] + table_name + s1[index+3:]
	index = s1.find('xyz')
	s1 = s1[:index] + yy + s1[index+3:]
	cur.execute(s1)
	db.commit()

	# Next step is read in each row and insert into table.
	row_ptr = 2
	while True:
		row_entries = []
		row_empty = 0
		for i in range(0,ss_len):
			try:
				entry1 = str(working.cell(row_ptr,i).value)
				row_empty = 1
			except:
				entry1 = ''

			row_entries.append(entry1)
			# Develop the SQL String
		if row_empty == 0:
			break

		entry2 = ''
		for ii in row_entries:
			var1 =''
			var2 = ''
			for i in ss:
				var1 = var1 + i + ','
				var2 = var2 + '%s,'
			var1 = var1[:-1]
			var2 = var2[:-1]
			s2 = "INSERT INTO xx1(xx2) VALUES(xx3)"
			index = s2.find('xx1')
			s2 = s2[:index] + table_name + s2[index+3:]
			index = s2.find('xx2')
			s2 = s2[:index] + var1 + s2[index+3:]
			index = s2.find('xx3')
			s2 = s2[:index] + var2 + s2[index+3:]
		cur.execute(s2,row_entries)
		db.commit()
		row_ptr = row_ptr + 1
	db.close()
	return
	# return render(request,"master_excel_message1.html")

#  Testing View for Excel Reading

def excel_test(request):
	
	# if needed this assigns mlist to the current path
#	mlist = os.getcwd()
	
#	Change to directory where imported inventory.xlsm is located
#		Use this for local testing
	label_link = 'c:/Projects/'
#		Use this one for actual server
	# label_link = '/home/file/import1/Inventory/importedxls'

	# Try below instead
	# Label_link = '/var/www/html/django/trakberry/trakberry'  # This is the patch to the root on server

	
	sheet = 'inventory.xlsx'
	sheet_name = 'Sheet1'
	os.chdir(label_link)
	
	book = xlrd.open_workbook(sheet)
	
	#working = book.sheet_by_index(1)
	working = book.sheet_by_name(sheet_name)
	
	# First variable is ROW 
	# Second variable is COLUMN
	
	tot = 28
	toc = 1

	tdate = tot+1
	jj = 0
	kk = 1

	a = [[] for x in range(1900)]
	b = [[] for y in range(1900)]
	d = [[] for z in range(1900)]
	for i in range(toc,tot):
		x = str(working.cell(i,0).value)
		# b[kk].append(x)
		# kk = kk + 1
		
		for ii in range(1,39):
			#x = working.cell(i,ii).value
			#if x > 0 and x < 10000000:
			#	x = int(x)
			#	dummy = 1
			#else:
			#	if len(str(x)) < 5:
			#		x = 0
			#	else:
			dummy = 1
			yy = len(x)
			# if len(str(working.cell(i,ii).value)) > 5:
			if len(x) > 3:
				#x = str(working.cell(i,ii).value) + "(" + str(working.cell(204,ii).value) + ")"
				y = str(working.cell(i,ii).value) 
				if len(y) < 1:
					y = 0
				else:
					y = float(y)
					y = int(y)
				# y = str(working.cell(0,ii).value) 
				
				# z = x + "(" + y + ")"
				a[jj].append(x)
				b[jj].append(y)
				d[jj].append(ii)
				jj = jj + 1
	#a = working.cell(1,0).value
	# Date
	c = working.cell(41,0).value
	# # yy = 9/0
	excel_date = int(c)
	dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date)
	ddt = vacation_set_current6(dt)

	# t = 9/0
	# excel_date = int(c)
	# dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date - 2)


	#tt = vacation_temp()

	e = zip(a,b,d)
	inventory_initial(request)
	db, cur = db_set(request)
	ctr = 0
	for i in e:
		p = ''.join(i[0])
		try:
			q = int("".join(map(str,i[1])))
			c = int("".join(map(str,i[2])))
		except:
			q = 0
			c = 0
		ctr = ctr + 1
		# if ctr > 3:
		# 	lenp = len(p)
		# 	x = 9/0
		if len(p)>1:

			cur.execute('''INSERT INTO tkb_inventory(Date,Part,Qty,Category) VALUES(%s,%s,%s,%s)''', (ddt,p,q,c))
			db.commit()

	db.close()



	return render(request,"test4.html",{'D':ddt,'A':e})
	
	
	#adate = working.cell(tdate,1).value
	#b = working.cell(7,0).value
	#mlist = book.sheet_names()
	#mlist.encode('ascii','ignore')
	#c = a[5][5]
	#mlist = xl_workbook.nsheets

	#mlist = os.listdir('.')
	

	#mlist = 'Done'
	


#	tx = ' ' + tx
#	if (tx.find('"'))>0:
#		#request.session["test_comment"] = tx
#		#return out(request)
#		ty = list(tx)
#		ta = tx.find('"')
#		tb = tx.rfind('"')
#		ty[ta] = "'"
#		ty[tb] = "'"
#		tc = "".join(ty)

	#mlist = mlist + 4


	
	#b = 35
	
#	Only uncomment below line to re do table completely	
# inventory_initial()

#	Select today as the date to put in for entry
	# current_first = vacation_set_current4(dt)
	
	db, cur = db_set(request)
#  Below Section will insert a as a new entry
# It uses Try and Except to see if one for that date exists

# Above won't work.   Need to confirm todays date is in inventory


# The below Code was for Inventory

	x = 1
	for i in range(1,jj):
		#y = a[i]
		y = str(a[i][0])
		#y = "a"
		yy = str(b[i][0])
		cur.execute('''INSERT INTO tkb_inventory(Employee,Shift) VALUES(%s,%s)''', (y,yy))
		db.commit()
	request.session["test_excel"] = "Added New One"

	db.close()


	return render(request,"test4.html",{'Date':current_first})

	
	# If there's a current date already there put it into temp_a[][] compare to a[][]
	ch = 0
	
	sql = "SELECT * FROM tkb_inventory where Date_Entered = '%s'" %(current_first)
	cur.execute(sql)
	tmp = cur.fetchall()
	
	i = 0    # Initialize ctr i to use as row increment in both arrays
	try:
		for j in tmp:
			i = i + 1
		
			pn_1 = str(j[2])
			in_1 = j[4]
			va_1 = j[3]
		
			ij = 0
			for h in a:
				if ij > 0:  # First row of a is empty.
					#return render(request,"test5.html",{'a':a,'b':pp,'AA':oo})
					if pn_1 == str(h[0]):  # Results in a positive match of part number with 'a' and 'j'
						aa = (h[in_1])
						bb = va_1
						
						
						return render(request,"test5_match.html",{'aa':aa,'bb':bb})  # results in a positive hit of part number
						
				ij = ij + 1

			return render(request,"test5_nomatch.html")
					
#				if ij > 0:
#				return render(request,"test5.html",{'a':a,'b':j,'AA':h})
#				ij = ij + 1

				
				# j[3] is the value 
				# j[4] is the index (Column)
				# j[0] is the part number
				
			bb = j[3]
			x = round((a[1][10]),0)
			if bb == x :
				ch = 1
			else:
				ch = 0
			return render(request,"test5.html",{'a':a,'b':j,'AA':x})
				
#			for ii in range(1,35):
#				return render(request,"test5.html",{'a':a,'b':j,'AA':a[i+1]})
#				if a[i,ii] != j[ii]:
#					ch = 1
	except:

		return render(request,"test5_error.html")
	
	if ch == 1:
		return render(request,"test5_nomatch.html")
	elif ch == 0:
		return render(request,"test5_match.html")
	
	db.close()
	return render(request,"test5.html",{'a':a,'b':current_first})
 
def inventory_initial(request):

	# create inventory table if one doesn't exist
	db, cursor = db_set(request)  
#	Use below line to recreate the table format
	cursor.execute("""DROP TABLE IF EXISTS tkb_inventory""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_inventory(Id INT PRIMARY KEY AUTO_INCREMENT,Date Date,Part Char(80),Qty Int(20), Category Int(10))""")
	db.commit()
	db.close()
	return

	
def manpower_initial(request):
	# create inventory table if one doesn't exist
	db, cursor = db_set(request)  
	# cursor.execute("""DROP TABLE IF EXISTS tkb_matrix_cache""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix_cache(Id INT PRIMARY KEY AUTO_INCREMENT,Area CHAR(80), Shift CHAR(80), Matrix TEXT(1000000), Job TEXT(1000000))""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_manpower(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Clock CHAR(80), Shift_Mod Char(80))""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_allocation""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_allocation(Id INT PRIMARY KEY AUTO_INCREMENT,Job CHAR(80), Area CHAR(80),Asset1 CHAR(20),Asset2 CHAR(20),Asset3 CHAR(20),Asset4 CHAR(20),Asset5 CHAR(20),Asset6 CHAR(20),Sig1 Char(10), Part1 CHAR(20), Part2 CHAR(20), Part3 CHAR(20), Part4 CHAR(20))""")
# #	Use below line to recreate the table format
	cursor.execute("""DROP TABLE IF EXISTS tkb_manpower2""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_manpower2(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Clock CHAR(80), Shift_mod Char(80))""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_allocation2""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_allocation2(Id INT PRIMARY KEY AUTO_INCREMENT,Job CHAR(80), Area CHAR(80),Asset1 CHAR(20),Asset2 CHAR(20),Asset3 CHAR(20),Asset4 CHAR(20),Asset5 CHAR(20),Asset6 CHAR(20),Sig1 Char(10), Part1 CHAR(20), Part2 CHAR(20), Part3 CHAR(20), Part4 CHAR(20))""")
# 	# cursor.execute("""DROP TABLE IF EXISTS tkb_matrix""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Job Char(100), Trained Char(100),Enabled CHAR(10),Clock CHAR(80))""")
	db.commit()
	db.close()
	return

def manpower_update(request):  # This will run every 30 min on the refresh page to see if update occurs
	t=int(time.time())
	tm = time.localtime(t)
	x1 = tm[1]
	c = 0 
	hr1 = str(tm[3])
	min1 = str(tm[4])
	time1 = str(tm[1])+"/"+str(tm[2])+"/"+str(tm[0])+" 12:00 am"  # Sets the update time to midnight each day
	check = 0
	# Determing if current time is stored to check and if that time has been run
	db, cur = db_set(request)  
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_updater(Id INT PRIMARY KEY AUTO_INCREMENT,current_date CHAR(80),updated_date CHAR(80),set_time CHAR(80),program CHAR(80))""")
	sql = "SELECT * From tkb_updater" 
	cur.execute(sql)
	tmp = cur.fetchall()

	
	
	
	try:
		sql = "SELECT * From tkb_manpower_updater where timestamp = '%s'" % (time1)
		cur.execute(sql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
	except:
		cur.execute('''INSERT INTO tkb_manpower_updater(timestamp,dummy) VALUES(%s,%s)''', (time1,c))
		db.commit()
		check = 1
		# return manpower_tester(request)
		return manpower_update_run(request)
		# This is where you run the update
	sql = "SELECT MAX(Id) From tkb_manpower_updater"
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	tmp3 = tmp2[0]

	sql = "SELECT timestamp From tkb_manpower_updater where Id = '%s'" % (tmp3)
	cur.execute(sql)
	finished1 = cur.fetchall()
	request.session["finished_update"] = finished1[0]


	return render(request,'manpower_updater.html')

def manpower_tester(request):
	return render(request,"manpower_updater.html")

def manpower_update_run(request):
	# comment below when running local
	# label_link = '/home/file/import1/Inventory/importedxls'
	# os.chdir(label_link)
	# ********************************
	
	# request.session["time_manpower_update"] = tm

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


	manpower_initial(request)   # Initialize the Manpower list
	# matrix_cache_matrix(request) # Transfer current cache to matrix table
	db, cur = db_set(request)
	x = 1
	for i in abc:
		y = str(i[0])
		yy = str(i[1])
		yyy = str(i[2])
		cur.execute('''INSERT INTO tkb_manpower2(Employee,Shift,Clock,Shift_Mod) VALUES(%s,%s,%s,%s)''', (y,yy,yyy,yy))
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
		cur.execute('''INSERT INTO tkb_allocation2(Job,Area,Asset1,Asset2,Asset3,Asset4,Asset5,Asset6,Sig1,Part1,Part2,Part3,Part4) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (job3,area3,a1,a2,a3,a4,a5,a6,s3,p1,p2,p3,p4))
		db.commit()

	sql = "SELECT * From tkb_manpower2 WHERE tkb_manpower2.Employee NOT IN (SELECT Employee From tkb_manpower)"
	cur.execute(sql)
	tmp = cur.fetchall()   # This shows all new employees to add to manpower

	sql = "SELECT * From tkb_manpower WHERE tkb_manpower.Employee NOT IN (SELECT Employee From tkb_manpower2)"
	cur.execute(sql)
	tmp2 = cur.fetchall()   # This shows all employees that should be removed, or made inactive

	sql = "SELECT * From tkb_allocation2 WHERE tkb_allocation2.job NOT IN (SELECT job From tkb_allocation)"
	cur.execute(sql)
	tmp_job = cur.fetchall()   # This shows all new jobs to add

	sql = "SELECT * From tkb_allocation WHERE tkb_allocation.job NOT IN (SELECT job From tkb_allocation2)"
	cur.execute(sql)
	tmp_job2 = cur.fetchall()   # This shows all jobs to delete


	active = 'active'
	inactive = 'inactive'

	# Add employee if they show new from manpower to matrix
	for a in tmp:
		cur.execute('''INSERT INTO tkb_manpower(Employee,Shift,Clock,Shift_Mod) VALUES(%s,%s,%s,%s)''', (a[1],a[2],a[3],a[2]))
		db.commit()
	# Remove employees if they don't show in manpower 
	for a in tmp2:
		dql = ('DELETE FROM tkb_manpower WHERE Employee="%s" and Shift="%s"' % (a[1],a[2]))
		cur.execute(dql)
		db.commit()


	# Change Employee to inactive if they've been removed from manpower
	ctr1 = 0
	# for a in tmp2:
	# 	sql =( 'update tkb_matrix SET Enabled="%s" WHERE Employee="%s"' % (inactive,a[1]))
	# 	cur.execute(sql)
	# 	db.commit()

	# Fix all continental so they are on the appropriate shift
	adj_shift = [('A Days P1','Plant 1 Days'),('B Days P1','Plant 1 Days'),('A Days A3','Plant 4 Day'),('B Days A3','Plant 4 Day'),('A Nights P1','Plant 1 Mid'),('B Nights P1','Plant 1 Mid'),('A Nights A3','Plant 4 Mid'),('B Nights A3','Plant 4 Mid')]
	for index in adj_shift:
		t1 = index[1]
		s1 = index[0]
		mql =( 'update tkb_manpower SET Shift = "%s" WHERE Shift_Mod ="%s"' % (t1,s1))
		cur.execute(mql)
		db.commit()

	cur.execute("""DROP TABLE IF EXISTS tkb_matrix_cache""") # Clear all Cache and start fresh
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix_cache(Id INT PRIMARY KEY AUTO_INCREMENT,Area CHAR(80), Shift CHAR(80), Matrix TEXT(1000000), Job TEXT(1000000))""")
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
	shift ,area = 'A Days P1','Area 1'
	matrix_read(shift,area,request)


	# full_update(request)   # Fully update the matrix

	# return   # Return from module call of updating manpower
	return render(request,"manpower_updater.html")

# This will be needed to read data directly and write to cache
def matrix_read(shift,area,request):
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_manpower where Shift = '%s'" %(shift)
	cur.execute(sql)
	tmp = cur.fetchall()
	request.session["matrix"] = tmp
	sql2 = "SELECT * FROM tkb_allocation where Area = '%s'" %(area)
	cur.execute(sql2)
	jobs = cur.fetchall()
	x=[]
	z2=[]
	z3=[]
	zz=0
	xaxis=1
	yaxis=1
	y = []
	area1 = []
	for i in tmp:
		w=[]
		area1.append(area)
		for ii in jobs:
			z1=[]
			zindex1 = []
			a = i[1]
			b = ii[1]
			z1.append(a)
			zindex1.append(i[3])
			try:
				sql3 = '''SELECT * FROM tkb_matrix where Employee = "%s" and Job = "%s"'''%(a,b)
				cur.execute(sql3)
				tmp3 = cur.fetchall()
				tmp32 = tmp3[0][4]
			except:
				tmp32 = 'Not Trained'
			xa,ya = three_digit(xaxis,yaxis)
			tmp32=ya+xa+tmp32
			w.append(tmp32)
			xaxis=xaxis+1
		xaxis=1
		yaxis=yaxis+1
		w=tuple(w)
		x.append(w)
		z1=tuple(z1)
		zindex1=tuple(zindex1)
		z2.append(z1)
		z3.append(zindex1)
	x=tuple(x)
	area1=tuple(area1)
	z2 = tuple(z2)
	z3 = tuple(z3)
	matrix = zip(z2,x,z3,area1)  # matrix will have first tuple name second tuple are all jobs third is clock number
	mmatrix = str(matrix)
	jjobs = str(jobs)
	hhh = len(mmatrix)
	db, cur = db_set(request)
	cur.execute('''INSERT INTO tkb_matrix_cache(Area,Shift,Matrix,Job) VALUES(%s,%s,%s,%s)''', (area,shift,mmatrix,jjobs))
	db.commit()
	db.close()
	return

def matrix_cache_matrix(request): # Transfer Cache to clean Matrix
	db, cur = db_set(request)
	cur.execute("""DROP TABLE IF EXISTS tkb_matrix""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Job Char(100), Trained Char(100),Enabled CHAR(10),Clock CHAR(80))""")
	db.close()

	shift ,area = 'Plant 1 Mid','Area 1'
	matrix_cache_transfer(shift,area,request)
	shift ,area = 'Plant 1 Aft','Area 1'
	matrix_cache_transfer(shift,area,request)
	shift ,area = 'Plant 1 Days','Area 1'
	matrix_cache_transfer(shift,area,request)
	shift ,area = 'Plant 3 Days','Area 2'
	matrix_cache_transfer(shift,area,request)
	shift ,area = 'Plant 3 Mid','Area 2'
	matrix_cache_transfer(shift,area,request)
	shift ,area = 'Plant 3 Aft','Area 2'
	matrix_cache_transfer(shift,area,request)
	shift ,area = 'Plant 4 Day','Area 3'
	matrix_cache_transfer(shift,area,request)
	shift ,area = 'Plant 4 Aft','Area 3'
	matrix_cache_transfer(shift,area,request)
	shift ,area = 'Plant 4 Mid','Area 3'
	matrix_cache_transfer(shift,area,request)
	return 

def matrix_cache_transfer(shift,area,request):
	db, cur = db_set(request)
	sql3 = '''SELECT * FROM tkb_matrix_cache where Area = "%s" and Shift = "%s"'''%(area,shift)
	cur.execute(sql3)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	matrix = tmp2[3]
	jobs = tmp2[4]
	matrix = eval(matrix)
	jobs = eval(jobs)
	clock = 1
	enabled = 'active'
	for i in matrix:
		name1 = i[0][0]   # Name
		x=0
		for ii in jobs:
			level = i[1][x]
			level = level[6:]
			job1 = ii[1]
			if level != 'Not Trained':
				cur.execute('''INSERT INTO tkb_matrix(Employee,Shift,Job,Trained,Enabled,Clock) VALUES(%s,%s,%s,%s,%s,%s)''', (name1,shift,job1,level,enabled,clock))
				db.commit()
			x = x + 1
	db.close()

	return

def training_matrix2(request):
	request.session['matrix_update'] = 0   # This variable is determining if we update all or one person
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


	xaxis = 1
	yaxis = 1

	matrix_new = []
	matrix_name = []
	matrix_id = []
	matrix_area = []

	if request.POST:

		z2=[]
		z3=[]

		for i in matrix:
			name1 = i[0][0]
			area1 = i[3]
			h = i[1]

			x1=[]

			for ii in i[1]:
				z1=[]
				zindex1 = []
				z1.append(name1)
				zindex1.append(i[2][0])

				xa,ya = three_digit(xaxis,yaxis)
				digit1 = str(ya + xa)
				matrix_temp = request.POST.get(digit1)
				if matrix_temp =='':
					matrix_temp = 'Not Trained'
				ii_temp = ii[6:]
				matrix_temp=str(matrix_temp)
				# This section is trial to rebuild Matrix
				temp_var1 = digit1 + matrix_temp
				x1.append(temp_var1)
				xaxis = xaxis + 1
			yaxis = yaxis + 1
			xaxis = 1

			z1=tuple(z1)
			zindex1=tuple(zindex1)
			z2.append(z1)
			z3.append(zindex1)
			x1=tuple(x1)
			matrix_new.append(x1)
			matrix_name.append(name1)
			matrix_area.append(area1)
			# matrix_new=tuple(matrix_new)
			# matrix_area=tuple(matrix_area)
		z2=tuple(z2)

		mmm  = zip(z2,matrix_new,z3,matrix_area)
		
		# Below is input of any new Shift to review
		current_shift = shift
		current_area = area
		matrix_shift = request.POST.get('matrix_shift')
		matrix_area = shift_area(matrix_shift)
		request.session["matrix_shift"] = matrix_shift
		request.session["matrix_area"] = matrix_area
		matrix_cache1 = str(mmm)  # The updated cache

		db,cur = db_set(request)
		matrix_shift = str(matrix_shift)

		dql = ('DELETE FROM tkb_matrix_cache WHERE Id="%s"' % (Id1))
		cur.execute(dql)
		db.commit()

		cur.execute('''INSERT INTO tkb_matrix_cache(Area,Shift,Matrix,Job) VALUES(%s,%s,%s,%s)''', (current_area,current_shift,matrix_cache1,jobs_current))
		db.commit()

		return render(request,"redirect_training_matrix2.html")

	else:
		form = kiosk_dispForm4()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	request.session['data_matrix'] = matrix
	request.session['data_jobs'] = jobs

	return render(request,"training_matrix2.html",{'args':args,'matrix':matrix,'jobs':jobs})

def bounce_matrix(request):
	request.session["bounce_matrix"] = 1
	return render(request,'redirect_training_matrix2.html')

def three_digit(xaxis,yaxis):
	xa=str(xaxis)
	ya=str(yaxis)
	if len(xa)==1:
		xa='0'+xa
	if len(xa)==2:
		xa='0'+xa
	if len(ya)==1:
		ya='0'+ya
	if len(ya)==2:
		ya='0'+ya
	return xa,ya


def shift_area(matrix_shift):
	matrix_area = 'Area 1'
	if matrix_shift == 'Plant 1 Mid':
		matrix_area = 'Area 1'
	elif matrix_shift == 'Plant 1 Aft':
		matrix_area = 'Area 1'
	elif matrix_shift == 'Plant 1 Days':
		matrix_area = 'Area 1'
	elif matrix_shift == 'Plant 3 Mid':
		matrix_area = 'Area 2'
	elif matrix_shift == 'Plant 3 Aft':
		matrix_area = 'Area 2'
	elif matrix_shift == 'Plant 3 Days':
		matrix_area = 'Area 2'
	elif matrix_shift == 'Plant 4 Mid':
		matrix_area = 'Area 3'
	elif matrix_shift == 'Plant 4 Aft':
		matrix_area = 'Area 3'
	elif matrix_shift == 'Plant 4 Day':
		matrix_area = 'Area 3'
	return matrix_area

# This will find what the person can run and put it in tkb_matrix
# Don't think we even need tkb_matrix_cache here so why not start fresh and
# develope the tkb_matrix right from tkb_manpower then convert to fresh tkb_matrix_cache
def training_matrix_find(request,index):
	shift1 = request.session["matrix_shift"]
	area1 = request.session["matrix_area"]
	clock2 = str(index) + '.0'
	clock1 = str(index)
	db, cur = db_set(request)

	sql = "SELECT * FROM tkb_matrix_cache where Area = '%s' and Shift = '%s'" %(area1,shift1)
	cur.execute(sql)
	tmp = cur.fetchall()
	tmp2 = tmp[0]
	Id1 = tmp2[0]

	sql="SELECT * FROM tkb_manpower where Clock = '%s'" % (clock2)
	cur.execute(sql)
	tmp=cur.fetchall()
	name1 = tmp[0][1]

	cur.execute("""DROP TABLE IF EXISTS tkb_matrix""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Job Char(100), Trained Char(100),Enabled CHAR(10),Clock CHAR(80))""")
	db.close()
	matrix_cache_transfer(shift1,area1,request)  # Develop the temp matrix

	area1 = shift_area(shift1)
	enabled1 = 'active'

	db, cur = db_set(request)
	sql1 = "SELECT * FROM tkb_allocation where Area = '%s'"%(area1)
	cur.execute(sql1)
	tmp1 = cur.fetchall()

	
	for i in tmp1:
		job1 = i[1]
		asset1 = i[3]
		sig1 = i[4]
		part1 = i[5]
		asset1 = float(asset1)
		asset1 = int(asset1)

		if int(clock1) != 0:

			if sig1 == 1:
				sql2= '''SELECT COUNT(*) FROM sc_production1 where comments = "%s" and asset_num = "%s" and partno = "%s"''' % (clock1,asset1,part1)
			else:
				sql2= '''SELECT COUNT(*) FROM sc_production1 where comments = "%s" and asset_num = "%s"''' % (clock1,asset1)
			cur.execute(sql2)
			tmp2 = cur.fetchall()
			count1 = int(tmp2[0][0])
		else:
			count1 = 0
		trained1 = 'Not Trained'
		if int(count1) > 0:
			trained1 = 'Training <5 days'
		if int(count1) > 4:
			trained1 = 'Training >4 days'
		if int(count1) >9:
			trained1 = 'Trained'
		if int(count1) > 25:
			trained1 = 'A Trainer'
		sql3= '''SELECT COUNT(*) FROM tkb_matrix where Employee = "%s" and job = "%s"''' % (name1,job1)
		cur.execute(sql3)
		tmp3 = cur.fetchall()
		count3 = int(tmp3[0][0])


		if count1 == 0 and count3 == 1:
			dql = ('DELETE FROM tkb_matrix WHERE Employee="%s" and Job="%s"' % (name1,job1))
			cur.execute(dql)
			db.commit()
		elif count1 > 0 and count3 == 1:
			cql = ('update tkb_matrix SET Trained = "%s" WHERE Employee ="%s" and Job = "%s"' % (trained1,name1,job1))
			cur.execute(cql)
			db.commit()
		elif count1 > 0 and count3 == 0:
			cur.execute('''INSERT INTO tkb_matrix(Employee,Job,Trained,Shift,Enabled) VALUES(%s,%s,%s,%s,%s)''', (name1,job1,trained1,shift1,enabled1))
			db.commit()

	dql = ('DELETE FROM tkb_matrix_cache WHERE Id="%s"' % (Id1))
	cur.execute(dql)
	db.commit()
	db.close()

	matrix_read(shift1,area1,request)   # Transfer the matrix to cache

	if request.session['matrix_update'] == 1:
		return
	else:
		return render(request,"redirect_training_matrix2.html")

# This will update all shifts training matrix
def full_update(request):
	shift = ['Plant 1 Mid','Plant 1 Aft','Plant 1 Days','Plant 3 Mid','Plant 3 Aft','Plant 3 Days','Plant 4 Mid','Plant 4 Aft','Plant 4 Day']
	for i in shift:
		shift1 = i
		area1 = shift_area(shift1)
		request.session["matrix_shift"] = shift1
		request.session["matrix_area"] = area1
		db, cur = db_set(request)
		sql = "SELECT * FROM tkb_matrix_cache where Area = '%s' and Shift = '%s'" %(area1,shift1)
		cur.execute(sql)
		tmp = cur.fetchall()
		tmp2 = tmp[0]
		db.close()
		matrix = tmp2[3]
		matrix = eval(matrix) # Convert string from database read to required tuple
		for x in matrix:
			clock = str(x[2][0])
			clock = clock[:-2]
			if clock == '':
				clock = 0
			else:
				try:
					clock = int(clock)
					training_matrix_find(request,clock)
				except:
					clock = 0
	request.session['bounce_matrix'] = 0
	request.session['matrix_update'] = 0

	return
	# return render(request,"redirect_training_matrix2.html")

def training_matrix_update_all(request):
	matrix = request.session['data_matrix']
	request.session['matrix_update'] = 1
	for x in matrix:
		clock = str(x[2][0])
		clock = clock[:-2]
		if clock == '':
			clock = 0
		else:
			clock = int(clock)
			training_matrix_find(request,clock)
	request.session['bounce_matrix'] = 0
	request.session['matrix_update'] = 0
	return render(request,"redirect_training_matrix2.html")

	# matrix1 = request.session['matrix']
	# for x in matrix1:
	# 	index = x[0]
	# 	update_matrix_all(index,request)
	# request.session['bounce_matrix'] = 0
	# request.session['matrix_update'] = 0
	# return render(request,"redirect_training_matrix2.html")

def update_matrix_cancel(request):
	request.session['bounce_matrix'] = 0
	return render(request,"redirect_training_matrix2.html")

def update_matrix_all(index,request):
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_manpower where Id = '%s'" %(index)
	cur.execute(sql)
	tmp = cur.fetchall()
	name1 = tmp[0][1]
	try:
		clock1 = float(tmp[0][3])
	except:
		clock1 = '0'
	clock1 = int(clock1)
	clock1 = str(clock1)
	shift1 = tmp[0][2]
	area1 = shift_area(shift1)

	enabled1 = 'active'

	db, cur = db_set(request)
	sql1 = "SELECT * FROM tkb_allocation where Area = '%s'"%(area1)
	cur.execute(sql1)
	tmp1 = cur.fetchall()

	for i in tmp1:
		job1 = i[1]
		asset1 = i[3]
		sig1 = i[4]
		part1 = i[5]

		asset1 = float(asset1)
		asset1 = int(asset1)

		if sig1 == 1:
			sql2= '''SELECT COUNT(*) FROM sc_production1 where comments = "%s" and asset_num = "%s" and partno = "%s"''' % (clock1,asset1,part1)
		else:
			sql2= '''SELECT COUNT(*) FROM sc_production1 where comments = "%s" and asset_num = "%s"''' % (clock1,asset1)
		cur.execute(sql2)
		tmp2 = cur.fetchall()
		count1 = int(tmp2[0][0])

		trained1 = 'Not Trained'
		if int(count1) > 0:
			trained1 = 'Training <5 days'
		if int(count1) > 4:
			trained1 = 'Training >4 days'
		if int(count1) >9:
			trained1 = 'Trained'
		if int(count1) > 25:
			trained1 = 'A Trainer'

		sql3= '''SELECT COUNT(*) FROM tkb_matrix where Employee = "%s" and job = "%s"''' % (name1,job1)
		cur.execute(sql3)
		tmp3 = cur.fetchall()
		count3 = int(tmp3[0][0])

		if count1 == 0 and count3 == 1:
			dql = ('DELETE FROM tkb_matrix WHERE Employee="%s" and Job="%s"' % (name1,job1))
			cur.execute(dql)
			db.commit()
		elif count1 > 0 and count3 == 1:
			cql = ('update tkb_matrix SET Trained = "%s" WHERE Employee ="%s" and Job = "%s"' % (trained1,name1,job1))
			cur.execute(cql)
			db.commit()
		elif count1 > 0 and count3 == 0:
			cur.execute('''INSERT INTO tkb_matrix(Employee,Job,Trained,Shift,Enabled) VALUES(%s,%s,%s,%s,%s)''', (name1,job1,trained1,shift1,enabled1))
			db.commit()
	db.close()
	return

# One system will be running this and it will do all the daily updates.
# Check production entries, update manpower, update matrix
def auto_updater(request):  # This will run every 30 min on the refresh page to see if update occurs
	t=int(time.time())
	tm = time.localtime(t)
	hr1 = str(tm[3])
	min1 = str(tm[4])
	cur_date  = str(tm[1])+"/"+str(tm[2])+"/"+str(tm[0]) # Sets the current date
	if len(min1) == 1: # Add a 0 if it's less than 10 min so it's the correct length
		min1 = '0'+min1
	cur_time = hr1 + min1
	update_time = cur_date + " " + hr1 + ":" + min1
	db, cur = db_set(request)  
	# cur.execute("""DROP TABLE IF EXISTS tkb_updater""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_updater(Id INT PRIMARY KEY AUTO_INCREMENT,cur_date CHAR(80),set_time CHAR(80), program Char(80))""")
	sql= '''SELECT * FROM tkb_updater'''
	cur.execute(sql)
	tmp = cur.fetchall()
	for i in tmp:
		date2 = i[1]
		id2 = i[0]
		set_time = i[2]
		if date2 != cur_date:
			if int(cur_time) > int(set_time):
				mql =( 'update tkb_updater SET cur_date = "%s" WHERE Id ="%s"' % (cur_date,id2))
				cur.execute(mql)
				db.commit()
				sql = "SELECT program FROM tkb_updater where Id = '%s'"%(id2)
				cur.execute(sql)
				tmp2 = cur.fetchall()
				program1 = tmp2[0][0]
				request.session['tkb_program'] = program1
				request.session['tkb_update_time'] = update_time
				return render(request,'redirect_program.html')
	return render(request,'tkb_updater.html')