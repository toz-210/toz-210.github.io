---
layout: page
title: 블로그/기술문서
permalink: /category/tech-doc/
---

{%- assign posts = site.categories["블로그/기술문서"] -%}
{%- if posts and posts.size > 0 %}
{% for p in posts %}
- [{{ p.title }}]({{ p.url | relative_url }}) <small>{{ p.date | date: "%Y.%m.%d" }}</small>
{%- endfor %}
{% else %}
준비 중
{% endif %}

관련 저장소: [blog-technology](https://github.com/toz-210/blog-technology)

[← 카테고리 목록]({{ '/categories/' | relative_url }})
