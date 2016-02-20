import pickle

with open('cityData', 'rb') as handle:
	places = pickle.loads(handle.read())



with open("cities","wb") as output : 
	for place in places :
		if 'rentSalaryRatio' in place and 'javaJobs' in place : 
			output.write(place['city']+"\t"+place['state']+"\t"+place['population']+"\t"+str(place['javaJobs'])+"\t"+str(place['rentSalaryRatio'])+"\n")


