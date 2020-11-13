import flask, json
from flask import request
from ttrss.client import TTRClient
import configparser
from bs4 import BeautifulSoup
import re

app = flask.Flask(__name__)


@app.route('/get_feed_tree', methods=['get'])
def get_feed_tree() -> dict:
    client.login()
    feeds = client.get_feed_tree()
    del feeds["categories"]['items'][0]
    feed_tree = []
    for items in feeds["categories"]['items']:
        feed_list = []
        for item in items["items"]:
            if item["icon"]:
                feed_data = {
                    "feed_title": item['name'],
                    "feed_icon":
                    "https://rss.xukecheng.tech/%s" % item['icon'],
                    "feed_id": item['bare_id'],
                }
            else:
                feed_data = {
                    "feed_title": item['name'],
                    "feed_icon":
                    "https://picgo-1253786286.cos.ap-guangzhou.myqcloud.com/image/1603502539.png",
                    "feed_id": item['bare_id']
                }
            feed_list.append(feed_data)
        data = {
            "category_id": items['bare_id'],
            "category_name": items['name'],
            "category_feed": feed_list,
        }
        feed_tree.append(data)
    client.logout()
    return {"code": 200, "data": feed_tree, "message": "success"}


@app.route('/get_feeds', methods=['get'])
def get_feeds() -> dict:
    client.login()
    feeds_list = client.get_feeds(cat_id=-3)
    feed_tree = client.get_feed_tree()
    feeds = []
    for feed in feeds_list:
        feed_id = feed.id
        for items in feed_tree["categories"]['items']:
            for item in items["items"]:
                if item['bare_id'] == feed_id:
                    if item["icon"]:
                        feed_icon = "https://rss.xukecheng.tech/%s" % item[
                            'icon']
                    else:
                        feed_icon = "https://picgo-1253786286.cos.ap-guangzhou.myqcloud.com/image/1603502539.png"

        feeds.append({
            "feedId": feed.id,
            "categoryId": feed.cat_id,
            "feedTitle": feed.title,
            "feedIcon": feed_icon,
        })

    client.logout()
    return {"code": 200, "data": feeds, "message": "success"}


@app.route('/get_unreads', methods=['get'])
def get_unreads() -> dict:
    client.login()
    unread_articles = client.get_headlines(view_mode="unread",
                                           show_excerpt=False,
                                           limit=0,
                                           show_content=True,
                                           skip=0)
    articles = []
    for article in unread_articles:
        description = BeautifulSoup(article.content).get_text(strip=True)
        try:
            description = description[0:51]
        except IndexError:
            pass

        article_data = {
            "id": article.id,
            "feedId": article.feed_id,
            "title": article.title,
            "isMarked": 1 if article.marked else 0,
            "isUnread": 1 if article.unread else 0,
            "description": description,
            "htmlContent": article.content,
            "flavorImage": article.flavor_image,
            "articleOriginLink": article.link,
            "publishTime": int(article.updated.timestamp()),
        }
        articles.append(article_data)
    client.logout()
    return {"code": 200, "data": articles, "message": "success"}


@app.route('/article_detail', methods=['get'])
def article_detail() -> dict:
    id = request.args.get('id')
    client.login()
    article = client.get_articles(id)[0]
    data = {
        "id": article.id,
        "title": article.title,
        "time": str(article.updated),
        "feed_id": article.feed_id,
        "content": article.content,
        "labels": article.labels,
        "link": article.link,
        "feed_title": article.feed_title,
        "author": article.author
    }
    client.logout()
    return {"code": 200, "data": data, "message": "success"}


@app.route('/mark_read', methods=['get'])
def mark_read():
    id_list = []
    id_list.append(request.args.get('id'))
    client.login()
    client.mark_read(id_list)
    return {"code": 200, "message": "success"}


if __name__ == '__main__':
    cf = configparser.ConfigParser()
    cf.read('./config.ini', encoding='UTF-8')
    ttrss_url = cf.get('TinyTinyRssServer', 'TinyTinyRssUrl')
    ttrss_account = cf.get('TinyTinyRssServer', 'TinyTinyAccount')
    ttrss_password = cf.get('TinyTinyRssServer', 'TinyTinyPassword')
    client = TTRClient(ttrss_url,
                       ttrss_account,
                       ttrss_password,
                       auto_login=True)
    app.run(debug=True, port=8888, host='0.0.0.0')
