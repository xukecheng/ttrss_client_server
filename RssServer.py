import json
from ttrss.client import TTRClient
import configparser
from bs4 import BeautifulSoup
import re


class RssServer():
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read('./config.ini', encoding='UTF-8')
        ttrss_url = cf.get('TinyTinyRssServer', 'TinyTinyRssUrl')
        ttrss_account = cf.get('TinyTinyRssServer', 'TinyTinyAccount')
        ttrss_password = cf.get('TinyTinyRssServer', 'TinyTinyPassword')
        client = TTRClient(ttrss_url,
                           ttrss_account,
                           ttrss_password,
                           auto_login=True)
        self.client = client

    def get_unreads(self) -> dict:
        self.client.login()
        unread_articles = self.client.get_headlines(view_mode="unread",
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
                "isRead": 0 if article.unread else 1,
                "description": description,
                "htmlContent": article.content,
                "flavorImage": article.flavor_image,
                "articleOriginLink": article.link,
                "publishTime": int(article.updated.timestamp()),
            }
            articles.append(article_data)
        self.client.logout()
        return articles

    def mark_read(self, article_id_list: list):
        try:
            self.client.login()
            self.client.mark_read(article_id_list)
            return "已读完成"
        except Exception as e:
            print(e)
            self.client.login()
            self.client.mark_read(article_id_list)
            return "已读失败"


# def get_feed_tree() -> dict:
#     client.login()
#     feeds = client.get_feed_tree()
#     del feeds["categories"]['items'][0]
#     feed_tree = []
#     for items in feeds["categories"]['items']:
#         feed_list = []
#         for item in items["items"]:
#             if item["icon"]:
#                 feed_data = {
#                     "feed_title": item['name'],
#                     "feed_icon":
#                     "https://rss.xukecheng.tech/%s" % item['icon'],
#                     "feed_id": item['bare_id'],
#                 }
#             else:
#                 feed_data = {
#                     "feed_title": item['name'],
#                     "feed_icon":
#                     "https://picgo-1253786286.cos.ap-guangzhou.myqcloud.com/image/1603502539.png",
#                     "feed_id": item['bare_id']
#                 }
#             feed_list.append(feed_data)
#         data = {
#             "category_id": items['bare_id'],
#             "category_name": items['name'],
#             "category_feed": feed_list,
#         }
#         feed_tree.append(data)
#     client.logout()
#     return feed_tree

# def get_feeds() -> dict:
#     client.login()
#     feeds_list = client.get_feeds(cat_id=-3)
#     feed_tree = client.get_feed_tree()
#     feeds = []
#     for feed in feeds_list:
#         feed_id = feed.id
#         for items in feed_tree["categories"]['items']:
#             for item in items["items"]:
#                 if item['bare_id'] == feed_id:
#                     if item["icon"]:
#                         feed_icon = "https://rss.xukecheng.tech/%s" % item[
#                             'icon']
#                     else:
#                         feed_icon = "https://picgo-1253786286.cos.ap-guangzhou.myqcloud.com/image/1603502539.png"

#         feeds.append({
#             "feedId": feed.id,
#             "categoryId": feed.cat_id,
#             "feedTitle": feed.title,
#             "feedIcon": feed_icon,
#         })

#     client.logout()
#     return {"code": 200, "data": feeds, "message": "success"}

# def article_detail() -> dict:
#     id = request.args.get('id')
#     client.login()
#     article = client.get_articles(id)[0]
#     data = {
#         "id": article.id,
#         "title": article.title,
#         "time": str(article.updated),
#         "feed_id": article.feed_id,
#         "content": article.content,
#         "labels": article.labels,
#         "link": article.link,
#         "feed_title": article.feed_title,
#         "author": article.author
#     }
#     client.logout()
#     return {"code": 200, "data": data, "message": "success"}
