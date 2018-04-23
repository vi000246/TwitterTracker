# 放置和資料存取紀錄有關的程式碼
import csv
import datetime
import os

# 讀取最近一次上線紀錄 ，喜歡的內容數量
def GetLastRecord(userId):
    csvPath = _GetFilePath(userId)

    if not os.path.isfile(csvPath):
        return '',''

    with open(csvPath, 'r', encoding='utf-8-sig', newline='') as myfile:
        last_line = myfile.readlines()[-1].replace('"', '').strip()
        lis = last_line.split(',')
        return lis[0],lis[1]

def RemoveLastRecord(userId):
    csvPath = _GetFilePath(userId)
    if not os.path.isfile(csvPath):
        return

    inputs = open(csvPath, encoding='utf-8-sig',newline='')
    all_lines = inputs.readlines()
    all_lines.pop(len(all_lines) - 1)  # removes last line
    inputs.close()  # closes file

    # truncate file and write all lines except the last line
    with open(csvPath, "w",encoding='utf-8-sig',newline='') as out:
        for line in all_lines:
            out.write(line.strip() + "\n")




# 寫入CSV檔
def SaveToCSV(userId,logintime,likeNum):
    # 判斷檔案存不存在
    csvPath = _GetFilePath(userId)
    # 要寫入的欄位
    rows = [logintime,likeNum]

    # 如果不存在就開一個新檔案
    if not os.path.isfile(csvPath):
        with open(csvPath, 'w',encoding='utf-8-sig',newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            csvHeader = [u'登入時間',u'喜歡的內容數']
            wr.writerow(csvHeader)
            wr.writerow(rows)

    # 如果存在就append new row
    else:
        with open(csvPath, 'a',encoding='utf-8-sig',newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(rows)

# 取得檔案連結
def _GetFilePath(userId):
    FileName = userId + '_' + datetime.datetime.now().strftime('%Y%m') + '.csv'
    directory = os.getcwd() + '\\LoginHistory\\'
    if not os.path.exists(directory):
        os.makedirs(directory)
    csvPath = directory + FileName
    return csvPath



if __name__ == "__main__":
    SaveToCSV('digforapples','2018-01-30 11:30:26','4599')
    # a,b = GetLastRecord('digforapples')
    # RemoveLastRecord('digforapples')