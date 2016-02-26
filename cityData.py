#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from BeautifulSoup import BeautifulSoup
from lxml import etree
import requests
import re
from io import StringIO, BytesIO
import urllib

places = []


with open('cityData', 'rb') as handle:
	places = pickle.loads(handle.read())

def writeIt() :
	with open('cityData', 'wb') as handle:
		pickle.dump(places, handle)

def extractNumbeo(soup,containsText) :
 	trs = soup.findAll('tr')
 	for atr in trs :
 		if containsText in atr.text :
		 	tag = atr.findAll('td',attrs={'class' : 'priceValue '})[0]
			val = tag.text.replace('<td style="text-align: right" class="priceValue "> ',"")
			return val.replace('&nbsp;&#8364;',"").replace(",","")


for i,place in enumerate(places) :
	print place
	if not 'javaJobs' in place :
		response = requests.get(urllib.unquote("http://www.indeed.fr/emplois?q=java&l="+place['city']).decode('utf8'))
		soup = BeautifulSoup(response.text)
		count = [div.text for div in soup.findAll('div', attrs={'id': 'searchCount'})]
		if count : 
			print count[0]
			sjavaJobs = re.sub("Emplois 1 à 10 sur ","",count[0].encode('utf-8')).strip()
			sjavaJobs = re.sub("\D","",sjavaJobs)
			javaJobs = int(sjavaJobs.replace(" ",""))
		else :
			javaJobs = 0
		place['javaJobs'] = javaJobs
		writeIt()

	filename = "./numbeoData/"+place['city']
	 	
	if not 'numbeoData' in place : 
		response = requests.get(urllib.unquote('http://www.numbeo.com/cost-of-living/city_result.jsp?country=France&city='+place['city']).decode('utf8'))
		with open(filename,"wb") as f :
 			f.write(response.text.encode('UTF-8'))
 			place['numbeoData'] = filename
 			writeIt()
 	if not 'rentSalaryRatio' in place : 
	 	with open(filename,"rb") as f : 
	 		soup = BeautifulSoup(f.read())
	 		print 'http://www.numbeo.com/cost-of-living/city_result.jsp?country=France&city='+place['city']
	 		rent = extractNumbeo(soup,"Apartment (3 bedrooms) in City Centre")
	 		salary = extractNumbeo(soup,"Average Monthly Disposable Salary")
	 		if rent == "?" or salary == "?" or not rent or not salary:
	 			print "ERROR CANNOT GET DATA FOR",place
	 		else : 
	 			print rent,salary
	 			frent = float(rent)
	 			fsalary = float(salary)
		 		place['rentSalaryRatio'] = frent/fsalary
		 		writeIt()
	







