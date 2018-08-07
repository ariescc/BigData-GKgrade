# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import urllib.request,re,time,random,gzip,json,csv
from bs4 import BeautifulSoup
from urllib.parse import quote
#一些必要的声明
universitys =('北京大学','清华大学','中国人民大学','北京航空航天大学',
            '北京理工大学','中国农业大学','北京师范大学','中央民族大学','南开大学',
            '天津大学','大连理工大学','吉林大学','哈尔滨工业大学','复旦大学','同济大学',
            '上海交通大学','华东师范大学','南京大学','东南大学','浙江大学','中国科学技术大学',
            '厦门大学','山东大学','中国海洋大学','武汉大学','华中科技大学','中南大学','中山大学',
            '华南理工大学','四川大学','重庆大学','电子科技大学','西安交通大学','西北工业大学',
            '兰州大学','国防科技大学')
provinces=('安徽','北京','重庆','福建','广东','广西','甘肃','贵州','河北','河南','湖南','湖北',
           '海南','黑龙江','吉林','江苏','江西','辽宁','内蒙古','宁夏','青海','上海','四川',
           '山西','山东','陕西','天津','新疆','西藏','云南','浙江')
#用于保证表头只写一次的变量
COUNT=0;
#定义编码函数
def encode(string):
    string=quote(string)
    return string
#定义保存csv文件函数
def saveFile(mydict):
    #返回数据为空时跳出函数
    if len(mydict)==0 or mydict['totalRecord']['num']=='0':
        return 1;
    #不为空继续操作
    path="Q:\\output"+".csv"
    with open(path,'a+',newline='') as csvfile:
        fieldnames=mydict['school'][0].keys()
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        global COUNT
        if not COUNT:
            writer.writeheader()
            COUNT=COUNT+1
        writer.writerows(mydict['school'])
        csvfile.close()
    #输出当前状态
    info='current: sity: '+mydict['school'][0]['schoolname']+" province: "\
            +mydict['school'][0]['localprovince']+' subject: '\
            +mydict['school'][0]['studenttype']
    print(info)
    return 0
#定义爬虫类
class spider:
    url='http://data.api.gkcx.eol.cn/soudaxue/queryProvinceScore.html'\
    '?messtype=jsonp&lunum=1&callback=jQuery18305139846284800378_1508414690282'\
    '&provinceforschool=&schooltype=&page=1&size=10'\
    '&keyWord=%s'\
    '&schoolproperty=&schoolflag='\
    '&province=%s'\
    '&fstype=%s'\
    '&zhaoshengpici=&fsyear=&_=1508414692133'
    headers={'connection':'keep-alive',
                 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            }
    def _init_(self,url):
        self.url=url
        self.headers=headers
    def getonepage(self,sity,province,subject):
        url=self.url%(encode(sity),encode(province),encode(subject))
        request= urllib.request.Request(url=url,headers=self.headers)
        response = urllib.request.urlopen(request)
        #序列化返回的数据
        data=response.read().decode('utf-8')
        data=re.sub(r'jQuery18305139846284800378_1508414690282\(|\)|\s|;',"",data)
        mydict=json.loads(data)
        #输出错误状态
        if saveFile(mydict):
            error='丢失'+sity+' '+province+' '+subject+' '
            print(error)
    def setpage(self):
        for sity in universitys:
            for province in provinces:
                self.getonepage(sity,province,'文科')
                time.sleep(2)
                self.getonepage(sity,province,'理科')
                time.sleep(2)
crawl=spider()
print(crawl.url)
crawl.setpage();          
#url='http://gkcx.eol.cn/soudaxue/queryProvinceScoreNum.html?&keyWord1=%s&studentprovince=%s&fstype=%s' \
   # %(encode(universitys[1]),encode(provinces[2]),encode('理科')) 
#murl=murl%(encode(universitys[1]),encode(provinces[2]),encode('理科'))
#request= urllib.request.Request(url=murl,headers=headers)
#response = urllib.request.urlopen(request)
#data=response.read()
#data=data.decode('utf-8')
#data
##解析结果为json格式字符串
#test=re.sub(r'jQuery18305139846284800378_1508414690282\(|\)|\s|;',"",data)
##
#test
#test1=json.loads(test)
#a=test1['totalRecord']['num']
#test1['school']
#saveFile(test1)
#type(test1['school'])
#a=int(a)
#data=data.decode('utf-8')
#data






