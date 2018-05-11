# # !/usr/bin/env/Python3
# -*- coding: utf-8 -*-
# #爬虫
import urllib
import urllib.request
import re
import sys
import os
from bs4 import BeautifulSoup
import time
from datetime import datetime
import csv
import random
from multiprocessing import Process

def environmentseting():
    global now_date,now_time,WorkingPath,webheader,url_main,totaldownload,totalresult,downpicturelimit,rangewithend,DataBankName
    now_date = time.strftime("%d/%m/%Y")
    now_time = time.strftime("%H:%M")
    WorkingPath = 'd:\Python\CarData\Collected'
    webheader = {'User-Agent':'Mozilla/5.0(Window NT 6.1;WOW64;rv:23) Gecko/20100101 Firefox/23.0'}
    url_main = 'https://www.autoscout24.de/ergebnisse?'
    totalresult=0
    totaldownload=0
    downpicturelimit=3
    rangewithend=lambda start,end: range(start,end+1)
    global program_start_time
    program_start_time = time.time()
environmentseting()

def getUsedtime():
    used_min, used_sec = divmod(time.time() - program_start_time,60)
    usedtime=used_min+used_sec/60
    return usedtime

def gettimenow():
    return datetime.now().strftime('%H:%M')

def EstimatedTime(downloadedqty,totalqty,usedtime):
    percentage=downloadedqty/totalqty
    timeall=usedtime/percentage
    timeleft=timeall-usedtime
    return timeleft

def DownPictures(carname,Carsoupitem,countpercar):  ##########down load all jpg in the html section
    ################# 保存图片########
    TargetDic = 'd:\Python\Pic'
    if os.path.exists(TargetDic)==False:
        os.mkdir(TargetDic)
    counter=1
    countpercar=countpercar +1

    for link,t in set(re.findall(r'(https*:[^\s)]*?(jpg))',str(Carsoupitem))):
        if (counter==countpercar):
            break
        print('%s Downloading....%s' % (counter,link))
        TargetName=TargetDic+'\\'+str(carname)+'-'+str(counter)+'.jpg'
        try:
            counter = counter + 1
            urllib.request.urlretrieve(link,TargetName)
            time.sleep(random.random())

        except:

            print('failed to download %s' % (link))
            print(sys.exc_info())

def url_to_soup(url):
    req=urllib.request.Request(url=url,headers=webheader)
    response = urllib.request.urlopen(req)
    data = response.read() #获取url对应的数据
    data = data.decode('UTF-8') #解码 UTF8
    soup = BeautifulSoup(data,"lxml")
    return soup

def getbrandcode(brandname=None):
    if brandname==None:
        return None
    codelist = []
    namelist = []
    codedict = {}
    a = open('BrandCode.txt', 'r', encoding='utf-8')
    for line in a:
        try:
            b = re.match(r'(\s+)(.+?)(\")(\d+)(.+)(\")(.+?)(\")', line).group(4)
            c = re.match(r'(\s+)(.+?)(\")(\d+)(.+)(\")(.+?)(\")', line).group(7)
            codelist.append(b)
            namelist.append(c)
        except:
            continue
    Name_and_Code = zip(namelist, codelist)
    for name, code in Name_and_Code:
        codedict[name] = code
    brandcode=codedict.get(brandname)
    print('Get brand code = %s for brand name %s' %(brandcode,brandname))
    return brandcode

def Urlfilter(Targeturl,brandcode=None,priceloopstart=0,priceloopend=0,fregfrom=0,fregto=0,kmfrom=0,kmto=0,powerfrom=0,powerto=0,country='D'):
    if brandcode!=None:
        Targeturl = Targeturl+'&mmvmk0='+str(brandcode)+'&mmvco=1'
    # if pricefrom !=0:
    #     Targeturl = Targeturl + '&pricefrom='+str(pricefrom)
    # if priceto !=0:
    #     Targeturl=Targeturl+'&priceto='+str(priceto)
    if priceloopstart !=0:
        Targeturl = Targeturl + '&pricefrom='+str(priceloopstart)
    if priceloopend !=0:
        Targeturl=Targeturl+'&priceto='+str(priceloopend)
    if fregfrom !=0:
        Targeturl=Targeturl+'&fregfrom='+str(fregfrom)
    if fregto !=0:
        Targeturl=Targeturl+'&fregto='+str(fregto)
    if kmfrom !=0:
        Targeturl=Targeturl+'&kmfrom='+str(kmfrom)
    if kmto !=0:
        Targeturl=Targeturl+'&kmto='+str(kmto)
    if powerfrom !=0:
        Targeturl=Targeturl+'&powerfrom='+str(powerfrom)
    if powerto !=0:
        Targeturl=Targeturl+'&powerto='+str(powerto)
    if country!=None:
        Targeturl=Targeturl+'&cy=D'
    return Targeturl

def downloadinfo(soup,databank,downloadpictures=False,page=1,): ############# download info from a soup object
    ############ carlist is a list, with each paragraph HTML started with "li", which contains information of one car####
    carlist = [car for car in soup.findAll('li',class_="classified-list-item",attrs={"data-item-name":"list-item"})]
    carcounter=0

    ########################## process each item in carlist
    for car in carlist:
        carcounter=carcounter+1
        # print('Start collecting No.%s car'%carcounter)
        carsoup = BeautifulSoup(str(car),"lxml")
        carname = carsoup.h2.text     ############# car name

        carprice1 = carsoup.span.text  ############# car price
        carprice2 = re.sub('\n','',carprice1)
        carprice3=re.sub(r'\.', '', carprice2)
        carprice = re.match(r'(.+?)(\d+)',carprice3).group(2)

        CarMilageText=carsoup.findAll('span',attrs={"data-test":"milage"})
        CarMilageSoup = BeautifulSoup(str(CarMilageText),"lxml")
        try:  # sometimes  .span get nonetype
            carmilage = CarMilageSoup.span.text  ##########milage    use beautiful soup to search span
        except:
            carmilage=0

        CarfirstRegistrationText=carsoup.findAll('span',attrs={"data-test":"firstRegistration"})
        CarfirstRegistrationSoup = BeautifulSoup(str(CarfirstRegistrationText),"lxml")
        carfirstRegistration = CarfirstRegistrationSoup.span.text  ##########milage

        CarPowerText=carsoup.findAll('span',attrs={"data-test":"power"})
        CarPowerSoup = BeautifulSoup(str(CarPowerText),"lxml")
        carpower = CarPowerSoup.span.text
        CarkW = re.match(r'(.+[\s]kW)(.+[\s]PS)',carpower).group(1)
        CarPS = re.match(r'(.+[\s]kW)(.+[\s]PS)',carpower).group(2)

        CarDisText=carsoup.findAll('div',class_='envkv')
        CarDis2 = BeautifulSoup(str(CarDisText),'lxml').text
        CarDis= re.match(r'^(.+[\s]+)(.*)',CarDis2).group(2)

        CarDealer3=str(carsoup.findAll('div',attrs={"data-item":"vendorDataCompact"}))
        CarDealer2 = re.sub(r'\n','',CarDealer3)
        CarDealer = re.match(r'(.+>)(.+)(<.+>)',CarDealer2).group(2)

        CarAddr3=carsoup.findAll('div',attrs={"data-item":"contact-person-address"})
        CarAddr2 = BeautifulSoup(str(CarAddr3),"lxml")
        CarAdd = CarAddr2.p.text

        Carlink3 = carsoup.findAll('a',attrs={"data-item-name":"detail-page-link"})
        Carlink2 = BeautifulSoup(str(Carlink3),'lxml')
        Carlink1 = Carlink2.a['href']
        Carlink = 'https://www.autoscout24.de'+ Carlink1

    ############### put all information in a list############
        CarAllData= [carcounter,now_date,now_time,carname,carprice,carmilage,carfirstRegistration,CarkW,CarPS,CarDis,Carlink,CarDealer]

        # print('Page %s No.%s car\'s name is: %s. Price is %s Milage is %s FR is %s' %(page,carcounter,carname,carprice,carmilage,carfirstRegistration))
        with open(databank,'a',encoding='utf-8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(CarAllData)
        f.close()
        if downloadpictures==True:
            DownPictures(carname,car,downpicturelimit)



    # ################ Save HTML data catch in txt file##########
    # catchpath = 'd:\Python\CarData\Catch.html'
    # with open(catchpath,'w',encoding='UTF-8') as f:
    #     f.write(data)
    # f.close()

def resultqty_getfromsoup(soup):
    resultqty2=soup.findAll('span',id="resultsSummary")
    resultqty3=re.sub('\.','',str(resultqty2))
    qtystr = re.match(r'(.+?)(\d+)', str(resultqty3)).group(2)
    qtyint= int(qtystr)
    return qtyint

def makeDataBank(path,brandname,pricefrom,priceto):
    ########################## make a new csv file nammed as DataBank ########################
    for n in range(1, 100):
        if os.path.exists(path + '\\' + str(brandname) + '_' + str(pricefrom) + '_' + str(
                priceto) + 'DataBank' + str(n) + '.csv'):
            n = n + 1
            databank = path + '\\' + str(brandname) + '_' + str(pricefrom) + '_' + str(
                priceto) + 'DataBank' + str(n) + '.csv'

            continue
        else:
            databank = path + '\\' + str(brandname) + '_' + str(pricefrom) + '_' + str(
                priceto) + 'DataBank' + str(n) + '.csv'
            break
    return databank

def CollectMain(brand=None,pricefrom=0,priceto=0,priceinterval=10):
    # WorkingPath = 'd:\Python\CarData\Collected'
################# set brand, price, year, milage etc. here #####################
    brandname= brand
    brandcode = getbrandcode(brandname)   ############default brandname=None
       ############ default interval 1, download 100% data if possible ############
    fregfrom=0
    fregto= 0
    kmfrom = 0
    kmto= 0
    powerfrom=0   ###########default unit=kw
    powerto=0
    pageloop =20  ####### page numbers
    totalresult = 0
    totaldownload = 0

    ####### new data bank ########
    DataBankName=makeDataBank(WorkingPath,brandname,pricefrom,priceto)

    # ########### get data for process bar ##############
    PriceUrl=Urlfilter(url_main,brandcode,pricefrom,priceto,country=None)
    Pricesoup=url_to_soup(PriceUrl)
    Pricetotal=resultqty_getfromsoup(Pricesoup)
    print('||Start|| %s ||%s --- %s || Need to download--> %s ' %(brandname,pricefrom,priceto,Pricetotal))

    ##### price loop, set interval between pricefrom and priceto smaller get more results #####
    for pricestart in range(pricefrom,priceto+1,priceinterval):


        priceend=pricestart+priceinterval
        priceloopend=priceend-1
        priceloopstart = pricestart

        Targeturl = Urlfilter(url_main,brandcode,priceloopstart,priceloopend,fregfrom,fregto)      ##############  add filter after main url
        soup = url_to_soup(Targeturl)        #############   turn url to soup
        resultqty = resultqty_getfromsoup(soup)
        pricelooptotalqty = 0

      ######### result in a price =0 , continue to next price loop ###########
        if resultqty==0:
            # print('Result in price loop is 0 ,skiped price loop %s to %s' % (priceloopstart,priceloopend))
            continue

        ############ if result in a price loop <= 400 #########  go into page loop set up amount of page loop number needed #############
        if resultqty<=400:

            totalresult = totalresult+resultqty
            totaldownload=totaldownload+resultqty
            if resultqty%20==0:
                pageloop = resultqty // 20
            else:
                pageloop=resultqty//20+1

            ################ page loop, from page 1 to page 20 if exist #################
            for n in rangewithend(1,pageloop):
                Pageloopurl=Targeturl+'&page='+str(n)+'&size=20'
                # print('download %s'%Pageloopurl)
                soup = url_to_soup(Pageloopurl)
                # resultqty=resultqty_getfromsoup(soup)
                downloadinfo(soup,page=n,databank=DataBankName)    ############### if pictures needed , use downloadpictures=True

            # print('Total result: %s total download %s' % (totalresult,totaldownload))
            # DownloadPercentage = (totaldownload / Pricetotal) * 100
            # pricelooptimeused = getUsedtime()
            # needtofinish = EstimatedTime(totaldownload, Pricetotal, pricelooptimeused)
            # print('||Processing....|| %s || %s || in ((%s -> %s)) || Done (%s) in (%s)'
            #       '||%.2f %%||Used Time(%.2f)||Time to finish: %.2f' % (
            #       brandname, priceloopstart, pricefrom, priceto, totaldownload, Pricetotal, DownloadPercentage,
            #       pricelooptimeused, needtofinish))

        ######if >400, extra year loop ,,,,calculate information downloaded in each loop ##############
        if resultqty > 400:
            # # priceloop_percentage= (400/resultqty)*100
            # # totaldownload = totaldownload + 400
            # print('Result in price loop  %s to %s is %s \nStart year loop' % (priceloopstart,priceloopend,resultqty))

            ############ start an extra year loop, if more than 400 , contains also a page loop ##################3
            for year in range(1997,2017,1):
                yearloopstart=year
                Yearloopurl = Targeturl + '&fregfrom=' + str(year) +'&fregto='+str(year)
                soup = url_to_soup(Yearloopurl)
                yearloopqty= resultqty_getfromsoup(soup)

                if yearloopqty == 0:
                    # print('Year loop %s Get %s Results ,skip ' % (year, yearloopqty))
                    continue

                if yearloopqty <= 400:
                    # print('Year loop  %s Get %s Results ' % (year, yearloopqty))
                    pricelooptotalqty = pricelooptotalqty + yearloopqty
                    totalresult=totalresult+yearloopqty
                    totaldownload=totaldownload+yearloopqty
                    if yearloopqty % 20 == 0:
                        pageloop = yearloopqty // 20
                    else:
                        pageloop = yearloopqty // 20 + 1

                    for n in rangewithend(1, pageloop):
                        Pageloopurl = Targeturl + '&page=' + str(n) + '&size=20'
                        # print('Download page %s: %s'% (n,Pageloopurl))
                        soup = url_to_soup(Pageloopurl)
                        # resultqty=resultqty_getfromsoup(soup)
                        downloadinfo(soup, page=n,databank=DataBankName)  ############### if pictures needed , use downloadpictures=True
                    # print('Total result : %s total download %s' % (totalresult, totaldownload))
                    continue

                if yearloopqty>400:
                    # print('Year loop  %s Get %s Results ' % (year, yearloopqty))
                    # print('Result >400, only 400 results will be downloaded')
                    pricelooptotalqty= pricelooptotalqty+400
                    totalresult=totalresult+yearloopqty
                    totaldownload=totaldownload+400
                    pageloop=20
                    for n in rangewithend(1, pageloop):
                        Pageloopurl = Targeturl + '&page=' + str(n) + '&size=20'
                        # print(Pageloopurl)
                        soup = url_to_soup(Pageloopurl)
                        # resultqty=resultqty_getfromsoup(soup)
                        downloadinfo(soup, page=n,databank=DataBankName)  ############### if pictures needed , use downloadpictures=True
                    continue

            # DownloadPercentage = (totaldownload / Pricetotal) * 100
            # pricelooptimeused = getUsedtime()
            # needtofinish = EstimatedTime(totaldownload, Pricetotal, pricelooptimeused)
            # print('||Processing....|| %s || %s || in ((%s -> %s)) || Done (%s) in (%s)'
            #       '||%.2f %%||Used Time(%.2f)||Time to finish: %.2f' % (
            #       brandname, priceloopstart, pricefrom, priceto, totaldownload, Pricetotal, DownloadPercentage,
            #       pricelooptimeused, needtofinish))

        ################ Print process bar #################
        DownloadPercentage=(totaldownload/Pricetotal)*100
        pricelooptimeused=getUsedtime()
        needtofinish=EstimatedTime(totaldownload,Pricetotal,pricelooptimeused)

        print('||Processing....|| %s || %s || in ((%s -> %s)) || Done (%s) in (%s)'
              '||%.2f %%||Used Time(%.2f)||Now %s ||Time to finish (%.2f)'%(brandname,priceloopstart,pricefrom,priceto,totaldownload,Pricetotal,DownloadPercentage,pricelooptimeused,gettimenow(),needtofinish))

    ################ ending print infomation ###########################
    totalpercentage=(totaldownload/totalresult)*100
    used=getUsedtime()
    print("_______________________________________________________________________________________")
    print('||Download finished||%s ||Time: %s||(%s) in (%s)(From 1997) downloaded||%.2f'%(brand,used,totaldownload,totalresult,totalpercentage))
    print('_______________________________________________________________________________________')


def brandqtycollect():
    codelist = []
    namelist = []
    codedict = {}
    a = open('BrandCode.txt', 'r', encoding='utf-8')
    for line in a:
        try:
            b = re.match(r'(\s+)(.+?)(\")(\d+)(.+)(\")(.+?)(\")', line).group(4)
            c = re.match(r'(\s+)(.+?)(\")(\d+)(.+)(\")(.+?)(\")', line).group(7)
            codelist.append(b)
            namelist.append(c)
        except:
            continue
    Name_and_Code = dict(zip(namelist, codelist))

    brandlistdatabank = 'BrandPriceDistribution_Germay.csv'
    # brandlistdatabank = 'BrandTotal.csv'

    for brand in Name_and_Code:

        row=[brand]
        brandcode = Name_and_Code.get(brand)
        url = Urlfilter(url_main, brandcode)
        soup = url_to_soup(url)
        brandtotal = resultqty_getfromsoup(soup)



        # get price interval
        if  brandtotal<=20000:
            print('skiped<20000 %s'%brand)
            continue
        if brandtotal >= 40000:
            print('skiped >40000%s' %brand)
            continue

        for price in range(0,100000,2000):
            priceend=price+1999
            brandcode=Name_and_Code.get(brand)
            url=Urlfilter(url_main,brandcode,priceloopstart=price,priceloopend=priceend)
            print(url)
            soup=url_to_soup(url)
            brandtotal=resultqty_getfromsoup(soup)
            print(brand,price,brandtotal)
            row.append(brandtotal)

        # #only total
        # brandcode = Name_and_Code.get(brand)
        # url = Urlfilter(url_main, brandcode)
        # print(url)
        # soup = url_to_soup(url)
        # brandtotal = resultqty_getfromsoup(soup)
        # print(brand, brandtotal)
        # row.append(brandtotal)


        with open(brandlistdatabank, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        f.close()

def main():
    pricefrom=18700
    priceto=20000
    priceinterval=20
    for brand in Brandstocollect:
        # print('Starting new process to collect %s'% brand)
        SubProcess=Process(target=CollectMain,args=(brand,pricefrom,priceto,priceinterval))
        print('SubProcess for %s started' % brand)
        SubProcess.start()

# Brandstocollect=['Audi','BMW','Citroen','Fiat','Ford','Hyundai','Mazda','Mercedes-Benz','Opel','Peugeot','Renault','SEAT','Skoda','Suzuki','Toyota','Volkswagen']
# Brandstocollect=['Citroen','Fiat','Ford','Hyundai','Mazda','Peugeot']
# Brandstocollect = ['Suzuki']
Brandstocollect=['BMW']


if __name__ == '__main__':
    # branddict=brandqtycollect()
    main()


