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
#	Use below line to recreate the table format
	cursor.execute("""DROP TABLE IF EXISTS tkb_manpower""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_manpower(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Clock CHAR(80))""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_allocation""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_allocation(Id INT PRIMARY KEY AUTO_INCREMENT,Job CHAR(80), Area CHAR(80),Asset CHAR(20),Sig1 Char(10), Part CHAR(20))""")
	# cursor.execute("""DROP TABLE IF EXISTS tkb_matrix""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Job Char(100), Trained Char(100),Enabled CHAR(10),Clock CHAR(80))""")
	db.commit()
	db.close()
	return
	
# Update DB so it has current manpower
def manpower_update(request):
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
	sig1 = [[] for ww in range(600)]
	part1 = [[] for uu in range(600)]

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
	# return render(request,"test71.html",{'matrix':abc})
	for fnd in range(start1,900):  # Determine what row to start reading manpower from
		fnd_cell = str(working.cell(fnd,0).value)
		if fnd_cell == 'Area 1':
			start2 = fnd-1
			break

	kk = 1
	for i in range((start2+1),(start2+180)):
		try:
			if len(str(working.cell(i,0).value)) > 5:
				x = str(working.cell(i,0).value) 
				y = str(working.cell(i,1).value) 
				z = str(working.cell(i,2).value) 
				w = str(working.cell(i,3).value) 
				u = str(working.cell(i,4).value) 
				area1[kk].append(x)
				job1[kk].append(y)
				asset1[kk].append(z)
				sig1[kk].append(w)
				part1[kk].append(u)
				kk = kk + 1
			else:
				break
		except:
			break


	manpower_initial(request)   # Initialize the Manpower list
	db, cur = db_set(request)
	x = 1
	for i in abc:
		y = str(i[0])
		yy = str(i[1])
		yyy = str(i[2])
		cur.execute('''INSERT INTO tkb_manpower(Employee,Shift,Clock) VALUES(%s,%s,%s)''', (y,yy,yyy))
		db.commit()
	for i in range(1,kk):
		y = str(job1[i][0])
		yy = str(area1[i][0])
		yyy = str(asset1[i][0])
		yyyy = str(sig1[i][0])
		yyyyy =  str(part1[i][0])

		cur.execute('''INSERT INTO tkb_allocation(Job,Area,Asset,Sig1,Part) VALUES(%s,%s,%s,%s,%s)''', (y,yy,yyy,yyyy,yyyyy))
		db.commit()


	sql = "SELECT * From tkb_manpower WHERE tkb_manpower.Employee NOT IN (SELECT Employee From tkb_matrix)"
	cur.execute(sql)
	tmp = cur.fetchall()

	sql = "SELECT * From tkb_matrix WHERE tkb_matrix.Employee NOT IN (SELECT Employee From tkb_manpower)"
	cur.execute(sql)
	tmp2 = cur.fetchall()

	# stp = 7/0

	active = 'active'
	inactive = 'inactive'

	# Add employee if they show new from manpower to matrix
	for a in tmp:
		cur.execute('''INSERT INTO tkb_matrix(Employee,Shift,Enabled,Clock) VALUES(%s,%s,%s,%s)''', (a[1],a[2],active,a[3]))
		db.commit()

	# Change Employee to inactive if they've been removed from manpower
	for a in tmp2:
		sql =( 'update tkb_matrix SET Enabled="%s" WHERE Employee="%s"' % (inactive,a[1]))
		cur.execute(sql)
		db.commit()
	db.close()
	return render(request,"test4.html")


def training_matrix2(request):
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

	if request.session["bounce_matrix"] == 0:
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
		for i in tmp:
			w=[]
			for ii in jobs:
				z1=[]
				zindex1 = []
				a = i[1]
				b = ii[1]
				z1.append(a)
				zindex1.append(i[0])
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
		matrix = zip(z2,x,z3)  # matrix will have first tuple name second tuple are all jobs third is clock number

	else:
		matrix = request.session["data_matrix"]
		jobs = request.session["data_jobs"]


	xaxis = 1
	yaxis = 1
	if request.POST:

		for i in matrix:
			name1 = i[0][0]
			for ii in i[1]:
				xa,ya = three_digit(xaxis,yaxis)
				digit1 = ya + xa
				matrix_temp = request.POST.get(digit1)
				if matrix_temp =='':
					matrix_temp = 'Not Trained'
				ii_temp = ii[6:]
				if ii_temp != matrix_temp:  # old and new different so do something
					bbb = jobs[int(xa)-1][1]
					if ii_temp == 'Not Trained':
						enabled1='active'
						db, cur = db_set(request)
						cur.execute('''INSERT INTO tkb_matrix(Employee,Job,Trained,Shift,Enabled) VALUES(%s,%s,%s,%s,%s)''', (name1,bbb,matrix_temp,shift,enabled1))
						db.commit()
						db.close()
					elif matrix_temp == 'Not Trained':
						db, cur = db_set(request)
						dql = ('DELETE FROM tkb_matrix WHERE Employee="%s" and Job="%s"' % (name1,bbb))
						cur.execute(dql)
						db.commit()
						db.close()
					else:
						dummy=2
						db, cur = db_set(request)
						cql = ('update tkb_matrix SET Trained = "%s" WHERE Employee ="%s" and Job = "%s" and Shift = "%s"' % (matrix_temp,name1,bbb,shift))
						cur.execute(cql)
						db.commit()
						db.close()
				xaxis = xaxis + 1
			yaxis = yaxis + 1
			xaxis = 1

		# Below is input of any new Shift to review
		matrix_shift = request.POST.get('matrix_shift')
		matrix_area = shift_area(matrix_shift)
		request.session["matrix_shift"] = matrix_shift
		request.session["matrix_area"] = matrix_area

		return render(request,"redirect_training_matrix2.html")

	else:
		form = kiosk_dispForm4()
	args = {}
	args.update(csrf(request))
	args['form'] = form

	# return render(request,"test71.html",{'matrix':matrix,'jobs':jobs})
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

def training_matrix_find(request,index):
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_manpower where Id = '%s'" %(index)
	cur.execute(sql)
	tmp = cur.fetchall()
	name1 = tmp[0][1]
	clock1 = float(tmp[0][3])
	clock1 = int(clock1)
	clock1 = str(clock1)
	shift1 = tmp[0][2]
	area1 = shift_area(shift1)
	enabled1 = 'active'

	a1 = []
	a2 = []
	a3 = []
	a4 = []
	a5 = []
	a6 = []

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
			r=4/0
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

		a1.append(job1)
		a2.append(asset1)
		a3.append(count1)
		a4.append(trained1)
		a5.append(clock1)
		a6.append(name1)

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

	aa = zip(a1,a2,a3,a4,a5,a6)
	db.close()

	# return render(request,"test71.html",{'matrix':aa})
	return render(request,"redirect_training_matrix2.html")

def training_matrix_update_all(request):
	matrix1 = request.session['matrix']
	for x in matrix1:
		index = x[0]
		update_matrix_all(index,request)
	request.session['bounce_matrix'] = 0
	return render(request,"redirect_training_matrix2.html")

def update_matrix_cancel(request):
	request.session['bounce_matrix'] = 0
	return render(request,"redirect_training_matrix2.html")

def update_matrix_all(index,request):
	db, cur = db_set(request)
	sql = "SELECT * FROM tkb_manpower where Id = '%s'" %(index)
	cur.execute(sql)
	tmp = cur.fetchall()
	name1 = tmp[0][1]
	clock1 = float(tmp[0][3])
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