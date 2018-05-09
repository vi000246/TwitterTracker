import yaml
import requests
from lxml import etree
import FileHandle
import time
import logging

def main():
    # 獲取logger實例，如果參數為空則返回root logger
    logger = logging.getLogger("TwitterTracker")

    # 指定logger輸出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

    # 文件日誌
    file_handler = logging.FileHandler("error.log")
    file_handler.setFormatter(formatter)  # 可以通過setFormatter指定輸出格式

    # 為logger添加的日誌處理器
    logger.addHandler(file_handler)

    # 指定日誌的最低輸出級別，默認為WARN級別
    logger.setLevel(logging.INFO)

    try:
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
    except Exception as e:

        logger.error(str(e))


if __name__ == "__main__":
    main()
