import schedule
import sys
import time
import logging
from datetime import  datetime
from datetime import timedelta
from WebCrawler import WebCrawler
import configparser as cp



class configurations:
    def __init__(self):
        configParser = cp.ConfigParser()
        configParser.read('config.cfg')
        self.logging_level=int(configParser.get('Head','logging_level'))
        self.retry_Automated_downloads=configParser.get('Head','RETRY_AUTOMATED_DOWNLOADS')
        self.number_retry=int(configParser.get('Head','NUMBER_RETRY'))
        self.automated_days_download=int(configParser.get('Head','AUTOMATED_DAYS_DOWNLOAD'))
        self.automated_scheduled_time=configParser.get('Head','AUTOMATED_SCHEDULED_TIME')
        
    
    def printConfigurations(self):
        print('________Configurations________')
        print('LOGGING LEVEL: {}'.format(self.logging_level))
        print('AUTO SCHEDULE TIME: {}'.format(self.automated_scheduled_time))
        print('LOWER LIMIT FOR AUTOMATED DAYS: {}'.format(self.automated_days_download))
        print('RETRY_AUTOMATED_DOWNLOADS: {}'.format(self.retry_Automated_downloads))
        print('NUMBER_RETRY: {}'.format(self.number_retry))

config=configurations()
sgxCrawler=WebCrawler()

def AutoMode():
    print('Fetching Data Automatically')
    schedule.every().day.at(config.automated_scheduled_time).do(AutoUpdate)
    while True:
        try:
            schedule.run_pending()
            sys.stdout.write('\r')
            sys.stdout.write('automation standby .')
            time.sleep(1)
            sys.stdout.write('\r')
            sys.stdout.write('automation standby ..')
            time.sleep(1)
            sys.stdout.write('\r')
            sys.stdout.write('automation standby ...')
            time.sleep(1)
            sys.stdout.write('\r')
            time.sleep(1)
        except Exception as e:
            logging.error(str(e) + 'automation failed!')


def AutoUpdate():
    day_before=max(2,config.automated_days_download)
    date=datetime.strftime(datetime.today() - timedelta(day_before),'%Y%m%d')
    sgxCrawler.download(date,False)

    #redownload

    if(config.retry_Automated_downloads =='True'):
        retryDownload()



def retryDownload():
    
    failedDownloads=sgxCrawler.getFailedDownloadFiles()
    if(config.number_retry < len(failedDownloads)):
        failedDownloads = failedDownloads[:config.number_retry ]
    logging.info('Retrying the follwoign Downloads {}'.format(failedDownloads))
    sgxCrawler.download(failedDownloads,False)
    for download in failedDownloads:
        sgxCrawler.modifyFailedDownloadFiles(download,delete=True)


def showHelp():
    file = open('help.txt', 'r+')
    data=file.read().split(',')
    print('________Help Menu________')
    for string in data:
        print(string)

def parseMultipleDates():
    file = open('download.txt', 'r+')
    data=file.read().split(',')
    selector = data.pop(0)
    return selector,data


