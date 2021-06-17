import requests, threading, time,sqlite3,json
from bs4 import BeautifulSoup
from queue import Queue




def run_forever(func):
    def wrapper(obj):
        while obj.event:
            func(obj)
    return wrapper



class QiubaiSpider:
    def __init__(self, li_list, count=(1, 1, 1)):
        self.event = True
        self.li_list = li_list
        self.all_num = len(li_list)
        self.now_num = 0
        self.count = count
        self.now_time = 1
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
        # url 队列
        self.url_queue = Queue()
        # 响应队列
        self.page_queue = Queue()
        # 数据队列
        self.data_queue = Queue()

    def add_url_to_queue(self):
        # 把URL添加url队列
        for i in self.li_list:
            self.url_queue.put(i)

    @run_forever
    def add_page_to_queue(self):
        # 发送请求获取数据
        try:
            url = self.url_queue.get()
            if url:
               # print(1)
                response = requests.get(url, headers=self.headers,timeout=3)
            else:
                self.page_queue.put((None, url))
                return
            if response.status_code != 200:
                response.encoding = response.apparent_encoding
                if response.text=='对不起，请稍后再打开！':
                    self.wrong_info_insert(url)
                    self.page_queue.put((None, url))
                else:
                    self.url_queue.put(url)
            else:
                if response.status_code != 500:
                    self.page_queue.put((response,url))
                else:
                    self.page_queue.put((None,url))
        except requests.exceptions.RequestException :
            #print('网络连接超时')
            print('网址:',url,'无法访问;')
            self.url_queue.put(None)
        finally:
            time.sleep(1)
            self.url_queue.task_done()

    def wrong_info_insert(self,url):
        string = str((url,)).replace(',', '')
        conn = sqlite3.connect('save.db', timeout=5)
        c = conn.cursor()
        c.execute('''CREATE TABLE  IF NOT EXISTS 错误网址
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ADDRESS       CHAR(255) NOT NULL);''')
        conn.commit()
        c.execute("SELECT * FROM 错误网址 WHERE address='{}';".format(url))
        row = c.fetchone()
        if not row:
            grammar = "INSERT INTO 错误网址 (ADDRESS)       VALUES {}".format(string)
            # print(grammar)
            c.execute(grammar)
            conn.commit()
        else:
            if url == row[1]:
                pass
                # print('已经存在数据')
                # print("ID = ", row[0])
                # print("ADDRESS = ", row[1], "\n")
            else:
                grammar = "INSERT INTO 错误网址 (ADDRESS)       VALUES {}".format(string)
                c.execute(grammar)
                conn.commit()
        conn.close()



    @run_forever
    def add_dz_to_queue(self):
        try:
            dic={}
            page,url = self.page_queue.get()
            if page:
                page.encoding = page.apparent_encoding
                if page.text=='':
                    self.wrong_info_insert(url)
                    self.data_queue.put((None,url))
                    return
                soup = BeautifulSoup(page.text, features='html.parser')
                if not soup.find('title'):
                    self.wrong_info_insert(url)
                    self.data_queue.put((None,url))
                    return
                if soup.find('title').get_text()=='出现错误！':
                    # print('出现错误！')
                    self.wrong_info_insert(url)
                    self.data_queue.put((None,url))
                    return
                dic['web'] = url
                dic['title'] = soup.find('title').get_text()
                self.data_queue.put((dic,url))
            else:
                self.data_queue.put((None,url))
        except BaseException as e:
            print(e)
            self.page_queue.put((page,url))
        finally:
            time.sleep(1)
            self.page_queue.task_done()

    @run_forever
    def save_dz_list(self):
        try:
            data,url = self.data_queue.get()
            #连接数据库
            conn = sqlite3.connect('save.db',timeout=5)
            #conn.text_factory = str
            #获取到指针
            c = conn.cursor()
            #c.execute('PRAGMA encoding="UTF-8";')
            #如果没有表创建表
            c.execute('''CREATE TABLE  IF NOT EXISTS 网址与标题
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ADDRESS        CHAR(255)   NOT NULL,
            TITLE          CHAR(255) NOT NULL);''')
            #提交更改
            conn.commit()
            
            #通过上面函数获取内容
            if data:
                #分别获取数据
                web=data.get('web')
                title=data.get('title')
                string=str((title,web))
                c.execute("SELECT * FROM 网址与标题 WHERE address='{}';".format(url))
                row=c.fetchone()
                if not row:
                    #print(string)
                    #构建sql语句
                    grammar="INSERT INTO 网址与标题 (TITLE,ADDRESS)       VALUES {}".format(string)
                    #进行入库操作
                    c.execute(grammar)
                    #提交更改
                    conn.commit()
                else:
                    if title==row[2] and web==row[1]:
                        pass
                        #print('已经存在数据')
                        #print ("ID = ", row[0])
                        #print ("NAME = ", row[1])
                        #print ("ADDRESS = ", row[2])
                        #print ("AUTHOR = ", row[3], "\n")
                    else:
                        #构建sql语句
                        grammar="INSERT INTO 网址与标题 (TITLE,ADDRESS)       VALUES {}".format(string)
                        #进行入库操作
                        c.execute(grammar)
                        #提交更改
                        conn.commit()
                #断开数据库连接
                conn.close()
            self.now_num += 1
        except BaseException as e:
            print(e)
            self.data_queue.put((data,url))
        finally:
            time.sleep(0.5)
            self.data_queue.task_done()

    def run_use_more_task(self, func, count=1):
        # 把func放到线程中执行,count:开启多少线程执行
        for i in range(0, count):
            t = threading.Thread(target=func)
            t.setDaemon(True)
            t.start()

    def verification_event(self):
        while True:
            if self.now_num == self.all_num:
                self.event = False
                break
            else:
                print(self.now_num,self.all_num)
                time.sleep(1)

    def run(self):
        # 开启线程执行上面的几个方法
        url_t = threading.Thread(target=self.add_url_to_queue)
        url_t.setDaemon(True)
        url_t.start()

        p = threading.Thread(target=self.verification_event)
        p.setDaemon(True)
        p.start()

        self.run_use_more_task(self.add_page_to_queue, self.count[0])
        self.run_use_more_task(self.add_dz_to_queue, self.count[1])
        self.run_use_more_task(self.save_dz_list, self.count[2])

        self.url_queue.join()
        self.page_queue.join()
        self.data_queue.join()



if __name__=='__main__':
    url='http://my{}.com'
#    url='http://www.69t{}.com'
    start=0
    end=998
    count=30
    l=[]
    
    for i in range(start,end+1):
        l.append(url.format(str(i).zfill(3)))
    #print(l)
    QiubaiSpider(l,(count,count,count)).run()


