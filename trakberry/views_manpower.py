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
from views3 import matrix_read,shift_area

def manpower_layout(request):

	db, cur = db_set(request)
	TimeOut = -1
	part = '50-9341'
	sql = "SELECT DISTINCT asset_num FROM sc_production1 WHERE partno = '%s'" %(part)
	cur.execute(sql)
	tmp = cur.fetchall()
	return render(request, "kiosk/kiosk_test.html",{'tmp':tmp})

def manpower_initial_v2(request):
	db, cursor = db_set(request)  
	cursor.execute("""DROP TABLE IF EXISTS tkb_manpower2""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_manpower""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_manpower(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Clock CHAR(80), Shift_Mod Char(80))""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_allocation""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_allocation2""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_allocation(Id INT PRIMARY KEY AUTO_INCREMENT,Job CHAR(80), Area CHAR(80),Asset1 CHAR(20),Asset2 CHAR(20),Asset3 CHAR(20),Asset4 CHAR(20),Asset5 CHAR(20),Asset6 CHAR(20),Sig1 Char(10), Part1 CHAR(20), Part2 CHAR(20), Part3 CHAR(20), Part4 CHAR(20))""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_matrix_cache""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix_cache(Id INT PRIMARY KEY AUTO_INCREMENT,Area CHAR(80), Shift CHAR(80), Matrix TEXT(1000000), Job TEXT(1000000))""")
	cursor.execute("""DROP TABLE IF EXISTS tkb_matrix""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix(Id INT PRIMARY KEY AUTO_INCREMENT,Employee CHAR(80), Shift CHAR(80),Job Char(100), Trained Char(100),Enabled CHAR(10),Clock CHAR(80))""")
	db.commit()
	db.close()
	return

def manpower_update_v2(request):
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
	# Write new Manpower and Allocation
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

	matrix_update_v2(request)
	# cur.execute("""DROP TABLE IF EXISTS tkb_matrix_cache""") # Clear all Cache and start fresh
	# cur.execute("""CREATE TABLE IF NOT EXISTS tkb_matrix_cache(Id INT PRIMARY KEY AUTO_INCREMENT,Area CHAR(80), Shift CHAR(80), Matrix TEXT(1000000), Job TEXT(1000000))""")
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
	return render(request,"test71.html")
	return render(request,"manpower_updater.html")

def matrix_update_v2(request):
	shift = ['Plant 1 Mid','Plant 1 Aft','Plant 1 Days','Plant 3 Mid','Plant 3 Aft','Plant 3 Days','Plant 4 Mid','Plant 4 Aft','Plant 4 Day']
	for i in shift:
		shift1 = i
		area1 = shift_area(i)
		enabled1 = '1'
		db, cur = db_set(request)
		sql="SELECT * FROM tkb_manpower where Shift = '%s'" % (shift1)
		cur.execute(sql)
		tmp1=cur.fetchall()
		sql = "SELECT * FROM tkb_allocation where Area = '%s'"%(area1)
		cur.execute(sql)
		tmp2 = cur.fetchall()

		for i in tmp1:
			try:
				clock = int(i[3][:-2])
			except:
				clock = 0
			name1 = i[1]
			for ii in tmp2:
				job1 = ii[1]
				asset1 = ii[3][:-2]
				asset2 = ii[4][:-2]
				asset3 = ii[5][:-2]
				asset4 = ii[6][:-2]
				asset5 = ii[7][:-2]
				asset6 = ii[8][:-2]
				sig = ii[9]

				if sig == 1:
					sql2= '''SELECT COUNT(*) FROM sc_production1 where comments = "%s" and (asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s") and partno = "%s"''' % (clock,asset1,asset2,asset3,asset4,asset5,asset6,part1)
				else:
					sql2= '''SELECT COUNT(*) FROM sc_production1 where comments = "%s" and (asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s" or asset_num = "%s")''' % (clock,asset1,asset2,asset3,asset4,asset5,asset6)
				cur.execute(sql2)
				tmp3 = cur.fetchall()
				count1 = int(tmp3[0][0])

				trained1 = 'Not Trained'
				if int(count1) > 0:
					trained1 = 'Training <5 days'
				if int(count1) > 4:
					trained1 = 'Training >4 days'
				if int(count1) >9:
					trained1 = 'Trained'
				if int(count1) > 25:
					trained1 = 'A Trainer'
				if count1 > 0:
					cur.execute('''INSERT INTO tkb_matrix(Employee,Job,Trained,Shift,Enabled) VALUES(%s,%s,%s,%s,%s)''', (name1,job1,trained1,shift1,enabled1))
					db.commit()
		db.close()
	return

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
