import json
import requests
import re


class unsplash_spider:
    def __init__(self,max):
        f = open("D:/data/photos/task.json","r")
        task = f.readlines()
        task = ''.join(task)
        task = json.loads(task)
        self.pid = task["next_pid"]
        self.next_pid = ""
        self.num = int(task["num"])
        self.count = 0
        f.close()
        self.download(max)

    def get_url(self):
        url = "https://unsplash.com/napi/feeds/home?after="
        url += self.pid
        return url

    def get_next_pid(self):
        headers = {'x-unsplash-client': 'web'}
        url = self.get_url()
        response = requests.get(url, headers = headers)
        next_pid = None
        if response.status_code == 200:
            content = response.text
            content = json.loads(content)
            next_page = content["next_page"]
            next_pid = re.findall("after=(.*)",next_page)[0]
        return next_pid

    def get_photos_url(self):
        headers = {'x-unsplash-client': 'web'}
        url = self.get_url()
        response = requests.get(url, headers = headers)
        photos_url = []
        if response.status_code == 200:
            content = response.text
            photo = re.findall("\"raw\":\"(.*?)\"",content)
            for i in photo:
                photos_url.append(i)
        return photos_url

    def save_photo(self,url):
        print("*"*35)
        print("正在下载"+str(self.num)+".jpg")
        print(url)
        img = requests.get(url).content
        num = str(self.num)
        f = open("D:/data/photos/"+num+".jpg","wb")
        f.write(img)
        f.close()
        print("下载成功，本次任务共下载"+str(self.count+1)+"张图片")
        print("*"*35)
        self.num += 1
        self.count += 1

    def save_task(self):
        f = open("D:/data/photos/task.json","r")
        task = f.readlines()
        task = ''.join(task)
        task = json.loads(task)
        f.close()
        f = open("D:/data/photos/task.json","w")
        task["next_pid"] = self.next_pid
        task["num"] = self.num
        task = json.dumps(task,sort_keys=True,ensure_ascii=False,indent = 2)
        f.write(task)
        f.close()

    def download(self,max):
        while self.count <= max-9:
            photos_url = self.get_photos_url()
            for url in photos_url:
                self.save_photo(url)
            self.next_pid = self.get_next_pid()
            self.save_task()
            self.pid = self.next_pid



def main():
    spider = unsplash_spider(100)

if __name__ == '__main__':
    main()