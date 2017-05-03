from bs4 import BeautifulSoup
import requests
import time
import unicodedata as ud

def getPage(link, para = None):
    time.sleep(0.1)
    
    if para:
        page = requests.get(link, params = para)
    else:
        page = requests.get(link)
    #print("Getting data from link " + page.url)
    
    page.encoding = "utf-8"
    return page.text
    
def extractPageNumber(page):
    soup = BeautifulSoup(page, "html.parser")
    a = soup.find("a", "pagebutton")
    s = a["href"]
    e = s.find("page=") + 5
    res = 0
    for i in s[e:]:
        if i in "0123456789":
           res = res * 10 + int(i)
        else:
            break
    return res
    
def getListPage():
    link = "http://www.yanglaocn.com/yanglaoyuan/yly/"
    rgSelect = ["010", "022", "0311"]
    para = {"RgSelect":0, "BNSelect":1, "BTSelect":2, "PRSelect":1, "NaSelect":1, "page":1}
    
    data = []
    
    for rg in rgSelect:
        #set region
        para["RgSelect"] = rg
        para["page"] = 1
        
        #get first page text
        page = getPage(link, para)
        
        #get total page number
        pageNumber = extractPageNumber(page)
        
        #get other page text
        for i in range(1, pageNumber + 1):
            para["page"] = i
            data.append(getPage(link, para))
            
    return data
    
def getTargetLink(page):
    soup = BeautifulSoup(page, "html.parser")
    res = []
    
    for a in soup.find_all("a", "ameth43"):
        res.append(a["href"])
        
    return list(set(res))
        
def getData(page):
    soup = BeautifulSoup(page, "html.parser")
    res = {}
    
    t = soup.find("div", id = "BasicInformation")
    title = t.find("div", "leftcontexttitle")
    res[title.span.text] = title.label.text
    
    for d in t.find_all("div", "leftcontexttitleT"):
        key = d.span.extract().text
        res[key] = d.text
        
    t = soup.find("div", id = "ContactUs")
    for d in t.find_all("div", "leftcontexttitle"):
        key = d.span.extract().text
        res[key] = d.text
        
    return res
        
if __name__ == "__main__":
    print("Getting List Page")
    data = getListPage()
    print("{0} pages got.".format(len(data)))
    
    print("Extract target page link")
    link = []
    for d in data:
        link += getTargetLink(d)
    print("{0} links got.".format(len(link)))
        
    print("Downloading.. 0%", end = "\r")
    data = []
    count = 0
    length = len(link)
    for l in link:
        count += 1
        
        data.append(getData(getPage(l)))
        
        if count % 10 == 0:
            print("Downloading.. %.2f%%" %(count * 100/length), end = "\r")
    print("Downloading.. finished!")   
    print("Writing..")
    file = open(r"e:\data.csv", "w")
    file.write(",".join(data[0].keys()))
    count = 0
    for d in data:
        count += 1
        file.write("\n")
        
        strList = [d["机构名称："], d["成立时间："], d["床位数量："],  \
                    d["占地面积："], d["收住对象："], d["收费区间："], \
                    d["员工人数："], d["机构性质："], d["机构类型："], \
                    d["电子邮箱："], d["邮政编码："],     \
                    d["所在地区："], d["联系地址："]]
        strList = [ud.normalize("NFKD", i).strip() for i in strList]
        file.write(",".join(strList))
    file.close()
    
    
    