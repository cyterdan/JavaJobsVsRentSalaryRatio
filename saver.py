import pickle

with open('cityData', 'rb') as handle:
	places = pickle.loads(handle.read())



with open("cities","wb") as output : 
	output.write("["+"City"+",RentSalaryRation"+",JavaJobs"+",State"+",Population],\n")
	for place in places :
		if 'rentSalaryRatio' in place and 'javaJobs' in place : 
			output.write("['"+place['city']+"',"+str(place['rentSalaryRatio'])+","+str(place['javaJobs'])+",'"+place['state'].replace("'","")+"',"+str(place['population'].replace(",",""))+"],\n")


