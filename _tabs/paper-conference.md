---
layout: page
title: 논문/컨퍼런스
icon: fas fa-file-lines
order: 5
---

{%- assign posts = site.categories["논문/컨퍼런스"] -%}
{%- if posts and posts.size > 0 %}
{% for p in posts %}
- [{{ p.title }}]({{ p.url | relative_url }}) <small>{{ p.date | date: "%Y.%m.%d" }}</small>
{%- endfor %}
{% else %}
준비 중
{% endif %}

관련 저장소: [paper-conference](https://github.com/toz-210/paper-conference)
