import logging
from WebCrawler import WebCrawler
import controller

sgxCrawler= WebCrawler()
config=controller.configurations()

logging.basicConfig(filename='logOutput.log',
                    level=config.logging_level)

def menuOptions(menu):
    if(menu=='main'):
        print('{} Download SGX Data'.format(1))
        print('{} Get Failed Downloads'.format(2))
        print('{} Initiate Automation Script'.format(3))
        print('{} Show Configurations '.format(4))
        print('{} Help'.format(5))
        print('{} Exit'.format(0))
        


ASK_OPTION='Please Select an option: '

if __name__ == '__main__':

    options = 1

    while (options !=-0):
        print('Welcome to SGX Derivatives Downloader \n')

        menuOptions('main')
        try:
            options = int(input(ASK_OPTION))
        except:
            print('invalid input retry')

        if(options == 1):
            options = input('Download Multiple Dates? [Y/N]: ')
            if(options == 'Y' or options == 'y'):
                print('Please add dates to download.txt file \n')
                options = input('Proceed? [Y/N]: ')
                if(options == 'Y' or options == 'y'):
                    selector,dates=controller.parseMultipleDates()
                    sgxCrawler.download(dates,selector)
            elif(options == 'N' or options == 'n'):
                date = input('Please enter the Date: ')
                sgxCrawler.download(date,False)
            else:
                print('invalid input retry')

        elif(options == 2):
            print('Fetching Failed Downloads')
            failedDownloads=sgxCrawler.getFailedDownloadFiles()
            print(failedDownloads)
            options = input('Retry Failed Downloads? [Y/N]: ')
            if(options == 'Y' or options == 'y'):
                controller.retryDownload()
        
        elif(options == 3):
            controller.AutoMode()
            
        
        elif(options == 4):
            config.printConfigurations()
            

        elif (options == 5):
            controller.showHelp()

        elif (options==0):
            break
            

        else:
            print('Invalid Option')


    

