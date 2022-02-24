import datetime
import threading
import os
import shutil
import pandas as pd
import json

today = datetime.date.today()

text = today.strftime('%d%m%y')
file = None
def getData():
        global file
        global text
        file= requests.get(f'https://archives.nseindia.com/archives/equities/bhavcopy/pr/PR{text}.zip',allow_redirects=True)
thread = threading.Thread(target=getData)
from zipfile import ZipFile
import requests
while True:
    file = None
    thread.start()
    thread.join(timeout=1.5)
    # print("Thread Ended")
    if file == None:
        today = today - datetime.timedelta(1)
        text = today.strftime('%d%m%y')
        thread = threading.Thread(target=getData)
        # print(text)
        continue
    else:
        break
open('test.zip', 'wb').write(file.content)
try:    
    shutil.rmtree('BhavCopy')
except FileNotFoundError:
    pass
os.mkdir('BhavCopy')
with ZipFile('test.zip', 'r') as zip:
    # printing all the contents of the zip file
    # zip.printdir()
    zip.extract(f'Pd{text}.csv',path='BhavCopy')

bhavcopy = pd.read_csv(f'BhavCopy/Pd{text}.csv')
name = pd.DataFrame()
name['SECURITY'] = bhavcopy['SECURITY']
name['SYMBOL'] = bhavcopy['SYMBOL']

    
def get_stocksymbol(comp):
    symbols = []
    for to_sein in comp:
        to_search = to_sein
        file=open('similar_comp.json')
        similar_words = json.load(file)
        file.close()
        allWords = []
        for x in similar_words.values():
            for z in x:
                allWords.append(z)
        # Removes any special characters
        for x in to_search:
            if not x.isalnum() and x != '-':
                to_search = to_search.replace(x," ")
        to_search = to_search.upper()
        
        match = []
        for y,i in enumerate(name['SECURITY'],0):
            temp = 0
            if i in allWords:
                for x in similar_words.values():
                    if i in x:
                        for z in x:
                            if z == to_search:
                                temp = 1
                                break
                            else:
                                continue
            elif len(to_search.split())==1 and (to_search in i.split()):
                temp = 1
            elif len(to_search.split()) > 1:
                for x in to_search.split():
                    if x in i.split() and to_search.split()[0]==x:
                        temp += 1/len(to_search.split())
                        temp += 1
                    elif x in allWords:
                        for z in similar_words.values():
                            if x in z:
                                for word in z:
                                    if word in i.split() and to_search.split()[0]==x:
                                        temp += 1/len(to_search.split())
                                        temp +=1
                                    elif word in i.split():
                                        temp += 1/len(to_search.split())
                    elif x in i.split():
                        temp += 1/len(to_search.split())
                    else:
                        temp -= 1/len(to_search.split())
                # for x in to_search.split():
                #     if x in i:
                #         temp += 1/len(to_search.split())
                #     else:
                #         for z in similar_words.values():
                #             if x in z:
                #                 for word in z:
                #                     if word in i:
                #                         temp += 1/len(to_search.split())
            else:
                temp = 0   
            for x in to_search.split():
                if x in name.iloc[y,1] and to_search.split()[0] == x:
                    temp += 1.5
                elif x in name.iloc[y,1]:
                    temp +=0.5
            match.append(temp)

        name['Match'] = match

        sorted_name = name.sort_values(by = ['Match'], ascending =False)
        if sorted_name.iloc[0,0] == 'Nifty 50' and to_search in name['SYMBOL'].to_list():
            symbols.append(to_search)
        elif sorted_name.iloc[0,0] == 'Nifty 50':
            symbols.append("N/A")
        else:
            symbols.append(sorted_name.iloc[0,1])
       
    return symbols
