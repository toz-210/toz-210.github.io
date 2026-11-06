---
layout: page
title: 공모전/자격증
permalink: /category/contest-cert/
---

{%- assign posts = site.categories["공모전/자격증"] -%}
{%- if posts and posts.size > 0 %}
{% for p in posts %}
- [{{ p.title }}]({{ p.url | relative_url }}) <small>{{ p.date | date: "%Y.%m.%d" }}</small>
{%- endfor %}
{% else %}
준비 중
{% endif %}

관련 저장소: [Contests-Certifications](https://github.com/toz-210/Contests-Certifications)

[← 카테고리 목록]({{ '/categories/' | relative_url }})
