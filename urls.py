import tornado

from views import DocumentGetAPIView, DocumentCreateAPIView, DocumentListAPIView, DocumentDeleteAPIView

handlers = [

    tornado.web.url(r"/list", DocumentListAPIView),
    tornado.web.url(r"/get/([^/]+)", DocumentGetAPIView),
    tornado.web.url(r"/create", DocumentCreateAPIView),
    tornado.web.url(r"/delete/([^/]+)", DocumentDeleteAPIView),

 ]
