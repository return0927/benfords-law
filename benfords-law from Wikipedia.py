import re, requests, bs4, codecs, threading
from tkinter import *

end = 10

#urls = ["https://ko.wikipedia.org/wiki/%EC%83%81%ED%88%AC%EB%A9%94_%ED%94%84%EB%A6%B0%EC%8B%9C%ED%8E%98_%EB%8F%84%EB%B8%8C%EB%9D%BC"]
urls = []
for n in range(500):
    urls += ["https://ko.wikipedia.org/wiki/%ED%8A%B9%EC%88%98:%EC%9E%84%EC%9D%98%EB%AC%B8%EC%84%9C"]

global soupDict
soupDict = {}

def getSoup(url):
    soupDict[url] = bs4.BeautifulSoup(requests.get(url).text, 'html.parser')

for n in range(len(urls)):
    threading.Thread(target=getSoup, args=(urls[n],)).start()


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

def monitor():
    global root, data, titleText
    root = Tk()
    titleText = Label(root, text="Lastest Result")
    titleText.pack(anchor="w")

    data = {}
    for n in range(1,end+1):
        data[n] = 0
    
    result = "\n".join([ "  %2d | %6s"%(x, "{:,}".format(data[x])) for x in data.keys()])
    
    titlePlaceholder = Label(root, text=result)
    titlePlaceholder.pack(anchor="w")

    while threading.active_count() > 3:
        pass

    for url in urls:
        soup = soupDict[url]
        title = soup.find("title").text.replace(" - 위키백과, 우리 모두의 백과사전","")
        titleText.config(text="Lastest Result | %s"%title)
        texts = soup.findAll(text=True)

        a = "".join(list(filter(visible, texts)))

                
        for n in range(1,end+1):
            data[n] += a.count(str(n))

        total = sum([data[n] for n in range(1,end+1)])

        result = "\n".join([ "  %2d | %6s | %.2f%%"%(x, "{:,}".format(data[x]), data[x]/total*100 if data[x]!=0 else 0) for x in data.keys()])
        titlePlaceholder.config(text=result)

        root.update()


monitor()
