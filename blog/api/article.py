from flask_combo_jsonapi import ResourceDetail, ResourceList
from blog.schemas import ArticleSchema
from blog.database import db
from blog.models import Articles
from combojsonapi.event.resource import EventsResource


class ArticleListEvents(EventsResource):
    def event_get_count(self):
        return {"count": Articles.query.count()}


class ArticleList(ResourceList):
    events = ArticleListEvents
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Articles,
    }


class ArticleDetail(ResourceDetail):
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Articles,
    }
