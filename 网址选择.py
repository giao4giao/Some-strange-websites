import requests,json
from bs4 import BeautifulSoup
#from fake_useragent import UserAgent
def UserAgent():
	random={}
	def __init__(self):
		pass
	def random(self):
		return {}


def get_r(web):	
#	headers={'user-agent':UserAgent().random}
	headers={'user-agent':None}
	try:
		r=requests.get(web,headers=headers,timeout=2)
	#	if r.status_code==200:
	#		return r
		return r
	except requests.exceptions.RequestException :
		return 





for num in range(810 , 999):
	web='http://my{}.com'.format(str(num))
	print(web)
	r=get_r(web)
	print(r)
	if r:
		r.encoding = r.apparent_encoding
		s = BeautifulSoup(r.text,features='html.parser')
		print(s.find('title'))
		if s.find('title'):
			with open('wz.txt','a',encoding='utf_8')as f:
				#txt=json.dumps({'web':web,'title':str(s.find('title').get_text())})+'\n'
				txt=str({'web':web,'title':str(s.find('title').get_text())})+'\n'
				f.write(txt)










