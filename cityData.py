
import pickle
from BeautifulSoup import BeautifulSoup
from lxml import etree
import requests
import re
from io import StringIO, BytesIO

places = []
states = {
 "Alabama" : "AL",
 "Alaska" : "AK",
 "Arizona" : "AZ",
 "Arkansas" : "AR",
 "California" : "CA",
 "Colorado" : "CO",
 "Connecticut" : "CT",
 "District of Columbia" :"DC",
 "Delaware" : "DE",
 "Florida" : "FL",
 "Georgia" : "GA",
 "Hawaii" : "HI",
 "Hawai'i" : "HI",
 "Idaho" : "ID",
 "Illinois" : "IL",
 "Indiana" : "IN",
 "Iowa" : "IA",
 "Kansas" : "KS",
 "Kentucky" : "KY",
 "Louisiana" : "LA",
 "Maine" : "ME",
 "Maryland" : "MD",
 "Massachusetts" : "MA",
 "Michigan" : "MI",
 "Minnesota" : "MN",
 "Mississippi" : "MS",
 "Missouri" : "MO",
 "Montana" : "MT",
 "Nebraska" : "NE",
 "Nevada" : "NV",
 "New Hampshire" : "NH",
 "New Jersey" : "NJ",
 "New Mexico" : "NM",
 "New York" : "NY",
 "North Carolina" : "NC",
 "North Dakota" : "ND",
 "Ohio" : "OH",
 "Oklahoma" : "OK",
 "Oregon" : "OR",
 "Pennsylvania" : "PA",
 "Rhode Island" : "RI",
 "South Carolina" : "SC",
 "South Dakota" : "SD",
 "Tennessee" : "TN",
 "Texas" : "TX",
 "Utah" : "UT",
 "Vermont" : "VT",
 "Virginia" : "VA",
 "Washington" : "WA",
 "West Virginia" : "WV",
 "Wisconsin" : "WI",
 "Wyoming" : "WY"
}

with open('cityData', 'rb') as handle:
	places = pickle.loads(handle.read())


###replacements



def writeIt() :
	with open('cityData', 'wb') as handle:
		pickle.dump(places, handle)

def extractNumbeo(soup,containsText) :
 	trs = soup.findAll('tr')
 	for atr in trs :
 		if containsText in atr.text :
		 	tag = atr.findAll('td',attrs={'class' : 'priceValue '})[0]
			val = tag.text.replace('<td style="text-align: right" class="priceValue "> ',"")
			return val.replace('&nbsp;&#36;',"").replace(",","")


for i,place in enumerate(places) :
	print place
	if not 'javaJobs' in place :
		response = requests.get("http://www.indeed.com/jobs?q=java&l="+place['city']+","+place['state'])
		soup = BeautifulSoup(response.text)
		count = [div.text for div in soup.findAll('div', attrs={'id': 'searchCount'})]
		if count : 
			javaJobs = int(re.sub("Jobs [0-9] to [0-9]+ of ","",count[0]).replace(",",""))
		else :
			javaJobs = 0
		place['javaJobs'] = javaJobs
		writeIt()

	filename = "./numbeoData/"+place['city']
	 	
	if not 'numbeoData' in place : 
		response = requests.get('http://www.numbeo.com/cost-of-living/city_result.jsp?country=United+States&city='+place['city']+",+"+states[place['state']])
		with open(filename,"wb") as f :
 			f.write(response.text.encode('UTF-8'))
 			place['numbeoData'] = filename
 			writeIt()

 	if not 'rentSalaryRatio' in place : 
	 	with open(filename,"rb") as f : 
	 		soup = BeautifulSoup(f.read())
	 		print 'http://www.numbeo.com/cost-of-living/city_result.jsp?country=United+States&city='+place['city']+",+"+states[place['state']]
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
	
with open("cities","wb") as output : 
	for place in places :
		output.write(place['city']+"\t"+place['state']+"\t"+place['population']+"\t"+str(place['javaJobs'])+"\t"+str(place['rentSalaryRatio'])+"\n")







