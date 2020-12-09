from typing import Optional
from fastapi import FastAPI
from RssServer import RssServer

app = FastAPI()
server = RssServer()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_unreads")
def get_unreads():
    try:
        return {
            "code": 200,
            "data": server.get_unreads(),
            "message": "success"
        }
    except Exception:
        return {"code": 201, "data": "参数错误", "message": "success"}


@app.get("/mark_read")
def mark_read(article_id_string: str):
    try:
        article_id_list = article_id_string.split(",")
        return {
            "code": 200,
            "data": server.mark_read(article_id_list),
            "message": "success"
        }
    except Exception:
        return {"code": 201, "data": "参数错误", "message": "success"}


@app.get("/get_feed_tree")
def get_feed_tree():
    try:
        return {
            "code": 200,
            "data": server.get_feed_tree(),
            "message": "success"
        }
    except Exception:
        return {"code": 201, "data": "参数错误", "message": "success"}