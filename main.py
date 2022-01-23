import time
import pandas as pd
import math
from nsepy import get_quote
import stockdata
data = pd.read_csv('data.csv')
print(data)
sno = data['S No.'].max()
if math.isnan(sno):
    sno = 0
    data = data.iloc[0:0]

# import callretriever
# callretriever
def getReco(sno):
    '''Gets the Recommendation from RecoWebsiteScrape and then checks for Redundancy in the database and if
    new data is found it adds to the database. It recieves the max sno of the database as argument.
    '''
    global data
    global z
    sno_to_get = set()
    # print(data)
    import RecoWebsiteScrape
    reco = list(RecoWebsiteScrape.titles)
    for item in reco:
        if reco[-1] == item and (item in data.values):
            addSymboltoOld()
            z = False
            continue

        elif item in data.values:
            continue
        '''Initiating a temporary dictionary to add the data to'''
        keys = ['S No.','Reco Full','Reco Date','Reco Time','Reco Provider','Reco For','Target Price','Action',]
        RecoDict = dict(zip(keys, [None]*len(keys)))
        
        RecoDict['S No.']=(sno + 1)
        sno_to_get.add(sno+1)
        RecoDict['Reco Full']=(item)
        RecoDict['Reco Date']=(time.strftime("%d/%m/%Y",time.localtime()))
        RecoDict['Reco Time']=(time.strftime("%H:%M:%S",time.localtime()))
        s = item.split()
        RecoDict['Action']=(s[0])
        recofor = ''
        for x in range (1,s.index('target')):
            if len(recofor)==0:
                recofor += s[x]
            else:
                recofor =recofor + " " + s[x]
        RecoDict['Reco For']=(recofor.replace(",",""))
        RecoDict['Target Price']=(int(s[s.index('Rs')+1].replace(':',"")))
        recoprovider = ''
        for y in range (s.index('Rs')+2,len(s)):
            if len(recoprovider)==0:
                 recoprovider+= s[y]
            else:
                recoprovider+= " " + s[y]
        RecoDict['Reco Provider']=(recoprovider)
        sno = sno +1
        data = data.append(RecoDict,ignore_index=True)
        print(RecoDict)
        # print(data)
    
    return sno_to_get
    

def getSymbol(sno):
    '''Gets the company name from Serial No.'''
    global data
    companyname = []
    for i in list(sno):
        a = list(data['S No.'].loc[lambda x:x==float(i)].index)
        for y in a:
            companyname.append(data.iloc[y]['Reco For'])
    values = stockdata.start(companyname)
    companysym = {list(sno)[i]: values[i] for i in range(len(list(sno)))}
    print(companysym)
    return companysym

        # print(companyname)
def convert_to_float(str):
    '''Converts pricing to a float representation'''
    floattext = 0.0 
    if "," in str:
        str = str.replace(",","")
        floattext = float(str)
    else:
        floattext = float(str)
    return floattext

def addSymboltoOld():
    '''Checks for the old Recos to get the symbol and gets the S No. of them and gives that to getSymbol()
    function and further adds them to the database'''
    global data
    sno = set()
    a = 0
    checkfornan = data['Symbol'].isnull()
    print(checkfornan)
    for x in checkfornan:
        a+=1
        if x:
            sno.add(a)
        else:
            continue
    print(sno)
    companyname = []
    for i in list(sno):
        a = list(data['S No.'].loc[lambda x:x==float(i)].index)
        for y in a:
            companyname.append(data.iloc[y]['Reco For'])
    values = stockdata.start(companyname)
    compsym = {list(sno)[i]: values[i] for i in range(len(list(sno)))}
    for i in compsym.keys():
        a = data['S No.'].loc[lambda x:x==float(i)].index

        # data.insert(a,'Symbol', compsym[i])
        data.Symbol[a] = compsym[i]
        # data.loc[a,6] = compsym[i]
            
def firsttrade(sno):
    global data
    symbol = []
    for i in list(sno):
        a = list(data['S No.'].loc[lambda x:x==float(i)].index)
        for y in a:
            if data.iloc[y]['Symbol'] == 'N/A':
                continue
            elif isinstance(data.iloc[y]['Symbol'],str):
                sym = data.iloc[y]['Symbol']
                quote = get_quote(sym)
                ltp = convert_to_float(quote['data'][0]['lastPrice'])
                date = quote['lastUpdateTime'].split()
                if data.iloc[y]['Action'] == 'Buy' or data.iloc[y]['Action'] == 'Add' or data.iloc[y]['Action'] == 'Hold':
                    data.loc[y,'Buy Price'] = ltp
                    data.loc[y,'Buy Date'] = date[0]
                    data.loc[y,'Buy Time'] = date[1]
                    data.loc[y,'Quantity'] = 1
                elif data.iloc[y]['Action'] == 'Sell' or data.iloc[y]['Action'] == 'Reduce':
                    data.loc[y,'Sell Price'] = ltp
                    data.loc[y,'Sell Date'] = date[0]
                    data.loc[y,'Sell Time'] = date[1]
                    data.loc[y,'Quantity'] = -1

                print(f'{i} - {sym} - {str(ltp)} - {date[0]} - {date[1]}')
            continue
            
<<<<<<< HEAD
    print(symbol)    
    # a = stockdata.get_stock_quote(symbol)
    print(a)

def new_reco_procedure(sno):
    global data
    sno_to_get = getReco(sno)
    compsym = getSymbol(sno_to_get)
    for i in compsym.keys():
        a = data['S No.'].loc[lambda x:x==float(i)].index

        # data.insert(a,'Symbol', compsym[i])
        data.Symbol[a] = compsym[i]
    try:
        firsttrade(sno_to_get)
    except:
        pass
    
    data.to_csv('data.csv',index=False)

# z = True  
# while True:
#     while z== True:
#         new_reco_procedure(sno)
#     while z==False:
#         import RecoWebsiteScrape
#         reco = list(RecoWebsiteScrape.titles)
#         for item in reco:
#             if stockdata.marketstatus() == 'open':
#                 print('Market Open')
#             elif (item in data.values):
#                 print('Sleeping')
#                 time.sleep(5)
#                 continue
#             else:
#                 z = True

new_reco_procedure(sno)
# firsttrade({1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23})
=======
while True:
    getReco(sno)
# getSymbol({1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23})
>>>>>>> b5b7cceb96e540bfb96ca9269948857bead17284
# t = time.strftime("%H:%M:%S",time.localtime())
# print(t)