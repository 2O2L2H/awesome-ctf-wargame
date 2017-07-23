footer: © 2O2L2H How to use Jekyll Blog, 2017
slidenumbers: true

# [fit] How to use Jekyll Blog

#### 2O2L2H

---

## Blog

- Dynamic
    - [WordPress](https://ko.wordpress.com/create/?sgmt=gb&utm_source=adwords&utm_campaign=G_Search_Brand_Desktop_KR_ko_x_x&utm_medium=cpc&keyword=word%20press&creative=196934548301&campaignid=836791592&adgroupid=41250394525&matchtype=p&device=c&network=g&gclid=Cj0KCQjwktHLBRDsARIsAFBSb6wpNwbjZ0l5BniA5x8T66b_Cddc66ROp1TloTc_tQuXINo6IijqoCkaAq9qEALw_wcB) : 가입형, 설치형 
- Static
    - `username.github.io`  - [GitHub Pages](https://pages.github.com/)
    - [Jekyll : 심플하고 블로그 지향적인 정적 사이트](https://jekyllrb-ko.github.io/)    
    - [Hexo](https://hexo.io/ko/index.html)

---

# [fit] Jekyll


---

## Install Ruby & Jekyll

```bash
$ sudo gem install jekyll
```

```bash
$ jekyll --version
jekyll 3.5.0
```

---
## Jekyll

```
$ jekyll {build, clean, serve}
```

- `build` : markdown 으로부터 html 생성.
- `clean` : clean generate pages.
- `serve` :  local preview in `http://local:4000`
- `serve --watch` : local preview & incremental building.


---
## Clone repo

```bash
$ git clone https://github.com/2O2L2H/2O2L2H.github.io.git
```

## Install gem plugins

```bash
$ rake geminstall
$ sudo gem install jekyll-seo-tag jekyll-paginate jekyll-admin
```


---
## Setting

- `_config.yml` : Configuration
- `_posts` : Blog posting in markdown.
    - `2017-07-09-get-started.md`
    - `2017-07-23-gdb-switcher.md`

---
## Preview

```bash
$ jekyll serve --watch
```

- `_site` : Generated HTML.
- Local preview in `http://local:4000`

--- 
## Write a Posting

![left fit](https://raw.githubusercontent.com/2O2L2H/2O2L2H-etc/master/img/2017/0723/blog-title.png)

- `_posts/2017-MM-DD-title.md`

```
---
layout: post
title: "타이틀"
description: "설명 (표지에 표시)"
date: 2017-07-09
tags: [tag]
comments: true
share: true
---
```

---

## Build & Local Preview

```bash
$ jekyll serve --watch
```

---
## Image Hosting

- [2O2L2H/2O2L2H-etc: Image for 2O2L2H blog](https://github.com/2O2L2H/2O2L2H-etc)
- `https://raw.githubusercontent.com/2O2L2H/2O2L2H-etc/master/img/2017/0723/blog-title.png`

---
## JekyllAdmin

![left fit](https://raw.githubusercontent.com/2O2L2H/2O2L2H-etc/master/img/2017/0723/jekylladmin.png)

- `_config.yml`

```
plugins:
  - jekyll-seo-tag
  - jekyll-paginate
  - jekyll-admin
```

```
$ jekyll serve --watch
Configuration file: /Users/tkhwang/_2O2L2H/github/2O2L2H.github.io/_config.yml
            Source: /Users/tkhwang/_2O2L2H/github/2O2L2H.github.io
       Destination: /Users/tkhwang/_2O2L2H/github/2O2L2H.github.io/_site
 Incremental build: disabled. Enable with --incremental
      Generating...
                    done in 0.487 seconds.
 Auto-regeneration: disabled. Use --watch to enable.
 Auto-regeneration: disabled by JekyllAdmin.
                    The site will regenerate only via the Admin interface.
  JekyllAdmin mode: production
    Server address: http://127.0.0.1:4000/
  Server running... press ctrl-c to stop.
```

---
## Commit

- `git status`
- `git add XXXX`
- `git commit -m "MESSAGE"`
- `git push`
