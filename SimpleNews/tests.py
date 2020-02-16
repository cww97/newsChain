# -*- coding: utf-8 -*-
from django.test import TestCase

# Create your tests here.
from mongoengine import connect
# from views import md_html
import json
from models import *
connect('TrustNews', host='mongodb://localhost:27017/TrustNews')


def fuck_mongo_md():
    Page(title='杜特尔特称中菲关系改善不代表菲放弃南海权益 中方回应',content=u'据报道，23日，菲律宾总统杜特尔特发表国情咨文时提到菲中关系，回应了一段时间以来菲国内有关菲中关系的一些关切和质疑。杜高度评价中菲在打击跨国犯罪和禁毒等领域合作，并表示，中菲关系改善不代表菲放弃南海权益，双方正通过双边和多边渠道友好处理分歧。中国外交部发言人耿爽在今天（24日）的例行记者会上表示，中方注意到杜特尔特总统国情咨文中有关过去两年菲中关系持续改善，两国合作前所未有的积极评价。\n\n耿爽表示，中方赞赏菲律宾政府在杜特尔特总统领导下坚持独立自主外交政策，在相互平等、相互尊重的基础上发展同各国的正常关系和互利合作。2016年中菲关系转圜以来，双方各领域合作全面恢复并取得显著进展，为两国人民带来了实实在在的利益。安全合作是两国一大合作重点。中方坚定支持杜特尔特总统禁毒、反恐和打击跨国犯罪的努力，助力菲政府维护和平安宁。近年来两国合作实践充分说明，睦邻友好是符合两国和两国人民利益的唯一选择，是我们应始终坚持的正确方向。\n\n耿爽强调，杜特尔特总统就职以来，中菲就南海问题一直保持顺畅有效沟通，积极开展对话合作，维护了海上形势总体稳定。这一发展顺应两国人民的共同期盼，也为地区和平稳定作出重要贡献。中方愿同菲方一道，继续妥善管控分歧、聚焦务实合作，共同维护南海和平稳定。中方还将继续同包括菲律宾在内的东盟国家共建地区规则，推动“南海行为准则”磋商不断取得积极进展。（央视记者 申杨）').save()
    page = Page.objects[1]
    with open('../static/SampleData/SampleData.json', 'r', encoding='utf-8') as f:
        pages = json.load(f)
        st = pages[0]['content']
        print(st)
        print('text from local json, after md->html', type(st))
        # st = md_html(st)
        print(st)
    print('--------------------------------')
    st = page.content.encode('utf-8').decode('utf-8')
    print(st)
    print('\ntext from mongoDB, after md->html', type(st))
    st = "" + st
    # st = md_html(st)
    print(st)


def fuck_again():
    pass


class Fuck:
    _prr = 2
    def __init__(self):
        self.__pri = 1



if __name__ == '__main__':
    f = Fuck()
    f._prr = 2
    print(f.__pri)