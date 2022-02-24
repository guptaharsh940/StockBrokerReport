from py_compile import _get_default_invalidation_mode
from sys import api_version
# import nsepy
# import pynse
# import os
# import sys
import requests
import time
import subprocess as sub
from subprocess import call
import threading

# data = None
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
        nodepro = sub.Popen('node "stock-market-india"', shell=True)
        # nodepro = call('node "stock-market-india"', shell=True)
    except:
        print("Server Timed Out")    
    
    # sys.exit()

def get_stock_symbol(clist):
    '''Takes Company Name List and add corresponding symbol to the list'''
    # global data
    data = None
    global companysymbol
    global timeout
    timeout = 5
    for name in clist:
    # print("I am here")
        print(name)
        api_url = f'http://localhost:3000/nse/search_stocks?keyword={name}'
        try:
            data = requests.get(api_url).json()
            timeout = timeout+2
        except:
            print("This didn't work")
            companysymbol.append('N/A')
            run_server()
            continue
            # pass
        if data == None:
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
        data = None
    
    print("This has ended")
    timeout = 1

def get_stock_quote(symbol):
    '''Gives the ltp and last update time using node server
    Currently using nsepy library in the main file itself for this task'''
    global nodepro
    run_server()
    # Adding all the symbols with "," seperation
    a = ""
    for sym in symbol:
        
        if a =="":
            a = a + sym
        else:
            a = a + "," + sym
    print(a)
    url = f'http://localhost:3000/nse/get_multiple_quote_info?companyNames={a}'   
    quotes = requests.get(url).json()
    stock_ltp = []
    stock_lastupdate = []
    for x in quotes:
        stock_ltp.append(x['data']['lastPrice'])
        stock_lastupdate.append(x['lastUpdateTime'])
    nodepro.kill()
    return stock_ltp, stock_lastupdate
    
def timer(timeout,data):
    timeout_start = time.time()
    while True:
        if time.time() > timeout_start + timeout and data == None:    
            print("Timed Out as Stock not found")
            nodepro.kill()
            break

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

def marketstatus():
    global nodepro
    run_server()
    url = 'http://localhost:3000/get_market_status'
    status = (requests.get(url).json())["status"]
    nodepro.kill()
    return status