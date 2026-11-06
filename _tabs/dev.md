---
layout: page
title: 개발
icon: fas fa-code
order: 1
---

{%- assign posts = site.categories["개발"] -%}
{%- if posts and posts.size > 0 %}
{% for p in posts %}
- [{{ p.title }}]({{ p.url | relative_url }}) <small>{{ p.date | date: "%Y.%m.%d" }}</small>
{%- endfor %}
{% else %}
준비 중
{% endif %}

관련 저장소: [dev](https://github.com/toz-210/dev)
