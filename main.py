import time
import pandas as pd
import math
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
    sno_to_get = set()
    # print(data)
    import RecoWebsiteScrape
    reco = list(RecoWebsiteScrape.titles)
    for item in reco:
        if reco[-1] == item and (item in data.values):
            addSymboltoOld()
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
        print(data)
    compsym = getSymbol(sno_to_get)
    for i in compsym.keys():
        a = data['S No.'].loc[lambda x:x==float(i)].index

        # data.insert(a,'Symbol', compsym[i])
        data.Symbol[a] = compsym[i]

    
    data.to_csv('data.csv',index=False)

def getSymbol(sno):
    global data
    '''Gets the company name from Serial No.'''
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

def addSymboltoOld():
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


            

            
# while True:
getReco(sno)
# getSymbol({1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23})
# t = time.strftime("%H:%M:%S",time.localtime())
# print(t)