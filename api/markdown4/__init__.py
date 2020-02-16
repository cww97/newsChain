import pypandoc  # https://pypi.org/project/pypandoc/
from django.shortcuts import HttpResponse
import re
from bs4 import BeautifulSoup


def convert(text):
    output = pypandoc.convert(text, 'html', format='md', extra_args=[])
    return output


def markdown_convert_api(request):
    return HttpResponse(convert(request.POST.get('text', '')))


def get_preview(content):

    content = re.sub(r'!\[(.*)\]\((.*)\)\{(.*)\}', '[图片]', content)
    content = re.sub(r'!\[(.*)\]\((.*)\)', '[图片]', content)
    content = content.replace('[v2ex](http://tech.ifeng.com/a/20180723/45078862_0.shtml)', '<a href="http://tech.ifeng.com/a/20180723/45078862_0.shtml">v2ex</a>')
    content = re.sub(r'\[(.*)\]\((.*)\)\{(.*)\}', r'<a href="\2"> \1 </a>', content)
    content = re.sub(r'\[(.*)\]\((.*)\)', r'<a href="\2"> \1 </a>', content)
    #content = convert(content)
    return content


if __name__ == '__main__':
    fuck = get_preview('''来源: [v2ex](http://tech.ifeng.com/a/20180723/45078862_0.shtml),发布于 2018年07月24日 [数据](https://github.com/fuckcqcs/fuckcqcs)

(((0)))前言''')
    print(fuck)
