#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle

places = []


with open('cityData', 'rb') as handle:
	places = pickle.loads(handle.read())
	
with open("cities","wb") as output : 
	output.write("["+"Ville"+",RatioLoyerSalaire"+",JobsJava"+"Region"+",Population],\n")
	for place in places :
		if 'rentSalaryRatio' in place and 'javaJobs' in place : 
			output.write("['"+place['city']+"',"+str(place['rentSalaryRatio'])+","+str(place['javaJobs'])+",'"+place['region'].replace("'","")+"',"+str(place['population'].replace(",",""))+"],\n")

