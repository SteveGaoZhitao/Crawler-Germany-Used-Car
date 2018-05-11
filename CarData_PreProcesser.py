import csv
import re
from os import listdir
from os.path import isfile, join
import time
Data_Today=time.strftime("%m%d")
##############################################
# PreProcesser, transform the data from collector into usable data, only contains main info
##############################################

IsCombineFile=True
FolderPath= 'D:\Python\CarData\Collected\RowData'
# FolderPath='D:\Python\CarData\PreProcessed2'
FileNameList= [f for f in listdir(FolderPath) if isfile(join(FolderPath,f))]
skipedfailure=0
failuredict = {}
totaldict={}


for FileName in FileNameList:
    writercounter = 0
    skiped=0
    FileDir=join(FolderPath,FileName)
    print('Open File to write:',FileName)

    Brand = re.match(r'(.+?)(_)(.+)', str(FileName)).group(1)
    # output file seperate for each brand

    # single output file
    if IsCombineFile==True:
        OutputFile='D:\Python\CarData'+'\\'+'Preprocessed All'+Data_Today+'.csv'
    else:
        Brand = re.match(r'(.+?)(_)(.+)', str(FileName)).group(1)
        OutputFile = 'D:\Python\CarData\PreProcessed3' + '\\' + str(Brand + '.csv')

    failuredict.update({str(FileName):0})
    totaldict.update({str(FileName):0})


    with open(OutputFile,'a',encoding='utf-8',newline='') as output:
        linewriter=csv.writer(output)
        rowdata=open(FileDir,'r',newline='',encoding='ISO-8859-1')
        # print('Open File to read %s' % rowdata)
        linereader = csv.reader(rowdata)
        readercounter=0

        for row in linereader:
            totaldict[str(FileName)] += 1
            try:

                    # print(rcounter)
                    readercounter=readercounter+1
                    if len(row)!=12:
                        skiped=skiped+1
                        print('length not 12 skip')

                        continue
                    te=row[10][1:4]
                    if row[10][0:4]!='http':
                        print('first column not http')
                        skiped=skiped+1
                        continue


                    title=row[3]
                    mode=re.match(r'(\S+)(\s)(\S+)(.+)',str(title)).group(3)
                    price=row[4]
                    milage2=row[5]
                    milage3=re.sub('\.','',milage2)
                    milage=re.match(r'\d+',milage3).group()
                    freg=row[6]
                    fregm=freg[:2]
                    fregy=freg[-4:]
                    nowm=6
                    nowy=2017
                    usedm=(nowy-int(fregy))*12+nowm-int(fregm)
                    kw2=row[7]
                    ps2=row[8]
                    kw=re.match(r'\d+',str(kw2)).group()
                    ps3=re.sub(' ','',str(ps2))
                    ps=re.match(r'(\d+)',str(ps3)).group()
                    fuellist=['Benzin','Diesel']
                    for f in fuellist:
                        if str(f) in str(row[9]):
                            fuel=f
                            break
                        else:
                            fuel='Others'
                    dealer2=row[11][0]
                    if dealer2=='H':
                        dealer='Dealer'
                    else:
                        dealer='Private'

                    country = re.match(r'(.+?)(,)(.+?)(-)(\w+)', row[11]).group(3)
                    zipcode = re.match(r'(.+?)(,)(.+?)(-)(\w+)', row[11]).group(5)


                    towrite=[Brand,mode,price,title,milage,usedm,ps,kw,fuel,dealer,country,zipcode]

                    # print(towrite)
                    linewriter.writerows([towrite])
                    writercounter=writercounter+1
            except:
                    # print('Skiped because of failure in',FileName, skipedfailure)
                    skipedfailure=skipedfailure+1
                    failuredict[str(FileName)]+=1
                    # print(failuredict)
                    continue
        rowdata.close()
        print('In %s Read: %s  in %s Write: %s  Failure %.2f ' %(FileName,readercounter,OutputFile,writercounter,1-writercounter/readercounter))


print('Total skiped because of data: %s\n Because of failure %s' %(skiped,skipedfailure))
