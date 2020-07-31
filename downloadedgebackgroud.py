import requests
import os ,sys
import urllib

url='https://www.bing.com/HPImageArchive.aspx?idx=0&n=8&format=js&pid=HpEdgeAn&mkt=zh-cn'
res = requests.get(url)


def save_image(name,imageUrl):

    print("open image")
    request = urllib.request.Request(imageUrl)
    page  = urllib.request.urlopen(request)
    image = page.read()
    print("save image")
    fileName = name+'.jpg'
    with open(fileName, 'wb') as f:
        f.write(image)

images = res.json()['images']

def main():
    for i in range(0,len(images)):
        imgeurl='https://bing.com/'+ images[i]['url']
        name=images[i]['fullstartdate'] # name file
        print(imgeurl) 
        #找到图片路径下载
        save_image(name,imgeurl)

if __name__ == "__main__":
    main()