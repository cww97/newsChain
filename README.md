# Trust News

too many f words ?

## 目录结构说明

首先说一下令人疑惑的`TrustNews`和`SimpleNews`, 这和django的设计有些关系，`TrustNews`是项目名(project)，而`SimpleNews`为整个Project下的一个app, django的设计思路是，一个project下可以多有个app，同样，`account`和`api`也是两个app，其中`account`即用户系统，`api`是为了接受前端jquery的一些ajax请求方便而设立的。理论上一个app在不同的project之间是可以移植的。

对于TrustNews，`setting.py`里面是一下项目配置，这里主要配了一个数据库，`urls.py`不用多说了吧，当然整个project的`urls.py`，include了每个app的`urls.py`并设置了前缀（django推荐的写法）,这样request的时候，`http://example.com/app_name/detail_request`，本项目中`SimpleNews`是核心app于是前缀为空，直接进去。

再说每个app，主要编辑在三个文件，request的时候从`urls.py`里面找到在`views.py`中对应的函数(对request响应)，这些函数从`models.py`（数据库）中取值然后后渲染html文件然后返回，其他的文件几乎没有编辑。`api`里面比较乱，通过`urls.py`找吧。

再说一下其他几个文件夹，`templates`，全是`html`文件，显然，这里是前端模板，尽管django官方文档建议每个app目录下建`templates`文件夹，但实际项目中似乎没有看见有人真的这么干，于是，这里仿照了大多数django的样子建了这个`templates`文件夹，分app建子目录。至于`html`代码写的丑，~~我其实不会前端啊~~。

`static`，静态文件，各种图啊，js/css啥的,cd进去`npm install`一下，看见`node_modules`就好了，编辑器用的`editor.md`，由于定制化要求比较高，进去改了一些项目源码（于是这个部分没有用`npm install`）。

`doc`,文档，里面现在有个第一个版本的那个`draft.pdf`。

## Based on

- [web框架:Django2](https://www.djangoproject.com/)
- [前端~~抄的章鱼哥的EOJ~~](https://acm.ecnu.edu.cn/)
- [前端框架Semantic UI](https://semantic-ui.com/)
- [编辑器:editor.md](https://pandao.github.io/editor.md/)
- [MongoDB](https://www.mongodb.com/download-center#atlas)

## 部署环境

- [MongoDB](https://www.mongodb.com/download-center#atlas)
- `pipfile`
- cd进static文件夹里面 `$ npm install`

启动：
先启动mongodb:
mongodb/bin
`net start mongodb`

然后项目文件夹里

python manage.py runserver 0.0.0.0:8000



## 关于markdown

- 真实渲染使用pypandoc，听说是格式转换界的瑞士军刀
- 预览渲染稍微改了改editor.md(搜索fuck_attr即可找到)
- 为什么需要两套呢（xc: 防 js 注入攻击？）
