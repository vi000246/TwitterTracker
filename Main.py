import yaml
import requests
from lxml import etree
import FileHandle
import time

def main():
    # 取得目標帳號
    f = open('config.yaml', encoding='utf8')
    settings = yaml.load(f)
    TargetAccount = settings["TargetAccount"]

    # 取得喜歡的內容數量
    r = requests.get('https://twitter.com/'+TargetAccount)
    # print(r.text)
    tree = etree.HTML(r.text)
    likeNum = tree.xpath('//a[@data-nav="favorites"]//*/text()')[2].replace(",", "")

    # 從csv取得上一次喜歡的內容數量
    _ , lastLikeNum = FileHandle.GetLastRecord(TargetAccount)

    # 如果csv抓不到上次的likeNum 代表csv是空的 或是上次的likeNum不等於這次的likeNum
    if not lastLikeNum or likeNum != lastLikeNum:
        IsChangeLikeNum = True
    else:
        IsChangeLikeNum = False

    if IsChangeLikeNum:
        t = time.time()
        FileHandle.SaveToCSV(TargetAccount, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)), likeNum)



if __name__ == "__main__":
    main()
