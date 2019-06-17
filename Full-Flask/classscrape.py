import requests
import json 
from bs4 import BeautifulSoup
import time
import pickle

def make_3_magic_requests(datecode):
	first_url = 'https://banxessbprod.tru.ca/StudentRegistrationSsb/ssb/term/termSelection?mode=search'

	second_url = 'https://banxessbprod.tru.ca/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_term={}&startDatepicker=&endDatepicker=&pageOffset=0&pageMaxSize=500&sortColumn=subjectDescription&sortDirection=asc'.format(datecode)
	second_url = 'https://banxessbprod.tru.ca/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_subject={}&txt_term={}&startDatepicker=&endDatepicker=&pageOffset=0&pageMaxSize=500&sortColumn=subjectDescription&sortDirection=asc'.format(subj,datecode)


	header = {
	'Host':'banxessbprod.tru.ca',
	'Connection':'keep-alive',
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'X-Synchronizer-Token':'',
	'X-Requested-With':'XMLHttpRequest',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
	'Referer':'https://banxessbprod.tru.ca/StudentRegistrationSsb/ssb/classSearch/classSearch',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
	'Cookie':''
	}

	header2 = {
	'Host':'banxessbprod.tru.ca',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Accept':'*/*',
	'X-Synchronizer-Token':'',
	'X-Requested-With':'XMLHttpRequest',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
	'Referer':'https://banxessbprod.tru.ca/StudentRegistrationSsb/ssb/classSearch/classSearch',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
	'Cookie':''
	}



	my_session = requests.Session()

	first = my_session.get(first_url)
	soup = BeautifulSoup(first.text,'html.parser')
	token = soup.find('meta',{'name':'synchronizerToken'}).attrs['content']

	header['X-Synchronizer-Token'] = token
	header['Cookie'] = 'JSESSIONID'+'='+my_session.cookies['JSESSIONID']

	header2['X-Synchronizer-Token'] = token
	header2['Cookie'] = 'JSESSIONID'+'='+my_session.cookies['JSESSIONID']

	my_session.post('https://banxessbprod.tru.ca/StudentRegistrationSsb/ssb/term/search?mode=search',data='term={}&studyPath=&studyPathText=&startDatepicker=&endDatepicker='.format(datecode),headers=header2)

	final = my_session.get(second_url,headers=header)
	return json.loads(final.text)

def get_subj_set(datecode):
	url = 'https://banxessbprod.tru.ca/StudentRegistrationSsb/ssb/classSearch/get_subject?searchTerm=&term={}&offset=1&max=500&_=1515716220635'.format(datecode)
	class_page = requests.get(url).text
	subj_list = json.loads(class_page)
	crses = [i['code'] for i in subj_list]
	return crses

def get_semesters():
	#dont have to make a session or anything for this
	url = "https://banxessbprod.tru.ca/StudentRegistrationSsb/ssb/classSearch/getTerms?searchTerm=&offset=1&max=500"
	r = requests.get(url)
	semesters = json.loads(r.text)
	return semesters

def get_classes_for_semester(timecode):	
	num = 0
	output = []
	date = timecode
	file = open(date+'.pic','wb') 
	courses = [i for i in get_subj_set(date)]
	for course in courses:

		contents = make_3_magic_requests(date,course)
		print(date,course)
		for content in contents:
			print(content)
		output.append({course:contents})
		
	print(contents)
	pickle.dump(output,file)
	file.close()

def main():
	semesters = get_semesters()
	kam_semsters = list(filter(lambda x: int(x['code']) % 10 == 0, semesters))
	for semester in kam_semsters:
		code = semester['code']
		get_classes_for_semester(code)

if __name__ == '__main__':
	main()