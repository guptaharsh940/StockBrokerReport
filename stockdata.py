from py_compile import _get_default_invalidation_mode
from sys import api_version
import nsepy
import pynse
import os
import sys
import requests
import time
import subprocess as sub
import threading

data = None
status = True
timeout = 5
def run_server():
    global status
    global timeout
    print("This has started")
    try:
        sub.run('node "D:\Files\Code\Stock Market\stock-market-india"',timeout=timeout)
    except:
        print("Server Timed Out")    
    # sys.exit()

def get_stock_symbol(name):
    global data
    print("I am here")
    api_url = f'http://localhost:3000/nse/search_stocks?keyword={name}'
    try:
        data = requests.get(api_url).json()
    except:
        print("This didn't work")
        run_server()
        pass
    if len(data) == 0:
        print("Not found")
    else:
        for i in range (len(data)):
            print(data[i]['symbol'])
    print("This has ended")
    

def timecheck():
    global timeout
    global status
    print(timeout)
    # timeout = 10
    timeout_start = time.time()
    while True:
        print("This is timing")
        if time.time() > timeout_start + timeout:    
            print("Timed Out")
            break
            
        time.sleep(5)
        


    
    
z= True
while z == True:
    a = input("Enter Name - ")
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
    b = input("Press Enter to continue...")
    if b != "":
        z=False