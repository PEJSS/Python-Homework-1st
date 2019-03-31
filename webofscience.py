from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout
from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import csv
import re

def getLink(url,tag,attribute):#利用BeautifulSoup获取网页节点信息
    html = urlopen(url)
    bso = BeautifulSoup(html.read(),"lxml")
    temp = bso.find_all(tag,class_=attribute)
    return temp

def getInfo(url,PassageName=[],Info=[],Used=[],Summary=[],AuthorInfo=[],ReferInfo=[]):#通过节点信息爬取所需的内容
    html = urlopen(url)
    bso = BeautifulSoup(html.read(),"lxml")
    passagename = bso.find(PassageName[0],class_=PassageName[1]).value.string
    info = bso.find_all(Info[0],class_=Info[1])
    usedtimes = bso.find(Used[0],class_=Used[1]).string
    authorinfo = bso.find_all(AuthorInfo[0],class_=AuthorInfo[1])
    SU = bso.find_all(Summary[0],class_=Summary[1])
    for item in SU:
        if item.string == 'Abstract':
            summary = item.parent.find('p',class_='FR_field').contents[0]
            break
        else:
            summary = '无'
    keywords = ''
    email = ''
    for item in info:
        if item.string == 'By:':
            authorname = item.next_sibling.string
        if item.string == 'Published:':
            publishdate = item.parent.contents[2]
        if item.string == 'KeyWords Plus:':
            for child in item.next_siblings:
                keywords += child.string + '\n'
        if item.string == 'E-mail Addresses:':
            email = item.next_sibling.string
    address = ''
    for item in authorinfo:
        if item.a != None:
            address += item.a.string +'\n'
    referinfo = bso.find(ReferInfo[0],attrs={'title':ReferInfo[1]})
    if referinfo == None:
        refer = '无'
    else:
        link = 'http://apps.webofknowledge.com'+referinfo['href']
        html1 = urlopen(link)
        bso1 = BeautifulSoup(html1.read(),"lxml")
        N = bso1.find('span',id='pageCount.top').string
        N = int(N)
        refer = ''
        Url = bso1.find('form',id='summary_records_form')['paging_url']
        for i in range(1,N+1):
            referlink = Url + str(i)
            html2 = urlopen(referlink)
            bso2 = BeautifulSoup(html2.read(),"lxml")
            refers = bso2.find_all('div',class_='search-results-item')        
            for item in refers:
                authors = item.find_all('span',class_='label')
                for thing in authors:
                    if thing.string == 'By: ':
                        author = thing.parent.contents[2]
                    elif thing.string == 'Group Author(s):\n    ':
                        author = thing.parent.contents[2]
                    elif thing.string == 'Edited by: ':
                        author = thing.parent.contents[2]
                if item.find('span',class_='reference-title') == None:
                    refer += '标题不可用' + ' 作者:' + author + ';\n'
                else:
                    refer += item.find('span',class_='reference-title').value.string + ' 作者:' + author + ';\n'
    return [passagename,authorname,publishdate,usedtimes,keywords,summary,address,email,refer]

def getData():#将爬取的信息存为csv文件
    with open('American Economic Review.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['文章标题','作者名字','出版年','被引频次','关键词','摘要','作者地址','电子邮件','参考文献'])
    for i in range(1,396):
        journal=getLink("http://apps.webofknowledge.com/summary.do?product=WOS&parentProduct=WOS&search_mode=GeneralSearch&parentQid=&qid=1&SID=7BBPAcbDNVtCwsCcpHn&colName=WOS&&update_back2search_link_param=yes&page=" + str(i), "a","smallV110 snowplow-full-record")
        for item in journal:
            arti='http://apps.webofknowledge.com'+item['href']
            b=getInfo(url=arti,
                      PassageName=['div','title'],
                      Info=['span','FR_label'],
                      Used=['span','large-number'],
                      Summary=['div','title3'],
                      AuthorInfo=['td','fr_address_row2'],
                      ReferInfo=['a',"View this record's bibliography"])
            with open('American Economic Review','a',newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(b)

def readData():#读取文件存入矩阵中
    file_object = open('D:\文档\学习\爬虫\American Economic Review.txt')
    try:
        file_context = file_object.read()
    finally:
        file_object.close()
    data = re.sub('无\n','\n"\n',file_context).split('\n"\n')
    for i in range(len(data)):
        data[i] = data[i].split('\t')
    data = np.array(data)
    data = np.delete(data,data.shape[0]-1,axis=0)
    return data

class App(QWidget):#GUI界面
    def __init__(self, data):
        super().__init__()
        self.title = 'Web of Science:American Economic Review'
        self.initUI()
        self.data = data
    def initUI(self):
        self.setWindowTitle(self.title)
        text = QLabel('请输入需查询的文章标题')
        title = QLabel('Title')
        author = QLabel('Author')
        publishdate = QLabel('PublishDate')
        usedtimes = QLabel('UsedTimes')
        keywords = QLabel('KeyWords')
        summary = QLabel('Summary')
        address = QLabel('Address')
        email = QLabel('E-mail')
        refers = QLabel('References')
        self.textEdit = QLineEdit(self)
        self.titleEdit = QLineEdit()
        self.authorEdit = QLineEdit()
        self.publishdateEdit = QLineEdit()
        self.usedtimesEdit = QLineEdit()
        self.keywordsEdit = QLineEdit()
        self.summaryEdit = QTextEdit()
        self.addressEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.refersEdit = QTextEdit()
        self.button = QPushButton('Information', self)
        layout=QVBoxLayout()
        layout.addWidget(text)
        layout.addWidget(self.textEdit)
        layout.addWidget(title)
        layout.addWidget(self.titleEdit)
        layout.addWidget(author)
        layout.addWidget(self.authorEdit)
        layout.addWidget(publishdate)
        layout.addWidget(self.publishdateEdit)
        layout.addWidget(usedtimes)
        layout.addWidget(self.usedtimesEdit)
        layout.addWidget(keywords)
        layout.addWidget(self.keywordsEdit)
        layout.addWidget(summary)
        layout.addWidget(self.summaryEdit)
        layout.addWidget(address)
        layout.addWidget(self.addressEdit)
        layout.addWidget(email)
        layout.addWidget(self.emailEdit)
        layout.addWidget(refers)
        layout.addWidget(self.refersEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.getTitle)
        self.show()
    def getTitle(self):
        titleValue = self.textEdit.text()
        for item in self.data:
            if titleValue.strip('\'').strip('\"') == item[1].strip('\'').strip('\"'):
                self.titleEdit.setText(item[1])
                self.authorEdit.setText(item[2])
                self.publishdateEdit.setText(item[3])
                self.usedtimesEdit.setText(item[4])
                self.keywordsEdit.setText(item[5])
                self.summaryEdit.setPlainText(item[6])
                self.addressEdit.setText(item[7])
                self.emailEdit.setText(item[8])
                self.refersEdit.setPlainText(item[9])
        self.textEdit.setText('')