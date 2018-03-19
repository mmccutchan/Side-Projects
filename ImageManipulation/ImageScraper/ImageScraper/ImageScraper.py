import re
import os
import urllib.request
import html5lib
from bs4 import BeautifulSoup
import requests
from PIL import Image
import filecmp

def getImgs(search):

    totalCount = 0
    
    while totalCount < limit:
        page = requests.get("https://images.search.yahoo.com/search/images;_ylt=A2KLfSFRylpas0IArWRXNyoA;_ylu=X3oDMTB0N2Noc21lBGNvbG8DYmYxBHBvcwMxBHZ0aWQDBHNlYwNwaXZz?p=" + query + "&fr2=piv-web&fr=yfp-t&b=" + str(totalCount))
        text = page.text
        soup = BeautifulSoup(text, "html5lib")

        urls = re.sub('%2F', '/', str(soup))
        urls = re.sub('%2B', '-', urls)
        urls = re.findall(re.compile(regex), urls)

        soups = []
        count = 0
        print(len(urls))
        for imgUrl in urls:
            if imgUrl.startswith("http://") == 0:
                imgUrl = "http://" + imgUrl

            try:
                data = requests.get(imgUrl, headers=hdr)
                fileName = str(totalCount + count) + '.png'
                #print(fileName)
                file = open(dir + '\\' + folder + "\\" + fileName, 'wb')
                file.write(data.content)
                file.close()

                img = Image.open(dir + '\\' + folder + "\\" + fileName)
                width, height = img.size
                img.close()

                if size != 'n' and (width != w or height != h):
                    os.remove(dir + '\\' + folder + "\\" + fileName)
                
                else:
                    count += 1

                if totalCount + count >= limit:
                    break

            except Exception as e:
                print(imgUrl + " " + str(e))

        totalCount += count
      
def deleteCopies():
    for file in os.listdir(os.path.join(dir, folder)):
        try:
            img = Image.open(os.path.join(dir, folder, file))
            for fileComp in os.listdir(os.path.join(dir, folder)):
                imgComp = Image.open(os.path.join(dir, folder, fileComp))
                if file != fileComp and img == imgComp:
                    os.remove(os.path.join(dir, folder, file))
                    break
        except:
            pass

dir = r"C:\Users\mmccutchan\Downloads"
regex = r'(?:imgurl=)(.[^&]*)(?:&)'
regexW = r'(?:width=")(.[^"]*)(?:")'
regexH = r'(?:height=")(.[^"]*)(?:")'
hdr = {'User-Agent': 'A bot'}
query = input("What image would you like to scrape? ")
folder = input("What folder should these be put in? ")
if not os.path.exists(dir + "\\" + folder):
    os.mkdir(dir + "\\" + folder)
limit = int(input("How many pictures would you like? "))
size = input("Would you like your pictures to be a specific size? (WxH) or n ")
if size != 'n':
    [w, h] = size.split("x")
    w = int(w)
    h = int(h)

getImgs(query)
deleteCopies()
print("Complete!")
