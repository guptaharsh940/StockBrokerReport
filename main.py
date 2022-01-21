import time
import pandas as pd
import math
from stockdata import get_stock_symbol
data = pd.read_csv('data.csv')
print(data)
sno = data['S No.'].max()
if math.isnan(sno):
    sno = 0
    data = data.iloc[0:0]

# import callretriever
# callretriever
def getReco(sno):
    global data
    # print(data)
    import RecoWebsiteScrape
    reco = list(RecoWebsiteScrape.titles)
    for item in reco:
        if item in data.values:
            continue
        '''Initiating a temporary dictionary to add the data to'''
        keys = ['S No.','Reco Full','Reco Date','Reco Time','Reco Provider','Reco For','Target Price','Action',]
        RecoDict = dict(zip(keys, [None]*len(keys)))
        
        RecoDict['S No.']=(sno + 1)
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
    
    
    data.to_csv('data.csv',index=False)


            
            

            


getReco(sno)
t = time.strftime("%H:%M:%S",time.localtime())
# print(t)