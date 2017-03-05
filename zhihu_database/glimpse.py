from zhihu_oauth import *
import zhihu_oauth
from typing import Sequence, TypeVar
import os

TOKEN_FILE = 'token.pkl'


client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)

client = ZhihuClient()

client.load_token(TOKEN_FILE)

glimpse_answer = client.answer(144732855)
glimpse_question = client.question(54335680)
glimpse_people = client.people('q1ngyang')

glimpse = {
    'answer': client.answer(144732855),
    'question': client.question(54335680),
    'people': client.people('q1ngyang'),
    'comment': glimpse_question.comments[0],
    'topic': client.topic(19558021),  # 汉语
    'column': client.column('se-research'),
    'article': client.article(25188921),
    'activity': glimpse_people.activities[0],
    'collection': client.collection(71883827),  # 上知乎看段子
}

print('glimpse', glimpse)

"""
Available types
1. String
2. Integer
3. TIMESTAMP
4. Boolean
"""


def spider_to_json(spider_object):
    model = dict()
    for key in dir(spider_object):
        final_value = ''
        if key[0] != '_':
            property_type = type(getattr(spider_object, key))
            if property_type is str:
                final_value = 'String'
                print(key, 'String')
            if property_type is bool:
                print(key, 'Boolean')
                final_value = 'Boolean'
            if property_type is int:
                print(key, 'Integer')
                final_value = 'Integer'
            if property_type is zhihu_oauth.zhcls.streaming.StreamingJSON:
                print(key, 'JSON')
                final_value = 'JSON'
            if issubclass(property_type, zhihu_oauth.zhcls.base.Base):
                print(key, property_type.__name__)
                final_value = property_type.__name__
            # print(key, property_type)
            if final_value != '':
                model[key] = final_value
    return model


def upperfirst(x):
    return x[0].upper() + x[1:]


model = dict()
for key in glimpse:
    model[upperfirst(key)] = spider_to_json(glimpse[key])
print()
