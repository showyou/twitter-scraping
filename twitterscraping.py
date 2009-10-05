# -*- coding: utf-8 -*-
import urllib2,urllib
import simplejson

class Twitter:
	def __init__(self, userdata):
		self.user = userdata
		self.url  = "twitter.com"
		self.serviceName = "Twitter API"
		self.serviceURL = "twitter.com"
		
	def setUser(self,userdata):
		self.user = userdata
	def setAuthService(self,service):
		if service == "twitter":
			self.serviceName = "Twitter API"
			self.serviceURL = "twitter.com"
			self.url = "twitter.com"

		if service == "wassr":
			self.serviceName = "API Authentication"
			self.serviceURL = "api.wassr.jp:80"
			self.url = "api.wassr.jp"
		
	def setAuthHandler(self):
		#ユーザ名等設定する
		#初回時のみで充分かなぁ
		auth_handler = urllib2.HTTPBasicAuthHandler()
		auth_handler.add_password(self.serviceName,self.serviceURL,self.user['user'],self.user['pass'])
		opener = urllib2.build_opener(auth_handler)
		urllib2.install_opener(opener)
		return opener
	def getHttpJson(self,url):
		self.setAuthHandler()
		data = urllib2.urlopen(url)
		urlstring = data.read()
		a = simplejson.loads(urlstring)
		return a
	def get(self,username): 
		a = self.getHttpJson("http://%s/statuses/friends_timeline.json" % self.url)
		return self.parseTwitJSON(a)
		
	def getPublicTimeline(self):
		a = self.getHttpJson("http://%s/statuses/public_timeline.json" % self.url)
		return self.parseTwitJSON(a)
		
	def getReplies(self,username):
		a = self.getHttpJson("http://%s/statuses/replies.json" % self.url)
		return self.parseTwitJSON(a)
	
	def getDM(self,username):
		s = "http://%s/direct_messages.json" % self.url
		#print "url+" +s
		a = self.getHttpJson(s) 
		return self.parseTwitJSONDM(a)
		
	def getWithPage(self,username,num): 
		# page番号つきget
		self.setAuthHandler()
		s = "http://%s/statuses/friends_timeline.json?page=%d" % self.url, num
		print "url+" +s
		a = self.getHttpJson(s)
		return self.parseTwitJSON(a)

	def getWithUser(self,user): 
		# page番号つきget
		self.setAuthHandler()
		s = "http://%s/statuses/user_timeline/%s.json" % self.url, user
		print "url+" +s
		a = getHttpJson(s)
		return self.parseTwitJSON(a)
	
	def getWithUserPage(self,username,num): 
		# page番号つきget
		self.setAuthHandler()
		s = "http://%s/statuses/user_timeline/%s.json?page=%d" % self.url, username, num
		print "url+" +s
		a = self.getHttpJson(s)
		return self.parseTwitJSON(a)

	def getFollowersLite(self,username):
		# followerを取得	
		
		self.setAuthHandler()
		# ここ変える
		s = "http://%s/statuses/followers.json?lite=true" % self.user
		print "url+" +s
		a = self.getHttpJson(s)	
		return self.parseTwitJSONFollowers(a)
	
	def parseTwitJSON(self,a):
		result = []
		for x in a:
			resultSub = []
			#resultSub.append(x['created_at'])
			#print x
			y = x['user']
			resultSub.append(y['screen_name'])
			resultSub.append(x['text'])
			if self.url != "api.wassr.jp" :
				resultSub.append(x['created_at'])
			else:
				resultSub.append(0)
			resultSub.append(y['profile_image_url'])
			resultSub.append(y['id'])
			resultSub.append(x['in_reply_to_status_id'])
			result.append(resultSub)
			#print resultSub[0]+resultSub[1]
		return result
	
	def parseTwitJSONDM(self,a):
		result = []
		for x in a:
			resultSub = []
			#resultSub.append(x['created_at'])
			y = x['sender']
			resultSub.append(y['screen_name'])
			resultSub.append(x['text'])
			resultSub.append(x['created_at'])
			resultSub.append(y['profile_image_url'])
			resultSub.append(y['id'])
			result.append(resultSub)
			#print resultSub[0]+resultSub[1]
		return result	
	
	def parseTwitJSONFollowers(self,a):
		result = []
		for x in a:
			resultSub = []
			#resultSub.append(x['created_at'])
			#y = x['sender']
			resultSub.append(x['screen_name'])
			#resultSub.append(x['text'])
			#resultSub.append(x['created_at'])
			result.append(resultSub)
			#print resultSub[0]+resultSub[1]
		return result		
	
	def put(self,s):
		self.setAuthHandler()
		postdata = {}
		postdata['status'] = s.encode('utf-8')
		#if self.url == "api.wassr.jp" :
		postdata['source']='python-scraping'
		param = urllib.urlencode(postdata)
		data = urllib2.urlopen("http://%s/statuses/update.json" % self.url, param)
		print data.read()

	"""
		Favする
	"""
	def createFavorite(self,id):
		
		self.setAuthHandler()
		postdata = {}
		#if self.url == "api.wassr.jp" :
		#	postdata['source']='crochet'
		#postdata['source'] = s
		param = urllib.urlencode(postdata)
		url = "http://%s/favorites/create/%d.json" % self.url, id
		data = urllib2.urlopen(url,param)
		print data.read()
	"""
		サインインします
		In: なし(クラスメンバ変数でuser,pass)
	"""
	def singIn(self,s):
		import cookielib
		#opener.open("http://twitter.com/sessions","username=&s&password%s" % (self.user['user'],self.user["pass"]))
		postdata = {}
		postdata['session[username_or_email]'] = self.user['user']
		postdata['session[password]'] = self.user['pass']
		#postdata['source'] = s
		en_post_data = urllib.urlencode(postdata)

		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

		# ログイン／cookie取得
		r = opener.open("http://twitter.com/sessions",en_post_data)
		r.read()
		return opener
	
	def getWithScraping(self,user,num=1):
		#ログイン必要？
		opener = self.singIn("")
		s = "http://%s/home?page=%d" % self.url, num
		data = opener.open(s)
		urlstring = data.read()
		#print urlstring
		if num == 1:
			return self.scrapeTwit(urlstring,True)
		else:
			return self.scrapeTwit(urlstring,False)
	
	def getUserPageWithScraping(self,user,num):

		self.setAuthHandler()
		s = "http://%s/%s?page=%d" % self.url, user, num
		print "url+" +s
		data = urllib2.urlopen(s)
		urlstring = data.read()
		if num == 1:
			return self.scrapeTwitUserPage(urlstring,True)
		else:
			return self.scrapeTwitUserPage(urlstring,False)
		
	# HTMLをスクレイプします。
	def scrapeTwitUserPage(self,a,isFirst):
		import re
		# <span class="entry-title entry-content">~</span>(最短)
		#reg = re.compile(r'<(.*?)>')
		retList = []
		
		reg = re.compile("<span class=\"entry-title entry-content\">([\w\W]*?)</span>[\w\W]*?<abbr class=\"published\" title=\"([\w\W]*?)\">.*?</abbr>",re.MULTILINE)
		reg2 = re.compile("<span class=\"entry-content\">([\w\W]*?)</span>[\w\W]*?<span class=\"published\" title=\"([\w\W]*?)\">.*?</span>",re.MULTILINE)
		# もし1ページ目なら、最新の発言も取ってくる
		#if isFirst :
		#	a3 = reg.findall(a)
		#	retList.append( a3[0] )

		a2 = reg2.findall(a)
		for aa in a2:
			retList.append( (aa[0].strip(),aa[1]) )

		return retList


	def scrapeTwit(self,str,flag):
		import re
		regTwit = re.compile("<tr [\w\W]*?(id=[\w\W]*?)</tr>",re.MULTILINE)
		regStatusID = re.compile("id=\"status_(\d*?)\"")
		regImage = re.compile("<img [\w\W]*? src=\"([\w\W]*?)\"",re.MULTILINE)
		regUserAndMessage = re.compile("<td class=\"status-body\">([\w\W]*?)</td>")
		regUser = re.compile("<a href=.*?>(.*?)</a>")
		regMessage= re.compile("<span class=\"entry-content\">\s*?(\S[\w\W]*?)</span>",re.MULTILINE)

		regTime = re.compile("<span class=\"[\w\W]*?\" title=\"([\w\W]*?)\">")
		regATagBegin = re.compile("<a href=.*?>")

		str = str.replace("\t","")
		str = str.replace("\n","")
		a = regTwit.findall(str)
		resultList = []
		for aa in a:
			resultData = {}

			statusID = regStatusID.search(aa)
			resultData['statusID'] = statusID.group(1)
			b = regImage.search(aa)
			resultData['image'] = b.group(1)
			c = regUserAndMessage.search(aa).group(1)
			d1 = regUser.search(c)
			d2 = regMessage.search(c)	
			resultData['user'] = unicode(d1.group(1),'utf-8')
			message = unicode(d2.group(1),'utf-8')
			#message2 = regATagBegin.sub("",message)
			#resultData['message'] = message2.replace("</a>","")
			resultData['message'] = message
			tm = regTime.search(aa)
			resultData['time'] = tm.group(1)
			result = []
			result.append(resultData['user'])
			result.append(resultData['message'].replace("&lt;","<").replace("&gt;",">"))
			result.append(resultData['time'])
			result.append(resultData['image'])
			result.append(resultData['statusID'])
			resultList.append(result)

		return resultList

	def replyID2text(self,id):
		s = "http://%s/statuses/show/%d.json" % (self.url, id) 
		print "url+" +s
		a = self.getHttpJson(s)
		return a

	def getAPILimit(self):
		s = "http://twitter.com/account/rate_limit_status.json"
		return self.getHttpJson(s)
