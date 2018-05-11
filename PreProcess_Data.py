#20180501 clean all data out of rational range

import csv
import re
from os import listdir
from os.path import isfile, join

PriceLimitLow=500
PriceLimitHigh=100000
MilageLimitLow=0
MilageLimitHigh=500000
UsedMonthLimitLow=0
UsedMonthLimitHigh=360
#germany Zip Code 5 digital
ZipLimitLength=5

PowerLimitLow=0
PowerlimitHigh=1000

LineCountOK=0
LineCountNOKString=0
LineCountNOKNumber=0
WriteCount=0

FolderPath= 'D:\\Python\\02_CarData\\ProcesseDone'
FileName='All_Detail_170725.csv'
FileNameOut='All_Detail_20180501.csv'

FileDir = join(FolderPath, FileName)
FileDirOut=join(FolderPath,FileNameOut)

## open file
# read each line of Input

with open(FileDirOut, 'w',newline='',encoding='utf-8') as output:
    Input = open(FileDir, 'r', newline='',encoding='utf-8')
    linereader = csv.reader(Input)
    linewriter = csv.writer(output)

    for row in linereader:

     #   if WriteCount==1000:
     #       break
        print('OK： ',LineCountOK,'NOK: ',LineCountNOKString,'NOK Number',LineCountNOKNumber)
        RowOK=0
        #print(row)
        try:
            Price=int(row[2])
            Title=row[3][0:25]
            Milage=int(row[4])
            UsedMonth=int(row[5])
            Power1=int(row[6])
            Power2=int(row[7])
            Zip=row[11]
        except:
            LineCountNOKString+=1
            continue

        if Price<PriceLimitHigh and Price>PriceLimitLow \
            and Milage<MilageLimitHigh and Milage>MilageLimitLow \
                and UsedMonth<UsedMonthLimitHigh and UsedMonth>UsedMonthLimitLow \
                    and Power1<PowerlimitHigh and Power2>PowerLimitLow and Power1<PowerlimitHigh and Power2>PowerLimitLow:

                        if row[11]=='DE':
                            if len(Zip)==ZipLimitLength:
                                RowOK=1
                            else:
                                RowOK=0
                        else: RowOK=1
        else:
            print(row)
            LineCountNOKNumber+=1
            continue

        LineCountOK+=1
        if RowOK==1:
            linewriter.writerow(row)
            WriteCount+=1
            print('write',WriteCount)

