import nsepy
import pynse
import os
import requests
def getData(name):
    try:
        os.system('node "D:\Files\Code\Stock Market\stock-market-india"')
        api_url = f'http://localhost:3000/nse/search_stocks?keyword={name}'
    except:
        return False
        pass

    
    data = requests.get(api_url).json()
    for i in range (len(data)):
        print(data[i]['symbol'])
z= True
while z == True:
    a = input("Enter Name - ")
    getData(a)
    b = input("Press Enter to continue...")
    if b != "":
        z=False