# 爬取电影摘要，由于需要二级url，因此单独爬取
import requests
from bs4 import BeautifulSoup
import time
import re
import pymysql
import pymysql.cursors

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36"
}

count = 0
nexturl = [] # 链接到详情页的url

file = open("next_page_url.txt","r")

for line in file:
    url = line.strip()
    if url != "\n":
        count = count + 1
        print(count)
        print(url)
        nexturl.append(url)

        response = requests.get(url, headers = headers)
        content = response.text
        soup = BeautifulSoup(content, "html.parser")

        summary = soup.find("span", attrs={"property": "v:summary"})
        if summary is None:
            print("no content")
        else:
            top_file = open(fr"movie\info\top{count}.txt", "a", encoding='utf-8')
            cleaned_text = re.sub(r'\s+', '', summary.get_text())
            print(cleaned_text)
            top_file.write(cleaned_text+"\n")
            top_file.close()
            # 1.连接mysql
            conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="1234", charset='utf8', db='movies')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            # 2.发送指令(summary为text类型不能设置default value，因此此处先插入null)
            sql = ("UPDATE tb_movie SET summary = %s WHERE id = %s")
            data = (cleaned_text, count)
            cursor.execute(sql, data)
            conn.commit()
            # 3.关闭连接
            cursor.close()
            conn.close()
        time.sleep(3)

file.close()
