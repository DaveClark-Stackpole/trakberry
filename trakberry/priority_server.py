def prioritize(request):
	db, cur = db_set(request)
	cur.execute("""DROP TABLE IF EXISTS tkb_asset_priority""")
	cur.execute("""CREATE TABLE IF NOT EXISTS tkb_asset_priority(Id INT PRIMARY KEY AUTO_INCREMENT,asset_num CHAR(80), part CHAR(80), priority int(10))""")
	sql = "SELECT DISTINCT asset_num FROM sc_production1"
	cur.execute(sql)
	tmp=cur.fetchall()
	asset2 = []
	for i in tmp:
		asset = i[0][:4]
		try:
			test1 = int(asset)
		except:
			asset = asset[:3]
		try:
			test1 = int(asset)
			asset2.append(asset)
		except:
			dummy = 1
	for i in asset2:
		tmp_asset2 = 1
		n = 'None'
		try:
			sql1 = "SELECT partno FROM sc_production1 where left(asset_num,4) = '%s' and partno != '%s' ORDER BY id DESC LIMIT 1" %(i,n)
			cur.execute(sql1)
			tmp_part = cur.fetchall()
			part2 = tmp_part[0][0]
			part2 = part2[:7]
			cur.execute('''INSERT INTO tkb_asset_priority(asset_num,part) VALUES(%s,%s)''', (i,part2))
			db.commit()
		except:
			dummy = 1
	sql1 = "SELECT * FROM tkb_priorities"
	cur.execute(sql1)
	tmp_pr = cur.fetchall()
	for i in tmp_pr:
		mql =( 'update tkb_asset_priority SET priority="%s" WHERE part="%s"' % (i[1],i[2]))
		cur.execute(mql)
		db.commit()
	db.close()
	return
