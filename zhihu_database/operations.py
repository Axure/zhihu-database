# sqlite://<nohostname>/<path>
# where <path> is relative:

from .connection import engine, session
import logging

logger = logging.getLogger('setup.py'
                           '')
from sqlalchemy import Column as SQL_Column
from sqlalchemy.types import CHAR, Integer, String, Boolean, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base
import zhihu_oauth
from .glimpse import model as g_model

BaseModel = declarative_base()

AnswerModel = {

}


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)

class Activity(BaseModel):
    __tablename__ = 'activity'

    id = SQL_Column(Integer, primary_key=True, autoincrement=True)


class Answer(BaseModel):
    __tablename__ = 'answer'

    id = SQL_Column(Integer, primary_key=True, autoincrement=True)


def json_to_orm(json, orm):
    for key in json:
        value = json[key]
        column_type = ''
        if (value == 'String'):
            column_type = String
        if (value == 'JSON'):
            column_type = JSON
        if (value == 'Integer'):
            column_type = Integer
        if (value == 'TIMESTAMP'):
            column_type = TIMESTAMP
        if (value == 'Boolean'):
            column_type = Boolean
        if key == 'id':
            key = str.lower(orm.__name__) + '_id'
        if column_type != '':
            print('Fucking setting attrib', column_type)
            setattr(orm, key, SQL_Column(column_type))


for key in dir(Answer):
    print(key, getattr(Answer, key))


def absorb(orm, spider_object):
    for key in dir(spider_object):
        true_data = ''
        if key[0] != '_':
            property_type = type(getattr(spider_object, key))
            if property_type is str:
                true_data = getattr(spider_object, key)
            if property_type is bool:
                true_data = getattr(spider_object, key)
            if property_type is int:
                true_data = getattr(spider_object, key)
            if property_type is zhihu_oauth.zhcls.streaming.StreamingJSON:
                logger.debug(getattr(spider_object, key).raw_data())
                true_data = getattr(spider_object, key).raw_data()
            if issubclass(property_type, zhihu_oauth.zhcls.base.Base):
                logger.warn('Should be id' + ', ' + 'key is: ' +
                            str.lower(property_type.__name__) + '_id')
                true_data = getattr(spider_object, key).id
                key = str.lower(property_type.__name__) + '_id'
            # print(key, property_type)

            if key == 'id':
                key = str.lower(type(orm).__name__) + '_id'
            setattr(orm, key, true_data)

            if true_data != '':
                pass
                # model[key] = final_value
    return orm


class Article(BaseModel):
    __tablename__ = 'article'

    id = SQL_Column(Integer, primary_key=True, autoincrement=True)


class Collection(BaseModel):
    __tablename__ = 'collection'

    id = SQL_Column(Integer, primary_key=True, autoincrement=True)


class Column(BaseModel):
    __tablename__ = 'column'

    id = SQL_Column(Integer, primary_key=True, autoincrement=True)


class Comment(BaseModel):
    __tablename__ = 'comment'

    id = SQL_Column(Integer, primary_key=True, autoincrement=True)


class People(BaseModel):
    __tablename__ = 'people'

    id = SQL_Column(Integer, primary_key=True, autoincrement=True)


class Question(BaseModel):
    __tablename__ = 'question'

    id = SQL_Column(Integer, primary_key=True, autoincrement=True)


def upperfirst(x):
    return x[0].upper() + x[1:]


class Topic(BaseModel):
    __tablename__ = 'topic'

    id = SQL_Column(Integer, primary_key=True, autoincrement=True)


Models = [Question, Answer, People, Activity,
          Article, Column, Collection, Topic, Comment]
print(g_model)
for model in Models:
    json_to_orm(g_model[model.__name__], model)
