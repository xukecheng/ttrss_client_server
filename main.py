import flask, json
from flask import request
from ttrss.client import TTRClient
import configparser

server = flask.Flask(__name__)

cf = configparser.ConfigParser()
cf.read('./config.ini', encoding='UTF-8')
ttrss_url = cf.get('TinyTinyRssServer', 'TinyTinyRssUrl')
ttrss_account = cf.get('TinyTinyRssServer', 'TinyTinyAccount')
ttrss_password = cf.get('TinyTinyRssServer', 'TinyTinyPassword')
client = TTRClient(ttrss_url, ttrss_account, ttrss_password)

@server.route('/get_feed_tree', methods=['get'])
def get_feed_tree() -> dict:
    client.login()
    feeds = client.get_feed_tree()
    del feeds["categories"]['items'][0]
    feed_tree = []
    for items in feeds["categories"]['items']:
        feed = []
        for item in items["items"]:
            if item["icon"]:
                feed_data = {
                    "feed_title": item['name'],
                    "feed_icon":
                    "https://rss.xukecheng.tech/%s" % item['icon'],
                    "feed_id": item['bare_id']
                }
            else:
                feed_data = {
                    "feed_title": item['name'],
                    "feed_icon":
                    "https://picgo-1253786286.cos.ap-guangzhou.myqcloud.com/image/1603502539.png",
                    "feed_id": item['bare_id']
                }
            feed.append(feed_data)
        data = {
            "category_id": items['bare_id'],
            "category_name": items['name'],
            "category_feed": feed,
        }
        feed_tree.append(data)
    client.logout()
    return {"code": 200, "data": feed_tree, "message": "success"}

@server.route('/get_feeds', methods=['get'])
def get_feeds() -> dict:
    client.login()
    feeds_list = client.get_feeds(cat_id=-3)
    feed_tree = client.get_feed_tree()
    feeds = {}
    for item in feeds_list:
        feed_title = item.title
        feed_unread_num = item.unread
        feed_id = item.id

        for items in feed_tree["categories"]['items']:
            for item in items["items"]:
                if item['bare_id'] == feed_id:
                    if item["icon"]:
                        feed_icon = "https://rss.xukecheng.tech/%s" % item[
                            'icon']
                    else:
                        feed_icon = "https://picgo-1253786286.cos.ap-guangzhou.myqcloud.com/image/1603502539.png"

        feeds[feed_id] = {
            "feed_title": feed_title,
            "feed_icon": feed_icon,
            "feed_unread_num": feed_unread_num
        }

    client.logout()
    return {"code": 200, "data": feeds, "message": "success"}

@server.route('/get_unreads', methods=['get'])
def get_unreads() -> dict:
    # page = request.args.get('page')
    # limit = request.args.get('limit')
    # if page:
    #     page = int(page)
    # else:
    #     page = 1

    # if limit:
    #     pass
    # else:
    #     limit = 15

    client.login()

    # unread_count = client.get_unread_count()
    # max_page = (unread_count//limit)+1
    # if page == 1:
    #     skip = 0
    # elif page :
    #     skip = (page-1)*limit
    # else:
    #     skip = (max_page-1)*limit

    unread_articles = client.get_headlines(view_mode="unread",
                                                show_excerpt=True,
                                                limit=0,
                                                skip=0)
    articles = {}
    num = 0
    for article in unread_articles:
        article_data = {
            "id": article.id,
            "title": article.title,
            "time": str(article.updated),
            "description": article.excerpt,
            "feed_id": article.feed_id,
            "feed_title": article.feed_title,
            "flavor_image": article.flavor_image,
            "tag": article.tags
        }
        articles[num] = article_data
        num += 1
    client.logout()
    return {"code": 200, "data": articles, "message": "success"}

@server.route('/article_detail', methods=['get'])
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

@server.route('/mark_read', methods=['get'])
def mark_read():
    id_list = []
    id_list.append(request.args.get('id'))
    client.login()
    client.mark_read(id_list)
    return {"code": 200, "message": "success"}

if __name__ == '__main__':
    server.run(debug=True, port=8888, host='0.0.0.0')
