from datetime import datetime
from datetime import timedelta
from datetime import date
import sys

import os
import logging
import requests
from tqdm import tqdm



def days_between(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    return (end - start).days


def createPath(date):
    data_dir = './downloads/' + str(date)
    if not os.path.exists(path=data_dir):
        os.mkdir(path=data_dir, mode=0o777)
    return data_dir


def getFileName(file,date):
    
    if file == 'WEBPXTICK_DT.zip':
        filename = 'WEBPXTICK_DT-' + str(date) + '.zip'
    elif file == 'TC.txt':
        filename = 'TC_' + str(date) + '.txt'
    else:
        filename = file
    
    return filename
    




def downloadTracker(dataDownloaded, size, filename):
    completed = round(float(dataDownloaded) / size * 100, 2)
    sys.stdout.write('\r')
    sys.stdout.write(filename + " Downloaded {}%".format(completed, filename))

    if dataDownloaded >= size:
        sys.stdout.write('\n')



class WebCrawler:
    def __init__(self):
        self.dateMap= {'date':'20200101' , 'key':4430}
        self.filesToDownload=['TC.txt', 'TickData_structure.dat', 'TC_structure.dat', 'WEBPXTICK_DT.zip']
        self.failedDownloadFiles=self.getFailedDownloadFiles()
        
    def getDateMap(self):
        return self.dateMap
    
    def setDateMap(self,newDateMap):
        self.dateMap = newDateMap
        
    def getDateKey(self,date):
        startDate,startKey=self.getDateMap().values()
        currentKey= startKey + days_between(startDate,date)
        return currentKey
    
    def getDateKeyTable(self):
        return self.dateKey_table
    
    def getFailedDownloadFiles(self):
            file = open('recovery.txt', 'r+').read().split(',')[:-1]
            return sorted(file)
    
    def modifyFailedDownloadFiles(self,date,delete=False):
        file = open('recovery.txt', 'r+')
        data=file.read().split(',')[:-1]
        
        if(delete and date in data):
            file.seek(0)  
            file.truncate()
            data.remove(date)
            for value in data:
                file.write(str(value) + ',')
        elif(delete and date not in data):
            logging.warning('{} date does not exist'.format(str(date)))
            
        
        if(date not in data and not delete):
            file.write(str(date) + ',')
                  
        file.close()
        self.failedDownloadFiles=self.getFailedDownloadFiles()

    
    
    def getDateRange(self,startDate,endDate):
        startDate=datetime.strptime(startDate, "%Y%m%d")
        endDate=datetime.strptime(endDate, "%Y%m%d")
        dayCount = (endDate - startDate).days + 1
        dateTable=[]
        for date in (startDate + timedelta(days=n) for n in range(dayCount)):
            strDate=datetime.strftime(date,'%Y%m%d')
            dateTable.append(strDate)
        return dateTable
            
    def downloadData(self,date, key):
        
        if(days_between(date,datetime.strftime(datetime.today(),'%Y%m%d'))  < 1):
            raise Exception('Download cancelled - data for {} is unavailable'.format(date))
    
        
        logging.info('Downloading {} files'.format(date))
        filePath=createPath(date)
        
        for file in self.filesToDownload:
            try:
                url = 'https://links.sgx.com/1.0.0/derivatives-historical/' + str(key) + '/' + file

                requestObject = requests.get(url, stream=True)
                size = int(requestObject.headers['content-length'])
                chunk_size = 65536
                dataDownloaded = 0
                
                filename=getFileName(file,date)
            
            
                f = open(filePath + '/' + filename, "wb")

                for dataBlock in requestObject.iter_content(chunk_size=chunk_size):
                    if dataBlock:
                        f.write(dataBlock)
                        dataDownloaded += len(dataBlock)
                        downloadTracker(dataDownloaded, size, filename)
                f.close()
                logging.info('Downloading Completed')
            except Exception as e:
                logging.warning('{} download failed '.format(str(date)) + str(e))
                self.modifyFailedDownloadFiles(date,delete=False)
                
    def download(self,date,startToEnd):
        
        if(type(date)==str):
                key = self.getDateKey(date)
                self.downloadData(date,key)
        else:
            if(startToEnd == 'True'):
                dateList=self.getDateRange(date[0],date[1])
                for value in dateList:
                    key = self.getDateKey(value)
                    self.downloadData(value,key)

            else:
                for value in date:
                    key = self.getDateKey(value)
                    self.downloadData(value,key)
