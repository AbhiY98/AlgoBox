import requests, json, os
from datetime import date, datetime, timezone
from APIServer.config import *
from APIServer.models import contest

def getContestList():
	today = str(datetime.now(timezone.utc).strftime("%Y-%m-%d"))
	API_UNAME = str(os.environ.get("CListUserName"))
	API_KEY = str(os.environ.get("CListAPIKey"))

	baseaddress = "https://clist.by/api/v1/contest/?format=json&username="+API_UNAME+"&api_key="+API_KEY+"&order_by=start"
	baseaddress += "&end__gte="
	baseaddress += today

	dict = {"objects":[]}
	sites = {0:"codeforces.com", 1:"topcoder.com", 2:"codechef.com", 3:" facebook.com/hackercup", 4:"codingcompetitions.withgoogle.com", 5:"codeforces.com/gyms", 6:"hackerearth.com", 7:"hackerrank.com", 8:"open.kattis.com", 9:"csacademy.com", 10:"leetcode.com", 11:"kaggle.com", 12:"atcoder.jp"}
	limits = {0:3, 1:3, 2:4, 3:2, 4:2, 5:2, 6:10, 7:3, 8:3, 9:2, 10:3, 11:4, 12:4}
	def getdata(i) :
		adrs = baseaddress+"&resource__name="+sites[i]+"&limit="+str(limits[i])
		data = requests.get(adrs)
		pymap = json.loads(data.content)
		for j in range(len(pymap["objects"])) :
			dict["objects"].append(pymap["objects"][j])
	for i in range(0, len(sites)) :
		getdata(i)
	jsonobject = json.dumps(dict)

	return jsonobject

def viewObject():
	jsonData = getContestList()
	dictObj = json.loads(jsonData)
	dictObj = dictObj['objects']
	return dictObj

def saveModel():
	dictObj = viewObject()
	print (dictObj)
	listOfContest = contest.objects.all()
	for obj in dictObj:
		if listOfContest.filter(event=obj["event"]).exists():
			continue
		else:
			con = contest(event=obj["event"], start=obj["start"], end=obj["end"], 
			duration=obj["duration"], href=obj["href"], domain=obj["resource"]["name"])
			con.save()
