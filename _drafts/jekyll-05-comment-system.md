---
layout: post
category: Jekyll
description: 如何添加评论系统如多说、DISQUS到Jekyll
title: Jekyll教程05-添加评论系统
keyword: Jekyll教程, 多说, disqus， Jekyll评论系统
---

预览着刚写完的文章，是否有点欣喜若狂呢？等等……怎么感觉好像缺少了些什么似的……

少年，我看你骨骼精奇，特此授于你添加评论系统的大法，此招切记不可轻易外传。

评论系统主要分两种，一是天朝内的，如`多说`；二是资本主义的，如`DISQUS` ，[瘾科技](http://cn.engadget.com/)用的就是*DISQUS* 。以下是详细的操作讲解。

<!-- more -->

本次操作前提是要注册并创建github博客项目

## 使用Disqus

到[官网](https://disqus.com/)注册个账号，在[此页面](https://disqus.com/admin/create/) 创建站点，关联到你的github博客，通常是`yourname.github.io`。

创建完成后，你将获得一个**shortname** ，形如`your_shortname.disqus.com` ， 然后访问 *https://your_shortname.disqus.com/admin/settings/install/* 获得通用代码，把通用代码添加到本地jekyll博客即可，操作步骤如下：

- 新建 `disqus.html`

```html
<!-- 在 _includes 目录下新建 disqus.html 文件，内容即拷贝的通用代码-->
<div id="disqus_thread"></div>
<script type="text/javascript">

var disqus_config = function () {
    this.page.url = "";  // Replace PAGE_URL with your page's canonical URL variable
    //改为你的shortname，不带.disqus.com后缀
    this.page.identifier = 'your_shortname'; 
};
(function() { // DON'T EDIT BELOW THIS LINE
    var d = document, s = d.createElement('script');
    //改为你的shortname，不带.disqus.com后缀
    s.src = '//your_shortname.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a><
/noscript>
```

- 添加到*post*模板

```html
<!-- 编辑 _layouts/post.html 文件，在末尾添加如下内容-->
{% if page.disqus != false %}
  {% include disqus.html %}
  <!-- 改为你的shortname，不带.disqus.com后缀
   此条用于显示网站所有的评论总数-->
  <script id="dsq-count-scr" src="//your_shortname.disqus.com/count.js" async></script>
{% endif %}
```

赶紧刷新刚才查看的文章，嘿嘿，已经看到*disqus*的评论框了吧!!!

等等……如果哪天我改用新的*disqus*账号，岂不是要修改上述三个*shortname* ？这得多麻烦啊。还记得之前说过的 主配置文件_config.yml 吗？只要在主配置文件中指定即可，其他页面使用变量的形式代替。

```shell
# 在 _config.yml 末尾添加
disqus: your_shortname

# 替换 _includes/disqus.html、_layout/post.html
# 中的 your_shortname 为
{{ site.disqus }}

# 更改主配置使其生效的方式是要 重启服务 噢
```



## 使用多说

注册登录多说后，同样需要创建一个站点，获取你的*shortname* ，同样是不带后缀的。鉴于操作比较类似，就不再详细展开了。

- 新建 `_includes/duoshuo.html`

```html
<!-- {{ page.title }}、{{ page.id }}、{{ site.url }}{{ page.url }} 和 {{ site.duoshuo }} 为修改的内容  -->
<div class="ds-thread" data-title="{{ page.title }}" data-thread-key="{{ page.id }}" data-url="{{ site.url }}{{ page.url }}"></div>
<script type="text/javascript">
var duoshuoQuery = {short_name:"{{ site.duoshuo }}"};
    (function() {
        var ds = document.createElement('script');
        ds.type = 'text/javascript';ds.async = true;
        ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
        ds.charset = 'UTF-8';
        (document.getElementsByTagName('head')[0] 
         || document.getElementsByTagName('body')[0]).appendChild(ds);
    })();
    </script>
```

- 修改 `_config.yml`

```shell
# 在末尾添加
duoshuo: your_duoshuo_shortname

# 重启服务使其生效
```





