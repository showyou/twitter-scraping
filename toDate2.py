def toDate2(date):
	import time,datetime
	dates = time.strptime(date,"%Y-%m-%dT%H:%M:%S+00:00")
	dt = datetime.datetime(dates[0],dates[1],dates[2],dates[3],dates[4],dates[5],dates[6])+datetime.timedelta(hours=9)
	
	return dt

if __name__ == "__main__":
	import datetime
	date = "2008-02-24T06:39:37+00:00"
	
	print toDate2(date)
	print datetime.datetime.today()
	