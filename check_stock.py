import requests
from bs4 import BeautifulSoup as bs
import time

GPUTypes_url = "https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%205500%20XT%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%205600%20XT%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%20570%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%205700%20XT%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%20580%20GTS%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206600%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206600%20XT%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206600M%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206700%20XT%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206800%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206800%20XT%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206900%20XT%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GT%201030%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GT%20710%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GT%20730%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GTX%201060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GTX%201650%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GTX%201650%20SUPER%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GTX%201660%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GTX%201660%20SUPER%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20GTX%201660%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090&st=graphics+card"
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }

def GPUTypesDictonary():

    GpuDict = {}
    GpuTypes = GPUTypes_url.split("qp=")
    GpuTypes.pop(0)
    GpuTypes = "".join(GpuTypes)
    GpuTypes = GpuTypes.rsplit("&st")
    GpuTypes.pop(-1)
    GpuTypes = "".join(GpuTypes)
    GpuTypes = GpuTypes.split("%5E")

    for GPUType in GpuTypes:
        x = GPUType.rfind("%20",0, GPUType.rfind("%20"))
        x = GPUType[x:].replace("%20", "")
        GpuDict[x] = GPUType

    return(GpuDict)

def search(keywords, min_price = "0", max_price = "Up", GpuType = None):
    
    url = "https://www.bestbuy.com/site/searchpage.jsp?"
    GpuDict = GPUTypesDictonary()

    if min_price or max_price:
        url += "qp="

    if min_price or max_price:
        url += f"currentprice_facet%3DPrice~{min_price}%20to%20{max_price}%5E"

    for index, Gpu in enumerate(GpuType):
        if Gpu in GpuDict:
            url += GpuDict[Gpu]
            if index + 1 != len(GpuType):
                url+="%5E"
    
    url += "&st="+keywords.replace(" ", "+")
    return(getPages(url))

def getPages(url):

    pages = []

    pages.append(url)
    r = requests.get(url, headers=headers)
    soup = bs(r.text, features="html.parser")
    count = soup.find_all("li", {"class": "page-item"})

    for x in count:
        url = x.find('a', href=True)
        if url:
            pages.append("https://www.bestbuy.com"+url['href'])

    return(getItems(pages))

def getItems(pages):

    URLS = []

    for url in pages:
        r = requests.get(url, headers=headers)
        soup = bs(r.text, features="html.parser")
        urldiv = soup.find_all("div", {"class": "sku-title"})
        for x in urldiv:
            url = x.find('a', href=True)
            URLS.append("https://www.bestbuy.com"+url['href'])

    return(URLS)

def fetch_url():
    x = 0
    URLS = search(keywords="Graphics card", min_price="110", max_price="650", GpuType=["RTX3060", "3060Ti","RTX3070"])
    while True:
        for url in URLS:
            try:
                r = requests.get(url, headers=headers)
                soup = bs(r.text, features="html.parser")
                sold_out = soup.find(text="Sold Out")
                if sold_out:
                    x += 1
                    print(sold_out+ " " + str(r) + " " + "(" + str(x) + ")" + " " + url)
                    time.sleep(.25)
                else:
                    return url
            except Exception as e:
                print(e)
            if url == URLS[-1]:
                print("HERE")
                URLS = search(keywords="Graphics card", min_price="110", max_price="650", GpuType=["RTX3060", "3060Ti","RTX3070"])