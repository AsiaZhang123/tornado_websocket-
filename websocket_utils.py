# -*-coding: utf-8-*-
"""
# Author: Asian_zhang
# Email: zhangyazhou@mofanghr.com
"""
import tornado.web
import tornado.websocket
from tornado.web import RequestHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from core import request_handler, get_request_params,return_data
import logging
import json


socklist = {}


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        logging.info('socket open ip:')
        logging.info(self.request.remote_ip)
        # print self.request.remote_ip
        # pass

    def on_message(self, message):
        self.write_message(u"Your message was: " + message)
        socklist[message] = self
        logging.info('socket userInfo(mobile$$resumeID):')
        logging.info(message)
        self.write_message(u"hahhahahah")
        self.write_message(json.dumps({"a":1,"b":2}))

    def on_close(self):
        logging.info('socket close ip:')
        logging.info(self.request.remote_ip)
        print 'socket close'
        # pass

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

    @staticmethod
    def send_message(userKey,msg): # userKey = "mobile$$resumeID"
        socklist.get(userKey).write_message(msg)


class BuyResume(RequestHandler):
    @request_handler()
    def get(self):
        params = get_request_params()
        mobile = str(params.get('user_mobile')) # 用户电话 用来识别socket
        resumeID = str(params.get('userID'))  # 简历ID 用来识别socket
        user_socketKey = mobile + "$$" + resumeID  # 用户socket链接标志
        if params.get('status') == 1:
            code = 200
        else:
            code = -1
        msg = json.dumps({
            "data":{
                "name":params.get("name",''),
                "mobile":params.get('resume_mobile','')
            },
            "code":code
        })
        WebSocketHandler.send_message(user_socketKey,msg)
        return return_data()


class AccountBind(RequestHandler):
    @request_handler()
    def get(self):
        params = get_request_params()
        userID = str(params.get('userID'))  # hr用户ID 用来识别socket
        user_socketKey = userID  # 用户socket链接标志
        if params.get('status') == 1:
            code = 200
        else:
            code = -1
        msg = json.dumps({
            "data":{
                "params":params
            },
            "type":12,
            "code":code
        })
        WebSocketHandler.send_message(user_socketKey,msg)
        return return_data()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/member/resume/buyResult.json', WebSocketHandler),
            (r'/inner/resume/buyResumeResult.json',BuyResume),
            (r'/inner/account/bindStateResult.json',AccountBind)
        ]
        tornado.web.Application.__init__(self, handlers)
        
 
 def main():
    ws_app = Application()
    server = HTTPServer(ws_app)
    server.listen(8889)
    IOLoop.instance().start()
    
if __name__ == "__main__":
    main()
