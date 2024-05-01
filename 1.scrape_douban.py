import requests
import time
from bs4 import BeautifulSoup
import re
import pymysql
import pymysql.cursors

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36"
}

titles = [] # 电影标题
intros = [] # 电影简介
nexturl = [] # 链接到详情页的url
rates = [] # 电影评分
img = [] # 电影图片

count = 0

file = open("next_page_url.txt","a")
# 一共有10页，一页25条，一页一页爬取，每次改变start后面的数字
response = requests.get(f"https://movie.douban.com/top250?start=225", headers = headers)

if response.status_code == 200:
    content = response.text
    soup = BeautifulSoup(content, "html.parser")

    # 爬标题 最终250top movies的中文标题依次被存放在titles列表中
    all_titles = soup.find_all("span",attrs={"class":"title"})

    for title in all_titles:
        temp = title.string
        if "/" not in temp: # 仅保留中文标题
            titles.append(temp)

    # 爬链接到详情页的url 最终存放在nexturl列表中
    all_links = soup.find_all("a")
    for link in all_links:
        url = link["href"] if link else None
        # 只找链接到详情页的链接
        if url not in nexturl and len(url) >= 25 and url[8] == "m" and url[25] == "s":
            nexturl.append(url)
            file.write(url+"\n")

    # 爬图片url 最终存放在img列表中
    all_img = soup.find_all("img")
    for imgs in all_img:
        imgurl = imgs["src"] if imgs["src"] else None
        if imgurl not in img and len(url) >= 27 and imgurl[26] == "v" and imgurl[31] == "p":
            img.append(imgurl)
            print(imgurl)

    # 爬简介 标签为<p class> 最终所有简介依次保存在intros列表中
    all_p_tags = soup.find_all("p")
    for ptags in all_p_tags:
        if "class" in ptags.attrs and (not ptags["class"]):
            intros.append(ptags.get_text().strip())


    # 爬评分 最终存放在rates列表中
    all_rates = soup.find_all("span",
                              attrs={"class":"rating_num", "property":"v:average"})
    for rate in all_rates:
        rates.append(rate.text)

    time.sleep(2)

    print(len(titles))
    print(len(intros))
    print(len(img))
    print(len(nexturl))
    print(len(rates))
    file.close()

    # 将相关信息写入文件+写入数据库
    for count in range(0, 25, 1):
        f = open(fr"movie\info\top{count+226}.txt", "w", encoding='utf-8')
        cleaned_title = re.sub(r'\s+', '', titles[count])
        cleaned_intro = re.sub(r'\s+','', intros[count])

        f.write(cleaned_title+"\n"+cleaned_intro+"\n"+rates[count]+"\n")
        f.close()

        # 1.连接mysql
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="1234", charset='utf8', db='movies')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 2.发送指令(summary为text类型不能设置default value，因此此处先插入null)
        sql = ("INSERT INTO tb_movie(id, title, intros, img, rate, nexturl, summary) VALUES (%s, %s, %s, %s, %s, %s, '') "
                       "ON DUPLICATE KEY UPDATE "
                       "title = %s, intros = %s, img = %s, rate = %s, nexturl = %s, summary = ''")
        data = (count+226, cleaned_title, cleaned_intro, img[count], rates[count], nexturl[count],
                cleaned_title, cleaned_intro, img[count], rates[count], nexturl[count])
        cursor.execute(sql, data)
        conn.commit()
        # 3.关闭连接
        cursor.close()
        conn.close()

else:
    print("requirement failed")
    print(response.status_code)
    print(response.reason)