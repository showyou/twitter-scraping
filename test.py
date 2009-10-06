#!/usr/bin/env python

"""
	Test for twitter-scraping( needs nose )
"""

import twitterscraping
import userdata
class Test:
	def getAuthData(self,fileName):
		return

	def testGetTwitterStatus(self):
		tw = twitterscraping.Twitter(userdata.conf)
		d = tw.get("")
		assert len(d) != 0

	def testAPILimit(self):
		tw = twitterscraping.Twitter(userdata.conf)
		l = tw.getAPILimit()
		print l

if __name__ == '__main__':
	import nose
	#nose.main()
	t = Test()
	#t.testGetTwitterStatus()
	t.testAPILimit()
	
