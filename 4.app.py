from flask import Flask, render_template, request
from utils import fuzzy_search
import pymysql
import pymysql.cursors

app = Flask(__name__)

@app.route("/")
def index():
    search_text = request.values.get('searchText','')
    ids = fuzzy_search(search_text)
    # 索引值全部+1，方便在数据库中搜索
    ids = [x + 1 for x in ids]
    print(ids)
    # 将ids列表中的元素转换为字符串，并用逗号分隔
    ids_str = ', '.join(map(str, ids))
    # 查询对应电影的所有信息
    # 1.连接mysql
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="1234", charset='utf8', db='movies')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 2.发送指令
    # sql = ("SELECT * FROM tb_movie WHERE id IN (%s)")
    # data = [ids_str]
    # cursor.execute(sql, data)
    # movie_list = cursor.fetchall()
    # 初始时显示top10的电影
    if len(ids) == 0:
        ids = [1,2,3,4,5,6,7,8,9,10]
    ids_tuple = tuple(ids)
    print(ids_tuple)
    sql = "SELECT * FROM tb_movie WHERE id IN %s"
    cursor.execute(sql,(ids_tuple,))
    movie_list = cursor.fetchall()
    # 3.关闭连接
    cursor.close()
    conn.close()

    print(movie_list)

    context = {
        'search_text': search_text,
        'movie_list': movie_list
    }
    return render_template("index.html", **context)

if __name__ == "__main__":
    app.run(debug=True)