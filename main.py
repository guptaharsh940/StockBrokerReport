import time

# import callretriever
# callretriever
def getReco():
    import RecoWebsiteScrape
    reco = list(RecoWebsiteScrape.titles)
    for item in reco:
        s = item.split()
        # for i in s:


getReco()
t = time.strftime("%H:%M:%S",time.localtime())
# print(t)