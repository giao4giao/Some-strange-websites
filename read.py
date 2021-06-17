
from bs4 import BeautifulSoup


with open('text.html',encoding='utf-8') as f:
	r=f.read()
soup = BeautifulSoup(r, features='html.parser')
l= soup.find_all('a')
ls=[]
for a in l:
	ls+=[a['href']+'     '+a.text,]
with open('text.txt','w',encoding='utf-8') as f:
	f.write('\n'.join(ls))
