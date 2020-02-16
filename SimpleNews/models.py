from account.models import User
import datetime
from mongoengine import *
from api import markdown4
from bs4 import BeautifulSoup
# Create your models here.


class Object(DynamicDocument):
    content_type = StringField()
    timeStamp = DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True,  # for inherit
            'ordering': ['-timeStamp']}  # for sort


class Picture(Object):
    photo = FileField(required=True)
    content_type = StringField(required=True)


class WebIndex(DynamicDocument):
    meta = {'allow_inheritance': True}  # maybe 'revision' later


class Tag(WebIndex):
    name = StringField(required=True)
    pages = ListField(ReferenceField(Object))

    meta = {'ordering': ['-pages.count']}

    def __unicode__(self):
        return self.name


class Page(Object):
    title = StringField(max_length=200, required=True)
    author = ReferenceField(User, required=True)
    tags = ListField(StringField())
    content = StringField(required=True)
    is_final = BooleanField(default=False)  # True: onChain, else draft
    ref_list = ListField(DictField())  # reference
    include_list = ListField(DictField())
    pre_vision = ReferenceField(Object)  # Page

    def __unicode__(self):
        return self.title

    def tag_str(self):
        return ','.join(self.tags)

    def create_or_get_tags(self, tag_names: str, draft=False):
        tag_names = tag_names.replace('，', ',')
        tag_names = [x for x in tag_names.split(',')]
        for tag_name in tag_names:
            if tag_name == '' or tag_name in self.tags: continue
            self.tags.append(tag_name)
            if not draft and not Tag.objects(name=tag_name):
                Tag(name=tag_name).save()

    def get_reference(self):
        soup = BeautifulSoup(markdown4.convert(self.content), 'html.parser')

        refs = soup.find_all('a', attrs={'name': 'cite'})
        for ref in refs:
            ref = {'cite': ref.get('cite'), 'vote': int(ref.get('vote')),
                   'page': ref.get('href').replace('/', '').replace('detail', '')}
            if ref in self.ref_list: continue
            self.ref_list.append(ref)

        includes = soup.find_all('img', attrs={'name': 'include'})
        for include in includes:
            include = {'include_id': include.get('src').replace('/api/image/', '').replace('/','')}
            self.include_list.append(include)

    def create(self, request, original: bool, update_draft=False):
        self.original = original
        self.title = request.POST['title']
        self.author = User.objects.get(id=request.session['user_id'])
        self.content = '\n' + request.POST['content']
        self.is_final = True if request.POST['action'] == 'submit' else False
        self.create_or_get_tags(request.POST['tags'], draft=update_draft)
        self.get_reference()
        self.save()

    def delete_with_tags(self):
        # if tags have no pages any longer, delete the tag
        #
        self.delete()


if __name__ == '__main__':
    Page.objects[0].delete()
