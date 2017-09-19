# coding=utf-8
__author__ = "Kasaimiluo"
__date__ = "2017/9/19 20:26"
import pymysql
import requests
from bs4 import BeautifulSoup
baseUrl = "https://movie.douban.com/top250?start=%d&filter="
def get_movies(start):
    url = baseUrl % start
    lists = []
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    items = soup.find("ol", "grid_view").find_all("li")
    for i in items:
        movie = {}
        movie["rank"] = i.find("em").text
        movie["link"] = i.find("div","pic").find("a").get("href")
        movie["poster"] = i.find("div","pic").find("a").find('img').get("src")
        movie["name"] = i.find("span", "title").text
        movie["score"] = i.find("span", "rating_num").text
        movie["quote"] = i.find("span", "inq").text if(i.find("span", "inq")) else ""
        movie["evaluate"]=i.find("div","bd").find("div","star").find("span").text
        lists.append(movie)
    return lists

if __name__ == "__main__":
    db = pymysql.connect(host="localhost",user="root",password="995307887",db="test",charset="utf8mb4")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS movies")
    createTab = """CREATE TABLE movies(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        rank VARCHAR(4) NOT NULL,
        link VARCHAR(50) NOT NULL,
        poster VARCHAR(100) NOT NULL,
        score VARCHAR(4) NOT NULL,
        quote VARCHAR(50),
        evaluate VARCHAR (50)
    )charset=utf8"""
    cursor.execute(createTab)
    start = 0
    while (start < 250):
        lists = get_movies(start)
        for i in lists:
            sql = "INSERT INTO `movies`(`name`,`rank`,`link`,`poster`,`score`,`quote`,evaluate) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            try:
                cursor.execute(sql, (i["name"], i["rank"], i["link"], i["poster"], i["score"], i["quote"],i["evaluate"]))
                db.commit()
                print(i["evaluate"]+" is success")
            except:
                db.rollback()
        start += 25
    db.close()