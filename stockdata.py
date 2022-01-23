from py_compile import _get_default_invalidation_mode
from sys import api_version
# import nsepy
# import pynse
# import os
# import sys
import requests
import time
import subprocess as sub
import threading

data = None
companysymbol = []
# status = True
timeout = 5
nodepro = None
def run_server():
    # global status
    global timeout
    global nodepro
    print("This has started")
    try:
        nodepro = sub.Popen('node "stock-market-india"')
    except:
        print("Server Timed Out")    
    
    # sys.exit()

def get_stock_symbol(clist):
    '''Takes Company Name List and add corresponding symbol to the list'''
    global data
    global companysymbol
    global timeout
    timeout = (len(clist) * 2) + 5
    for name in clist:
    # print("I am here")
        api_url = f'http://localhost:3000/nse/search_stocks?keyword={name}'
        try:
            data = requests.get(api_url).json()
        except:
            print("This didn't work")
            companysymbol.append('N/A')
            run_server()
            continue
            # pass
        if len(data) == 0:
            print("Not found")
        else:
            for i in range (len(data)):
                if 'Mutual Fund' in data[i]['name'] or 'ETF' in data[i]['name']:
                    continue
                elif (i==len(data) - 1) and (name.split()[0] not in data[i]['name']):
                    companysymbol.append('N/A')
                    break
                elif name.split()[0] not in data[i]['name']:
                    continue
                else:
                    companysymbol.append(data[i]['symbol'])
                    print(data[i]['symbol'])
                    break
    
    print("This has ended")
    timeout = 1

def timecheck():
    global timeout
    # global status
    global nodepro
    # print(timeout)
    # timeout = 10
    timeout_start = time.time()
    while True:
        # print("This is timing")
        if time.time() > timeout_start + timeout:    
            print("Timed Out")
            nodepro.kill()
            break
            
        time.sleep(2)
        
def start(a):
    global companysymbol
    if len(a) == 0:
        return False
    else:
    # if __name__ == '__main__':
        runserver = threading.Thread(target=run_server)
        timemanage = threading.Thread(target=timecheck)
        datacollector = threading.Thread(target=get_stock_symbol,args=(a,))
        # get_data = threading.Thread(target=getData())
        runserver.start()
        timemanage.start()
        datacollector.start()
        # get_data.start()
        runserver.join()
        timemanage.join()
        datacollector.join()
        # get_data.join()
        return companysymbol