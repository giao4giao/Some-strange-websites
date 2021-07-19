import sqlite3,json,time



conn = sqlite3.connect('save.db',timeout=5)
c = conn.cursor()
c.execute('''CREATE TABLE  IF NOT EXISTS 错误网址
			(ID INTEGER PRIMARY KEY AUTOINCREMENT,
			ADDRESS       CHAR(255) NOT NULL);''')
conn.commit()
'''
cursor = c.execute("SELECT id, address  from 错误网址")
l=[]
for row in cursor:
   num = row[1].split('/')[-1].replace('.html', '')
   #l.append(int(num))
   print ("ID = ", row[0])
   print ("ADDRESS = ", row[1])
'''
'''
cursor = c.execute("SELECT id, address ,title from 网址与标题")
l=[]
for row in cursor:
   print ("ID = ", row[0])
   print ("ADDRESS = ", row[1])
   print('TITLE = ',row[2])
   print()
   print()
'''
cursor = c.execute("SELECT id, address ,title from 网址与标题")
cursor=[i for i in cursor if str(i[2]).find('for Sale')<0 and i[2].find('域名售卖')<0]
cursor=[i for i in cursor if i[2].find('没有找到站点')<0 and str(i[2]).find('for purchase')<0 and str(i[2]).find('for sale')<0 and str(i[2]).find('HugeDomains')<0 and str(i[2]).find('已过期')<0]
l=['<tr><th>{}</th><th><a href={}>{}</a></th></tr>'.format('{}',row[1],(row[2].replace('{'+row[2].split('{')[-1].split('}')[0]+'}','') if not row[2].strip()=='' else '数据库内容为空，自动加字(点击可能有惊喜)')) for row in cursor]


l=[l[i].format(str(i+1)) for i in range(len(l))]


#print(l)
html1='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>网址查询</title>
</head>
<body>
<style>
    .table11_7 table {
        width:200%;
        margin:20px 0;
        border:0;
    }
    .table11_7 th {
        background-color:;
        color: red; 
        font-size: 20px
        color:#FFFFFF
    }
    .table11_7,.table11_7 th,.table11_7 td {
        font-size:0.95em;
        text-align:center;
        padding:4px;
        border-collapse:collapse;
    }
    .table11_7 th,.table11_7 td {
        border: 1px solid #2087fe;
        border-width:1px 0 1px 0;
        border:2px inset #ffffff;
    }
    .table11_7 tr {
        border: 1px solid #ffffff;
    }
    .table11_7 tr:nth-child(odd){
        background-color:#aae1fe;
    }
    .table11_7 tr:nth-child(even){
        background-color:#ffffff;
    }
</style>
<table class=table11_7>
 <colgroup>
    <col span="5" style="background-color:red">
    <col style="background-color:yellow">
  </colgroup>'''

html2='''
</table>
</body>
</html>
'''
html=html1+'\n'.join(l)+html2
print(html)
file=html
conn.close()

with open('text.html','w',encoding='utf-8')as f:
	f.write(str(file))




